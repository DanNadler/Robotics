#!/usr/bin/env python3

import rclpy.duration
import rclpy.publisher
import rclpy.time
# import rospy
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, Image, CameraInfo
import message_filters
import tf2_ros
import tf2_geometry_msgs
# import tf.transformations
# import tf_transformations
from scipy.spatial.transform import Rotation as R
import numpy as np
import cv2
from cv_bridge import CvBridge
from geometry_msgs.msg import PointStamped
from std_msgs.msg import Int32
from rclpy.task import Future

# from control_msgs.msg import PointHeadAction, PointHeadGoal

# from rclpy.exceptions import ParameterNotDeclaredException
# from tf2_ros import LookupException, ConnectivityException, ExtrapolationException


# Load ArUco dictionary and parameters
ARUCO_DICT = cv2.aruco.DICT_6X6_250
# ARUCO_DICT = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
ARUCO_PARAMS = cv2.aruco.DetectorParameters()
# ARUCO_PARAMS = cv2.aruco.DetectorParameters_create()

class TiagoPixelTo3D(Node):
    def __init__(self, show_image=False):

        # Set up subscribers
        super().__init__('TiagoPixelTo3D')
        self.rgb_sub = message_filters.Subscriber(self, Image, '/head_front_camera/rgb/image_raw')
        self.depth_sub = message_filters.Subscriber(self, Image, '/head_front_camera/depth_registered/image_raw')
        self.camera_info_sub = self.create_subscription(CameraInfo, '/head_front_camera/rgb/camera_info', self.camera_info_callback, 10)

        # Approximate time synchronizer for RGB and Depth
        self.ts = message_filters.ApproximateTimeSynchronizer([self.rgb_sub, self.depth_sub], queue_size=10, slop=0.1)
        self.ts.registerCallback(self.image_callback)

        # Publisher for ArUco marker transformed positions and IDs
        self.marker_pub = self.create_publisher(PointStamped, '/vision/aruco_marker', 10) #todo: define new type of messages
        # self.marker_pub = rclpy.publisher('/vision/aruco_marker', PointStamped, queue_size=10)
        self.id_pub = self.create_publisher(Int32, '/vision/aruco_marker_id', 10) #todo: define new type of messages
        # self.id_pub = rclpy.publisher('/vision/aruco_marker_id', Int32, queue_size=10)

        # Transformation buffer and listener for TF2
        self.tf_buffer = tf2_ros.Buffer(cache_time=rclpy.duration.Duration(seconds=20.0))
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # Initialize CvBridge
        self.bridge = CvBridge()

        # Store the CameraInfo data
        self.camera_info_received = False
        self.camera_matrix = None
        self.dist_coeffs = None

        # Set the show_image option
        self.show_image = show_image

        # Create display windows only if show_image is True
        if self.show_image:
            cv2.namedWindow("RGB Image")
            cv2.namedWindow("Depth Image")
        processing_interval = 10.0
        self.timer = self.create_timer(processing_interval, self.timer_callback)

    def image_callback(self, rgb_msg, depth_msg):
        # self.get_logger().info("in timer callback")
        self.last_depth = depth_msg
        self.last_rgb = rgb_msg        

    def camera_info_callback(self, camera_info_msg):
        if not self.camera_info_received:
            self.camera_matrix = np.array(camera_info_msg.k).reshape(3, 3)
            self.dist_coeffs = np.array(camera_info_msg.d)
            self.camera_info_received = True

    def timer_callback(self):
        depth_image_msg = self.last_depth
        rgb_image_msg = self.last_rgb
        if not self.camera_info_received:
            # self.get_logger().warn("Camera info not received yet.")
            return
        # self.get_logger().warn("step 0")
        # Convert the RGB image to an OpenCV image
        self.cv_rgb_image = self.bridge.imgmsg_to_cv2(rgb_image_msg, desired_encoding='bgr8')
        cv_depth_image = self.bridge.imgmsg_to_cv2(depth_image_msg, desired_encoding='passthrough')

        # Normalize depth image for visualization
        # self.get_logger().warn("step 1")
        cv_depth_image_normalized = cv2.normalize(cv_depth_image, None, 0, 255, cv2.NORM_MINMAX)
        cv_depth_image_normalized = np.uint8(cv_depth_image_normalized)
        aruco_dict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
        # self.get_logger().warn("step 2")
        # detector = cv2.aruco.ArucoDetector(dictionary=cv2.aruco.getPredefinedDictionary(ARUCO_DICT), parameters)
        corners, ids, _ = detector.detectMarkers(self.cv_rgb_image)
        # self.get_logger().warn("step 3")
        # If markers are detected
        if ids is not None:
            self.get_logger().info("detection occured")
            success = False
            while not success:
                # self.get_logger().warn("step 4")
                rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.08, self.camera_matrix, self.dist_coeffs)
                for i in range(len(ids)):
                    cv2.aruco.drawDetectedMarkers(self.cv_rgb_image, corners, ids)
                    # cv2.aruco.drawAxis(self.cv_rgb_image, self.camera_matrix, self.dist_coeffs, rvecs[i], tvecs[i], 0.1)
                    cv2.drawFrameAxes(self.cv_rgb_image, self.camera_matrix, self.dist_coeffs, rvecs[i], tvecs[i], 0.1)  # Length of each axis in meters)
                    # Get the translation vector (tvecs) in the camera frame (camera_optical_frame)
                    marker_position_camera = np.array(tvecs[i]).flatten()

                    # Transform the position directly to base_footprint
                    transformed_position_base, euler_angles = self.transform_to_base_footprint(marker_position_camera, rgb_image_msg.header.stamp)
                    self.get_logger().warn(f"transformed position: {transformed_position_base}")
                    if transformed_position_base:
                        # Log and publish the transformed position and marker ID
                        # self.get_logger().info(f"Transformed position in base_footprint: {transformed_position_base}")
                        # self.get_logger().info(f"Yaw: {euler_angles[0]}, Pitch: {euler_angles[1]}, Roll: {euler_angles[2]}")
                        
                        # Publish the transformed position as PointStamped
                        point_msg = PointStamped()
                        point_msg.header.stamp = rgb_image_msg.header.stamp
                        point_msg.header.frame_id = 'base_footprint'
                        point_msg.point.x = transformed_position_base[0]
                        point_msg.point.y = transformed_position_base[1]
                        point_msg.point.z = transformed_position_base[2]
                        self.marker_pub.publish(point_msg)
                        self.get_logger().info("published position")

                        # Publish the marker ID
                        id_msg = Int32()
                        id_msg.data = int(ids[i][0])
                        self.id_pub.publish(id_msg)
                        self.get_logger().info("published ID")
                        success = True
        # Show the RGB and depth images only if show_image is True
        # self.get_logger().warn("step 6")
        if self.show_image:
            cv2.imshow("RGB Image", self.cv_rgb_image)
            cv2.imshow("Depth Image", cv_depth_image_normalized)
            cv2.waitKey(1)

    def transform_to_base_footprint(self, marker_position, stamp):
        time = rclpy.time.Time()
        try:
            # Create a PointStamped message for the marker's position in camera_optical_frame
            point_camera_optical = PointStamped()
            point_camera_optical.header.frame_id = 'head_front_camera_optical_frame'
            point_camera_optical.header.stamp = stamp
            point_camera_optical.point.x = marker_position[0]
            point_camera_optical.point.y = marker_position[1]
            point_camera_optical.point.z = marker_position[2]

            # Get the full transform from camera_optical_frame to base_footprint
            # transform = self.tf_buffer.lookup_transform('base_footprint', 'head_front_camera_optical_frame', stamp, rclpy.time.Duration(1.0))

            # duration = rclpy.duration.Duration(seconds=1.0)
            
            transform = self.tf_buffer.lookup_transform('base_footprint', 'head_front_camera_optical_frame', time)
            # if self.tf_buffer.can_transform('base_footprint', 'head_front_camera_optical_frame', stamp, duration):
            #     transform = self.tf_buffer.lookup_transform('base_footprint', 'head_front_camera_optical_frame', stamp, duration)
            # else:
            #     self.get_logger().warn("Transform not available for the requested time.")
            #     return None, None

            # Transform the point to base_footprint
            transformed_point = tf2_geometry_msgs.do_transform_point(point_camera_optical, transform)

            # Extract the translation part
            transformed_position = [transformed_point.point.x, transformed_point.point.y, transformed_point.point.z]

            # Extract the rotation as a quaternion
            quaternion = (
                transform.transform.rotation.x,
                transform.transform.rotation.y,
                transform.transform.rotation.z,
                transform.transform.rotation.w
            )

            # Convert quaternion to Euler angles (roll, pitch, yaw)
            roll, pitch, yaw = R.from_quat(quaternion).as_euler('xyz', degrees=False)
            return transformed_position, (yaw, pitch, roll)

        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            self.get_logger().info(f"Transform failed: {e}")
            return None, None

        # except (Exception) as e:
        #     self.get_logger().error(f"Transform failed: {e}")
        #     return None, None


    
if __name__ == '__main__':
    rclpy.init(args=None)
    # show_image = rclpy.get_parameter("~show_image", False)
    show_image = False
    processor = TiagoPixelTo3D(show_image=show_image)
    try:
        # rclpy.spin_until_future_complete(processor, processor.future)
        rclpy.spin(processor)
    except KeyboardInterrupt:
        pass
    finally:
        processor.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows() 
