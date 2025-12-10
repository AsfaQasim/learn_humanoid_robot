---
title: ROS 2 Services
description: Understanding request-response communication in ROS 2.
---

# ROS 2 Services

## Introduction

ROS 2 Services provide a request-response communication pattern where a client sends a request and receives a response from a server. Unlike topics which provide asynchronous communication, services offer synchronous communication that's ideal for operations that need a direct response. This lesson will explore the concepts of services, clients, and servers in ROS 2.

## Service Communication Overview

Services in ROS 2 implement a request-response pattern where:

- **Service Server** provides a specific functionality and waits for requests
- **Service Client** requests a specific functionality and waits for the response
- **Request/Response Messages** define the data structure for communication

This synchronous pattern is appropriate for operations that need a definitive response before proceeding.

### Service Flow

```
Client Node A → Request → Service Server → Response → Client Node A
Client Node B → Request → Service Server → Response → Client Node B
```

## Creating Services and Clients

Here's an example of how to create a service server and client in Python:

### Service Definition

First, you need a service definition file (typically in an `srv` package). For example, `AddTwoInts.srv`:

```
int64 a
int64 b
---
int64 sum
```

### Service Server Example

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(
            AddTwoInts, 
            'add_two_ints', 
            self.add_two_ints_callback
        )

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(
            f'Incoming request\na: {request.a}, b: {request.b}\n'
            f'Returning: {response.sum}'
        )
        return response

def main(args=None):
    rclpy.init(args=args)
    minimal_service = MinimalService()
    rclpy.spin(minimal_service)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Service Client Example

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MinimalClient(Node):
    def __init__(self):
        super().__init__('minimal_client')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main():
    rclpy.init()
    minimal_client = MinimalClient()
    response = minimal_client.send_request(1, 2)
    minimal_client.get_logger().info(
        f'Result of add_two_ints: {response.sum}'
    )
    minimal_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Service Commands

Useful ROS 2 command-line tools for working with services:

```
ros2 service list                    # List all active services
ros2 service info <service_name>    # Get information about a service
ros2 service call <service_name> <type> <args>  # Call a service
ros2 service type <service_name>    # Get the type of a service
```

## When to Use Services vs Topics

Use services when you need:

- Synchronous communication with guaranteed response
- Action confirmation (e.g., "turn on/off device")
- Data queries (e.g., "get current sensor values")
- Operations with a clear success/failure result

Use topics when you need:

- Asynchronous communication
- Continuous data streams
- Broadcast to multiple receivers
- Decoupled communication patterns

## Service-Quality of Service

Similar to topics, services also support QoS settings:

```python
from rclpy.qos import qos_profile_services_default

# Use default service QoS profile
self.srv = self.create_service(
    AddTwoInts, 
    'add_two_ints', 
    self.add_two_ints_callback,
    qos_profile=qos_profile_services_default
)
```

## Best Practices

- Use services for operations that require a response
- Handle service call timeouts appropriately
- Design service interfaces to be idempotent when possible
- Consider the performance implications of synchronous calls
- Use appropriate service types from standard interfaces when available

## Summary

ROS 2 Services provide a reliable request-response communication mechanism for robotic applications. Understanding when to use services versus topics is crucial for designing effective ROS 2 systems. In the next chapter, we'll explore how Python agents can interact with ROS controllers using rclpy.

