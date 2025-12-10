---
title: Python Agents & ROS Controllers
description: Connecting Python-based agents to ROS controllers for robot control.
---

# Python Agents & ROS Controllers

## Introduction

This lesson explores how Python-based agents can interact with ROS controllers to provide intelligent control for robotic systems. We'll examine the architecture patterns, communication protocols, and implementation strategies that enable effective bridging between high-level Python agents and low-level ROS controllers.

## Architecture Overview

The connection between Python agents and ROS controllers typically involves:

- **High-level Python Agent**: Implements decision-making, planning, or learning algorithms
- **ROS Bridge**: Facilitates communication between Python agent and ROS ecosystem
- **ROS Controllers**: Execute low-level commands on hardware or simulation
- **Robot Hardware/Model**: Physical or simulated robotic platform

### Common Patterns

1. **Direct Integration**: Python agent runs as a ROS node
2. **External Agent**: Python agent communicates via ROS topics/services
3. **Action-based**: Using ROS actions for complex goal-oriented tasks

## Implementing the Bridge

### Direct Integration Approach

When implementing the Python agent as a ROS node:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import JointState
from control_msgs.msg import JointTrajectoryControllerState
import numpy as np
import tensorflow as tf  # Example ML library

class AgentControllerNode(Node):
    def __init__(self):
        super().__init__('agent_controller')
        
        # Subscribers for sensor data
        self.sensor_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.sensor_callback,
            10
        )
        
        # Publishers for control commands
        self.command_pub = self.create_publisher(
            Float32MultiArray,
            '/agent_commands',
            10
        )
        
        # Initialize the agent (example: neural network)
        self.agent = self.initialize_agent()
        
        # Store sensor data
        self.current_state = None
        
        # Timer for agent decision-making
        self.timer = self.create_timer(0.1, self.agent_callback)
    
    def sensor_callback(self, msg):
        """Receive sensor data from the robot"""
        self.current_state = np.array(msg.position + msg.velocity)
    
    def initialize_agent(self):
        """Initialize the agent (e.g., trained neural network)"""
        # Example: Simple neural network
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(10,)),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(6, activation='tanh')  # 6 DOF example
        ])
        # Load trained weights here
        return model
    
    def agent_callback(self):
        """Run the agent to determine control actions"""
        if self.current_state is not None:
            # Normalize state input
            normalized_state = self.normalize_state(self.current_state)
            
            # Get action from agent
            action = self.agent.predict(np.expand_dims(normalized_state, axis=0))
            
            # Publish the action as a command
            cmd_msg = Float32MultiArray()
            cmd_msg.data = action[0].tolist()
            self.command_pub.publish(cmd_msg)
    
    def normalize_state(self, state):
        """Normalize the state for the agent"""
        # Example normalization
        return (state - np.mean(state)) / (np.std(state) + 1e-8)

def main(args=None):
    rclpy.init(args=args)
    agent_node = AgentControllerNode()
    
    try:
        rclpy.spin(agent_node)
    except KeyboardInterrupt:
        pass
    finally:
        agent_node.destroy_node()
        rclpy.shutdown()
```

### Controller Interface

Connecting to ROS controllers typically involves:

```python
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class ControllerInterface(Node):
    def __init__(self):
        super().__init__('controller_interface')
        
        # Publisher to joint trajectory controller
        self.traj_pub = self.create_publisher(
            JointTrajectory,
            '/position_trajectory_controller/joint_trajectory',
            10
        )
        
        # Example: Send a trajectory command
        self.send_trajectory_command()
    
    def send_trajectory_command(self):
        """Send a joint trajectory command to the controller"""
        traj_msg = JointTrajectory()
        traj_msg.joint_names = ['joint1', 'joint2', 'joint3']  # Example joint names
        
        # Create trajectory point
        point = JointTrajectoryPoint()
        point.positions = [1.0, 0.5, -0.3]  # Target positions
        point.velocities = [0.0, 0.0, 0.0]   # Desired velocities
        point.time_from_start = Duration(sec=2, nanosec=0)  # 2 seconds to reach
        
        traj_msg.points = [point]
        
        # Publish the trajectory
        self.traj_pub.publish(traj_msg)
```

## Communication Strategies

### 1. Topic-Based Communication

For continuous data exchange:

```python
# Publisher example
self.agent_action_pub = self.create_publisher(Float32MultiArray, '/agent_action', 10)

# Subscriber example
self.robot_state_sub = self.create_subscription(
    JointState, 
    '/joint_states', 
    self.state_callback, 
    10
)
```

### 2. Service-Based Communication

For request-response interactions:

```python
from example_interfaces.srv import Trigger

class AgentNode(Node):
    def __init__(self):
        super().__init__('agent_node')
        
        # Service client to request reset from environment
        self.reset_client = self.create_client(Trigger, '/reset_simulation')
        
        # Service server to accept goals from higher level
        self.goal_service = self.create_service(
            Trigger, 
            '/agent/set_goal', 
            self.goal_callback
        )
    
    async def call_reset_service(self):
        """Call the reset service"""
        if self.reset_client.wait_for_service(timeout_sec=1.0):
            request = Trigger.Request()
            future = self.reset_client.call_async(request)
            return await future
        else:
            self.get_logger().error('Reset service not available')
            return None
```

### 3. Action-Based Communication

For goal-oriented tasks with feedback:

```python
from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory

class AgentNode(Node):
    def __init__(self):
        super().__init__('agent_node')
        
        self.action_client = ActionClient(
            self, 
            FollowJointTrajectory, 
            '/position_trajectory_controller/follow_joint_trajectory'
        )
    
    def send_goal(self, trajectory_points):
        """Send a trajectory goal to the controller"""
        goal_msg = FollowJointTrajectory.Goal()
        goal_msg.trajectory = trajectory_points
        
        self.action_client.wait_for_server()
        return self.action_client.send_goal_async(goal_msg)
```

## Best Practices for Agent-Controller Integration

### 1. Asynchronous Communication

Use asynchronous patterns to prevent blocking:

```python
import asyncio

class AsyncAgentNode(Node):
    def __init__(self):
        super().__init__('async_agent')
        
        # Timer for periodic agent updates
        self.timer = self.create_timer(0.1, self.timer_callback)
    
    def timer_callback(self):
        """Non-blocking agent update"""
        # Don't block here; use threading or async if computationally intensive
        future = self.perform_agent_computation()
        # Handle future asynchronously if needed
```

### 2. State Synchronization

Ensure proper synchronization between agent and controller:

```python
class SynchronizedAgentNode(Node):
    def __init__(self):
        super().__init__('sync_agent')
        self.state_lock = threading.Lock()
        self.current_robot_state = None
    
    def sensor_callback(self, msg):
        """Update robot state with thread safety"""
        with self.state_lock:
            self.current_robot_state = msg
```

### 3. Error Handling and Recovery

Implement robust error handling:

```python
def agent_callback(self):
    try:
        # Agent computation
        action = self.compute_action()
        
        # Publish action
        self.publish_action(action)
        
    except Exception as e:
        self.get_logger().error(f'Agent error: {e}')
        # Implement safe recovery strategy
        self.fallback_behavior()
```

## Performance Considerations

- **Real-time constraints**: Consider timing requirements for control loops
- **Computational load**: Move complex computations off the main thread if needed
- **Communication overhead**: Optimize message frequency and size
- **Memory management**: Monitor memory usage during long-running operations

## Summary

Connecting Python agents to ROS controllers requires careful consideration of architecture patterns, communication strategies, and performance requirements. The direct integration approach works well for many applications, but external agents may be appropriate when using complex ML frameworks that don't integrate well with ROS. In the next lesson, we'll examine specific bridging mechanisms that facilitate this connection.

