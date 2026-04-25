from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution

def generate_launch_description():
    pkg = FindPackageShare('testbed_navigation')

    map_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([pkg, 'launch', 'map_loader.launch.py'])
        ])
    )

    amcl_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([pkg, 'launch', 'amcl.launch.py'])
        ])
    )

    nav_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([pkg, 'launch', 'navigation.launch.py'])
        ])
    )

    set_initial_pose = ExecuteProcess(
        cmd=['ros2', 'topic', 'pub', '--once', '/initialpose',
             'geometry_msgs/msg/PoseWithCovarianceStamped',
             '{"header": {"frame_id": "map"}, "pose": {"pose": {"position": {"x": 0.001, "y": 5.043, "z": 0.0}, "orientation": {"x": 0.0, "y": 0.0, "z": 0.001, "w": 1.0}}, "covariance": [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853]}}'],
        output='screen'
    )

    return LaunchDescription([
        map_launch,
        TimerAction(period=3.0, actions=[amcl_launch]),
        TimerAction(period=5.0, actions=[set_initial_pose]),
        TimerAction(period=10.0, actions=[nav_launch]),
    ])
