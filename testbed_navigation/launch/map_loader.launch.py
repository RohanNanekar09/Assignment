from launch import LaunchDescription
from launch_ros.actions import Node
import os

def generate_launch_description():

    # Path to the map file
    map_path = os.path.expanduser(
        '~/assignment_ws/src/testbed_bringup/maps/testbed_world.yaml'
    )

    # Map server node
    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{
            'yaml_filename': map_path,
            'use_sim_time': True
        }]
    )

    # Lifecycle manager for map server
    lifecycle_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_map',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'autostart': True,
            'node_names': ['map_server']
        }]
    )

    return LaunchDescription([
        map_server_node,
        lifecycle_node
    ])
