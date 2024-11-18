#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import time
from rclpy.task import Future
from geometry_msgs.msg import PoseWithCovarianceStamped


class HeadController(Node):
    def __init__(self):
        super().__init__('head_controller')
        self.publisher = self.create_publisher(JointTrajectory, '/head_controller/joint_trajectory', 10)
        self.publisher_initial_pose = self.create_publisher(PoseWithCovarianceStamped, '/initialpose', 10)
        for i in range(100):
            self.publish_initial_pose()
            time.sleep(0.1)
        self.timer = self.create_timer(0.1, self.timer_callback)  # Timer at 0.1 seconds
        self.head_1_goal = 0.0  # Replace with desired value
        self.head_2_goal = -0.3  # Replace with desired value
        self.timer_count = 0
        self.timer_done_future = Future()
    
    def timer_callback(self):
        if self.timer_count < 100:
            self.move_head(self.head_1_goal, self.head_2_goal)
            self.timer_count = self.timer_count + 1
        else:
            self.timer.cancel()
            # self.destroy_node()
            self.timer_done_future.set_result(True)
            
    
    def move_head(self, head_1_goal, head_2_goal):
        traj_msg = JointTrajectory()
        traj_msg.joint_names = ['head_1_joint', 'head_2_joint']

        point = JointTrajectoryPoint()
        point.positions = [head_1_goal, head_2_goal]  # Goal positions for the joints
        point.velocities = [0.1, 0.1]  # Example velocities; adjust as needed
        point.time_from_start.sec = 2  # Time to reach the goal
        
        traj_msg.points.append(point)
        self.publisher.publish(traj_msg)
        self.get_logger().info(f'Sent head trajectory command to move to [{head_1_goal}, {head_2_goal}] with velocities [0.1, 0.1]')

    def publish_initial_pose(self):
        # Define the message
        msg = PoseWithCovarianceStamped()
        msg.header.frame_id = 'map'

        # Set position
        msg.pose.pose.position.x = 0.0
        msg.pose.pose.position.y = 0.0
        msg.pose.pose.position.z = 0.0

        # Set orientation (facing forward, no rotation)
        msg.pose.pose.orientation.x = 0.0
        msg.pose.pose.orientation.y = 0.0
        msg.pose.pose.orientation.z = 0.0
        msg.pose.pose.orientation.w = 1.0

        # Set covariance
        msg.pose.covariance = [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1e6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1e6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1e6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01]
        # Publish the message
        #[0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1e6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1e6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1e6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0685]
        self.publisher_initial_pose.publish(msg)
        self.get_logger().info('Published initial pose')

def main(args=None):
    rclpy.init(args=args)
    controller = HeadController()
    rclpy.spin_until_future_complete(controller, controller.timer_done_future)  # Run the node with spinning
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
