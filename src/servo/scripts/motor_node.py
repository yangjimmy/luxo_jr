#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point as msg_Point
from dynamixel_sdk_custom_interfaces.msg import SetPosition
from dynamixel_sdk_custom_interfaces.srv import GetPosition

import numpy as np
import os

# Outline:
# Receive hand location message
# Calculate inverse kinematics
# Send joint positions as motor commands to motor

class MotorNode(Node):
    def __init__(self):
        super().__init__('MotorNode')
        self.hand_location_subscriber = self.create_subscription(msg_Point, '/camera/camera/hand_loc', self.hand_loc_received_callback, 10)
        self.publisher_ = self.create_publisher(SetPosition, 'set_position', 10)
        self.CurrentPosClient = self.create_client(GetPosition, 'get_position')
        timer_ts = 0.1 # Timer Period
        self.timer = self.create_timer(timer_ts, self.timer_callback)
        self.MotorIDs = [1,2,3,4,5,6]
        self.MotorZeroPos = [3.14, 3.14, 3.14, 3.14, 3.14, 2.45]
        self.MotorDirection = [1, 1, 1, 1, 1, 1] # put 1 and -1
        self.L1 = 300 #mm # Linkage Length Information
        self.L2 = 50 #mm 
        self.L3 = 40 #mm 
        self.L4 = 25 #mm 
        self.L5 = 317 #mm 
        self.L6 = 80 #mm 
        self.L7 = 300 #mm 
        self.L8 = 50 #mm
        self.L9 = 73 #mm 
        self.L11 = 31.5 #mm 
        self.L12 = self.L11+self.L8/2-self.L9/2 
        self.DH_alpha = [0,np.pi/2,0,np.pi/2,np.pi/2,np.pi/-2,np.pi/-2]; # Link twist angles (alpha_i-1)
        self.DH_a     = [0,0,self.L1,self.L7,self.L12,0,0]; # Link lengths (a_i-1)
        self.DH_d     = [self.L4,self.L11,0,0,0,0,0]; # Link offsets (d_i)
        while not self.CurrentPosClient.wait_for_service(timeout_sec = 1.0):
            self.get_logger().info('Waiting for get_position service')
        
    def hand_loc_received_callback(self, msg):
        """
        Updates the center location of the hand from 2D image
        self: MotorNode
        msg: message (Array.Array)
        returns: None
        """
        x,y,z = msg.x, msg.y, msg.z
        pass
        
    def timer_callback(self):
        CommandingMotors = [1,1,1,1,1,1] # Driving which Motor: put one for motor you want to command, put zero for the others
        TargetPos = [0.1,-1.6,-0.1,-np.pi/2,0,0] # in rad  # Leave zero for the motors not being commanded
        CurrentMotorPos = self.AllMotorsGo(CommandingMotors, TargetPos)
        FK_TransformationMatrix = self.FK(CurrentMotorPos)
        self.get_logger().info(f'Current Motor Pos:{CurrentMotorPos}')
        self.get_logger().info(f'Current Transformation Matrix from M5(camera) base to M6(feed):{FK_TransformationMatrix}')
        
        
    def FK(self, MotorAngles):
        theta_M1, theta_M2, theta_M3, theta_M4, theta_M5, theta_M6 = MotorAngles
        theta_array = np.zeros(7)
        theta_array[0] = theta_M5
        theta_array[1] = theta_M1
        temp_a = self.L2*np.cos(theta_M2)-self.L4-self.L1*np.cos(theta_M1)
        temp_b = self.L2*np.sin(theta_M2)-self.L3-self.L1*np.sin(theta_M1)
        temp_c = (self.L6**2 - self.L5**2 + temp_a**2 + temp_b**2)/(2*self.L6)
        temp_t = (temp_b-2*np.sqrt(temp_b**2+temp_a**2-temp_c**2))/(temp_a+temp_c)
        P1 = [self.L1*np.cos(theta_M1), self.L1*np.sin(theta_M1)]
        P2 = [self.L2*np.cos(theta_M2) - self.L4, self.L2*np.sin(theta_M2) - self.L3]
        theta_3R = np.arctan2((1-temp_t**2)/(1+temp_t**2),2*temp_t/(1+temp_t**2))
        P3R = [self.L1*np.cos(theta_M1) + self.L6*np.cos(theta_3R), self.L1*np.sin(theta_M1) + self.L6*np.sin(theta_3R)]
        theta_array[2] = theta_3R
        theta_array[3] = np.pi/(-2) 
        temp_a = self.L2*np.cos(theta_M4)-self.L4-self.L1*np.cos(theta_M3)
        temp_b = self.L2*np.sin(theta_M4)-self.L3-self.L1*np.sin(theta_M3)
        temp_c = (self.L6**2 - self.L5**2 + temp_a**2 + temp_b**2)/(2*self.L6)
        temp_t = (temp_b-2*np.sqrt(temp_b**2+temp_a**2-temp_c**2))/(temp_a+temp_c)
        theta_3L = np.arctan2((1-temp_t**2)/(1+temp_t**2),2*temp_t/(1+temp_t**2))
        P3L = [self.L1*np.cos(theta_M3) + self.L6*np.cos(theta_3L), self.L1*np.sin(theta_M3) + self.L6*np.sin(theta_3L)]
        theta_array[4] = np.arcsin((P3L[0]-P3R[0])/self.L9)
        theta_array[5] = np.arcsin((P3R[1]-P3L[1])/self.L9)
        theta_array[6] = theta_M6
        Whole_FK_matrix = self.ForwardK_with_Arrays(self.DH_alpha, self.DH_a, self.DH_d, theta_array)
        return Whole_FK_matrix
    def ForwardK_with_Arrays(self, Alpha_Array, a_array, d_array, theta_array):
        JointNumber = np.shape(d_array)[0]
        Whole_FK_matrix = np.eye(4)
        for i in range(JointNumber):
            Dx = [[1,0,0,a_array[i]],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
            Dz = [[1,0,0,0],[0,1,0,0],[0,0,1,d_array[i]],[0,0,0,1]]
            Tx = [[1,0,0,0],[0,np.cos(Alpha_Array[i]),-1*np.sin(Alpha_Array[i]),0],[0,np.sin(Alpha_Array[i]),np.cos(Alpha_Array[i]),0],[0,0,0,1]]
            Tz = [[np.cos(theta_array[i]),-1*np.sin(theta_array[i]),0,0],[np.sin(theta_array[i]),np.cos(theta_array[i]),0,0],[0,0,1,0],[0,0,0,1]]
            FK_matrix_per_joint = np.array(Tx)@np.array(Dx)@np.array(Tz)@np.array(Dz)
            Whole_FK_matrix = np.dot(Whole_FK_matrix,FK_matrix_per_joint)
        return Whole_FK_matrix    
    def CommandMotor(self, motor_id, CmdPos):
        Motor_msg = SetPosition()
        Motor_msg.id = motor_id
        Motor_msg.position = CmdPos
        self.publisher_.publish(Motor_msg)
        self.get_logger().info(f'Publishing: ID={Motor_msg.id}, position = {Motor_msg.position}')
    def MotorGoInRad(self, MotorID, TargetPositionInRad):
        TargetPosition = int((TargetPositionInRad*self.MotorDirection[MotorID-1]+self.MotorZeroPos[MotorID-1])*2048/np.pi)
        Motor_msg = SetPosition()
        Motor_msg.id = MotorID
        Motor_msg.position = TargetPosition
        self.publisher_.publish(Motor_msg)
        #self.get_logger().info(f'Publishing: ID={Motor_msg.id}, position = {Motor_msg.position}')        
    def AllMotorsGo(self, IDarrayToGo, motorTargetPos):
        FeedbackPos = np.zeros(6)
        for k in range(6):
            if IDarrayToGo[k] == 1:
                self.MotorGoInRad(self.MotorIDs[k], motorTargetPos[k])
        return motorTargetPos
    
def main(args=None):

    """
    The main function.
    :param args: Not used directly by the user, but used by ROS2 to configure
    certain aspects of the Node.
    """
    try:
        rclpy.init(args=args)
        motor_node = MotorNode()
        rclpy.spin(motor_node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
