import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    # Path to the world file
    world_file_name = 'cafe_upgraded.world'
    world_path = os.path.join(get_package_share_directory('tiago_gazebo'), 'worlds', world_file_name)

    # Gazebo launch command
    gazebo = ExecuteProcess(
        cmd=['gazebo', '--verbose', world_path, '-s', 'libgazebo_ros_factory.so'],
        output='screen'
    )

    # Nodes for controlling the TIAGo robot (Navigation 2)
    tiago_nav2 = Node(
        package='nav2_bringup',
        executable='bringup_launch',
        name='nav2_bringup',
        output='screen',
        parameters=[{'use_sim_time': True}],
    )

    return LaunchDescription([
        gazebo,
        tiago_nav2
    ])
