#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point as msg_Point
from dynamixel_sdk_custom_interfaces.msg import SetPosition
from dynamixel_sdk_custom_interfaces.srv import GetPosition

from scipy.spatial.transform import Rotation as R
import numpy as np
import time

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
        self.timer_ts = 0.1 # Timer Period
        self.timer = self.create_timer(self.timer_ts, self.timer_callback)
        self.MotorIDs = [1,2,3,4,5,6]
        #self.MotorZeroPos = [3.215+0.035, 4.303, 3.044, 1.666, 3.127, 5.61]
        #self.MotorDirection = [1, 1, -1, -1, 1, 1] # put 1 and -1
        self.MotorZeroPos = [3.215+0.035-0.36, 4.303-1.01+1.57, 3.044-0.3, 1.666+1.83-1.57, 3.127, 5.6-3.95]
        self.MotorDirection = [1, 1, -1, -1, 1, -1] # put 1 and -1
        #self.L1 = 300 #mm # Linkage Length Information
        self.L1 = 200 #mm  Shotened for torque issue
        self.L2 = 50 #mm 
        self.L3 = 40 #mm 
        self.L4 = 25 #mm 
        #self.L5 = 317 #mm 
        self.L5 = 217 #mm  Shotened for torque issue
        self.L6 = 80 #mm 
        #self.L7 = 300 #mm 
        self.L7 = 245 #mm  Shotened for torque issue
        self.L8 = 50 #mm
        self.L9 = 73 #mm 
        self.L11 = 31.5 #mm 
        self.L12 = self.L11+self.L8/2-self.L9/2 
        self.DH_alpha = [0,np.pi/-2,0,np.pi/2,np.pi/2,np.pi/-2,np.pi/-2]; # Link twist angles (alpha_i-1)
        self.DH_a     = [0,0,self.L1,self.L7,self.L12,0,0]; # Link lengths (a_i-1)
        self.DH_d     = [self.L4,self.L11,0,0,0,0,0]; # Link offsets (d_i)
        
        self.MotorUpperLimit = np.array([np.pi, np.pi, np.pi, np.pi, np.pi, np.pi])
        self.MotorLowerLimit = np.array([-np.pi, -1.7, -np.pi, -1.7, -np.pi, -np.pi])
        self.L13 = 10
        self.L14 = 210
        self.DH2_alpha = [0,np.pi/-2,0,np.pi/2,np.pi/2,np.pi/-2,np.pi/-2,np.pi/-2,np.pi/-2]; # Link twist angles (alpha_i-1)
        self.DH2_a     = [0,0,self.L1,self.L7,self.L12,0,0,0,self.L14]; # Link lengths (a_i-1)
        self.DH2_d     = [self.L4,self.L11,0,0,0,0,self.L9/2,self.L13,0]; # Link offsets (d_i)
        self.DemoStage = 1
        self.Current_roll = 0
        self.Current_pitch = 0
        self.Current_yaw = 0
        
        self.DemoEndPos = [] #  Pos for looking aside
        self.EndPos = [0.53,-0.85,0.76,-0.51,0.47,0.88] #  Pos for looking aside
        self.EndPosInterpolateSteps = 100
        self.EndPosInterpolateStepsCounter = 0
        self.EndPosDiff = []
        self.DemoCycleEndWaitingCounter = int(3*(1/self.timer_ts)) # 3 seconds waiting at the end of demo cycle
        #while not self.CurrentPosClient.wait_for_service(timeout_sec = 1.0):
        #    self.get_logger().info('Waiting for get_position service')
        ##
        self.CommandingMotors = [1,1,1,1,1,1] # Driving which Motor: put one for motor you want to command, put zero for the others
        # self.TargetPos = [0.12,-1.2,0.12,-1.2,0,0.59] # in rad  # Leave zero for the motors not being commanded
        #self.TargetPos = [0.7, -0.4, 0.7, -.4, 0, -0.59]
        #self.TargetPos = [0,-1.43,0,-1.43,0,1.57] # For demo 6 dof freedom
        self.TargetPos = [0.1,-1.2,0.1,-1.2,0,1.57] # For demo 6 dof freedom
        self.InitialPos = self.TargetPos
        self.CurrentMotorPos = self.AllMotorsGo(self.CommandingMotors, self.InitialPos, initial=False) # Target pos in rad
        self.CurrentJointAngles = self.MotorPos2JointAngle(self.CurrentMotorPos)
        self.CurrentTransformMatrix = self.FK(self.CurrentJointAngles)
        self.DesiredTransformMatrix = self.CurrentTransformMatrix.copy()
        self.InitialTransformMatrix = self.CurrentTransformMatrix.copy()
        self.Current9JointAngles = self.MotorPos2JointAngle2(self.CurrentMotorPos) # 9 joints
        self.Current9TransformMatrix = self.FK2(self.Current9JointAngles) # 9 joints
        self.Desired9TransformMatrix = self.Current9TransformMatrix.copy() # 9 joints
        self.Initial9TransformMatrix = self.Current9TransformMatrix.copy() # 9 joints
        self.TimerCounter = 0
        self.Handx_camera = 100
        self.Handy_camera = 100
        self.Handz_camera = 100
        
        self.InitialWaitTime = int(1*(1/self.timer_ts)) # 1 seconds initial wait time
        self.PrintMotorAngles = False
        
    def hand_loc_received_callback(self, msg):
        """
        Updates the center location of the hand from 2D image
        self: MotorNode
        msg: message (Array.Array)
        returns: None
        """
        self.get_logger().info(f'Received hand location: x={msg.x}, y={msg.y}, z={msg.z}')
        if msg.x == 0 and msg.y == 0 and msg.z == 0:
            return
        
        # d = 600     # distance from camera to object
        self.Handx_camera, self.Handy_camera, self.Handz_camera = msg.x , msg.y, msg.z # adjust for offset between camera and robot base

        
    def timer_callback(self, demo=False):
        
        if(self.InitialWaitTime > 0):
            self.InitialWaitTime -= 1
            return
        
        if self.DemoStage == 20:
            self.DemoEndPos = self.CurrentMotorPos.copy()
            self.EndPosDiff = self.EndPos - self.DemoEndPos
            self.EndPosInterpolateSteps = np.linalg.norm(self.EndPosDiff, ord=2)/0.05
            print("Current Motor Positions (rad):", self.CurrentMotorPos)
            print("Target Motor Positions (rad):", self.EndPos)
            print("Steps To end point :", self.EndPosInterpolateSteps)
            self.DemoStage = 21
        elif self.DemoStage == 21:
            TempPosToGo = self.EndPosInterpolateStepsCounter*self.EndPosDiff/self.EndPosInterpolateSteps + self.DemoEndPos
            self.CurrentMotorPos = self.AllMotorsGo(self.CommandingMotors, TempPosToGo) # Target pos in rad
            print("Current Motor Positions (rad):", self.CurrentMotorPos)
            self.EndPosInterpolateStepsCounter += 1
            if self.EndPosInterpolateStepsCounter > self.EndPosInterpolateSteps:
                self.DemoStage = 22
                self.EndPosInterpolateStepsCounter = 0
                print("End Position Reached")
        elif self.DemoStage == 22:
            pass
        else:
            self.CurrentMotorPos = self.AllMotorsGo(self.CommandingMotors, self.TargetPos) # Target pos in rad
        #self.CurrentMotorPos = self.AllMotorsGo(self.CommandingMotors, self.TargetPos) # Target pos in rad
        #print("Current Motor Positions (rad):", self.CurrentMotorPos)
        self.CurrentJointAngles = self.MotorPos2JointAngle(self.CurrentMotorPos) # 7 joints
        self.Current9JointAngles = self.MotorPos2JointAngle2(self.CurrentMotorPos) # 9 joints
        self.CurrentTransformMatrix = self.FK(self.CurrentJointAngles) # 7 joints
        self.Current9TransformMatrix = self.FK2(self.Current9JointAngles) # 9 joints
        #self.get_logger().info(f'Current End Effector Position: x={self.CurrentTransformMatrix[0,3]}, y={self.CurrentTransformMatrix[1,3]}, z={self.CurrentTransformMatrix[2,3]}') # 7 joints
        #self.get_logger().info(f'Current End Effector Position: x={self.Current9TransformMatrix[0,3]}, y={self.Current9TransformMatrix[1,3]}, z={self.Current9TransformMatrix[2,3]}') # 9 joints
        demo = True
        omega = 0.5
        t = self.TimerCounter*self.timer_ts
        if demo:
            #print("Demo Mode now")
            
            #self.Desired9TransformMatrix = self.Demo6DOF(self.Initial9TransformMatrix, self.Current9TransformMatrix, Xrange=75, Yrange=90, Zrange=90, PitchAngleRange=0.4, RollAngleRange=0.7, YawAngleRange=0.4)
            self.Desired9TransformMatrix = self.Demo6DOF(self.Initial9TransformMatrix, self.Desired9TransformMatrix , Xrange=75, Yrange=90, Zrange=90, PitchAngleRange=0.4, RollAngleRange=0.7, YawAngleRange=0.4)
            #CircleRadius = 40 # in mm
            #CircleCenter = np.arr  ay([self.InitialTransformMatrix[0,3] - CircleRadius, self.InitialTransformMatrix[1,3]]) # in mm
            #self.DesiredTransformMatrix[0,3] = CircleCenter[0] + CircleRadius * np.cos(t*omega)
            #self.DesiredTransformMatrix[1,3] = CircleCenter[1] + CircleRadius * np.sin(t*omega)
            #CircleCenter = np.array([self.Initial9TransformMatrix[0,3] - CircleRadius, self.Initial9TransformMatrix[2,3]]) # in mm
            #self.Desired9TransformMatrix[0,3] = CircleCenter[0] + CircleRadius * np.cos(t*omega)
            #self.Desired9TransformMatrix[2,3] = CircleCenter[1] + CircleRadius * np.sin(t*omega)
            #self.get_logger().info(f'Desired End Effector Position: x={self.DesiredTransformMatrix[0,3]}, y={self.DesiredTransformMatrix[1,3]}, z={self.DesiredTransformMatrix[2,3]}') # 9 joints
        else:
            print("Tracking Mode: Moving to Hand Position")
            self.get_logger().info(f"Hand Position in camera frame: x={self.Handx_camera}, y={self.Handy_camera}, z={self.Handz_camera}")
            if self.Handx_camera >= 300:
                target_position_frame7 = np.array([-(self.Handx_camera - 400) + 200.379, self.Handz_camera, self.Handy_camera + 36.5, 1]).reshape((4,1))
                self.Handx_camera = 0
                self.Handy_camera = 0
                self.Handz_camera = 0
                
                # world_coords = np.matmul(self.CurrentTransformMatrix, np.expand_dims(np.array([self.Handx_camera, self.Handy_camera, self.Handz_camera, 1]).T, axis=1))
                world_coords = self.CurrentTransformMatrix @ target_position_frame7
                self.DesiredTransformMatrix[0,3] = world_coords[0,0]
                self.DesiredTransformMatrix[1,3] = world_coords[1,0]
                self.DesiredTransformMatrix[2,3] = world_coords[2,0]
                # self.DesiredTransformMatrix[0:3,3] = world_coords[0:3,0]
                # for debugging
                # self.DesiredTransformationMatrix = self.CurrentTransformMatrix.copy()
                self.get_logger().info(f"Desired Position in world frame: x={self.DesiredTransformMatrix[0,3]}, y={self.DesiredTransformMatrix[1,3]}, z={self.DesiredTransformMatrix[2,3]}")

        # Inverse Kinematics to get joint angles
        #SolvedJointAngles, success = self.IK(self.DesiredTransformMatrix, self.CurrentJointAngles) # 7 joints
        Solved9JointAngles, success = self.IK2(self.Desired9TransformMatrix, self.Current9JointAngles)  # 9 joints
        if success:
            #SolvedMotorPos, success2 = self.JointAngle2MotorPos(SolvedJointAngles, np.array(self.CurrentMotorPos))  # 7 joints
            SolvedMotorPos, success2 = self.JointAngle2MotorPos(Solved9JointAngles, np.array(self.CurrentMotorPos)) # 9 joints
            if not success2:
                self.get_logger().info(f"Motor position solver did not converge")
            else:
                # self.TargetPos = SolvedMotorPos
                #print("Current Motor Positions (rad):", self.CurrentMotorPos)
                if self.PrintMotorAngles == True:
                    print("Solved Motor Positions (rad):", SolvedMotorPos)
                pass
        else:
            SolvedMotorPos = None
            self.get_logger().info(f"IK solver did not converge")
        # 
        if SolvedMotorPos is not None:
            self.TargetPos = SolvedMotorPos
        # command motor
        
        self.TimerCounter = self.TimerCounter + 1

    def CommandMotor(self, motor_id, CmdPos):
        Motor_msg = SetPosition()
        Motor_msg.id = motor_id
        Motor_msg.position = CmdPos
        self.publisher_.publish(Motor_msg)
        #self.get_logger().info(f'Publishing: ID={Motor_msg.id}, position = {Motor_msg.position}')
        
    def MotorGoInRad(self, MotorID, TargetPositionInRad):
        TargetPosition = int((TargetPositionInRad*self.MotorDirection[MotorID-1]+self.MotorZeroPos[MotorID-1])*2048/np.pi)
        Motor_msg = SetPosition()
        Motor_msg.id = MotorID
        Motor_msg.position = TargetPosition
        self.publisher_.publish(Motor_msg)
        #self.get_logger().info(f'Publishing: ID={Motor_msg.id}, position = {Motor_msg.position}')
          
    def AllMotorsGo(self, IDarrayToGo, motorTargetPos, initial=False):
        
        # IDarrayToGo = [1,1,1,1,1,1] # For testing, command all motors --- IGNORE ---
        for k in range(6):
            # if IDarrayToGo[k] == 1:
            self.MotorGoInRad(self.MotorIDs[k], motorTargetPos[k])
            #time.sleep(0.02)  # Small delay between motor commands to prevent queue saturation
                
        # Return numeric array for downstream numeric processing
        if initial:
            print("Initial Positioning of All Motors")
            time.sleep(.5)
        return np.array(motorTargetPos, dtype=float)
    
    def MotorPos2JointAngle(self, MotorAngles): # 7 joints
        theta_M1, theta_M2, theta_M3, theta_M4, theta_M5, theta_M6 = MotorAngles
        theta_array = np.zeros(7)
        theta_array[0] = theta_M5
        theta_array[1] = theta_M1 - np.pi/2
        theta_array[2], theta_array[4], theta_array[5] = self.Motor1to4toJointsAngle([theta_M1, theta_M2, theta_M3, theta_M4])
        theta_array[3] = np.pi/(-2) 
        theta_array[6] = theta_M6
        return theta_array
    def MotorPos2JointAngle2(self, MotorAngles):  # 9 joints
        theta_M1, theta_M2, theta_M3, theta_M4, theta_M5, theta_M6 = MotorAngles
        #theta_M1, theta_M5, theta_M3, theta_M4, theta_M2, theta_M6 = MotorAngles
        theta_array = np.zeros(9)
        theta_array[0] = theta_M5
        theta_array[1] = theta_M1 - np.pi/2
        theta_array[2], theta_array[4], theta_array[5] = self.Motor1to4toJointsAngle([theta_M1, theta_M2, theta_M3, theta_M4])
        theta_array[3] = np.pi/(-2) 
        theta_array[6] = theta_M6
        theta_array[7] = np.pi
        theta_array[8] = 0
        return theta_array
    
    def Motor1to4toJointsAngle(self, MotorAngles):
        theta_M1, theta_M2, theta_M3, theta_M4 = MotorAngles
        temp_a = self.L2*np.cos(theta_M2)-self.L4-self.L1*np.cos(theta_M1)
        temp_b = self.L2*np.sin(theta_M2)-self.L3-self.L1*np.sin(theta_M1)
        temp_c = (self.L6**2 - self.L5**2 + temp_a**2 + temp_b**2)/(2*self.L6)
        temp_t = (temp_b+np.sqrt(temp_b**2+temp_a**2-temp_c**2))/(temp_a+temp_c)
        P1 = [self.L1*np.cos(theta_M1), self.L1*np.sin(theta_M1)]
        P2 = [self.L2*np.cos(theta_M2) - self.L4, self.L2*np.sin(theta_M2) - self.L3]
        theta_3R = np.arctan2(2*temp_t/(1+temp_t**2),(1-temp_t**2)/(1+temp_t**2))
        P3R = [self.L1*np.cos(theta_M1) + self.L6*np.cos(theta_3R), self.L1*np.sin(theta_M1) + self.L6*np.sin(theta_3R)]
        theta3 = theta_3R - theta_M1
        temp_a = self.L2*np.cos(theta_M4)-self.L4-self.L1*np.cos(theta_M3)
        temp_b = self.L2*np.sin(theta_M4)-self.L3-self.L1*np.sin(theta_M3)
        temp_c = (self.L6**2 - self.L5**2 + temp_a**2 + temp_b**2)/(2*self.L6)
        temp_t = (temp_b+np.sqrt(temp_b**2+temp_a**2-temp_c**2))/(temp_a+temp_c)
        theta_3L = np.arctan2(2*temp_t/(1+temp_t**2),(1-temp_t**2)/(1+temp_t**2))
        P3L = [self.L1*np.cos(theta_M3) + self.L6*np.cos(theta_3L), self.L1*np.sin(theta_M3) + self.L6*np.sin(theta_3L)]
        theta5 = np.arcsin((P3R[0]-P3L[0])/self.L9)
        theta6 = np.arcsin((P3R[1]-P3L[1])/self.L9) - np.pi/2
        theta_3and5and6 = [theta3, theta5, theta6]
        return theta_3and5and6
    def JointAngle2MotorPos(self, JointAngles, M0, lambda_=0.01, max_iter=200, tol=1e-3): # For both 7 and 9 joints
        Motor5 = JointAngles[0] 
        Motor1 = JointAngles[1] + np.pi/2
        Motor6 = JointAngles[6]
        Joint3and5and6 = [JointAngles[2], JointAngles[4], JointAngles[5]]
        CurrentM1toM4 = [M0[0], M0[1], M0[2], M0[3]]
        SolvedM1toM4, okMotor = self.Motor1to4_dls(Joint3and5and6, CurrentM1toM4, lam=lambda_, max_iter=max_iter, tol=tol)
        M = np.array([Motor1,  SolvedM1toM4[1], SolvedM1toM4[2], SolvedM1toM4[3], Motor5, Motor6])
        return M, okMotor
        
    def jacobian_motor(self,M, h=1e-6):
        """
        Numerical Jacobian of q = Motor1to4toJointsAngle(M)
        Returns a matrix J (m x n)
        """
        M = M.astype(float)
        q0 = self.Motor1to4toJointsAngle(M)
        m = len(q0)
        n = len(M)
        J = np.zeros((m, n))
        for i in range(n):
            Mp = M.copy()
            Mp[i] += h
            qp = self.Motor1to4toJointsAngle(Mp)
            J[:, i] = (np.array(qp) - np.array(q0)) / h
        return J
        
    def Motor1to4_dls(self, Joint3and5and6, M0, lam=0.1, max_iter=200, tol=1e-5):
        M = np.array(M0, dtype=float).reshape(-1)
        success = False
        # Store error history the same way MATLAB does
        errorArray = np.zeros((len(Joint3and5and6), max_iter))
        for k in range(max_iter):
            # q = Motor1to4toJointsAngle(M)   # your function
            q = self.Motor1to4toJointsAngle(M)
            # Error term
            #e = Joint3and5and6.reshape(-1) - np.array(q).reshape(-1)
            e = np.array(Joint3and5and6) - np.array(q)
            errorArray[:, k] = e
            # Check convergence
            if np.linalg.norm(e) < tol:
                success = True
                return M, success
            # Jacobian J = ∂q/∂M
            J = self.jacobian_motor(M)    # must return numpy array
            # Damped least squares: dM = (JᵀJ + λ²I)⁻¹ Jᵀ e
            JT = J.T
            dim = J.shape[1]
            dM = np.linalg.solve(JT @ J + (lam ** 2) * np.eye(dim), JT @ e)
            # Update ONLY motor indices 1:4 (MATLAB 2:4)
            M[1:4] = M[1:4] + dM[1:4]
            # If you want to update *all* motors:
            # M = M + dM
        # After max iterations
        return M, success
    
    def FK(self, theta_array): # 7 joints
        Whole_FK_matrix = self.ForwardK_with_Arrays(self.DH_alpha, self.DH_a, self.DH_d, theta_array)
        return Whole_FK_matrix
    def FK2(self, theta_array): # 9 joints
        Whole_FK_matrix = self.ForwardK_with_Arrays(self.DH2_alpha, self.DH2_a, self.DH2_d, theta_array)
        return Whole_FK_matrix
    def ForwardK_with_Arrays(self, Alpha_Array, a_array, d_array, theta_array):
        JointNumber = np.shape(d_array)[0]
        Whole_FK_matrix = np.eye(4)
        for i in range(JointNumber):
        #for i in range(4):
            Dx = [[1,0,0,a_array[i]],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
            Dz = [[1,0,0,0],[0,1,0,0],[0,0,1,d_array[i]],[0,0,0,1]]
            Tx = [[1,0,0,0],[0,np.cos(Alpha_Array[i]),-1*np.sin(Alpha_Array[i]),0],[0,np.sin(Alpha_Array[i]),np.cos(Alpha_Array[i]),0],[0,0,0,1]]
            Tz = [[np.cos(theta_array[i]),-1*np.sin(theta_array[i]),0,0],[np.sin(theta_array[i]),np.cos(theta_array[i]),0,0],[0,0,1,0],[0,0,0,1]]
            FK_matrix_per_joint = np.array(Tx)@np.array(Dx)@np.array(Tz)@np.array(Dz)
            Whole_FK_matrix = np.dot(Whole_FK_matrix,FK_matrix_per_joint)
        return Whole_FK_matrix   
        
    def IK(self, T_des, q0, max_iter=200, lambda_=0.1, tol_pos=1e-4, tol_ori=1e-4): # For 7 joints
        """
        Numerical IK using Damped Least Squares (DLS)
        T_des        : 4x4 desired pose
        q0           : initial joint guess (N,)
        jacobian_func: function returning 6xN Jacobian: J = jacobian_func(q)
        Returns:
            q        : final joint configuration
            success  : True / False
        """
        q = np.asarray(q0, dtype=float).copy()
        success = False
        for _ in range(max_iter):
            # ---- Forward Kinematics ----
            #T = fk_func(q)
            T = self.FK(q)
            p = T[0:3, 3]
            R = T[0:3, 0:3]
            p_des = T_des[0:3, 3]
            R_des = T_des[0:3, 0:3]
            # ---- Position error ----
            dp = p_des - p
            # ---- Orientation error (axis-angle) ----
            Re = R.T @ R_des                # equivalent rotation
            axis, angle = self.rotm2axang(Re)    
            dphi = axis * angle             # 3×1
            # ---- Full 6D error vector ----
            dx = np.concatenate((dp, dphi))
            # ---- Convergence check ----
            if np.linalg.norm(dp) < tol_pos and np.linalg.norm(dphi) < tol_ori:
                success = True
                return q, success
            J = self.jacobian_numeric(q) # shape (6,N)             
            # ---- Compute numeric Jacobian ----
            # ---- Damped Least Squares Update ----
            # dq = (JᵀJ + λ²I)⁻¹ * Jᵀ * dx
            JTJ = J.T @ J + (lambda_**2) * np.eye(J.shape[1])
            dq = np.linalg.solve(JTJ, J.T @ dx)
            # ---- Update joints ----
            q = q + dq
        return q, success
    def IK2(self, T_des, q0, # 9 joints
        max_iter=200, lambda_=0.1,
        tol_pos=1e-4, tol_ori=1e-4):         # 9 joints
        """
        Numerical IK using Damped Least Squares (DLS)
        T_des        : 4x4 desired pose
        q0           : initial joint guess (N,)
        jacobian_func: function returning 6xN Jacobian: J = jacobian_func(q)
        Returns:
            q        : final joint configuration
            success  : True / False
        """
        q = np.asarray(q0, dtype=float).copy()
        success = False
        for _ in range(max_iter):
            # ---- Forward Kinematics ----
            #T = fk_func(q)
            T = self.FK2(q)
            p = T[0:3, 3]
            R = T[0:3, 0:3]
            p_des = T_des[0:3, 3]
            R_des = T_des[0:3, 0:3]
            # ---- Position error ----
            dp = p_des - p
            # ---- Orientation error (axis-angle) ----
            Re = R.T @ R_des                # equivalent rotation
            axis, angle = self.rotm2axang(Re)    
            dphi = axis * angle             # 3×1
            # ---- Full 6D error vector ----
            dx = np.concatenate((dp, dphi))
            # ---- Convergence check ----
            if np.linalg.norm(dp) < tol_pos and np.linalg.norm(dphi) < tol_ori:
                success = True
                return q, success
            #J = jacobian_func(q)   # shape (6,N)
            J = self.jacobian_numeric2(q) # shape (6,N)             # ---- Compute numeric Jacobian ----
            # ---- Damped Least Squares Update ----
            # dq = (JᵀJ + λ²I)⁻¹ * Jᵀ * dx
            JTJ = J.T @ J + (lambda_**2) * np.eye(J.shape[1])
            dq = np.linalg.solve(JTJ, J.T @ dx)
            # ---- Update joints ----
            q = q + dq
        return q, success
    def jacobian_numeric(self, q): # 7 joints
        """
        Numerical 6×N Jacobian for any robot
        q       : (N,) numpy array of joint values
        """
        q = np.asarray(q, dtype=float)
        n = len(q)
        J = np.zeros((6, n))
        h = 1e-6
        # Current FK
        T = self.FK(q)
        p = T[0:3, 3]
        R = T[0:3, 0:3]
        for i in range(n):
            # Perturb joint i
            q_pert = q.copy()
            q_pert[i] += h
            # FK after perturbation
            T2 = self.FK(q_pert)
            p2 = T2[0:3, 3]
            R2 = T2[0:3, 0:3]
            # Position derivative
            dp = (p2 - p) / h
            # Orientation derivative
            # Compute relative rotation dR = R^T * R2
            dR = R.T @ R2
            axis, angle = self.rotm2axang(dR)
            domega = axis * angle / h
            # Fill Jacobian column
            J[:, i] = np.concatenate((dp, domega))
        return J
    def jacobian_numeric2(self, q): # 9 joints
        """
        Numerical 6×N Jacobian for any robot
        q       : (N,) numpy array of joint values
        """
        q = np.asarray(q, dtype=float)
        n = len(q)
        J = np.zeros((6, n))
        h = 1e-6
        # Current FK
        T = self.FK2(q)
        p = T[0:3, 3]
        R = T[0:3, 0:3]
        for i in range(n):
            # Perturb joint i
            q_pert = q.copy()
            q_pert[i] += h
            # FK after perturbation
            T2 = self.FK2(q_pert)
            p2 = T2[0:3, 3]
            R2 = T2[0:3, 0:3]
            # Position derivative
            dp = (p2 - p) / h
            # Orientation derivative
            # Compute relative rotation dR = R^T * R2
            dR = R.T @ R2
            axis, angle = self.rotm2axang(dR)
            domega = axis * angle / h
            # Fill Jacobian column
            J[:, i] = np.concatenate((dp, domega))
        return J
    def rotm2axang(self, Rm):
        """
        Convert rotation matrix to axis-angle representation
        R : 3x3 rotation matrix
        Returns:
            axis  : 3x1 unit vector
            angle : scalar
        """
        r = R.from_matrix(Rm)
        rotvec = r.as_rotvec()          # axis * angle
        angle = np.linalg.norm(rotvec)  # rotation magnitude
        axis = rotvec / angle if angle != 0 else np.array([1,0,0])
        return axis, angle
    
    def Rx(self,angle_rad):
        """Rotation matrix around x-axis."""
        g = angle_rad
        return np.array([
            [1,          0,           0],
            [0,  np.cos(g), -np.sin(g)],
            [0,  np.sin(g),  np.cos(g)]
        ])
    def Ry(self,angle_rad):
        """Rotation matrix around y-axis."""
        g = angle_rad
        return np.array([
            [ np.cos(g), 0, np.sin(g)],
            [          0, 1,          0],
            [-np.sin(g), 0, np.cos(g)]
        ])
    def Rz(self,angle_rad):
        """Rotation matrix around z-axis."""
        g = angle_rad
        return np.array([
            [np.cos(g), -np.sin(g), 0],
            [np.sin(g),  np.cos(g), 0],
            [         0,          0, 1]
        ])   
    def Demo6DOF0(self, InitialTransformMatrix, CurrentTransformMatrix, Xrange=20, Yrange=20, Zrange=20, PitchAngleRange=0.5, RollAngleRange=0.5, YawAngleRange=0.5):
        MovingStepInmm = 2
        RotationStepInRad = 0.015
        UpperLimitX = InitialTransformMatrix[0,3] + Xrange/2
        LowerLimitX = InitialTransformMatrix[0,3] - Xrange/2
        UpperLimitY = InitialTransformMatrix[1,3] + Yrange/2
        LowerLimitY = InitialTransformMatrix[1,3] - Yrange/2
        UpperLimitZ = InitialTransformMatrix[2,3] + Zrange/2
        LowerLimitZ = InitialTransformMatrix[2,3] - Zrange/2
        Initial_R = R.from_matrix(InitialTransformMatrix[0:3,0:3])
        #Initial_roll, Initial_pitch, Initial_yaw = Initial_R.as_euler('xyz', degrees=False)
        Initial_roll, Initial_pitch, Initial_yaw = 0, 0, 0 #self.Current_roll, self.Current_pitch, self.Current_yaw
        UpperLimitPitch = Initial_pitch + RollAngleRange/2
        LowerLimitPitch = Initial_pitch - RollAngleRange/2
        UpperLimitRoll = Initial_roll + PitchAngleRange/2
        LowerLimitRoll = Initial_roll - PitchAngleRange/2
        UpperLimitYaw = Initial_yaw + YawAngleRange/2
        LowerLimitYaw = Initial_yaw - YawAngleRange/2
        match self.DemoStage:
            case 1:
                CurrentTransformMatrix[0,3] = CurrentTransformMatrix[0,3] + MovingStepInmm
                if CurrentTransformMatrix[0,3] >= UpperLimitX:
                    self.DemoStage = 2
                return CurrentTransformMatrix
            case 2:
                CurrentTransformMatrix[0,3] = CurrentTransformMatrix[0,3] - MovingStepInmm
                if CurrentTransformMatrix[0,3] <= LowerLimitX:
                    self.DemoStage = 3
                return CurrentTransformMatrix
            case 3:
                CurrentTransformMatrix[0,3] = CurrentTransformMatrix[0,3] + MovingStepInmm
                if CurrentTransformMatrix[0,3] >= InitialTransformMatrix[0,3]:
                    self.DemoStage = 4
                return CurrentTransformMatrix
            case 4:
                CurrentTransformMatrix[1,3] = CurrentTransformMatrix[1,3] + MovingStepInmm
                if CurrentTransformMatrix[1,3] >= UpperLimitY:
                    self.DemoStage = 5
                return CurrentTransformMatrix
            case 5:
                CurrentTransformMatrix[1,3] = CurrentTransformMatrix[1,3] - MovingStepInmm
                if CurrentTransformMatrix[1,3] <= LowerLimitY:
                    self.DemoStage = 6
                return CurrentTransformMatrix
            case 6:
                CurrentTransformMatrix[1,3] = CurrentTransformMatrix[1,3] + MovingStepInmm
                if CurrentTransformMatrix[1,3] >= InitialTransformMatrix[1,3]:
                    self.DemoStage = 7
                    print("Moving in Z direction now")
                    self.PrintMotorAngles = True
                return CurrentTransformMatrix
            case 8:
                CurrentTransformMatrix[2,3] = CurrentTransformMatrix[2,3] + MovingStepInmm
                if CurrentTransformMatrix[2,3] >= UpperLimitZ:
                    self.DemoStage = 9
                return CurrentTransformMatrix
            case 7:
                CurrentTransformMatrix[2,3] = CurrentTransformMatrix[2,3] - MovingStepInmm
                if CurrentTransformMatrix[2,3] <= LowerLimitZ:
                    self.DemoStage = 8
                return CurrentTransformMatrix
            case 9:
                CurrentTransformMatrix[2,3] = CurrentTransformMatrix[2,3] - MovingStepInmm
                if CurrentTransformMatrix[2,3] <= InitialTransformMatrix[2,3]:
                    self.DemoStage = 10
                    self.PrintMotorAngles = False
                return CurrentTransformMatrix
            case 10:
                CurrentTransformMatrix[0:3,0:3] = CurrentTransformMatrix[0:3,0:3] @ self.Rz(RotationStepInRad)
                self.Current_pitch = self.Current_pitch + RotationStepInRad
                if self.Current_pitch >= UpperLimitPitch:
                    self.DemoStage = 11
                return CurrentTransformMatrix
            case 11:
                CurrentTransformMatrix[0:3,0:3] = CurrentTransformMatrix[0:3,0:3] @ self.Rz(-RotationStepInRad)
                self.Current_pitch = self.Current_pitch - RotationStepInRad
                if self.Current_pitch <= LowerLimitPitch:
                    self.DemoStage = 12
                return CurrentTransformMatrix
            case 12:
                CurrentTransformMatrix[0:3,0:3] = CurrentTransformMatrix[0:3,0:3] @ self.Rz(RotationStepInRad)
                self.Current_pitch = self.Current_pitch + RotationStepInRad
                if self.Current_pitch >= Initial_pitch:
                    self.DemoStage = 13
                return CurrentTransformMatrix
            case 13:
                CurrentTransformMatrix[0:3,0:3] = CurrentTransformMatrix[0:3,0:3] @ self.Rx(RotationStepInRad)
                self.Current_roll = self.Current_roll + RotationStepInRad
                if self.Current_roll >= UpperLimitRoll:
                    self.DemoStage = 14
                return CurrentTransformMatrix
            case 14:
                CurrentTransformMatrix[0:3,0:3] = CurrentTransformMatrix[0:3,0:3] @ self.Rx(-RotationStepInRad)
                self.Current_roll = self.Current_roll - RotationStepInRad
                if self.Current_roll <= LowerLimitRoll:
                    self.DemoStage = 15
                return CurrentTransformMatrix
            case 15:
                CurrentTransformMatrix[0:3,0:3] = CurrentTransformMatrix[0:3,0:3] @ self.Rx(RotationStepInRad)
                self.Current_roll = self.Current_roll + RotationStepInRad
                if self.Current_roll >= Initial_roll:
                    self.DemoStage = 16
                return CurrentTransformMatrix
            case 16:
                CurrentTransformMatrix[0:3,0:3] = CurrentTransformMatrix[0:3,0:3] @ self.Ry(RotationStepInRad)
                self.Current_yaw = self.Current_yaw + RotationStepInRad
                if self.Current_yaw >= UpperLimitYaw:
                    self.DemoStage = 17
                return CurrentTransformMatrix
            case 17:
                CurrentTransformMatrix[0:3,0:3] = CurrentTransformMatrix[0:3,0:3] @ self.Ry(-RotationStepInRad)
                self.Current_yaw = self.Current_yaw - RotationStepInRad
                if self.Current_yaw <= LowerLimitYaw:
                    self.DemoStage = 18
                return CurrentTransformMatrix
            case 18:
                CurrentTransformMatrix[0:3,0:3] = CurrentTransformMatrix[0:3,0:3] @ self.Ry(RotationStepInRad)
                self.Current_yaw = self.Current_yaw + RotationStepInRad
                if self.Current_yaw >= Initial_yaw:
                    self.DemoStage = 0
                    print("Demo cycle completed")
                return CurrentTransformMatrix
            case _:
                return CurrentTransformMatrix
        return CurrentTransformMatrix
    def Demo6DOF(self, InitialTransformMatrix, CurrentTransformMatrix, Xrange=20, Yrange=20, Zrange=20, PitchAngleRange=0.5, RollAngleRange=0.5, YawAngleRange=0.5):
        MovingStepInmm = 2
        RotationStepInRad = 0.015
        UpperLimitX = InitialTransformMatrix[0,3] + Xrange/2
        LowerLimitX = InitialTransformMatrix[0,3] - Xrange/2
        UpperLimitY = InitialTransformMatrix[1,3] + Yrange/2
        LowerLimitY = InitialTransformMatrix[1,3] - Yrange/2
        UpperLimitZ = InitialTransformMatrix[2,3] + Zrange/2
        LowerLimitZ = InitialTransformMatrix[2,3] - Zrange/2
        Initial_R = R.from_matrix(InitialTransformMatrix[0:3,0:3])
        #Initial_roll, Initial_pitch, Initial_yaw = Initial_R.as_euler('xyz', degrees=False)
        Initial_roll, Initial_pitch, Initial_yaw = 0, 0, 0 #self.Current_roll, self.Current_pitch, self.Current_yaw
        UpperLimitPitch = Initial_pitch + RollAngleRange/2
        LowerLimitPitch = Initial_pitch - RollAngleRange/2
        UpperLimitRoll = Initial_roll + PitchAngleRange/2
        LowerLimitRoll = Initial_roll - PitchAngleRange/2
        UpperLimitYaw = Initial_yaw + YawAngleRange/2
        LowerLimitYaw = Initial_yaw - YawAngleRange/2
        match self.DemoStage:
            case 1:
                CurrentTransformMatrix[0,3] = CurrentTransformMatrix[0,3] + MovingStepInmm
                if CurrentTransformMatrix[0,3] >= UpperLimitX:
                    self.DemoStage = 2
                return CurrentTransformMatrix
            case 2:
                CurrentTransformMatrix[0,3] = CurrentTransformMatrix[0,3] - MovingStepInmm
                if CurrentTransformMatrix[0,3] <= LowerLimitX:
                    self.DemoStage = 3
                return CurrentTransformMatrix
            case 3:
                CurrentTransformMatrix[0,3] = CurrentTransformMatrix[0,3] + MovingStepInmm
                if CurrentTransformMatrix[0,3] >= InitialTransformMatrix[0,3]:
                    self.DemoStage = 4
                return CurrentTransformMatrix
            case 4:
                CurrentTransformMatrix[1,3] = CurrentTransformMatrix[1,3] + MovingStepInmm
                if CurrentTransformMatrix[1,3] >= UpperLimitY:
                    self.DemoStage = 5
                return CurrentTransformMatrix
            case 5:
                CurrentTransformMatrix[1,3] = CurrentTransformMatrix[1,3] - MovingStepInmm
                if CurrentTransformMatrix[1,3] <= LowerLimitY:
                    self.DemoStage = 6
                return CurrentTransformMatrix
            case 6:
                CurrentTransformMatrix[1,3] = CurrentTransformMatrix[1,3] + MovingStepInmm
                if CurrentTransformMatrix[1,3] >= InitialTransformMatrix[1,3]:
                    self.DemoStage = 7
                return CurrentTransformMatrix
            case 7:
                CurrentTransformMatrix[2,3] = CurrentTransformMatrix[2,3] + MovingStepInmm
                if CurrentTransformMatrix[2,3] >= UpperLimitZ:
                    self.DemoStage = 8
                return CurrentTransformMatrix
            case 8:
                CurrentTransformMatrix[2,3] = CurrentTransformMatrix[2,3] - MovingStepInmm
                if CurrentTransformMatrix[2,3] <= LowerLimitZ:
                    self.DemoStage = 9
                return CurrentTransformMatrix
            case 9:
                CurrentTransformMatrix[2,3] = CurrentTransformMatrix[2,3] + MovingStepInmm
                if CurrentTransformMatrix[2,3] >= InitialTransformMatrix[2,3]:
                    self.DemoStage = 10
                return CurrentTransformMatrix
            case 10:
                CurrentTransformMatrix[0:3,0:3] = CurrentTransformMatrix[0:3,0:3] @ self.Rz(RotationStepInRad)
                self.Current_pitch = self.Current_pitch + RotationStepInRad
                if self.Current_pitch >= UpperLimitPitch:
                    self.DemoStage = 11
                return CurrentTransformMatrix
            case 11:
                CurrentTransformMatrix[0:3,0:3] = CurrentTransformMatrix[0:3,0:3] @ self.Rz(-RotationStepInRad)
                self.Current_pitch = self.Current_pitch - RotationStepInRad
                if self.Current_pitch <= LowerLimitPitch:
                    self.DemoStage = 12
                return CurrentTransformMatrix
            case 12:
                CurrentTransformMatrix[0:3,0:3] = CurrentTransformMatrix[0:3,0:3] @ self.Rz(RotationStepInRad)
                self.Current_pitch = self.Current_pitch + RotationStepInRad
                if self.Current_pitch >= Initial_pitch:
                    self.DemoStage = 13
                return CurrentTransformMatrix
            case 13:
                CurrentTransformMatrix[0:3,0:3] = CurrentTransformMatrix[0:3,0:3] @ self.Rx(RotationStepInRad)
                self.Current_roll = self.Current_roll + RotationStepInRad
                if self.Current_roll >= UpperLimitRoll:
                    self.DemoStage = 14
                return CurrentTransformMatrix
            case 14:
                CurrentTransformMatrix[0:3,0:3] = CurrentTransformMatrix[0:3,0:3] @ self.Rx(-RotationStepInRad)
                self.Current_roll = self.Current_roll - RotationStepInRad
                if self.Current_roll <= LowerLimitRoll:
                    self.DemoStage = 15
                return CurrentTransformMatrix
            case 15:
                CurrentTransformMatrix[0:3,0:3] = CurrentTransformMatrix[0:3,0:3] @ self.Rx(RotationStepInRad)
                self.Current_roll = self.Current_roll + RotationStepInRad
                if self.Current_roll >= Initial_roll:
                    self.DemoStage = 16
                return CurrentTransformMatrix
            case 16:
                CurrentTransformMatrix[0:3,0:3] = CurrentTransformMatrix[0:3,0:3] @ self.Ry(RotationStepInRad)
                self.Current_yaw = self.Current_yaw + RotationStepInRad
                if self.Current_yaw >= UpperLimitYaw:
                    self.DemoStage = 17
                return CurrentTransformMatrix
            case 17:
                CurrentTransformMatrix[0:3,0:3] = CurrentTransformMatrix[0:3,0:3] @ self.Ry(-RotationStepInRad)
                self.Current_yaw = self.Current_yaw - RotationStepInRad
                if self.Current_yaw <= LowerLimitYaw:
                    self.DemoStage = 18
                return CurrentTransformMatrix
            case 18:
                CurrentTransformMatrix[0:3,0:3] = CurrentTransformMatrix[0:3,0:3] @ self.Ry(RotationStepInRad)
                self.Current_yaw = self.Current_yaw + RotationStepInRad
                if self.Current_yaw >= Initial_yaw:
                    self.DemoStage = 19
                    print("Demo cycle completed")
                return CurrentTransformMatrix
            case 19:
                if self.DemoCycleEndWaitingCounter > 0:
                    self.DemoCycleEndWaitingCounter -= 1
                else:
                    self.DemoStage = 20
                    print("Go to end position")
                return CurrentTransformMatrix   
            case _:
                return CurrentTransformMatrix
        return CurrentTransformMatrix
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
