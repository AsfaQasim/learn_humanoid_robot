# Data Model: Module 1 Content

This document describes the data model for the content of Module 1, "The Robotic Nervous System (ROS 2)," based on the feature specification. The entities primarily represent the hierarchical structure and associated metadata of the textbook content.

## Entities

### 1. Module

Represents a top-level organizational unit of the textbook, containing multiple chapters.

*   **Name**: Module
*   **Attributes**:
    *   `title` (String): The title of the module.
*   **Validation Rules**:
    *   `title` MUST be "Module 1: The Robotic Nervous System (ROS 2)".
*   **Relationships**:
    *   Has many `Chapter`s.

### 2. Chapter

Represents a major section within a Module, containing multiple lessons.

*   **Name**: Chapter
*   **Attributes**:
    *   `title` (String): The title of the chapter (H1 equivalent in Markdown).
    *   `metaDescription` (String): A concise summary of the chapter for SEO purposes.
*   **Validation Rules**:
    *   Each chapter MUST contain a minimum of 3 `Lesson`s.
    *   `title` MUST be formatted as an H1 heading.
    *   `metaDescription` MUST be less than 160 characters.
    *   The collective word count of its `Lesson`s should contribute to the overall module word count and keep individual chapter length concise (~500 words).
*   **Relationships**:
    *   Belongs to one `Module`.
    *   Has many `Lesson`s.

### 3. Lesson

Represents an individual instructional unit within a Chapter, containing the core content.

*   **Name**: Lesson
*   **Attributes**:
    *   `title` (String): The title of the lesson (H2 equivalent in Markdown).
    *   `body` (Markdown Text): The main content of the lesson. This includes subsections (H3 equivalent).
*   **Validation Rules**:
    *   `title` MUST be formatted as an H2 heading.
    *   Subsections within the `body` MUST be formatted as H3 headings.
    *   Each lesson should be concise, approximately 500 words.
    *   Content MUST cover relevant topics (ROS 2, rclpy, URDF) as specified.
    *   All factual claims within the `body` MUST be verifiable and cited.
*   **Relationships**:
    *   Belongs to one `Chapter`.
