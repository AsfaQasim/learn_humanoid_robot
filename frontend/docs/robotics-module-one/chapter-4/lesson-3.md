---
title: ROS 2 Launch Files
description: Managing complex robotic systems with ROS 2 Launch files.
---

# ROS 2 Launch Files

## Introduction

ROS 2 Launch files provide a powerful way to manage complex robotic systems by launching multiple nodes with specific configurations simultaneously. They support parameter loading, conditional execution, remapping, and integration with system tools. This lesson explores the launch system architecture, syntax, and best practices for complex robotic applications.

## Launch System Overview

The ROS 2 launch system enables:

- **Multiple node orchestration**: Launch several nodes in a coordinated fashion
- **Parameter management**: Load parameters from YAML files
- **Conditional execution**: Start nodes based on conditions
- **Remapping**: Connect nodes with custom topic/service names
- **Lifecycle management**: Control node lifecycle during runtime

## Launch File Syntax

### Basic Launch File (Python)

Create a basic launch file (`launch/basic_launch.py`):

```python
# launch/basic_launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Declare launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    robot_name = LaunchConfiguration('robot_name', default='my_robot')
    
    # Declare launch arguments
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time'
    )
    
    declare_robot_name = DeclareLaunchArgument(
        'robot_name',
        default_value='my_robot',
        description='Robot name for namespace'
    )
    
    # Create a node
    my_node = Node(
        package='my_package',
        executable='my_node',
        name='my_node',
        parameters=[
            {'use_sim_time': use_sim_time},
            {'robot_name': robot_name}
        ],
        remappings=[
            ('/original_topic', '/remapped_topic'),
            ('/cmd_vel', [LaunchConfiguration('robot_name'), '/cmd_vel'])
        ],
        output='screen',
        arguments=['--ros-args', '--log-level', 'info']
    )
    
    # Return launch description
    return LaunchDescription([
        declare_use_sim_time,
        declare_robot_name,
        my_node
    ])
```

### Launch File with Multiple Nodes

```python
# launch/multi_node_launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node, PushRosNamespace
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_rviz = LaunchConfiguration('use_rviz', default='true')
    
    # Navigation stack node
    nav_stack = Node(
        package='nav2_bringup',
        executable='nav2_world',
        name='nav2_world',
        parameters=[
            PathJoinSubstitution([
                FindPackageShare('my_robot_bringup'),
                'config', 'nav2_params.yaml'
            ]),
            {'use_sim_time': use_sim_time}
        ],
        output='screen'
    )
    
    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[
            PathJoinSubstitution([
                FindPackageShare('my_robot_description'),
                'config', 'robot_params.yaml'
            ]),
            {'use_sim_time': use_sim_time}
        ],
        arguments=[
            PathJoinSubstitution([
                FindPackageShare('my_robot_description'), 
                'urdf', 'robot.urdf.xacro'
            ])
        ]
    )
    
    # Joint state publisher
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        parameters=[
            {'use_sim_time': use_sim_time}
        ]
    )
    
    # RViz with conditional execution
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=[
            '-d', 
            PathJoinSubstitution([
                FindPackageShare('my_robot_bringup'),
                'rviz', 'default.rviz'
            ])
        ],
        condition=IfCondition(use_rviz),
        output='screen'
    )
    
    return LaunchDescription([
        # Launch arguments
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time if true'
        ),
        DeclareLaunchArgument(
            'use_rviz',
            default_value='true',
            description='Open RViz if true'
        ),
        
        # Nodes
        robot_state_publisher,
        joint_state_publisher,
        nav_stack,
        rviz
    ])
```

## Advanced Launch Features

### 1. Conditional Launch

Use conditions to control node startup:

```python
from launch.conditions import IfCondition, UnlessCondition

def generate_launch_description():
    # Launch arguments
    use_sim = LaunchConfiguration('use_sim')
    use_real_hardware = LaunchConfiguration('use_real_hardware')
    
    # Conditional nodes
    sim_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'my_robot',
            '-file', PathJoinSubstitution([
                FindPackageShare('my_robot_description'),
                'models', 'my_robot.sdf'
            ])
        ],
        condition=IfCondition(use_sim)
    )
    
    real_hardware_node = Node(
        package='my_hardware_interface',
        executable='real_hardware_node',
        condition=IfCondition(use_real_hardware)
    )
    
    return LaunchDescription([
        DeclareLaunchArgument('use_sim', default_value='false'),
        DeclareLaunchArgument('use_real_hardware', default_value='false'),
        sim_node,
        real_hardware_node
    ])
```

### 2. Parameter Files

Load parameters from YAML files:

```python
from launch.actions import SetEnvironmentVariable
from launch.substitutions import FindFile

def generate_launch_description():
    # Path to parameter file
    param_file = PathJoinSubstitution([
        FindPackageShare('my_robot_bringup'),
        'config', 'robot_params.yaml'
    ])
    
    controller_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[
            param_file,  # Load from YAML
            {'use_sim_time': LaunchConfiguration('use_sim_time')}
        ],
        output='screen'
    )
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time if true'
        ),
        controller_node
    ])
```

### 3. Remapping and Namespacing

Handle remappings and namespaces effectively:

```python
def generate_launch_description():
    # Push namespace for group of nodes
    namespace_group = GroupAction(
        actions=[
            PushRosNamespace(LaunchConfiguration('robot_namespace')),
            
            # Nodes within namespace
            Node(
                package='navigation2',
                executable='bt_navigator',
                name='bt_navigator',
                parameters=[...],
                remappings=[
                    ('cmd_vel', 'cmd_vel_nav'),
                    ('odom', 'odometry/filtered')
                ]
            ),
            
            Node(
                package='navigation2',
                executable='controller_server',
                name='controller_server',
                parameters=[...]
            )
        ]
    )
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'robot_namespace',
            default_value='robot1',
            description='Robot namespace'
        ),
        namespace_group
    ])
```

## Launch File Best Practices

### 1. Modular Organization

Organize launch files hierarchically:

```
my_robot_bringup/
├── launch/
│   ├── robot.launch.py          # Main launch file
│   ├── controllers.launch.py    # Controller-specific launch
│   ├── navigation.launch.py     # Navigation stack
│   ├── sensors.launch.py        # Sensor drivers
│   └── simulation.launch.py     # Simulation-specific
├── config/
│   ├── robot_params.yaml
│   ├── controllers.yaml
│   └── navigation.yaml
└── rviz/
    └── default.rviz
```

### 2. Including Other Launch Files

Include other launch files using `IncludeLaunchDescription`:

```python
# launch/robot.launch.py
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Include sensor launch file
    sensors_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('my_robot_bringup'),
                'launch',
                'sensors.launch.py'
            ])
        )
    )
    
    # Include controller launch file
    controllers_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('my_robot_bringup'),
                'launch',
                'controllers.launch.py'
            ])
        )
    )
    
    # Include navigation launch file
    navigation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('my_robot_bringup'),
                'launch',
                'navigation.launch.py'
            ])
        )
    )
    
    return LaunchDescription([
        sensors_launch,
        controllers_launch,
        navigation_launch
    ])
```

### 3. Error Handling and Validation

Add validation to your launch files:

```python
from launch import LaunchDescription
from launch.actions import LogInfo, RegisterEventHandler
from launch.event_handlers import OnProcessStart, OnProcessExit
from launch_ros.actions import Node

def generate_launch_description():
    # Robot controller node
    controller_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        name='controller_manager',
        output='screen'
    )
    
    # Log when controller starts
    controller_start_event = LogInfo(
        msg="Controller manager started successfully",
        condition=OnProcessStart(target_action=controller_node)
    )
    
    return LaunchDescription([
        controller_node,
        RegisterEventHandler(controller_start_event)
    ])
```

## Launch File Patterns

### 1. Robot-Agnostic Pattern

Create launch files that work with different robots:

```python
def generate_launch_description():
    # Robot-specific arguments
    robot_description_package = LaunchConfiguration('robot_description_package')
    robot_description_file = LaunchConfiguration('robot_description_file')
    robot_config_package = LaunchConfiguration('robot_config_package')
    
    # Robot state publisher with configurable URDF
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            PathJoinSubstitution([
                FindPackageShare(robot_description_package),
                'urdf', robot_description_file
            ])
        ]
    )
    
    return LaunchDescription([
        DeclareLaunchArgument('robot_description_package'),
        DeclareLaunchArgument('robot_description_file'),
        DeclareLaunchArgument('robot_config_package'),
        robot_state_publisher
    ])
```

### 2. Simulation vs. Real Robot Pattern

Handle both simulation and real robot scenarios:

```python
def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    robot_type = LaunchConfiguration('robot_type')
    
    # Robot controller node
    controller_node = Node(
        package='my_robot_controller',
        executable='robot_controller',
        parameters=[
            PathJoinSubstitution([
                FindPackageShare('my_robot_bringup'),
                'config',
                [robot_type, '_config.yaml']
            ]),
            {'use_sim_time': use_sim_time}
        ]
    )
    
    # Conditional simulation nodes
    sim_nodes = GroupAction(
        condition=IfCondition(use_sim_time),
        actions=[
            # Simulation-specific nodes
            Node(
                package='gazebo_ros',
                executable='spawn_entity.py',
                arguments=['-entity', 'my_robot', '-topic', 'robot_description']
            )
        ]
    )
    
    # Conditional real robot nodes
    real_nodes = GroupAction(
        condition=UnlessCondition(use_sim_time),
        actions=[
            # Real robot-specific nodes
            Node(
                package='my_hardware_interface',
                executable='real_hardware_interface'
            )
        ]
    )
    
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument('robot_type', default_value='diff_drive'),
        controller_node,
        sim_nodes,
        real_nodes
    ])
```

## Launch Command-Line Interface

### Launch Commands

```bash
# Launch a specific launch file
ros2 launch my_package my_launch_file.py

# Launch with arguments
ros2 launch my_package my_launch_file.py use_sim_time:=true robot_name:=turtlebot3

# Launch with multiple arguments
ros2 launch my_package my_launch_file.py \
    use_sim_time:=true \
    robot_namespace:=robot1 \
    params_file:=config/my_params.yaml

# List active launch processes
ros2 launch list

# Get launch file information
ros2 launch --show-args my_package my_launch_file.py
```

## Debugging Launch Files

### 1. Logging and Debugging

```python
from launch.actions import LogInfo, SetEnvironmentVariable

def generate_launch_description():
    # Set environment variables for debugging
    debug_env = SetEnvironmentVariable(
        name='RCUTILS_LOGGING_SEVERITY_THRESHOLD',
        value='DEBUG'
    )
    
    # Log at different stages
    log_start = LogInfo(msg='Starting robot launch process...')
    
    # Main nodes
    robot_node = Node(
        package='my_robot',
        executable='robot_node',
        output='both'  # Both log and screen
    )
    
    log_end = LogInfo(msg='Robot launch complete.')
    
    return LaunchDescription([
        debug_env,
        log_start,
        robot_node,
        log_end
    ])
```

### 2. Launch File Validation

```python
def generate_launch_description():
    # Validate configurations before launch
    validation_node = Node(
        package='my_validation_package',
        executable='config_validator',
        parameters=[
            {'config_file': LaunchConfiguration('config_file', default='default.yaml')}
        ],
        on_exit=[LogInfo(msg='Configuration validation complete')]
    )
    
    return LaunchDescription([validation_node])
```

## Launch File Performance Considerations

### 1. Startup Optimization

Launch nodes in dependency order:

```python
# Launch dependencies first
robot_state_publisher = Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    name='robot_state_publisher'
)

# Then nodes that depend on it
navigation_node = Node(
    package='navigation2',
    executable='bt_navigator',
    name='bt_navigator',
    # This node can wait for transforms published by robot_state_publisher
)
```

### 2. Resource Management

```python
from launch.actions import SetParameter

def generate_launch_description():
    # Set global parameters
    return LaunchDescription([
        # Set parameters that affect multiple nodes
        SetParameter(name='use_sim_time', value=LaunchConfiguration('use_sim_time')),
        
        # Launch nodes with appropriate resource limits
        Node(
            package='computationally_intensive_package',
            executable='heavy_computation_node',
            parameters=[
                {'process_priority': 'low'},  # If supported
                {'resource_limits': {'memory': '1GB'}}
            ]
        )
    ])
```

## Summary

ROS 2 Launch files are essential for managing complex robotic systems, enabling coordinated startup of multiple nodes with specific configurations. They provide powerful features for parameter management, conditional execution, and system orchestration. Understanding launch file syntax, organization patterns, and best practices is crucial for building maintainable robotic applications. Proper use of launch files simplifies system deployment and configuration management across different environments.

The launch system's flexibility allows for sophisticated patterns like robot-agnostic configurations, simulation vs. real robot setups, and modular system organization. Well-designed launch files are a cornerstone of professional ROS 2 development.

