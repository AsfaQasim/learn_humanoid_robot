---
title: Bridging Mechanisms
description: Techniques for bridging between Python agents and ROS controllers.
---

# Bridging Mechanisms

## Introduction

This lesson explores various techniques and tools for bridging between Python agents and ROS controllers. We'll examine the ROS 2 bridge ecosystem, design patterns for effective integration, and practical implementation examples that demonstrate how to create robust connections between high-level Python code and ROS-based control systems.

## Overview of Bridging Approaches

There are several approaches to bridging Python agents with ROS controllers:

1. **Direct Integration**: Running Python agents as ROS nodes
2. **ROS Bridge**: Using rosbridge_suite for WebSocket communication
3. **Custom Adapters**: Building custom communication layers
4. **ROS 2 Python API**: Using rclpy directly
5. **External Interfaces**: Using ROS interfaces without full integration

## Direct Integration with rclpy

The most common and efficient approach is to implement the Python agent directly as a ROS node using rclpy:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory
import threading
import time

class DirectBridgingAgent(Node):
    def __init__(self):
        super().__init__('direct_bridging_agent')
        
        # Publishers for sending commands to controllers
        self.joint_cmd_pub = self.create_publisher(
            JointTrajectory,
            '/position_trajectory_controller/joint_trajectory',
            10
        )
        
        # Subscribers for receiving sensor data
        self.sensor_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.sensor_callback,
            10
        )
        
        # Store the latest sensor data
        self.latest_sensor_data = None
        
        # Timer for agent decision making
        self.agent_timer = self.create_timer(0.05, self.agent_logic)  # 20Hz
        
        # Lock for thread safety
        self.data_lock = threading.Lock()
    
    def sensor_callback(self, msg):
        """Receive sensor data from the robot"""
        with self.data_lock:
            self.latest_sensor_data = {
                'position': list(msg.position),
                'velocity': list(msg.velocity),
                'effort': list(msg.effort),
                'timestamp': msg.header.stamp
            }
    
    def agent_logic(self):
        """Main agent decision making logic"""
        with self.data_lock:
            sensor_data = self.latest_sensor_data
        
        if sensor_data is not None:
            # Process sensor data and make decisions
            action = self.compute_action(sensor_data)
            
            # Send action to controller
            self.send_action_to_controller(action)
    
    def compute_action(self, sensor_data):
        """Compute action based on sensor data"""
        # Example: Simple proportional controller
        target_position = [1.0, 0.5, -0.3]  # Example target
        current_position = sensor_data['position']
        
        # Compute desired joint velocities
        velocities = []
        for curr, target in zip(current_position, target_position):
            velocity = 0.5 * (target - curr)  # Simple proportional control
            velocities.append(velocity)
        
        return velocities
    
    def send_action_to_controller(self, action):
        """Send action to the ROS controller"""
        traj_msg = JointTrajectory()
        traj_msg.joint_names = ['joint1', 'joint2', 'joint3']  # Example joint names
        
        # Create trajectory point
        point = JointTrajectory.Point()
        # Convert velocities to positions for position controller
        # In practice, you'd implement proper trajectory planning
        point.velocities = action
        point.time_from_start.sec = 0
        point.time_from_start.nanosec = 50000000  # 50ms
        
        traj_msg.points = [point]
        self.joint_cmd_pub.publish(traj_msg)

def main(args=None):
    rclpy.init(args=args)
    agent = DirectBridgingAgent()
    
    try:
        rclpy.spin(agent)
    except KeyboardInterrupt:
        agent.get_logger().info('Agent stopped by user')
    finally:
        agent.destroy_node()
        rclpy.shutdown()
```

## ROS Bridge (rosbridge_suite)

For scenarios where the Python agent runs external to the ROS system:

```python
# Using rosbridge_library with roslibpy
import roslibpy

class ExternalBridgeAgent:
    def __init__(self, rosbridge_addr='localhost', rosbridge_port=9090):
        # Connect to ROS bridge
        self.ros = roslibpy.Ros(host=rosbridge_addr, port=rosbridge_port)
        self.ros.run()
        
        # Create publishers and subscribers
        self.cmd_pub = roslibpy.Topic(
            self.ros, 
            '/joint_trajectory', 
            'trajectory_msgs/JointTrajectory'
        )
        
        self.sensor_sub = roslibpy.Topic(
            self.ros, 
            '/joint_states', 
            'sensor_msgs/JointState'
        )
        
        # Set callback for sensor data
        self.sensor_sub.subscribe(self.sensor_callback)
        
        # Store sensor data
        self.latest_sensor_data = None
    
    def sensor_callback(self, message):
        """Callback for receiving sensor data via ROS bridge"""
        self.latest_sensor_data = message
    
    def send_command(self, command):
        """Send command via ROS bridge"""
        self.cmd_pub.publish(command)
    
    def close_connection(self):
        """Close the ROS bridge connection"""
        self.ros.close()

# Usage
agent = ExternalBridgeAgent()
# Run agent logic here
agent.close_connection()
```

## Custom Bridge Implementation

For custom requirements, you can create a bridge that uses alternative communication mechanisms:

```python
import socket
import json
import threading
from queue import Queue

class CustomBridgeAgent:
    def __init__(self, ros_bridge_port=8080):
        # Socket for communication with ROS bridge
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', ros_bridge_port))
        
        # Threading for non-blocking communication
        self.receive_queue = Queue()
        self.send_queue = Queue()
        
        # Start communication threads
        self.receive_thread = threading.Thread(target=self.receive_loop)
        self.send_thread = threading.Thread(target=self.send_loop)
        self.running = True
        
        self.receive_thread.start()
        self.send_thread.start()
    
    def receive_loop(self):
        """Receive messages from ROS bridge"""
        while self.running:
            try:
                data = self.sock.recv(1024)
                if data:
                    msg = json.loads(data.decode('utf-8'))
                    self.receive_queue.put(msg)
            except Exception as e:
                print(f"Receive error: {e}")
                break
    
    def send_loop(self):
        """Send messages to ROS bridge"""
        while self.running:
            try:
                if not self.send_queue.empty():
                    msg = self.send_queue.get()
                    self.sock.send(json.dumps(msg).encode('utf-8'))
                time.sleep(0.01)  # 100Hz
            except Exception as e:
                print(f"Send error: {e}")
                break
    
    def send_command(self, cmd_type, cmd_data):
        """Send a command through the bridge"""
        msg = {
            'type': cmd_type,
            'data': cmd_data
        }
        self.send_queue.put(msg)
    
    def get_sensor_data(self):
        """Get the latest sensor data"""
        messages = []
        while not self.receive_queue.empty():
            messages.append(self.receive_queue.get())
        return messages[-1] if messages else None
    
    def close(self):
        """Close the bridge connection"""
        self.running = False
        self.sock.close()

# ROS Bridge Component (typically implemented in C++ or Python as ROS node)
class ROSBridgeNode(Node):
    def __init__(self):
        super().__init__('ros_bridge_node')
        
        # ROS subscribers and publishers
        self.sensor_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.sensor_callback,
            10
        )
        
        self.cmd_pub = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory',
            10
        )
        
        # Socket server for external agent
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 8080))
        self.server_socket.listen(1)
        
        # Start socket handling thread
        self.socket_thread = threading.Thread(target=self.socket_handler)
        self.socket_thread.start()
    
    def sensor_callback(self, msg):
        """Forward sensor data to external agent"""
        # Convert ROS message to JSON and send via socket
        sensor_data = {
            'type': 'sensor',
            'position': list(msg.position),
            'velocity': list(msg.velocity),
            'effort': list(msg.effort),
            'timestamp': msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        }
        # Send via socket to external agent
    
    def socket_handler(self):
        """Handle socket communication with external agent"""
        while rclpy.ok():
            conn, addr = self.server_socket.accept()
            # Handle messages from external agent
            data = conn.recv(1024)
            if data:
                cmd = json.loads(data.decode('utf-8'))
                self.process_command(cmd)
    
    def process_command(self, cmd):
        """Process command from external agent"""
        if cmd['type'] == 'trajectory':
            # Convert JSON command to ROS message
            traj_msg = JointTrajectory()
            # Set up trajectory message from cmd['data']
            self.cmd_pub.publish(traj_msg)
```

## Hybrid Approaches

Often, the most effective approach combines multiple techniques:

```python
import rclpy
from rclpy.node import Node
from threading import Thread
import queue
import time

class HybridBridgingNode(Node):
    def __init__(self):
        super().__init__('hybrid_bridging')
        
        # ROS communication
        self.sensor_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.ros_sensor_callback,
            10
        )
        
        self.cmd_pub = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory',
            10
        )
        
        # Separate thread for Python agent computation
        self.agent_queue = queue.Queue()
        self.sensor_queue = queue.Queue()
        self.agent_thread = Thread(target=self.agent_worker)
        self.agent_thread.start()
        
        # Timer for sending data to agent thread
        self.ros_timer = self.create_timer(0.02, self.send_to_agent)
    
    def ros_sensor_callback(self, msg):
        """Receive sensor data from ROS"""
        sensor_data = {
            'position': list(msg.position),
            'velocity': list(msg.velocity)
        }
        self.sensor_queue.put(sensor_data)
    
    def send_to_agent(self):
        """Send latest sensor data to agent thread"""
        if not self.sensor_queue.empty():
            # Get the most recent sensor data
            while not self.sensor_queue.empty():
                sensor_data = self.sensor_queue.get()
            # Send to agent
            self.agent_queue.put(sensor_data)
    
    def agent_worker(self):
        """Worker thread for Python agent computation"""
        while True:
            try:
                # Wait for sensor data
                sensor_data = self.agent_queue.get(timeout=1.0)
                
                # Run agent computation (non-blocking for ROS)
                action = self.compute_agent_action(sensor_data)
                
                # Publish action via ROS (thread-safe using callbacks)
                self.get_logger().debug('Agent action computed')
                self.send_command(action)
                
            except queue.Empty:
                continue
            except Exception as e:
                self.get_logger().error(f'Agent worker error: {e}')
    
    def send_command(self, action):
        """Send command to ROS (called from agent thread)"""
        # Use a callback group to ensure thread safety
        self.get_logger().info(f'Sending command: {action}')
        # In practice, you'd use a separate publisher for thread safety

def main(args=None):
    rclpy.init(args=args)
    node = HybridBridgingNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

## Performance and Efficiency Tips

### 1. Message Optimization

Reduce the size and frequency of messages:

```python
# Instead of sending all sensor data, send only required information
def optimize_sensor_data(self, full_msg):
    """Extract only necessary sensor information"""
    return {
        'position': full_msg.position[:6],  # Only first 6 joints
        'timestamp': full_msg.header.stamp.sec
    }
```

### 2. Buffering Strategies

Use appropriate buffering for high-frequency data:

```python
from collections import deque

class BufferedAgent:
    def __init__(self):
        self.sensor_buffer = deque(maxlen=10)  # Keep last 10 sensor readings
    
    def sensor_callback(self, msg):
        """Add sensor data to buffer"""
        self.sensor_buffer.append(msg)
```

### 3. Asynchronous Processing

Avoid blocking operations in ROS callbacks:

```python
import asyncio

class AsyncBridgingNode(Node):
    def __init__(self):
        super().__init__('async_bridging')
        
        # For long-running agent computations
        self.agent_executor = concurrent.futures.ThreadPoolExecutor()
    
    def sensor_callback(self, msg):
        """Non-blocking callback that dispatches to thread pool"""
        future = self.agent_executor.submit(self.process_sensor_data, msg)
        future.add_done_callback(self.handle_agent_result)
```

## Summary

Bridging Python agents with ROS controllers can be achieved through various approaches depending on your specific requirements. Direct integration with rclpy provides the best performance and tightest coupling, while ROS bridge solutions offer flexibility for external agents. Custom bridges can provide specialized functionality when standard approaches don't meet your needs. In the next chapter, we'll explore the Unified Robot Description Format (URDF) and its role in humanoid robotics.

