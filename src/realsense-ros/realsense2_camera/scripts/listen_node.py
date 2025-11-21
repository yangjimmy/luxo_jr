#!/usr/bin/env python3 

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image as msg_Image
from sensor_msgs.msg import CameraInfo as msg_CameraInfo

from cv_bridge import CvBridge
import cv2
import numpy as np
import os

# Outline:
# Create subscription to rgb topic (type: msg_Image)
# Create subscription to depth topic (type: msg_Image)
# boudning box on image
# listen using YOLO

bridge = CvBridge()

class ListenNode(Node):

    def __init__(self):
        super().__init__('ListenNode')
        # use tiny model for fast inference
        self.depth_subscriber = self.create_subscription(msg_Image, '/camera/camera/depth/image_rect_raw', self.depth_received_callback, 10)
        self.img_subscriber = self.create_subscription(msg_Image, '/camera/camera/color/image_raw', self.img_recieved_callback, 10)
        self.cam_info_subscriber = self.create_subscription(msg_CameraInfo, '/camera/camera/color/camera_info', self.cam_info_received_callback, 10)
        self.depth_info_subscriber = self.create_subscription(msg_CameraInfo, '/camera/camera/depth/camera_info', self.depth_info_received_callback, 10)
    
    def img_recieved_callback(self, msg):
        """
        Updates the center location of the hand from 2D image
        self: ListenNode
        msg: message (Array.Array)
        returns: None
        """
        pass
        print("RGB image")
        msg_data = msg.data
        # print(len(msg_data))
        img = np.array(msg.data, dtype=np.uint8)
        # print(img.shape)
        img = bridge.imgmsg_to_cv2(msg, msg.encoding)
        img = img[:, :, [2, 1, 0]]  # Convert BGR to RGB
        os.chdir(r"/home/jimmy")
        np.save("color.npy",img)
        cv2.imwrite("color.jpg", img)

    def cam_info_received_callback(self, msg):
        """
        uint32 height
        uint32 width
        string distortion_model
        double[] d
        double[9] k
        double[9] r
        double[12] p
        uint32 binning_x
        uint32 binning_y
        """
        pass
        print("rgb info")
        # fix msg_data (msg.data is not valid for CameraInfo) and print all CameraInfo fields
        msg_data = msg

        # print("height:", msg_data.height)
        # print("width:", msg_data.width)
        # print("distortion_model:", msg_data.distortion_model)
        # print("d (distortion coefficients):", list(msg_data.d))
        # print("k (intrinsic matrix):", list(msg_data.k))
        # print("r (rectification matrix):", list(msg_data.r))
        print("p (projection/camera matrix):", list(msg_data.p))
        # print("binning_x:", msg_data.binning_x)
        # print("binning_y:", msg_data.binning_y)
        if hasattr(msg_data, "roi"):
            roi = msg_data.roi
            print("roi:", f"x_offset={roi.x_offset}, y_offset={roi.y_offset}, height={roi.height}, width={roi.width}, do_rectify={roi.do_rectify}")

        # TODO: extract relevant params

    def depth_info_received_callback(self, msg, echo=False):
        print("depth info")
        if echo:
            print("height:", msg.height)
            print("width:", msg.width)
            print("distortion_model:", msg.distortion_model)
            print("d (distortion coefficients):", list(msg.d))
            print("k (intrinsic matrix):", list(msg.k))
            print("r (rectification matrix):", list(msg.r))
            print("p (projection/camera matrix):", list(msg.p))
            print("binning_x:", msg.binning_x)
            print("binning_y:", msg.binning_y)
            if hasattr(msg, "roi"):
                roi = msg.roi
                print("roi:", f"x_offset={roi.x_offset}, y_offset={roi.y_offset}, height={roi.height}, width={roi.width}, do_rectify={roi.do_rectify}")
        else:
            pass

    def depth_to_relative_color(self, depth_image):
        depth = depth_image.astype(np.float32)
        # norm = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX)
        # norm_uint8 = norm.astype(np.uint8)
        # color = cv2.applyColorMap(norm_uint8, cv2.COLORMAP_JET)
        img = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX)
        return img
    
    def depth_received_callback(self, msg, echo=True):
        if echo:
            print("depth")
            msg_data = msg.data
            print(f"Image height: {msg.height}")
            print(f"Image width: {msg.width}")
            print(f"Image encoding: {msg.encoding}")
            # print(msg_data)
            # print(len(msg_data))
            # img = bridge.imgmsg_to_cv2(msg, msg.encoding)
            img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
            print("Image")
            print(img)
            # print(img.shape)
            # print(np.unique(img))
            os.chdir(r"/home/jimmy")
            np.save("depth.npy",img)
            depth_img = self.depth_to_relative_color(img)
            cv2.imwrite("depth.jpg", depth_img)
        else:
            pass


def main(args=None):

    """
    The main function.
    :param args: Not used directly by the user, but used by ROS2 to configure
    certain aspects of the Node.
    """
    try:
        rclpy.init(args=args)
        listen_node = ListenNode()
        rclpy.spin(listen_node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()