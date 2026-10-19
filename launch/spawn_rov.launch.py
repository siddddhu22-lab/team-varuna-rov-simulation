import os
import xml.etree.ElementTree as ET
 
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node


def generate_launch_description():
    # Locate the installed ROS 2 package
    pkg_share = get_package_share_directory('rov_simulation')

    world_path = os.path.join(
        pkg_share, 'worlds', 'underwater_world.sdf'
    )
    world_root = ET.parse(world_path).getroot()
    world_element = world_root.find('world')
    world_name = (
        world_element.get('name', 'default')
        if world_element is not None
        else 'default'
    )
    model_path = os.path.join(
        pkg_share, 'models', 'underwater_rov', 'model.sdf'
    )
    bridge_config = os.path.join(
        pkg_share, 'config', 'rov_bridge.yaml'
    )

    # Start Gazebo Sim with our underwater world
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_path],
        output='screen'
    )

    # Bridge Gazebo camera messages to ROS 2
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': bridge_config}],
        output='screen'
    )

    # Allow Gazebo time to start before spawning the ROV
    spawn_rov = TimerAction(
        period=5.0,
        actions=[
            Node(
                package='ros_gz_sim',
                executable='create',
                arguments=[
                    '-world', world_name,
                    '-file', model_path,
                    '-name', 'underwater_rov',
                    '-z', '-2.0',
                ],
                output='screen'
            )
        ]
    )

    # 4. Automatically launch rqt_image_view targeting your camera topic
    start_rqt = TimerAction(
        period=7.0,
        actions=[
            Node(
                package='rqt_image_view',
                executable='rqt_image_view',
                arguments=['/rov/camera/image_raw'],
                output='screen'
            )
        ]
    )

    return LaunchDescription([
        gazebo,
        bridge,
        spawn_rov,
        start_rqt   
    ])