# Chapter 2 Content Plan: Python & ROS 2 (rclpy)

## Required Diagrams

### 1. rclpy Architecture Diagram
- Shows rclpy as Python wrapper around rcl
- Relationship between Python code and ROS 2 system
- Node structure and components

### 2. Agent-Controller Bridge Architecture
- High-level Python agent connecting to ROS controllers
- Communication flow between agent and controllers
- Different integration patterns (direct, external, action-based)

### 3. Communication Strategy Comparison
- Topic-based vs Service-based vs Action-based communication
- When to use each approach
- Performance and reliability considerations

## Required Code Examples

### 1. Basic rclpy Node Structure
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

### 2. Parameter Declaration and Usage
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
```

### 3. Timer Usage in rclpy
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

### 4. Direct Integration Agent Pattern
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import JointState
import numpy as np

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
        
        # Store sensor data
        self.current_state = None
        
        # Timer for agent decision-making
        self.timer = self.create_timer(0.1, self.agent_callback)
    
    def sensor_callback(self, msg):
        """Receive sensor data from the robot"""
        self.current_state = np.array(msg.position + msg.velocity)
    
    def agent_callback(self):
        """Run the agent to determine control actions"""
        if self.current_state is not None:
            # Apply agent logic to determine action
            action = self.determine_action(self.current_state)
            
            # Publish the action as a command
            cmd_msg = Float32MultiArray()
            cmd_msg.data = action.tolist()
            self.command_pub.publish(cmd_msg)
```

### 5. Action-Based Communication
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

### 6. Synchronization Pattern for Agent-Controller
```python
import threading

class SynchronizedAgentNode(Node):
    def __init__(self):
        super().__init__('sync_agent')
        self.state_lock = threading.Lock()
        self.current_robot_state = None
    
    def sensor_callback(self, msg):
        """Update robot state with thread safety"""
        with self.state_lock:
            self.current_robot_state = msg
            
    def get_robot_state(self):
        """Get robot state with thread safety"""
        with self.state_lock:
            return self.current_robot_state
```