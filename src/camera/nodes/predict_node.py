#!/usr/bin/env python3 

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image as msg_Image
from sensor_msgs.msg import CameraInfo as msg_CameraInfo
from geometry_msgs.msg import Point as msg_Point

import numpy as np

import cv2
from cv_bridge import CvBridge 

import sys
import os
from pathlib import Path

# Add detection module to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'detection'))
from yolo import YOLO
from collections import deque

import time

# Outline:
# Create subscription to rgb topic (type: msg_Image)
# Create subscription to depth topic (type: msg_Image)
# boudning box on image
# predict using YOLO

class PredictNode(Node):

    def __init__(self):
        super().__init__('PredictNode')
        # use tiny model for fast inference
        # Get paths relative to this script
        detection_dir = Path(__file__).parent.parent / 'detection'
        config_file = str(detection_dir / 'configs' / 'cross-hands-tiny-prn.cfg')
        weights_file = str(detection_dir / 'models' / 'cross-hands-tiny-prn.weights')
        
        self.model = YOLO(config_file, weights_file, ["hand"])
        self.depth_subscriber = self.create_subscription(msg_Image, '/camera/camera/depth/image_rect_raw', self.depth_received_callback, 2)
        self.img_subscriber = self.create_subscription(msg_Image, '/camera/camera/color/image_raw', self.img_recieved_callback, 2)
        self.cam_info_subscriber = self.create_subscription(msg_CameraInfo, '/camera/camera/color/camera_info', self.cam_info_received_callback, 2)
        self.hand_loc_publisher = self.create_publisher(msg_Point, '/camera/camera/hand_loc', 2)

        # create timer for publishing hand location information
        self.timer_period = .5
        self.timer = self.create_timer(self.timer_period, self.publish_hand_loc)

        # image processing
        self.k = np.array([[384.6311340332031, 0.0, 318.7968444824219], [0.0, 384.6311340332031, 239.64767456054688], [0.0, 0.0, 1.0]])
        self.hand_loc_rgb = [0, 0]
        self.hand_loc_3d = [0, 0, 0]
        self.og_dim = (640, 480)
        self.model_dim = (640, 427) # input image dimensions to model
        self.model2og_dim = [ self.og_dim[0]/self.model_dim[0], self.og_dim[1]/self.model_dim[1] ]
        self.bridge = CvBridge()

        # camera info initialization
        self.fx = 318
        self.fy = 318
        self.cx = 0
        self.cy = 0
        self.hand_loc_px = [0,0]

        self.detected = False

        self.img = np.zeros((480,640,3), dtype=np.uint8)
        self.depth_img = np.zeros((480,640), dtype=np.uint16)
        
        self.image_queue = deque(maxlen=10)

    
    def img_recieved_callback(self, msg):
        """
        Updates the center location of the hand from 2D image
        self: PredictNode
        msg: message (Array.Array)
        returns: None
        """
        img =  self.bridge.imgmsg_to_cv2(msg, msg.encoding)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.image_queue.append(img)
        
    def cam_info_received_callback(self, msg):
        # TODO: process camera info to get camera parameters and convert px to mm
        cam_info_all = msg
        # TODO: extract relevant params
        self.fx = cam_info_all.k[0]
        self.fy = cam_info_all.k[4]
        self.cx = cam_info_all.k[2]
        self.cy = cam_info_all.k[5]
    
    def depth_received_callback(self, msg):
        # depth_img = self.bridge.imgmsg_to_cv2(msg, msg.encoding)
        self.depth_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")

       
    def hand_detection_depth(self):
        if self.image_queue == deque([]):
            return
        img = cv2.resize(self.image_queue.popleft(), self.model_dim) #TODO: resize to a smaller multiple of this for faster computation
        _,_,_,output = self.model.inference(img)
        # if any hands detected
        detected = False
        if output != []:
            # get most confident prediction
            max_conf_idx = max(range(len(output)), key=lambda i: output[i][2])
            _,_, confidence ,x,y,w,h = output[max_conf_idx]
            # draw bbox on resized image and save to disk
            x1, y1 = int(x), int(y)
            x2, y2 = int(x + w), int(y + h)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"hand {confidence:.2f}"
            cv2.putText(img, label, (x1, max(15, y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # upscale to original image size and save with timestamp
            vis_og = cv2.resize(img, self.og_dim)
            fname = f"/home/jimmy/ros2_ws/hand.jpg"
            cv2.imwrite(fname, vis_og)
            print("Saved bbox image to:", fname)
            detected = (confidence > .5)
            self.detected = detected
            # convert to original frame coordinates
            self.hand_loc_px = [round((x+w/2) * self.model2og_dim[0]), round((y+h/2)*self.model2og_dim[1])]

        # hand_loc_rgb is [x,y] in pixels in the original image frame
        depth = self.depth_img[self.hand_loc_px[1], self.hand_loc_px[0]]  # depth in mm
        x = (self.hand_loc_px[0] - self.cx) * depth / self.fx
        y = (self.hand_loc_px[1] - self.cy) * depth / self.fy
        z = depth

        x, y, z = z, -x, -y
        if detected:
            print("Hand coordinates (mm): ", x, y, z)
        else:
            print("No hand detected")

        # self.hand_loc_3d  = [ self.hand_loc_rgb[0], [depth_img[self.center[0], self.center[1]]], self.hand_loc_rgb[1] ]
        # self.hand_loc_3d  = [z, -x, -y]
        self.hand_loc_3d = [x, y, z]

    def publish_hand_loc(self):
        msg = msg_Point()
        self.hand_detection_depth()
        # print("Hand location (mm): ", self.hand_loc_3d)
        msg.x, msg.y, msg.z = float(self.hand_loc_3d[0]), float(self.hand_loc_3d[1]), float(self.hand_loc_3d[2])
        self.hand_loc_publisher.publish(msg)


def main(args=None):

    """
    The main function.
    :param args: Not used directly by the user, but used by ROS2 to configure
    certain aspects of the Node.
    """
    try:
        rclpy.init(args=args)
        predict_node = PredictNode()
        rclpy.spin(predict_node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()