# Quickstart Guide: Module 1 Content Creation

This guide provides a rapid onboarding for content creators to begin writing Module 1, "The Robotic Nervous System (ROS 2)," adhering to the established plan, data model, and content contracts.

## 1. Environment Setup

1.  **Clone the Repository**:
    ```bash
    git clone [repository-url]
    cd again_hackthone_project
    ```
2.  **Install Docusaurus Dependencies**:
    Navigate to the `frontend` directory and install Node.js dependencies:
    ```bash
    cd frontend
    npm install
    ```
3.  **Start Docusaurus Development Server (Optional, for live preview)**:
    ```bash
    npm run start
    ```
    Your content will be live-reloaded as you make changes.

## 2. Content Location and Structure

All Module 1 content will reside within the `frontend/docs/1-robotics-module-one/` directory.

```
frontend/docs/1-robotics-module-one/
├── chapter-1/
│   ├── _category_.json
│   ├── lesson-1.md
│   ├── lesson-2.md
│   └── lesson-3.md
├── chapter-2/
│   ├── _category_.json
│   ├── lesson-1.md
│   └── ...
└── ...
```

*   **Module Directory**: `frontend/docs/1-robotics-module-one/`
*   **Chapter Directories**: Create subdirectories (e.g., `chapter-1`, `chapter-2`, etc.) for each chapter.
*   **Lesson Files**: Create Markdown files (`.md`) within each chapter directory for lessons (e.g., `lesson-1.md`).

## 3. Creating New Chapters

1.  **Create a new chapter directory**:
    ```bash
    mkdir -p frontend/docs/1-robotics-module-one/chapter-N
    ```
    (Replace `chapter-N` with an appropriate, descriptive slug like `ros2-nodes-topics`)
2.  **Create `_category_.json`**:
    Inside the new chapter directory, create `_category_.json` with the following structure:
    ```json
    {
      "label": "Chapter N: Your Chapter Title",
      "position": N, // Sequential number for ordering
      "link": {
        "type": "generated-index",
        "slug": "/1-robotics-module-one/chapter-N"
      }
    }
    ```
    *   **`label`**: The title that appears in the Docusaurus sidebar.
    *   **`position`**: Ensures correct ordering of chapters.
    *   **`slug`**: A unique identifier for the chapter's index page.
3.  **Create the first lesson file**:
    Inside the new chapter directory, create `lesson-1.md`.

## 4. Creating New Lessons

1.  **Create a new Markdown file**:
    Inside the relevant chapter directory, create a new `.md` file (e.g., `lesson-X.md`).
2.  **Add Docusaurus Frontmatter**:
    At the top of each lesson file, add the following Docusaurus frontmatter:
    ```markdown
    ---
    title: Your Lesson Title
    description: A brief summary of this lesson.
    ---
    ```
    *   **`title`**: The title that appears in the browser tab and Docusaurus navigation.
    *   **`description`**: A short, optional summary of the lesson.
3.  **Structure your content**:
    *   Use an H2 heading for the main lesson title within the body of the Markdown.
    *   Use H3 headings for subsections.

    ```markdown
    ## Your Lesson Title

    ### Introduction

    This is the introduction to your lesson...

    ### Core Concept

    Explain the core concept here...
    ```

## 5. Content Guidelines

*   **Heading Hierarchy**: Strict adherence to H1 (Chapter Title), H2 (Lesson Title/Major Section), H3 (Subsection).
*   **Meta Descriptions**: Ensure each chapter's `_category_.json` (or an equivalent chapter-level Markdown file) has a concise description (<160 chars).
*   **Word Count**: Aim for ~500 words per lesson.
*   **Accuracy & Citations**: All factual claims MUST be accurate and properly cited using APA style. Use inline links for simple references where a full citation manager is not integrated yet.
*   **Plagiarism**: 0% plagiarism. Use your own words and properly attribute all sources.
*   **Code Examples**: Embed code blocks using Markdown fenced code blocks (e.g., ````python ... ````).

## 6. Validation (Pre-submission)

Before submitting content for review, ensure:

*   **Docusaurus Builds**: Run `npm run build` in the `frontend` directory to catch any build errors.
*   **Content Linting**: (Tools to be integrated) Check for word count, heading hierarchy, and meta description compliance.
*   **Manual Review**: Thoroughly proofread for clarity, accuracy, and adherence to all guidelines.