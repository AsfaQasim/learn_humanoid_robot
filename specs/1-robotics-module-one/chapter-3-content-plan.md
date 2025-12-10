# Chapter 3 Content Plan: Unified Robot Description Format (URDF)

## Required Diagrams

### 1. Basic URDF Structure Diagram
- Shows the relationship between links, joints, visual, collision, and inertial elements
- Hierarchical structure of a simple robot
- Parent-child relationships

### 2. Humanoid Robot Kinematic Tree
- Full humanoid structure with multiple DOF joints
- Left/right symmetry representation
- Torso-limb organization

### 3. URDF Validation Flow
- Process of URDF validation using check_urdf
- Graphviz visualization of kinematic tree
- RViz visualization pipeline

### 4. Inertial Properties Visualization
- Shows center of mass positioning
- Inertia tensor representation
- Mass distribution in humanoid robots

## Required Code Examples

### 1. Basic URDF Structure
```xml
<?xml version="1.0"?>
<robot name="my_robot">
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.5 0.2"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.5 0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
  </link>
</robot>
```

### 2. Joint Definitions with Different Types
```xml
<!-- Fixed joint -->
<joint name="fixed_joint" type="fixed">
  <parent link="parent_link"/>
  <child link="child_link"/>
</joint>

<!-- Revolute joint with limits -->
<joint name="revolute_joint" type="revolute">
  <parent link="parent_link"/>
  <child link="child_link"/>
  <origin xyz="0 0 0.1" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-1.57" upper="1.57" effort="10.0" velocity="1.0"/>
</joint>

<!-- Continuous joint -->
<joint name="continuous_joint" type="continuous">
  <parent link="parent_link"/>
  <child link="child_link"/>
  <axis xyz="0 0 1"/>
</joint>

<!-- Prismatic joint -->
<joint name="prismatic_joint" type="prismatic">
  <parent link="parent_link"/>
  <child link="child_link"/>
  <axis xyz="0 0 1"/>
  <limit lower="0.0" upper="0.5" effort="10.0" velocity="1.0"/>
</joint>
```

### 3. Humanoid Leg Structure Example
```xml
<!-- Left leg hip joints (3 DOF) -->
<joint name="left_hip_yaw" type="revolute">
  <parent link="pelvis"/>
  <child link="left_hip_yaw_link"/>
  <origin xyz="-0.05 -0.1 -0.05" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-0.7" upper="0.4" effort="100.0" velocity="1.0"/>
</joint>

<joint name="left_hip_roll" type="revolute">
  <parent link="left_hip_yaw_link"/>
  <child link="left_hip_roll_link"/>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <axis xyz="1 0 0"/>
  <limit lower="-0.4" upper="0.7" effort="100.0" velocity="1.0"/>
</joint>

<joint name="left_hip_pitch" type="revolute">
  <parent link="left_hip_roll_link"/>
  <child link="left_thigh"/>
  <origin xyz="0 0 -0.1" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-2.5" upper="0.7" effort="150.0" velocity="1.0"/>
</joint>
```

### 4. Xacro Macros for Humanoid Symmetry
```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="humanoid">

  <xacro:property name="M_PI" value="3.1415926535897931" />

  <!-- Define a leg macro -->
  <xacro:macro name="humanoid_leg" params="prefix reflect">
    <link name="${prefix}_hip_yaw_link">
      <inertial>
        <mass value="0.5"/>
        <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
      </inertial>
    </link>

    <joint name="${prefix}_hip_yaw" type="revolute">
      <parent link="pelvis"/>
      <child link="${prefix}_hip_yaw_link"/>
      <origin xyz="0 ${reflect * -0.1} -0.05" rpy="0 0 0"/>
      <axis xyz="0 0 1"/>
      <limit lower="-0.7" upper="0.4" effort="100.0" velocity="1.0"/>
    </joint>
    
    <!-- Additional leg components would follow -->
    
  </xacro:macro>

  <!-- Use the macro for both legs -->
  <xacro:humanoid_leg prefix="left" reflect="1"/>
  <xacro:humanoid_leg prefix="right" reflect="-1"/>

</robot>
```

### 5. Gazebo-Specific URDF Enhancements
```xml
<!-- Add Gazebo plugins -->
<gazebo>
  <plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so">
    <robotNamespace>/my_robot</robotNamespace>
  </plugin>
</gazebo>

<!-- Link-specific Gazebo properties -->
<gazebo reference="my_link">
  <mu1>0.2</mu1>
  <mu2>0.2</mu2>
  <material>Gazebo/Orange</material>
  <turnGravityOff>false</turnGravityOff>
</gazebo>

<!-- Transmission for joint control -->
<transmission name="tran1">
  <type>transmission_interface/SimpleTransmission</type>
  <joint name="joint1">
    <hardwareInterface>hardware_interface/PositionJointInterface</hardwareInterface>
  </joint>
  <actuator name="motor1">
    <hardwareInterface>hardware_interface/PositionJointInterface</hardwareInterface>
    <mechanicalReduction>1</mechanicalReduction>
  </actuator>
</transmission>
```

### 6. URDF Parsing in Python
```python
import urdf_parser_py.urdf as urdf

# Parse URDF
robot = urdf.Robot.from_xml_file('/path/to/robot.urdf')

# Access robot properties
print(f"Robot name: {robot.name}")
print(f"Links: {[link.name for link in robot.links]}")
print(f"Joints: {[joint.name for joint in robot.joints]}")

# Access specific link properties
for link in robot.links:
    if link.inertial:
        print(f"Link {link.name} mass: {link.inertial.mass}")
```