---
title: rclpy Basics
description: Introduction to the Python client library for ROS 2.
---

# rclpy Basics

## Introduction

rclpy is the Python client library for ROS 2, providing Python APIs that enable Python programs to communicate with other ROS 2 nodes. This lesson will introduce the fundamental concepts of rclpy, including node creation, parameter management, and basic communication patterns.

## What is rclpy?

rclpy is a Python wrapper around the ROS 2 client library (rcl) that provides:

- Node creation and management
- Publisher and subscriber interfaces
- Service and client interfaces
- Action server and client interfaces
- Parameter handling
- Time and timer utilities
- Logging capabilities

## Installing rclpy

rclpy comes pre-installed with ROS 2 distributions. You can import it in your Python scripts:

```python
import rclpy
from rclpy.node import Node
```

## Creating Your First Node

Here's a basic example of a node using rclpy:

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node_name')
        self.get_logger().info('Hello ROS 2 World!')

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Node Construction and Destruction

### Creating a Node

```python
class MyNode(Node):
    def __init__(self):
        # Initialize the node with a name
        super().__init__('my_node_name')
        
        # Create a parameter descriptor
        from rclpy.parameter import Parameter
        self.declare_parameter('my_parameter', 'default_value')
        
        # Access the parameter value
        my_param = self.get_parameter('my_parameter').value
        self.get_logger().info(f'Parameter value: {my_param}')
```

### Proper Node Shutdown

Always ensure proper cleanup:

```python
def main(args=None):
    rclpy.init(args=args)
    try:
        node = MyNode()
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard interrupt received')
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

## Logging with rclpy

rclpy provides built-in logging capabilities:

```python
class MyNode(Node):
    def __init__(self):
        super().__init__('my_node_name')
        
        # Different log levels
        self.get_logger().debug('Debug message')
        self.get_logger().info('Info message')
        self.get_logger().warn('Warning message')
        self.get_logger().error('Error message')
        self.get_logger().fatal('Fatal message')
```

## Working with Parameters

Parameters in rclpy allow for configuration of nodes:

```python
class ParameterNode(Node):
    def __init__(self):
        super().__init__('parameter_node')
        
        # Declare parameters with default values
        self.declare_parameter('string_param', 'default_value')
        self.declare_parameter('int_param', 42)
        self.declare_parameter('double_param', 3.14)
        self.declare_parameter('bool_param', True)
        
        # Get parameter values
        string_val = self.get_parameter('string_param').value
        int_val = self.get_parameter('int_param').value
        double_val = self.get_parameter('double_param').value
        bool_val = self.get_parameter('bool_param').value
        
        self.get_logger().info(
            f'Parameters: {string_val}, {int_val}, {double_val}, {bool_val}'
        )
        
        # Callback for parameter changes
        self.add_on_set_parameters_callback(self.parameters_callback)
    
    def parameters_callback(self, parameters):
        for param in parameters:
            self.get_logger().info(f'Parameter {param.name} changed to {param.value}')
        return SetParametersResult(successful=True)
```

## Timers in rclpy

Timers allow for periodic execution:

```python
class TimerNode(Node):
    def __init__(self):
        super().__init__('timer_node')
        
        # Create a timer that fires every 0.5 seconds
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.counter = 0
    
    def timer_callback(self):
        self.get_logger().info(f'Timer callback #{self.counter}')
        self.counter += 1
```

## Exception Handling

Proper exception handling is important for robust nodes:

```python
def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Node interrupted by user')
    except Exception as e:
        node.get_logger().error(f'Unhandled exception: {e}')
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

## Best Practices

- Always call `rclpy.init()` before creating nodes
- Use proper exception handling around `rclpy.spin()`
- Declare all parameters during node initialization
- Follow naming conventions for nodes, topics, and parameters
- Use logging appropriately to track node state
- Implement proper cleanup with `destroy_node()` and `rclpy.shutdown()`

## Summary

rclpy provides the essential tools for developing ROS 2 nodes in Python. Understanding the basics of node creation, parameter management, and proper shutdown procedures is fundamental to building reliable ROS 2 applications. In the next lesson, we'll explore how to bridge Python agents with ROS controllers using rclpy.

