---
title: ROS 2 Actions
description: Understanding and implementing goal-oriented communication with ROS 2 Actions.
---

# ROS 2 Actions

## Introduction

ROS 2 Actions provide a goal-oriented communication pattern that extends beyond the simple request-response of services or the asynchronous nature of topics. Actions are ideal for long-running tasks that may take time to complete, provide feedback during execution, and can be preempted or cancelled. This lesson explores the structure, implementation, and use cases for ROS 2 Actions.

## Actions Overview

Actions combine the features of services and topics to provide:

- **Goal requests**: Similar to service requests but for long-running tasks
- **Feedback**: Continuous updates during task execution
- **Result reporting**: Final outcome when the task completes
- **Cancel capability**: Ability to interrupt ongoing tasks
- **Preemption**: Ability to replace ongoing tasks with new ones

## Action Message Types

Each action definition creates three message types:

1. **Goal** (`action_name.action`): Defines the goal message structure
2. **Feedback** (`action_name.action`): Provides ongoing feedback during execution
3. **Result** (`action_name.action`): Contains the final result when complete

## Defining Action Messages

Action definitions use a special `.action` file format:

```
# NavigateToPose.action

# Goal definition
geometry_msgs/PoseStamped pose
string behavior_tree

---
# Result definition
bool reached_pose

---
# Feedback definition
geometry_msgs/PoseStamped current_pose
string message
float32 distance_remaining
```

This single file creates three message types:
- `NavigateToPose_Goal`
- `NavigateToPose_Result`  
- `NavigateToPose_Feedback`

## Action Server Implementation

### Basic Action Server

```python
import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from example_interfaces.action import Fibonacci  # Built-in example

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
    
    def destroy_node(self):
        self._action_server.destroy()
        super().destroy_node()
    
    def goal_callback(self, goal_request):
        """Accept or reject goal requests"""
        self.get_logger().info('Received goal request')
        # Accept all goals for this example
        return GoalResponse.ACCEPT
    
    def cancel_callback(self, goal_handle):
        """Accept or reject cancel requests"""
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT
    
    async def execute_callback(self, goal_handle):
        """Execute the goal - this runs in a separate thread"""
        self.get_logger().info('Executing goal...')
        
        # Get the goal order
        order = goal_handle.request.order
        
        # Create feedback message
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]
        
        # Simulate computation with feedback
        for i in range(1, order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()
            
            if not goal_handle.is_active:
                self.get_logger().info('Goal aborted')
                return Fibonacci.Result()
            
            # Calculate next Fibonacci number
            feedback_msg.sequence.append(
                feedback_msg.sequence[i] + feedback_msg.sequence[i-1]
            )
            
            # Publish feedback
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'Feedback: {feedback_msg.sequence}')
            
            # Sleep to simulate work
            from time import sleep
            sleep(0.5)
        
        # Goal completed successfully
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        self.get_logger().info(f'Goal succeeded with result: {result.sequence}')
        
        return result

def main(args=None):
    rclpy.init(args=args)
    action_server = FibonacciActionServer()
    
    try:
        rclpy.spin(action_server)
    except KeyboardInterrupt:
        pass
    finally:
        action_server.destroy_node()
        rclpy.shutdown()
```

### Advanced Action Server with Robot Navigation

```python
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from nav2_msgs.action import NavigateToPose  # Hypothetical navigation action
import threading
import time

class NavigationActionServer(Node):
    def __init__(self):
        super().__init__('navigation_action_server')
        
        # Create callback group for thread safety
        callback_group = ReentrantCallbackGroup()
        
        # Action server
        self._action_server = ActionServer(
            self,
            NavigateToPose,
            'navigate_to_pose',
            execute_callback=self.execute_callback,
            callback_group=callback_group
        )
        
        # Publishers and subscribers
        self.pose_sub = self.create_subscription(
            PoseWithCovarianceStamped,
            'amcl_pose',
            self.pose_callback,
            10,
            callback_group=callback_group
        )
        
        self.cmd_pub = self.create_publisher(
            Twist,
            'cmd_vel',
            10,
            callback_group=callback_group
        )
        
        # Store current robot pose
        self.current_pose = None
        self.current_pose_lock = threading.RLock()
    
    def pose_callback(self, msg):
        """Update current robot pose"""
        with self.current_pose_lock:
            self.current_pose = msg.pose.pose
    
    def calculate_distance(self, pose1, pose2):
        """Calculate Euclidean distance between two poses"""
        dx = pose1.position.x - pose2.position.x
        dy = pose1.position.y - pose2.position.y
        return (dx*dx + dy*dy) ** 0.5
    
    async def execute_callback(self, goal_handle):
        """Execute navigation goal"""
        goal = goal_handle.request.pose
        
        self.get_logger().info(f'Navigating to pose: ({goal.pose.position.x}, {goal.pose.position.y})')
        
        # Create feedback message
        feedback_msg = NavigateToPose.Feedback()
        
        # Navigation loop
        while rclpy.ok():
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Navigation canceled')
                return NavigateToPose.Result()
            
            if not goal_handle.is_active:
                self.get_logger().info('Navigation aborted')
                return NavigateToPose.Result()
            
            # Get current pose for feedback
            with self.current_pose_lock:
                if self.current_pose is None:
                    continue
                current = self.current_pose
            
            # Calculate distance to goal
            distance = self.calculate_distance(current, goal.pose)
            
            # Check if reached
            if distance < 0.2:  # 20cm threshold
                goal_handle.succeed()
                result = NavigateToPose.Result()
                result.reached_pose = True
                self.get_logger().info('Navigation completed successfully')
                return result
            
            # Provide feedback
            feedback_msg.current_pose.pose = current
            feedback_msg.distance_remaining = distance
            feedback_msg.message = f'Navigating, {distance:.2f}m remaining'
            
            goal_handle.publish_feedback(feedback_msg)
            
            # Generate navigation command (simplified)
            cmd = Twist()
            cmd.linear.x = min(0.5, distance)  # Approach speed based on distance
            cmd.angular.z = 0.5 * math.atan2(
                goal.pose.position.y - current.position.y,
                goal.pose.position.x - current.position.x
            )
            self.cmd_pub.publish(cmd)
            
            # Wait before next iteration
            time.sleep(0.1)
        
        # If we get here, something went wrong
        goal_handle.abort()
        result = NavigateToPose.Result()
        result.reached_pose = False
        return result
```

## Action Client Implementation

### Basic Action Client

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
        
        # Shutdown after receiving result
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    
    action_client = FibonacciActionClient()
    
    # Send goal
    action_client.send_goal(10)
    
    # Spin to process callbacks
    try:
        rclpy.spin(action_client)
    except KeyboardInterrupt:
        pass
    finally:
        action_client.destroy_node()
```

### Advanced Action Client

```python
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.duration import Duration
from geometry_msgs.msg import PoseStamped
from my_robot_msgs.action import MoveArm  # Hypothetical action

class AdvancedActionClient(Node):
    def __init__(self):
        super().__init__('advanced_action_client')
        
        self._action_client = ActionClient(
            self,
            MoveArm,
            'move_arm'
        )
    
    def send_navigation_goal(self, target_pose):
        """Send navigation goal with timeout and cancellation handling"""
        self._action_client.wait_for_server()
        
        goal_msg = MoveArm.Goal()
        goal_msg.target_pose = target_pose
        goal_msg.allow_replanning = True
        goal_msg.planning_attempts = 5
        
        # Send goal with feedback
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        
        # Set timeout for goal acceptance
        timer = self.create_timer(5.0, self.timeout_callback)
        
        self._send_goal_future.add_done_callback(
            lambda future: self.goal_response_callback(future, timer)
        )
    
    def goal_response_callback(self, future, timer):
        """Handle goal response with timer cancellation"""
        timer.cancel()
        
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
        
        self.get_logger().info('Goal accepted, waiting for result')
        
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.result_callback)
    
    def timeout_callback(self):
        """Handle timeout waiting for goal acceptance"""
        self.get_logger().info('Goal request timed out')
        rclpy.shutdown()
    
    def feedback_callback(self, feedback_msg):
        """Handle feedback with additional processing"""
        current_pose = feedback_msg.current_pose
        distance = feedback_msg.distance_remaining
        message = feedback_msg.message
        
        self.get_logger().info(
            f'Feedback: {message}, dist: {distance:.2f}m, '
            f'pos: ({current_pose.pose.position.x:.2f}, {current_pose.pose.position.y:.2f})'
        )
    
    def result_callback(self, future):
        """Handle result with error checking"""
        goal_result = future.result()
        result = goal_result.result
        status = goal_result.status
        
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Action completed successfully')
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().info('Action was canceled')
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().info('Action was aborted')
        else:
            self.get_logger().info(f'Action failed with status: {status}')
        
        # Process result based on success
        if hasattr(result, 'reached_pose') and result.reached_pose:
            self.get_logger().info('Reached target pose successfully')
        else:
            self.get_logger().info('Failed to reach target pose')
        
        rclpy.shutdown()
```

## Action Command-Line Tools

### Using ros2 action Command

```bash
# List all actions
ros2 action list

# Get action type information
ros2 action type /fibonacci

# Send a goal from command line
ros2 action send_goal /fibonacci example_interfaces/action/Fibonacci "{order: 5}"

# Send goal and stream feedback
ros2 action send_goal -f /fibonacci example_interfaces/action/Fibonacci "{order: 5}"

# Get action information
ros2 action info /fibonacci
```

## Action Best Practices

### 1. Proper Error Handling

```python
async def execute_callback(self, goal_handle):
    try:
        # Perform action
        result = await self.perform_action(goal_handle.request)
        
        if goal_handle.is_cancel_requested:
            goal_handle.canceled()
            return MyAction.Result()
        
        goal_handle.succeed()
        return result
        
    except Exception as e:
        self.get_logger().error(f'Action failed: {e}')
        goal_handle.abort()
        return MyAction.Result()  # or appropriate error result
```

### 2. Resource Management

```python
def destroy_node(self):
    """Properly clean up action server"""
    if hasattr(self, '_action_server'):
        self._action_server.destroy()
    super().destroy_node()
```

### 3. Appropriate Use Cases

Use actions when:

- **Long-running operations**: Tasks that take seconds to minutes
- **Progress feedback**: Need to report ongoing progress
- **Cancellable operations**: Tasks that can be interrupted
- **Preemptible goals**: Ability to replace current goal with new one

Use topics/services instead when:

- **Short operations**: Fast request-response patterns
- **Continuous data**: Streaming sensor information
- **Simple commands**: Toggle switches, configuration updates

## Integration with Navigation Systems

Actions are particularly useful in navigation systems:

```python
# Navigation action client example
class NavigationClient(Node):
    def __init__(self):
        super().__init__('navigation_client')
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
    
    def navigate_to(self, x, y, theta=0.0):
        """Navigate to a specific pose"""
        goal = NavigateToPose.Goal()
        goal.pose = PoseStamped()
        goal.pose.pose.position.x = x
        goal.pose.pose.position.y = y
        goal.pose.pose.orientation = self.yaw_to_quaternion(theta)
        
        # Send with feedback
        future = self.nav_client.send_goal_async(
            goal,
            feedback_callback=self.nav_feedback
        )
        future.add_done_callback(self.nav_goal_response)
    
    def nav_feedback(self, feedback_msg):
        """Handle navigation feedback"""
        self.get_logger().info(f'Navigating: {feedback_msg.feedback.message}')
```

## Summary

ROS 2 Actions provide a powerful communication pattern for long-running, goal-oriented tasks that require feedback and cancellation capabilities. They're ideal for navigation, manipulation, and other complex robotic behaviors that unfold over time. Understanding when and how to use actions is crucial for developing robust robotic applications. In the next lesson, we'll explore ROS 2 Launch files for managing complex system configurations.

