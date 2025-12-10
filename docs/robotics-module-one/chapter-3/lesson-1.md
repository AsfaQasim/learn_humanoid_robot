---
title: URDF Structure
description: Understanding the structure and components of Unified Robot Description Format.
---

# URDF Structure

## Introduction

The Unified Robot Description Format (URDF) is an XML-based format used to describe robots in ROS. URDF defines the physical and kinematic properties of a robot, including its links, joints, and visual/inertial properties. This lesson will explore the structure of URDF files and how to create effective robot descriptions.

## URDF Overview

URDF (Unified Robot Description Format) is an XML specification that defines:

- **Links**: Rigid bodies that make up the robot
- **Joints**: Connections between links with specific degrees of freedom
- **Visual**: How the robot appears in simulation and visualization tools
- **Collision**: Collision detection geometry for physics simulation
- **Inertial**: Mass properties for dynamics calculations

## Basic URDF Structure

A basic URDF file has the following structure:

```xml
<?xml version="1.0"?>
<robot name="my_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">
  <!-- Links definition -->
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
  
  <!-- Joints definition -->
  <joint name="base_to_wheel" type="continuous">
    <parent link="base_link"/>
    <child link="wheel_link"/>
    <origin xyz="0.0 0.2 0.0" rpy="0 0 0"/>
  </joint>
  
  <link name="wheel_link">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.2"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.002"/>
    </inertial>
  </link>
</robot>
```

## Link Elements

Links represent rigid bodies in the robot. Each link must have:

### Visual Element
Defines how the link appears in simulation and visualization:

```xml
<link name="my_link">
  <visual>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <!-- One of: box, cylinder, sphere, or mesh -->
      <box size="1.0 0.5 0.3"/>
    </geometry>
    <material name="my_material">
      <color rgba="0.8 0.2 0.1 1.0"/>
    </material>
  </visual>
</link>
```

Geometry types:
- **Box**: `<box size="x y z"/>`
- **Cylinder**: `<cylinder radius="r" length="l"/>`
- **Sphere**: `<sphere radius="r"/>`
- **Mesh**: `<mesh filename="package://robot_description/meshes/part.stl"/>`

### Collision Element
Defines collision detection geometry:

```xml
<collision>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <geometry>
    <box size="1.0 0.5 0.3"/>
  </geometry>
</collision>
```

### Inertial Element
Defines mass properties for dynamics simulation:

```xml
<inertial>
  <mass value="1.0"/>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <inertia 
    ixx="0.1" ixy="0.0" ixz="0.0" 
    iyy="0.1" iyz="0.0" 
    izz="0.1"/>
</inertial>
```

## Joint Elements

Joints connect links and define their relative motion:

### Joint Types

1. **Fixed**: No movement allowed
```xml
<joint name="fixed_joint" type="fixed">
  <parent link="parent_link"/>
  <child link="child_link"/>
</joint>
```

2. **Revolute**: Rotational joint with limits
```xml
<joint name="revolute_joint" type="revolute">
  <parent link="parent_link"/>
  <child link="child_link"/>
  <origin xyz="0 0 0.1" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-1.57" upper="1.57" effort="10.0" velocity="1.0"/>
</joint>
```

3. **Continuous**: Rotational joint without limits
```xml
<joint name="continuous_joint" type="continuous">
  <parent link="parent_link"/>
  <child link="child_link"/>
  <axis xyz="0 0 1"/>
</joint>
```

4. **Prismatic**: Linear sliding joint with limits
```xml
<joint name="prismatic_joint" type="prismatic">
  <parent link="parent_link"/>
  <child link="child_link"/>
  <axis xyz="0 0 1"/>
  <limit lower="0.0" upper="0.5" effort="10.0" velocity="1.0"/>
</joint>
```

5. **Planar**: Movement on a plane
6. **Floating**: 6-DOF movement

## Material Definitions

Materials can be defined globally and referenced by name:

```xml
<material name="red">
  <color rgba="0.8 0.1 0.1 1.0"/>
</material>

<material name="blue">
  <color rgba="0.1 0.1 0.8 1.0"/>
</material>

<material name="black">
  <color rgba="0.1 0.1 0.1 1.0"/>
</material>

<material name="white">
  <color rgba="1 1 1 1"/>
</material>
```

## Complete Robot Example

Here's a simple 3-DOF manipulator robot:

```xml
<?xml version="1.0"?>
<robot name="simple_arm">
  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.2"/>
      </geometry>
      <material name="blue"/>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.1" length="0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.02"/>
    </inertial>
  </link>

  <!-- First joint and link -->
  <joint name="joint1" type="revolute">
    <parent link="base_link"/>
    <child link="link1"/>
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="100.0" velocity="1.0"/>
  </joint>

  <link name="link1">
    <visual>
      <origin xyz="0 0 0.25" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="0.5"/>
      </geometry>
      <material name="red"/>
    </visual>
    <collision>
      <origin xyz="0 0 0.25" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="0.5"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.005"/>
    </inertial>
  </link>

  <!-- Second joint and link -->
  <joint name="joint2" type="revolute">
    <parent link="link1"/>
    <child link="link2"/>
    <origin xyz="0 0 0.5" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="1.57" effort="100.0" velocity="1.0"/>
  </joint>

  <link name="link2">
    <visual>
      <origin xyz="0 0 0.2" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="0.4"/>
      </geometry>
      <material name="green"/>
    </visual>
    <collision>
      <origin xyz="0 0 0.2" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.5"/>
      <inertia ixx="0.005" ixy="0.0" ixz="0.0" iyy="0.005" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>
</robot>
```

## URDF Best Practices

1. **Always have a base link**: Every robot must have one base link that's not a child of any joint
2. **Use consistent units**: Stick to meters for length, radians for angles
3. **Valid kinematic tree**: Ensure all links are connected in a proper tree structure (no loops)
4. **Realistic inertial properties**: Use actual mass and inertia values when possible
5. **Simplified collision geometry**: Use simpler shapes for collision than for visuals when possible
6. **Organized file structure**: Consider using Xacro for complex robots

## Validation and Tools

Use URDF validation tools to check your robot description:

- `check_urdf` command: Validates URDF syntax
- `urdf_to_graphiz`: Creates a kinematic tree visualization
- Rviz: For visualizing the robot structure

## Summary

URDF provides a comprehensive way to describe robot structure in ROS. Understanding link and joint elements, along with visual, collision, and inertial properties, is essential for creating functional robot models. The next lesson will explore how URDF applies specifically to humanoid robotics.

