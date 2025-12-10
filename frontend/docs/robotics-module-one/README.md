# Module 1: The Robotic Nervous System (ROS 2)

This directory contains the content for Module 1 of the Physical AI & Humanoid Robotics Textbook.

## Content Structure

The module is organized into 4 chapters, with each chapter containing 3 lessons:

- **Chapter 1**: ROS 2 Core Concepts (Nodes, Topics, Services)
- **Chapter 2**: Python & ROS 2 (rclpy) (Agent-controller integration)
- **Chapter 3**: Unified Robot Description Format (URDF) (Robot modeling)
- **Chapter 4**: Advanced ROS 2 Concepts (Parameters, Actions, Launch files)

## Content Creation Guidelines

1. **Heading Hierarchy**: Strictly follow H1/H2/H3 hierarchy:
   - H1 for main title (automatically added by Docusaurus from frontmatter)
   - H2 for major sections within lessons
   - H3 for subsections within lessons

2. **Frontmatter Requirements**: All lesson files must include:
   ```markdown
   ---
   title: Lesson Title
   description: Brief description (< 160 characters)
   ---
   ```

3. **Content Organization**: Each lesson should follow the structure:
   - Introduction with learning objectives
   - Main content with practical examples
   - Summary and next steps

## Validation Instructions

### Word Count Validation
Run the module word count validation:
```bash
cd frontend
node scripts/validate-module-word-count.js
```

### Markdown Linting
Run the markdown linter to ensure formatting compliance:
```bash
cd frontend
npm run lint:md
```

### Docusaurus Build Validation
Build the site to validate all links and structure:
```bash
cd frontend
npm run build
```

## Publication and Export

### Web Publication
The module is designed to be published as part of the Docusaurus website. To build for deployment:
```bash
cd frontend
npm run build
```

### PDF Export
To export as PDF, after building the site, you can use browser print functionality to save as PDF, or use tools like Puppeteer to automate the process.

## Technical Specifications

- Target length: 6,000-7,500 words total for module (1,500-1,875 words per chapter)
- Individual lesson length: ~500 words each
- Chapter meta descriptions: < 160 characters
- All content must be technically accurate regarding ROS 2 concepts

## Review Process

All content should undergo:
1. Technical accuracy review
2. Plagiarism check
3. Formatting validation
4. Cross-reference verification