# Chapter 4 Content Plan: Advanced ROS 2 Concepts

## Required Diagrams

### 1. Parameter System Architecture
- Shows parameter declaration, storage, and access patterns
- Node-specific parameter management
- YAML configuration file integration

### 2. Action Communication Flow
- Goal-Feedback-Result lifecycle
- Client-Server interaction pattern
- Cancellation and preemption flows

### 3. Launch System Architecture
- Launch file structure and relationships
- Node orchestration and dependency management
- Parameter and remapping handling

### 4. Action vs Service vs Topic Comparison
- Decision matrix for communication patterns
- Performance characteristics
- Use case recommendations

## Required Code Examples

### 1. Parameter Declaration with Descriptors
```python
from rclpy.node import Node
from rclpy.parameter import ParameterType
from rcl_interfaces.msg import ParameterDescriptor
from rcl_interfaces.msg import IntegerRange, FloatingPointRange

class ConstrainedParameterNode(Node):
    def __init__(self):
        super().__init__('constrained_parameter_node')
        
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
```

### 2. Parameter Callback with Validation
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
    
    def parameters_callback(self, params):
        """Callback for parameter changes"""
        result = SetParametersResult()
        result.successful = True
        
        for param in params:
            if param.name == 'kp' and param.type_ == Parameter.Type.DOUBLE:
                if param.value < 0 or param.value > 10:
                    result.successful = False
                    result.reason = 'kp must be between 0 and 10'
                    return result
        return result
```

### 3. Action Server Implementation
```python
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from example_interfaces.action import Fibonacci

class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        
        # Create action server
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )
    
    def goal_callback(self, goal_request):
        """Accept or reject goal requests"""
        return GoalResponse.ACCEPT
    
    def cancel_callback(self, goal_handle):
        """Accept or reject cancel requests"""
        return CancelResponse.ACCEPT
    
    async def execute_callback(self, goal_handle):
        """Execute the goal"""
        # Get the goal order
        order = goal_handle.request.order
        
        # Create feedback message
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]
        
        # Simulate computation with feedback
        for i in range(1, order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return Fibonacci.Result()
            
            if not goal_handle.is_active:
                return Fibonacci.Result()
            
            # Calculate next Fibonacci number
            feedback_msg.sequence.append(
                feedback_msg.sequence[i] + feedback_msg.sequence[i-1]
            )
            
            # Publish feedback
            goal_handle.publish_feedback(feedback_msg)
            
            # Sleep to simulate work
            from time import sleep
            sleep(0.5)
        
        # Goal completed successfully
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        
        return result
```

### 4. Action Client Implementation
```python
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci

class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        
        # Create action client
        self._action_client = ActionClient(
            self,
            Fibonacci,
            'fibonacci'
        )
    
    def send_goal(self, order):
        """Send goal to action server"""
        # Wait for action server
        self._action_client.wait_for_server()
        
        # Create goal message
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order
        
        # Send goal with callbacks
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        
        self._send_goal_future.add_done_callback(self.goal_response_callback)
    
    def goal_response_callback(self, future):
        """Handle goal response"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
        
        self.get_logger().info('Goal accepted')
        
        # Request result
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.result_callback)
    
    def feedback_callback(self, feedback_msg):
        """Handle feedback during execution"""
        self.get_logger().info(f'Received feedback: {feedback_msg.feedback.sequence}')
    
    def result_callback(self, future):
        """Handle final result"""
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')
```

### 5. Launch File with Multiple Nodes
```python
# launch/multi_node_launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {'use_sim_time': use_sim_time}
        ],
        arguments=[
            'path/to/robot.urdf'
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
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time if true'
        ),
        robot_state_publisher,
        joint_state_publisher
    ])
```

### 6. Conditional Launch with Remapping
```python
from launch import LaunchDescription
from launch.actions import GroupAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, PushRosNamespace

def generate_launch_description():
    use_rviz = LaunchConfiguration('use_rviz')
    
    # Namespace group
    namespace_group = GroupAction(
        actions=[
            PushRosNamespace(LaunchConfiguration('robot_namespace')),
            
            Node(
                package='navigation2',
                executable='bt_navigator',
                name='bt_navigator',
                remappings=[
                    ('cmd_vel', 'cmd_vel_nav'),
                    ('odom', 'odometry/filtered')
                ]
            ),
        ]
    )
    
    # Conditional RViz node
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', 'path/to/config.rviz'],
        condition=IfCondition(use_rviz)
    )
    
    return LaunchDescription([
        DeclareLaunchArgument('use_rviz', default_value='true'),
        DeclareLaunchArgument('robot_namespace', default_value='robot1'),
        namespace_group,
        rviz
    ])
```