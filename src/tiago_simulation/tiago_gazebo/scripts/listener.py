#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.executors import MultiThreadedExecutor
from rclpy.duration import Duration


import cv2
import numpy as np
import time
import threading
import subprocess
# import tf_transformations

from geometry_msgs.msg import Twist, Pose, PoseStamped, PointStamped, Quaternion
from gazebo_msgs.srv import GetModelState
from sensor_msgs.msg import Image
from std_msgs.msg import Int32
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

from tiago_gazebo.msg import Order
import tuck_arm 
from cv_bridge import CvBridge
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import Constraints, PositionConstraint, OrientationConstraint
from action_msgs.msg import GoalStatus
from shape_msgs.msg import SolidPrimitive

import math
# from tf_transformations import quaternion_from_euler
import tf2_ros
from prepare_pickup import PlayMotionActionClient
from vision import TiagoPixelTo3D
from scipy.spatial.transform import Rotation as R
import message_filters 
from builtin_interfaces.msg import Duration
from moveit_msgs.msg import CollisionObject
from geometry_msgs.msg import Pose as GeoPose

from moveit_msgs.srv import ApplyPlanningScene
from moveit_msgs.srv import GetPlanningScene
from moveit_msgs.msg import PlanningScene, PlanningSceneComponents
from geometry_msgs.msg import WrenchStamped
from moveit_msgs.action import Pickup
from moveit_msgs.msg import Grasp
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from gazebo_msgs.srv import GetEntityState, SetEntityState



class TiagoListener(Node):
    def __init__(self):
        super().__init__('tiago_listener')
        self.get_logger().info("Starting initialization of listener node")
        
        # Initialize components
        self.navigator = BasicNavigator()
        self.bridge = CvBridge()  # To convert ROS Image messages to OpenCV format

        # Subscribers and publishers
        self.get_logger().info("arrived here 0")
        self.vision_node = TiagoPixelTo3D()
        self.pos = self.create_subscription(PointStamped, '/vision/aruco_marker', self.vision_callback, 100)
        self.pos_id = self.create_subscription(Int32, '/vision/aruco_marker_id', self.id_callback, 100)

        self.get_logger().info("arrived here 1")
        self.subscription = self.create_subscription(Order, 'orders', self.listener_callback, 10)
        self.vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.head_cmd = self.create_publisher(JointTrajectory, '/head_controller/joint_trajectory', 10)
        self.move_group_client = ActionClient(self, MoveGroup, 'move_action')
        self.pickup_client = ActionClient(self, Pickup, 'pickup')
        self.move_group_client.wait_for_server()
        self.ft_sensor_subscription = self.create_subscription(
            WrenchStamped, '/ft_sensor_controller/wrench', self.ft_callback, 10)
        # FT Sensor Force Storage
        self.force_z = 0.0  # Stores Z-axis force
        self.play_motion_client = PlayMotionActionClient()

        self.aruco_position = None
        self.aruco_id = None

        self.item_locations = {"coca cola": (-1.308210, -5.157560, 0.975014)}
        # self.item_locations = {"coca cola 1": (-1.308210, -5.157560, 0.975014), "coca cola": (-1.308210, -5.768471, 0.975014)}
        # self.item_locations = {"coca cola": (-1.332914, -5.179209, 1.025000), (-1.332910, -5.790120, 1.025000)}
        self.table_positions = {1: (1.5, -5.5), 2: (-0.5, -9.0), 3: (1.5, -9.0), 4: (0.5, -2.5)}

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        

    def listener_callback(self, msg):
        self.get_logger().info("Processing order in listener_callback")
        # Example long-running task that will no longer block image processing
        threading.Thread(target=self.handle_order, args=(msg,)).start()

    def vision_callback(self, msg):
        self.get_logger().info("Processing vision in vision_callback")
        threading.Thread(target=self.handle_vision, args=(msg,)).start()
        self.get_logger().info("stopped processing vision in vision_callback")


    def id_callback(self, msg):
        self.get_logger().info("Processing id in id_callback")
        threading.Thread(target=self.handle_id, args=(msg,)).start()
        self.get_logger().info("stopped processing id in id_callback")

    def ft_callback(self, msg):
        self.force_z = msg.wrench.force.z

    def object_callback(self):
         threading.Thread(target=self.update_object_position).start()

    def pick_an_item(self, msg):
        bias = 0.17
        self.get_logger().info("Starting pick_an_item method")
        self.get_logger().info("Starting move callback")
        item_location = self.item_locations[msg.item]
        self.get_logger().info(f"Item '{msg.item}' location identified at {item_location}")
        self.nav_to_goal(item_location[0] + 0.66, item_location[1]+0.1, msg)
        self.rotate_robot_to_orientation(math.pi-bias)
        self.lower_head()
        time.sleep(10)#25
        self.play_motion_client.wait_for_server('unfold_arm_amendment')
        self.play_motion_client.send_goal('unfold_arm_amendment', skip_planning=False)
        self.play_motion_client.wait_for_server('open')
        self.play_motion_client.send_goal('open', skip_planning=False)
        time.sleep(25)#25
        while not self.aruco_position:
            self.get_logger().info("Waiting for aruco_position data...")
            time.sleep(0.2)
        x = self.aruco_position[0]
        y = self.aruco_position[1]
        z = self.aruco_position[2]
        self.get_logger().info(f"can positions relative to robot: x: {x}, y: {y}, z: {z}")
        time.sleep(20)#40
        pose = self.get_end_effector_position()
        self.get_logger().info(f"real position of the gripper: x: {pose.position.x}, y: {pose.position.y}, z: {pose.position.z}")
        self.get_logger().info(f"can positions relative to robot: x: {self.aruco_position[0]}, y: {self.aruco_position[1]}, z: {self.aruco_position[2]}")
        bias_x = 0.23
        # bias_x = 0.19
        initial_y_bias = 0.1
        final_y_bias = 0.01

        self.move_arm_torso(x+bias_x, y-0.1, 0.9)
        time.sleep(20)#60
        self.move_arm_torso(x+bias_x, y+0.02, 0.9)
        time.sleep(20)#60
        self.play_motion_client.wait_for_server('close_for_can_1')
        self.play_motion_client.send_goal('close_for_can_1', skip_planning=True)
        for i in range(10):
            self.get_logger().info(f"force exerted by gripper: {self.force_z}")
            time.sleep(0.5)
        time.sleep(20)#60
        self.move_arm_torso(x+bias_x, y+0.02, 1.1)
        time.sleep(20)#60
        return x, y, z


    def can_to_table(self, msg, x, y):
        bias = 0.17
        self.rotate_robot_to_orientation(0-bias)
        table_number = msg.destination_table_number
        self.get_logger().info("Starting can_to_table method")
        table_position = self.table_positions[table_number]
        if table_number==4:
            self.get_logger().info(f"Destination table position identified at {table_position}")
            self.get_logger().info("Navigating to exact table position for item placement")
            self.nav_to_goal(table_position[0], table_position[1], msg)
            self.rotate_robot_to_orientation(math.pi/2-bias)
        else:
            self.get_logger().info(f"Destination table position identified at {table_position}")
            if table_position[0] > 0:
                self.get_logger().info(f"Navigating to approach position at ({table_position[0] - 1}, {table_position[1]})")
                self.nav_to_goal(table_position[0] - 1, table_position[1], msg)
            else:
                self.get_logger().info(f"Navigating to approach position at ({table_position[0] + 1}, {table_position[1]})")
                self.nav_to_goal(table_position[0] + 1, table_position[1], msg)
            self.get_logger().info("Preparing to place item on table with 'prepare_pickup' motion")
            # self.play_motion_client.wait_for_server('prepare_pickup')
            # self.play_motion_client.send_goal('prepare_pickup', skip_planning=True)
            self.get_logger().info("Navigating to exact table position for item placement")
            self.nav_to_goal(table_position[0], table_position[1], msg)
            if table_position[0] > 0:
                self.rotate_robot_to_orientation(0-bias)
            else:
                self.rotate_robot_to_orientation(math.pi-bias)
        bias_x = 0.23
        self.move_arm_torso(x+bias_x, y+0.02, 0.93)
        time.sleep(20)#60
        self.get_logger().info("Opening gripper to release the item on the table")
        self.play_motion_client.wait_for_server('open')
        self.play_motion_client.send_goal('open', skip_planning=True)
        time.sleep(20)
        self.move_arm_torso(x+bias_x, y+0.02, 1.1)
        time.sleep(20)#60
        self.get_logger().info("Completed can_to_table method")


    def handle_order(self, msg):
        # Move to the initial goal, search for the can, and then pick it up
        x, y, _ = self.pick_an_item(msg)
        self.can_to_table(msg, x, y)



    def handle_vision(self, msg):
        self.get_logger().info("handling aruco position message")
        self.aruco_position = (msg.point.x, msg.point.y, msg.point.z)


    def handle_id(self, msg):
        self.get_logger().info("handling id message")
        self.aruco_id = msg.data


    def nav_to_goal(self, x, y, msg):
        self.navigator.waitUntilNav2Active()
        self.get_logger().info(f'TIAGo received an order: "{msg}"')
        
        goal_pose = PoseStamped()
        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = self.navigator.get_clock().now().to_msg()
        goal_pose.pose.position.x = x
        goal_pose.pose.position.y = y
        
        self.navigator.goToPose(goal_pose)
        # Do something during our route
        # (e.x. queue up future tasks or detect person for fine-tuned positioning)
        # Simply print information for workers on the robot's ETA for the demonstation
        i = 0
        while not self.navigator.isTaskComplete():
            i += 1
            feedback = self.navigator.getFeedback()
        self.navigator.cancelTask()
        self.stop_robot()

    def move_arm_torso(self, x, y, z):
        """Moves the arm to the position of the detected can."""
        
        self.get_logger().info("Started planning pickup")
        
        arm_pose = PoseStamped()
        arm_pose.header.frame_id = "base_footprint"
        arm_pose.pose.position.x = x  # Assume reachable distance, convert from pixel if needed
        arm_pose.pose.position.y = y
        arm_pose.pose.position.z = z
        # Set the orientation to keep the gripper parallel to the floor
        roll = 0.0
        pitch = 0.0
        yaw = math.pi/2  # Adjust yaw as needed or keep it zero for a default orientation
        quaternion = R.from_euler('xyz', [roll, pitch, yaw]).as_quat()
        arm_pose.pose.orientation = Quaternion(x=quaternion[0], y=quaternion[1], z=quaternion[2], w=quaternion[3])

        orientation_constraint = OrientationConstraint()
        orientation_constraint.header.frame_id = "base_footprint"
        orientation_constraint.link_name = "gripper_grasping_frame"

        orientation_constraint.orientation.x = quaternion[0]
        orientation_constraint.orientation.y = quaternion[1]
        orientation_constraint.orientation.z = quaternion[2]
        orientation_constraint.orientation.w = quaternion[3]
        orientation_constraint.absolute_x_axis_tolerance = 0.01
        orientation_constraint.absolute_y_axis_tolerance = 0.01
        orientation_constraint.absolute_z_axis_tolerance = 0.01
        orientation_constraint.weight = 1.0


        move_goal = MoveGroup.Goal()
        move_goal.request.group_name = "arm"
        move_goal.request.allowed_planning_time = 50.0  # Increased planning time for accuracy
        move_goal.request.num_planning_attempts = 50  # Multiple attempts to find an optimal path
        move_goal.request.max_velocity_scaling_factor = 0.3  # Slower speed for control
        move_goal.request.max_acceleration_scaling_factor = 0.3  # Lower acceleration for precision

        position_constraint = PositionConstraint()
        position_constraint.header.frame_id = "base_footprint"
        position_constraint.link_name = "gripper_grasping_frame"

        position_constraint.target_point_offset.x = 0.0
        position_constraint.target_point_offset.y = 0.0
        position_constraint.target_point_offset.z = 0.0

        box = SolidPrimitive()
        box.type = SolidPrimitive.BOX
        box.dimensions = [0.001, 0.001, 0.001]

        position_constraint.constraint_region.primitives.append(box)
        position_constraint.constraint_region.primitive_poses.append(arm_pose.pose)
        constraints = Constraints()
        constraints.position_constraints.append(position_constraint)
        constraints.orientation_constraints.append(orientation_constraint)
        move_goal.request.goal_constraints.append(constraints)
        move_goal.request.planner_id = 'PRMkConfigDefault'

        self.get_logger().info("Sending arm move goal...")
        self.move_group_client.send_goal_async(move_goal)

    def get_end_effector_position(self, target_frame='gripper_grasping_frame', base_frame='base_footprint'):
        try:
            now = rclpy.time.Time()
            trans = self.tf_buffer.lookup_transform(base_frame, target_frame, now, timeout=rclpy.duration.Duration(seconds=1.0))
            
            pose = Pose()
            pose.position.x = trans.transform.translation.x
            pose.position.y = trans.transform.translation.y
            pose.position.z = trans.transform.translation.z
            pose.orientation = trans.transform.rotation
            return pose
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            self.get_logger().error(f"Transform error: {e}")
            return None


    def stop_robot(self):
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.vel_publisher.publish(twist)
        self.get_logger().info("Robot stopped in front of the can.")


    def publish_spin_command(self):
        """Publishes a Twist message to make the robot spin."""
        # self.get_logger().info("published spinning command")
        twist = Twist()
        twist.angular.z = 0.3  # Adjust the speed as necessary
        self.vel_publisher.publish(twist)


    def rotate_robot_to_orientation(self, desired_yaw):
        """
        Rotates the robot to match the desired yaw orientation.
        """
        first_time_close = False
        current_yaw = None
        while not current_yaw:
            current_yaw = self.get_current_yaw()
            # self.get_logger().info("yaw is not ready")
            # time.sleep(0.1)
            time.sleep(0.01)
        
        # Calculate the shortest rotation direction
        yaw_difference = desired_yaw - current_yaw
        while abs(yaw_difference) > 0.001:  # Threshold for precision, adjust as needed
            
            # Normalize the yaw difference to be between -pi and pi
            yaw_difference = math.atan2(math.sin(yaw_difference), math.cos(yaw_difference))

            # Determine rotation direction and speed
            rotation_speed = 0.3
            twist = Twist()
            if abs(yaw_difference)<0.1:
                first_time_close = True
            if first_time_close:
                twist.angular.z = rotation_speed if yaw_difference > 0 else -rotation_speed
            else:
                twist.angular.z = -rotation_speed
            # Publish the rotation command
            self.vel_publisher.publish(twist)
            time.sleep(0.01)
            # Update the current yaw and yaw difference
            current_yaw = None
            while not current_yaw:
                current_yaw = self.get_current_yaw()
                # self.get_logger().info("yaw is not ready")
                #time.sleep(0.1)
                time.sleep(0.01)
            yaw_difference = desired_yaw - current_yaw
        
        # Stop the robot once the desired orientation is reached
        # self.stop_robot()
        self.get_logger().info("Rotation complete, robot aligned to desired orientation.")

    def get_current_yaw(self):
        """
        Gets the current yaw angle of the robot from the odometry or transformation.
        Returns:
            float: The current yaw angle in radians.
        """
        try:
            now = rclpy.time.Time()
            trans = self.tf_buffer.lookup_transform('map', 'base_footprint', now, timeout=rclpy.duration.Duration(seconds=1.0))
            # Extract orientation quaternion
            orientation_q = trans.transform.rotation
            # self.get_logger().info(f"step 1: {orientation_q}")
            # Convert quaternion to Euler angles
            orientation_r = R.from_quat([orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w])
            # self.get_logger().info(f"step 2: {orientation_r}")
            euler_angles = orientation_r.as_euler('xyz')
            # self.get_logger().info(f"step 3: {euler_angles}")
            yaw = euler_angles[2]
            return yaw
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            self.get_logger().error(f"Transform error: {e}")
            return None
    def lower_head(self):
        self.get_logger().info("Moving head down")
        jt = JointTrajectory()
        jt.joint_names = ['head_1_joint', 'head_2_joint']
        jtp = JointTrajectoryPoint()
        jtp.positions = [0.0, -0.8]
        duration = Duration()
        duration.sec = 2
        duration.nanosec = 0
        jtp.time_from_start = duration
        jt.points.append(jtp)
        self.head_cmd.publish(jt)
        self.get_logger().info("done")

    #this function are used for grasping an item using force exerted by the gripper feedback,
    #a nice method that we considered to implement

    # def grasp_an_item(self):
    #     self.get_logger().info("Starting pick_an_item method")
    #     # Dynamic gripper closing loop
    #     target_grip_force = 2  # Adjust this based on the can’s weight
    #     close_increment = 0.0008  # Amount to close each step, adjust as needed
    #     max_grip_position = 0.04  # Max gripper position to avoid over-closing
    #     min_grip_position = 0.015
    #     current_grip_position = 0.0  # Initial open position

    #     self.get_logger().info("Starting dynamic closing motion based on FT sensor readings.")
    #     while current_grip_position < max_grip_position:
    #         # Check the current force to see if the can is gripped
    #         if self.force_z > target_grip_force and current_grip_position>=0.015:
    #             self.get_logger().info("Can successfully grasped with optimal force.")
    #             break  # Stop closing as the desired force is reached

    #         # Incrementally close the gripper
    #         current_grip_position += close_increment
    #         self.move_gripper_to_position(current_grip_position)

    #         time.sleep(3)  # Small delay to allow FT sensor reading to stabilize
    #         self.get_logger().info(f"current grip position {current_grip_position}, current gripper force {self.force_z}")

    #     if current_grip_position >= max_grip_position:
    #         self.get_logger().warning("Reached max closing position without achieving desired force.")


    # def move_gripper_to_position(self, position):
    #     """Moves the gripper to the specified position."""
    #     gripper_goal = MoveGroup.Goal()
    #     gripper_goal.request.group_name = "gripper"
        
    #     joint_constraints = [
    #         self.create_joint_constraint("gripper_left_finger_joint", 0.044 - position),
    #         self.create_joint_constraint("gripper_right_finger_joint", 0.044 - position)
    #     ]
        
    #     constraints = Constraints()
    #     constraints.joint_constraints.extend(joint_constraints)
    #     gripper_goal.request.goal_constraints.append(constraints)
        
    #     self.get_logger().info(f"Sending gripper move goal to position: {position}")
    #     self.move_group_client.send_goal_async(gripper_goal)

    # def create_joint_constraint(self, joint_name, position):
    #     from moveit_msgs.msg import JointConstraint
    #     joint_constraint = JointConstraint()
    #     joint_constraint.joint_name = joint_name
    #     joint_constraint.position = position
    #     joint_constraint.tolerance_above = 0.01
    #     joint_constraint.tolerance_below = 0.01
    #     joint_constraint.weight = 1.0
    #     return joint_constraint 




def main(args=None):
    rclpy.init(args=args)
    node = TiagoListener()
    executor = MultiThreadedExecutor()  # Adjust the number of threads as needed
    executor.add_node(node)

    try:
        executor.spin()  # Start multi-threaded spinning
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows()  # Close OpenCV windows


if __name__ == '__main__':
    main()

