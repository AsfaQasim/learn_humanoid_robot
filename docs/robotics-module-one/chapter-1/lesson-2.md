---
title: ROS 2 Topics
description: Understanding publish-subscribe communication in ROS 2.
---

# ROS 2 Topics

## Introduction

ROS 2 Topics form the backbone of the publish-subscribe communication pattern in ROS 2. Topics enable asynchronous communication between nodes, allowing data to be shared efficiently in robotic systems. This lesson will explore the concepts of topics, publishers, and subscribers in ROS 2.

## Topic Communication Overview

Topics in ROS 2 implement a publish-subscribe communication pattern where:

- **Publishers** send messages to a specific topic
- **Subscribers** receive messages from a specific topic
- **Messages** are data structures that flow between nodes

This pattern allows for decoupled communication where publishers and subscribers don't need to know about each other directly.

### Message Flow

```
Publisher Node A → Topic → Subscriber Node B
Publisher Node C → Topic → Subscriber Node D
                    ↘ Subscriber Node E
```

## Creating Publishers and Subscribers

Here's an example of how to create a publisher and subscriber in Python:

### Publisher Example

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Subscriber Example

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Quality of Service (QoS)

ROS 2 provides Quality of Service (QoS) settings to control the behavior of topic communication:

- **Reliability**: Best effort or reliable delivery
- **Durability**: Volatile or transient local
- **History**: Keep last or keep all
- **Depth**: Number of messages to store in history

## Topic Commands

Useful ROS 2 command-line tools for working with topics:

```
ros2 topic list                    # List all active topics
ros2 topic info <topic_name>      # Get information about a topic
ros2 topic echo <topic_name>      # Print messages from a topic
ros2 topic pub <topic_name> <type> <data>  # Publish to a topic
```

## Best Practices

- Use descriptive topic names following ROS naming conventions
- Consider QoS settings based on application requirements
- Use appropriate message types for the data being exchanged
- Be mindful of message size and frequency for performance
- Use latching for static data that new subscribers need

## Summary

ROS 2 Topics provide a flexible and scalable communication mechanism for robotic systems. Understanding publishers, subscribers, and QoS settings is crucial for building robust ROS 2 applications. In the next lesson, we'll explore services for request-response communication patterns.

