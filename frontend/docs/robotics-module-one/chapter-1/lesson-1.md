---
title: ROS 2 Nodes
description: Understanding the fundamental building blocks of ROS 2 architecture.
---

# ROS 2 Nodes

## Introduction

ROS 2 Nodes are the fundamental building blocks of the Robot Operating System 2 (ROS 2) architecture. A node is an executable that uses ROS 2 to communicate with other nodes. This lesson will cover the core concepts of nodes, their role in the ROS 2 ecosystem, and how they function.

## What is a Node?

A ROS 2 node is an instance of a process that may subscribe to or publish to a topic. Nodes are the primary computational unit in ROS 2 and are used to implement robot applications by performing specific tasks such as sensor processing, control algorithms, or user interfaces.

### Key Characteristics

- **Encapsulation**: Each node encapsulates specific functionality
- **Communication**: Nodes communicate through topics, services, and actions
- **Isolation**: Nodes run in separate processes for better fault tolerance
- **Flexibility**: Nodes can be written in multiple programming languages

## Creating a Node

In ROS 2, nodes are created using client libraries such as `rclpy` for Python or `rclcpp` for C++. Here's a basic example of a node in Python:

```python
import rclpy
from rclpy.node import Node

class MinimalNode(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        # Node initialization code here
        self.get_logger().info('Minimal node initialized')

def main(args=None):
    rclpy.init(args=args)
    minimal_node = MinimalNode()
    
    try:
        rclpy.spin(minimal_node)
    except KeyboardInterrupt:
        pass
    finally:
        minimal_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Node Lifecycle

ROS 2 nodes follow a specific lifecycle state machine:

1. **Unconfigured**: Initial state after creation
2. **Inactive**: Configured but not active
3. **Active**: Fully operational and running
4. **Finalized**: Node is shutting down

This lifecycle management allows for better resource control and coordinated system startup/shutdown.

## Best Practices

- Use descriptive names for nodes to improve system readability
- Implement proper error handling and logging
- Follow the single responsibility principle for node design
- Use parameter servers for configurable behavior
- Implement lifecycle nodes for complex applications

## Summary

ROS 2 Nodes provide the foundation for distributed robotic applications. Understanding their creation, communication patterns, and lifecycle management is essential for developing ROS 2-based systems. In the next lesson, we'll explore how nodes communicate through topics.

