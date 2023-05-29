
import os
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.actions import LogInfo

def generate_launch_description():
    
    #RVIZ2
    rviz_config_dir = os.path.join(get_package_share_directory('localization_server'), 'rviz', 'path.rviz')
    rviz_node = Node(
            package='rviz2',
            executable='rviz2',
            output='screen',
            name='rviz_node',
            parameters=[{'use_sim_time': True}],
            arguments=['-d', rviz_config_dir])

    package_description = "map_server"

    arg_mapFile = DeclareLaunchArgument(
        'map_file', default_value= 'warehouse_map_real.yaml')

    map_config_file_name = LaunchConfiguration('map_file')

    global_path_to_map_file = PathJoinSubstitution([
        FindPackageShare(package_description),
        'config',
        map_config_file_name
    ])

    map_a =   Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[{'use_sim_time': True},
                        {'yaml_filename': global_path_to_map_file}
                ])

    nav2_yaml = os.path.join(get_package_share_directory('localization_server'), 'config', 'amcl_config.yaml')

    amcl_node=Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[nav2_yaml]
        )


    return LaunchDescription([
        arg_mapFile,
        map_a,
        amcl_node,
        rviz_node,
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_localization',
            output='screen',
            parameters=[{'use_sim_time': True},
                        {'autostart': True},
                        {'node_names': ['map_server','amcl']}]
        )
    ])

