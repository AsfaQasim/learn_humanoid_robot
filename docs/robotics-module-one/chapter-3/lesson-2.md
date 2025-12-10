---
title: Humanoid Robotics & URDF
description: Applying URDF to model humanoid robots with complex kinematic structures.
---

# Humanoid Robotics & URDF

## Introduction

Humanoid robots present unique challenges in URDF modeling due to their complex kinematic structures and anthropomorphic designs. This lesson explores the specific considerations for modeling humanoid robots in URDF, including multi-degree-of-freedom joints, symmetrical structures, and the challenges of representing complex human-like kinematics.

## Humanoid Robot Characteristics

Humanoid robots typically feature:

- **Bipedal locomotion**: Two legs for walking
- **Upper body dexterity**: Arms with hands for manipulation
- **Anthropomorphic proportions**: Similar to human body structure
- **Complex joint configurations**: Multiple DOF per limb
- **Symmetrical design**: Left/right symmetry in limbs

These characteristics require careful URDF design to properly represent the kinematic structure.

## Humanoid URDF Structure

A humanoid robot typically follows this kinematic structure:

```
base_link (torso)
├── pelvis_link
│   ├── left_leg_0_link
│   │   ├── left_leg_1_link
│   │   ├── left_leg_2_link
│   │   ├── ...
│   │   └── left_foot_link
│   └── right_leg_0_link
│       ├── right_leg_1_link
│       ├── right_leg_2_link
│       ├── ...
│       └── right_foot_link
├── upper_torso_link
│   ├── head_link
│   ├── left_arm_0_link
│   │   ├── left_arm_1_link
│   │   ├── left_arm_2_link
│   │   ├── ...
│   │   └── left_hand_link
│   └── right_arm_0_link
│       ├── right_arm_1_link
│       ├── right_arm_2_link
│       ├── ...
│       └── right_hand_link
```

## Modeling Humanoid Links and Joints

### Torso and Pelvis

The torso serves as the central reference point:

```xml
<link name="torso">
  <visual>
    <geometry>
      <box size="0.3 0.2 0.5"/>
    </geometry>
    <material name="light_gray">
      <color rgba="0.7 0.7 0.7 1.0"/>
    </material>
  </visual>
  <collision>
    <geometry>
      <box size="0.3 0.2 0.5"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="10.0"/>
    <inertia ixx="0.2" ixy="0.0" ixz="0.0" iyy="0.2" iyz="0.0" izz="0.1"/>
  </inertial>
</link>

<link name="pelvis">
  <visual>
    <geometry>
      <box size="0.3 0.25 0.1"/>
    </geometry>
  </visual>
  <collision>
    <geometry>
      <box size="0.3 0.25 0.1"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="3.0"/>
    <inertia ixx="0.05" ixy="0.0" ixz="0.0" iyy="0.05" iyz="0.0" izz="0.02"/>
  </inertial>
</link>

<joint name="torso_to_pelvis" type="fixed">
  <parent link="torso"/>
  <child link="pelvis"/>
  <origin xyz="0 0 -0.25" rpy="0 0 0"/>
</joint>
```

### Leg Structure

Humanoid legs typically have 6+ DOF for proper locomotion:

```xml
<!-- Left leg hip joints (3 DOF) -->
<joint name="left_hip_yaw" type="revolute">
  <parent link="pelvis"/>
  <child link="left_hip_yaw_link"/>
  <origin xyz="-0.05 -0.1 -0.05" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-0.7" upper="0.4" effort="100.0" velocity="1.0"/>
</joint>

<link name="left_hip_yaw_link">
  <inertial>
    <mass value="0.5"/>
    <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
  </inertial>
</link>

<joint name="left_hip_roll" type="revolute">
  <parent link="left_hip_yaw_link"/>
  <child link="left_hip_roll_link"/>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <axis xyz="1 0 0"/>
  <limit lower="-0.4" upper="0.7" effort="100.0" velocity="1.0"/>
</joint>

<link name="left_hip_roll_link">
  <inertial>
    <mass value="0.5"/>
    <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
  </inertial>
</link>

<joint name="left_hip_pitch" type="revolute">
  <parent link="left_hip_roll_link"/>
  <child link="left_thigh"/>
  <origin xyz="0 0 -0.1" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-2.5" upper="0.7" effort="150.0" velocity="1.0"/>
</joint>

<link name="left_thigh">
  <visual>
    <origin xyz="0 0 -0.2" rpy="0 0 0"/>
    <geometry>
      <capsule radius="0.06" length="0.3"/>
    </geometry>
  </visual>
  <collision>
    <origin xyz="0 0 -0.2" rpy="0 0 0"/>
    <geometry>
      <capsule radius="0.06" length="0.3"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="2.0"/>
    <inertia ixx="0.02" ixy="0.0" ixz="0.0" iyy="0.02" iyz="0.0" izz="0.005"/>
  </inertial>
</link>

<!-- Knee joint -->
<joint name="left_knee" type="revolute">
  <parent link="left_thigh"/>
  <child link="left_shin"/>
  <origin xyz="0 0 -0.4" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="0" upper="2.3" effort="150.0" velocity="1.0"/>
</joint>

<link name="left_shin">
  <visual>
    <origin xyz="0 0 -0.2" rpy="0 0 0"/>
    <geometry>
      <capsule radius="0.05" length="0.3"/>
    </geometry>
  </visual>
  <collision>
    <origin xyz="0 0 -0.2" rpy="0 0 0"/>
    <geometry>
      <capsule radius="0.05" length="0.3"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="1.5"/>
    <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.003"/>
  </inertial>
</link>

<!-- Ankle joints -->
<joint name="left_ankle_pitch" type="revolute">
  <parent link="left_shin"/>
  <child link="left_ankle_pitch_link"/>
  <origin xyz="0 0 -0.4" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-0.5" upper="0.5" effort="50.0" velocity="1.0"/>
</joint>

<joint name="left_ankle_roll" type="revolute">
  <parent link="left_ankle_pitch_link"/>
  <child link="left_foot"/>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <axis xyz="1 0 0"/>
  <limit lower="-0.3" upper="0.3" effort="50.0" velocity="1.0"/>
</joint>

<link name="left_foot">
  <visual>
    <geometry>
      <box size="0.25 0.1 0.08"/>
    </geometry>
  </visual>
  <collision>
    <geometry>
      <box size="0.25 0.1 0.08"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="0.8"/>
    <inertia ixx="0.002" ixy="0.0" ixz="0.0" iyy="0.008" iyz="0.0" izz="0.008"/>
  </inertial>
</link>
```

### Arm Structure

Humanoid arms typically have 7 DOF for dexterity:

```xml
<!-- Left shoulder (3 DOF) -->
<joint name="left_shoulder_pitch" type="revolute">
  <parent link="upper_torso"/>
  <child link="left_shoulder_pitch_link"/>
  <origin xyz="0.05 -0.15 0.1" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-2.0" upper="1.0" effort="50.0" velocity="1.0"/>
</joint>

<joint name="left_shoulder_roll" type="revolute">
  <parent link="left_shoulder_pitch_link"/>
  <child link="left_shoulder_roll_link"/>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <axis xyz="1 0 0"/>
  <limit lower="0" upper="2.5" effort="50.0" velocity="1.0"/>
</joint>

<joint name="left_shoulder_yaw" type="revolute">
  <parent link="left_shoulder_roll_link"/>
  <child link="left_upper_arm"/>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-1.5" upper="1.5" effort="50.0" velocity="1.0"/>
</joint>

<link name="left_upper_arm">
  <visual>
    <origin xyz="0 0 -0.15" rpy="0 0 0"/>
    <geometry>
      <capsule radius="0.05" length="0.2"/>
    </geometry>
  </visual>
  <collision>
    <origin xyz="0 0 -0.15" rpy="0 0 0"/>
    <geometry>
      <capsule radius="0.05" length="0.2"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="1.0"/>
    <inertia ixx="0.005" ixy="0.0" ixz="0.0" iyy="0.005" iyz="0.0" izz="0.001"/>
  </inertial>
</link>

<!-- Elbow joint -->
<joint name="left_elbow" type="revolute">
  <parent link="left_upper_arm"/>
  <child link="left_forearm"/>
  <origin xyz="0 0 -0.3" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="0" upper="2.5" effort="30.0" velocity="1.0"/>
</joint>

<link name="left_forearm">
  <visual>
    <origin xyz="0 0 -0.15" rpy="0 0 0"/>
    <geometry>
      <capsule radius="0.04" length="0.2"/>
    </geometry>
  </visual>
  <collision>
    <origin xyz="0 0 -0.15" rpy="0 0 0"/>
    <geometry>
      <capsule radius="0.04" length="0.2"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="0.7"/>
    <inertia ixx="0.003" ixy="0.0" ixz="0.0" iyy="0.003" iyz="0.0" izz="0.0008"/>
  </inertial>
</link>

<!-- Wrist joints -->
<joint name="left_wrist_yaw" type="revolute">
  <parent link="left_forearm"/>
  <child link="left_wrist_yaw_link"/>
  <origin xyz="0 0 -0.3" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-1.0" upper="1.0" effort="10.0" velocity="1.0"/>
</joint>

<joint name="left_wrist_pitch" type="revolute">
  <parent link="left_wrist_yaw_link"/>
  <child link="left_hand"/>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-0.8" upper="0.8" effort="10.0" velocity="1.0"/>
</joint>

<link name="left_hand">
  <visual>
    <geometry>
      <box size="0.15 0.08 0.1"/>
    </geometry>
  </visual>
  <collision>
    <geometry>
      <box size="0.15 0.08 0.1"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="0.3"/>
    <inertia ixx="0.0005" ixy="0.0" ixz="0.0" iyy="0.0008" iyz="0.0" izz="0.0005"/>
  </inertial>
</link>
```

## Symmetry and Repetition

Use Xacro macros to avoid repetition in symmetric parts:

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

    <!-- Additional leg joints and links would follow the same pattern -->
    <!-- ... -->
  </xacro:macro>

  <!-- Use the macro for both legs -->
  <xacro:humanoid_leg prefix="left" reflect="1"/>
  <xacro:humanoid_leg prefix="right" reflect="-1"/>

</robot>
```

## Center of Mass Considerations

For stable humanoid locomotion, proper center of mass positioning is critical:

```xml
<link name="torso">
  <!-- Visual and collision geometry -->
  <visual>
    <geometry>
      <box size="0.3 0.2 0.5"/>
    </geometry>
    <material name="light_gray">
      <color rgba="0.7 0.7 0.7 1.0"/>
    </material>
  </visual>
  <collision>
    <geometry>
      <box size="0.3 0.2 0.5"/>
    </geometry>
  </collision>
  <!-- Careful inertial specification for proper dynamics -->
  <inertial>
    <mass value="10.0"/>
    <!-- Center of mass positioned appropriately -->
    <origin xyz="0 0 0.1"/>
    <inertia ixx="0.5" ixy="0.0" ixz="0.0" iyy="0.5" iyz="0.0" izz="0.2"/>
  </inertial>
</link>
```

## Humanoid-Specific Challenges

### 1. Balance and Stability
- Accurate inertial properties are crucial
- Center of mass computation tools needed
- Consider using CAD software for complex shapes

### 2. Contact Modeling
- Foot contact with ground
- Hand-object interaction
- Proper friction coefficients

### 3. Range of Motion
- Human-like joint limits
- Avoiding self-collision
- Ensuring sufficient workspace

### 4. Computational Complexity
- High DOF systems
- Real-time control requirements
- Sensor integration

## Best Practices for Humanoid URDF

1. **Accurate inertial properties**: Use CAD software to calculate mass properties
2. **Realistic joint limits**: Based on human anatomy or robot specifications
3. **Symmetry considerations**: Use Xacro macros to reduce redundancy
4. **Validation**: Test in simulation early and often
5. **Layered approach**: Start simple, add complexity gradually
6. **Documentation**: Comment complex kinematic chains

## Summary

Modeling humanoid robots in URDF requires careful attention to kinematic structure, inertial properties, and human-like range of motion. The complex, multi-DOF structure of humanoid robots presents unique challenges that require thoughtful design of both the kinematic tree and dynamic properties. In the next lesson, we'll explore URDF tools and visualization techniques for humanoid robots.

