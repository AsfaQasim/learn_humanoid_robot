---
title: ROS 2 Parameters
description: Understanding and using parameters for configurable ROS 2 nodes.
---

# ROS 2 Parameters

## Introduction

Parameters in ROS 2 provide a flexible way to configure nodes at runtime without recompiling code. They enable dynamic adjustment of node behavior, making systems more adaptable to different environments and use cases. This lesson explores the parameter system in ROS 2, including declaration, access patterns, validation, and best practices.

## Parameter Overview

Parameters in ROS 2 are:

- **Node-specific**: Each node maintains its own parameter set
- **Runtime-configurable**: Can be changed during execution
- **Type-safe**: Strong typing with support for basic data types
- **Hierarchical**: Can be organized in a namespace hierarchy
- **Declarable**: Parameters can be declared with constraints

## Declaring Parameters

### Basic Parameter Declaration

Parameters must be declared before use, typically in the node constructor:

```python
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter

class ParameterNode(Node):
    def __init__(self):
        super().__init__('parameter_node')
        
        # Declare parameters with default values
        self.declare_parameter('robot_name', 'my_robot')
        self.declare_parameter('max_velocity', 1.0)
        self.declare_parameter('control_frequency', 50)
        self.declare_parameter('use_sim_time', False)
        self.declare_parameter('safety_thresholds', [0.5, 1.0, 2.0])
        
        # Access parameter values
        robot_name = self.get_parameter('robot_name').value
        max_velocity = self.get_parameter('max_velocity').value
        control_frequency = self.get_parameter('control_frequency').value
        
        self.get_logger().info(
            f'Initialized with robot_name: {robot_name}, '
            f'max_velocity: {max_velocity}, '
            f'control_frequency: {control_frequency}'
        )
```

### Parameter Descriptors

For more control over parameter constraints:

```python
from rclpy.node import Node
from rclpy.parameter import ParameterType
from rclpy.qos import qos_profile_system_default

class ConstrainedParameterNode(Node):
    def __init__(self):
        super().__init__('constrained_parameter_node')
        
        # Import parameter descriptor classes
        from rcl_interfaces.msg import ParameterDescriptor
        from rcl_interfaces.msg import IntegerRange, FloatingPointRange
        
        # Declare with descriptor for integer parameter
        int_descriptor = ParameterDescriptor(
            type=ParameterType.PARAMETER_INTEGER,
            description='Control loop frequency in Hz',
            additional_constraints='Must be positive',
            integer_range=[IntegerRange(from_value=1, to_value=1000, step=1)]
        )
        self.declare_parameter('control_frequency', 50, int_descriptor)
        
        # Declare with descriptor for float parameter
        float_descriptor = ParameterDescriptor(
            type=ParameterType.PARAMETER_DOUBLE,
            description='Maximum allowed velocity',
            additional_constraints='Must be positive',
            floating_point_range=[FloatingPointRange(from_value=0.0, to_value=10.0, step=0.1)]
        )
        self.declare_parameter('max_velocity', 1.0, float_descriptor)
        
        # Declare with descriptor for boolean parameter
        bool_descriptor = ParameterDescriptor(
            type=ParameterType.PARAMETER_BOOL,
            description='Enable safety checks'
        )
        self.declare_parameter('enable_safety', True, bool_descriptor)
```

## Accessing Parameter Values

### Basic Access

```python
class ParameterAccessNode(Node):
    def __init__(self):
        super().__init__('parameter_access_node')
        
        # Declare parameters
        self.declare_parameter('threshold', 1.0)
        self.declare_parameter('robot_id', 'robot_01')
        self.declare_parameter('enabled', True)
        
        # Get single parameter
        threshold = self.get_parameter('threshold').value
        robot_id = self.get_parameter('robot_id').value
        enabled = self.get_parameter('enabled').value
        
        # Get multiple parameters at once
        params = self.get_parameters(['threshold', 'robot_id', 'enabled'])
        threshold_alt = params[0].value
        robot_id_alt = params[1].value
        enabled_alt = params[2].value
        
        # Safely get parameter with fallback
        timeout = self.get_parameter_or('timeout', Parameter('timeout', value=5.0)).value
```

### Parameter Existence Check

```python
def check_and_access_parameter(self, param_name, default_value):
    """Check if parameter exists before accessing"""
    if self.has_parameter(param_name):
        return self.get_parameter(param_name).value
    else:
        # Declare with default if not exists
        self.declare_parameter(param_name, default_value)
        return self.get_parameter(param_name).value
```

## Parameter Callbacks

### On-Set Parameter Callbacks

React to parameter changes:

```python
from rcl_interfaces.msg import SetParametersResult

class CallbackParameterNode(Node):
    def __init__(self):
        super().__init__('callback_parameter_node')
        
        # Declare initial parameters
        self.declare_parameter('kp', 1.0)
        self.declare_parameter('ki', 0.1)
        self.declare_parameter('kd', 0.01)
        
        # Add callback for parameter changes
        self.add_on_set_parameters_callback(self.parameters_callback)
        
        # Initialize controller with current values
        self.update_controller_gains()
    
    def parameters_callback(self, params):
        """Callback for parameter changes"""
        result = SetParametersResult()
        result.successful = True
        
        # Process each parameter change
        for param in params:
            if param.name == 'kp' and param.type_ == Parameter.Type.DOUBLE:
                if param.value < 0 or param.value > 10:
                    result.successful = False
                    result.reason = 'kp must be between 0 and 10'
                    return result
                self.get_logger().info(f'Updating Kp to: {param.value}')
                
            elif param.name == 'ki' and param.type_ == Parameter.Type.DOUBLE:
                if param.value < 0 or param.value > 1:
                    result.successful = False
                    result.reason = 'ki must be between 0 and 1'
                    return result
                self.get_logger().info(f'Updating Ki to: {param.value}')
                
        # Update controller if all parameters are valid
        if result.successful:
            self.update_controller_gains()
        
        return result
    
    def update_controller_gains(self):
        """Update controller with current parameter values"""
        kp = self.get_parameter('kp').value
        ki = self.get_parameter('ki').value
        kd = self.get_parameter('kd').value
        # Apply gains to controller
        self.get_logger().info(f'Controller updated with gains: Kp={kp}, Ki={ki}, Kd={kd}')
```

## Parameter Types and Conversions

ROS 2 supports several parameter types:

```python
class ParameterTypesNode(Node):
    def __init__(self):
        super().__init__('parameter_types_node')
        
        # String parameter
        self.declare_parameter('robot_name', 'turtlebot')
        
        # Integer parameter
        self.declare_parameter('robot_id', 1)
        
        # Double parameter
        self.declare_parameter('max_speed', 0.5)
        
        # Boolean parameter
        self.declare_parameter('use_acceleration_limits', True)
        
        # Array parameters
        self.declare_parameter('joint_limits', [1.0, 2.0, 1.5])
        self.declare_parameter('color_rgba', [0.5, 0.5, 1.0, 1.0])
        
        # Get parameters with type checking
        robot_name = self.get_parameter('robot_name').value  # Returns str
        robot_id = self.get_parameter('robot_id').value      # Returns int
        max_speed = self.get_parameter('max_speed').value    # Returns float
        use_accel = self.get_parameter('use_acceleration_limits').value  # Returns bool
        joint_limits = self.get_parameter('joint_limits').value         # Returns list of floats
        color_rgba = self.get_parameter('color_rgba').value            # Returns list of floats
```

## Parameter Files and YAML Configuration

### Using YAML Parameter Files

Create a YAML parameter file (e.g., `config/robot_params.yaml`):

```yaml
parameter_node:
  ros__parameters:
    robot_name: "optimized_robot"
    max_velocity: 2.5
    control_frequency: 100
    safety_thresholds: [0.8, 1.2, 2.5]
    use_pid: true
    pid_gains:
      kp: 1.5
      ki: 0.2
      kd: 0.05
```

Load the parameter file in your launch file:

```python
# launch/parameter_demo.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    config = os.path.join(
        get_package_share_directory('my_package'),
        'config',
        'robot_params.yaml'
    )
    
    return LaunchDescription([
        Node(
            package='my_package',
            executable='parameter_node',
            name='parameter_node',
            parameters=[config]
        )
    ])
```

## Command Line Parameter Tools

### Setting Parameters from Command Line

```bash
# List all parameters of a node
ros2 param list /parameter_node

# Get a specific parameter value
ros2 param get /parameter_node robot_name

# Set a parameter value
ros2 param set /parameter_node max_velocity 3.0

# Get all parameters as YAML
ros2 param dump /parameter_node

# Load parameters from a YAML file
ros2 param load /parameter_node config.yaml
```

## Advanced Parameter Patterns

### 1. Dynamic Reconfiguration Pattern

```python
class DynamicConfigNode(Node):
    def __init__(self):
        super().__init__('dynamic_config_node')
        
        # Declare parameters with common robotics settings
        self.declare_parameter('linear_vel_limit', 1.0)
        self.declare_parameter('angular_vel_limit', 1.0)
        self.declare_parameter('acceleration_limit', 2.0)
        self.declare_parameter('deceleration_limit', 3.0)
        
        # Timer to periodically check and apply parameters
        self.timer = self.create_timer(1.0, self.check_parameter_updates)
        
        # Store previous values to detect changes
        self.prev_linear_vel = self.get_parameter('linear_vel_limit').value
        self.prev_angular_vel = self.get_parameter('angular_vel_limit').value
    
    def check_parameter_updates(self):
        """Check for parameter changes and apply them"""
        current_linear = self.get_parameter('linear_vel_limit').value
        current_angular = self.get_parameter('angular_vel_limit').value
        
        if current_linear != self.prev_linear_vel:
            self.get_logger().info(f'Linear velocity limit changed to: {current_linear}')
            # Apply new limit to controller
            self.apply_velocity_limit(current_linear)
            self.prev_linear_vel = current_linear
        
        if current_angular != self.prev_angular_vel:
            self.get_logger().info(f'Angular velocity limit changed to: {current_angular}')
            # Apply new limit to controller
            self.apply_angular_limit(current_angular)
            self.prev_angular_vel = current_angular
    
    def apply_velocity_limit(self, limit):
        """Apply velocity limit to robot controller"""
        # Implementation to update controller with new limit
        pass
    
    def apply_angular_limit(self, limit):
        """Apply angular limit to robot controller"""
        # Implementation to update controller with new limit
        pass
```

### 2. Parameter Groups

For complex systems, group related parameters:

```python
from rclpy.node import Node

class ComplexParameterNode(Node):
    def __init__(self):
        super().__init__('complex_parameter_node')
        
        # Control parameters
        self.declare_parameter('control.loop_frequency', 50)
        self.declare_parameter('control.max_velocity', 1.0)
        self.declare_parameter('control.max_acceleration', 2.0)
        
        # Navigation parameters
        self.declare_parameter('nav.planning_frequency', 5)
        self.declare_parameter('nav.global_plan_frequency', 1)
        self.declare_parameter('nav.local_plan_frequency', 10)
        
        # Safety parameters
        self.declare_parameter('safety.min_distance', 0.5)
        self.declare_parameter('safety.collision_threshold', 0.2)
        self.declare_parameter('safety.emergency_stop', True)
        
        # Get all parameters in a group
        control_params = self.get_parameters_by_prefix('control.')
        nav_params = self.get_parameters_by_prefix('nav.')
        safety_params = self.get_parameters_by_prefix('safety.')
        
        self.get_logger().info(f'Control parameters: {control_params}')
```

## Parameter Best Practices

### 1. Naming Conventions

```python
# Good parameter naming
self.declare_parameter('robot.max_linear_velocity', 1.0)
self.declare_parameter('controller.kp_linear', 1.0)
self.declare_parameter('sensors.laser_scan_range', 10.0)

# Avoid generic names
# self.declare_parameter('value', 1.0)  # Too generic
# self.declare_parameter('param1', 2.0)  # Not descriptive
```

### 2. Validation and Constraints

```python
class ValidatedParameterNode(Node):
    def __init__(self):
        super().__init__('validated_parameter_node')
        
        from rcl_interfaces.msg import ParameterDescriptor
        from rcl_interfaces.msg import FloatingPointRange
        
        # Define parameter with validation
        vel_descriptor = ParameterDescriptor(
            type=ParameterType.PARAMETER_DOUBLE,
            description='Maximum linear velocity limit',
            floating_point_range=[FloatingPointRange(from_value=0.0, to_value=5.0, step=0.01)]
        )
        self.declare_parameter('max_linear_vel', 1.0, vel_descriptor)
```

### 3. Default Values and Documentation

```python
def initialize_parameters(self):
    """Initialize all parameters with documented defaults"""
    # Control parameters
    self.declare_parameter(
        'control_loop_rate', 
        50, 
        ParameterDescriptor(description='Rate of the main control loop in Hz')
    )
    
    # Robot-specific parameters
    self.declare_parameter(
        'robot_wheel_radius', 
        0.05, 
        ParameterDescriptor(description='Radius of robot wheels in meters')
    )
    
    # Navigation parameters
    self.declare_parameter(
        'min_approach_distance', 
        0.1, 
        ParameterDescriptor(description='Minimum distance to goal before considering reached')
    )
```

## Integration with rclpy

Parameters integrate seamlessly with other rclpy features:

```python
class IntegratedParameterNode(Node):
    def __init__(self):
        super().__init__('integrated_parameter_node')
        
        # Declare parameters
        self.declare_parameter('publish_frequency', 10)
        
        # Create publisher based on parameter
        self.publisher = self.create_publisher(String, 'parameter_status', 10)
        
        # Create timer based on parameter frequency
        freq = self.get_parameter('publish_frequency').value
        self.timer = self.create_timer(1.0/freq, self.timer_callback)
    
    def timer_callback(self):
        """Publish parameter-dependent information"""
        current_vel = self.get_parameter('max_velocity', 1.0).value
        msg = String()
        msg.data = f'Max velocity is currently: {current_vel}'
        self.publisher.publish(msg)
```

## Summary

Parameters provide a powerful mechanism for configuring ROS 2 nodes at runtime. By properly declaring, accessing, and responding to parameter changes, you can create flexible and adaptable robotic systems. Understanding parameter callbacks and validation is particularly important for safety-critical applications. The next lesson will cover ROS 2 Actions for more complex goal-oriented communication patterns.

