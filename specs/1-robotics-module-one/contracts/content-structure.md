# Content Structure and Metadata Contracts

This document defines the "API contracts" for the textbook content, focusing on structural and metadata requirements to ensure consistency, Docusaurus compatibility, and adherence to SEO and academic standards. These contracts serve as guidelines for content creation and validation.

## 1. Module Contract

### Endpoint/Resource: `/docs/1-robotics-module-one/`

*   **Description**: Represents the top-level container for Module 1.
*   **Structure**:
    *   A directory named `1-robotics-module-one` under `frontend/docs/`.
    *   Contains subdirectories for each chapter.
*   **Metadata Requirements**:
    *   Implied by directory structure; Docusaurus handles module-level navigation.

## 2. Chapter Contract

### Endpoint/Resource: `/docs/1-robotics-module-one/{chapter-slug}/`

*   **Description**: Represents an individual chapter within Module 1.
*   **Structure**:
    *   A subdirectory (e.g., `chapter-1`) within the module directory.
    *   MUST contain an `_category_.json` file for Docusaurus sidebar ordering and metadata.
    *   MUST contain at least 3 lesson Markdown files (`.md` or `.mdx`).
*   **Metadata Requirements (`_category_.json` for Docusaurus)**:
    *   `label`: (String, Required) The display name of the chapter in the sidebar.
    *   `position`: (Number, Required) The order of the chapter in the sidebar.
    *   `link`: (Object, Optional) Configuration for a link associated with the category.
        *   `type`: (String, Optional) e.g., 'generated-index'.
        *   `slug`: (String, Optional) The slug for the generated index page.
*   **Content Requirements (Chapter Lead File - e.g., `index.md` or similar)**:
    *   MUST start with an H1 heading for the chapter title.
    *   MUST include a Docusaurus frontmatter `description` field for the meta description (< 160 characters).
*   **Validation Rules**:
    *   Minimum 3 lessons per chapter.
    *   `metaDescription` (from frontmatter) < 160 characters.
    *   H1 heading MUST be present.

## 3. Lesson Contract

### Endpoint/Resource: `/docs/1-robotics-module-one/{chapter-slug}/{lesson-slug}.md`

*   **Description**: Represents an individual lesson within a chapter.
*   **Structure**:
    *   A Markdown file (`.md` or `.mdx`) within a chapter directory.
*   **Metadata Requirements (Docusaurus Frontmatter)**:
    *   `title`: (String, Required) The display title of the lesson.
    *   `description`: (String, Optional) A short summary (can be used for page meta description if not provided by chapter).
    *   `slug`: (String, Optional) Custom URL slug for the lesson.
*   **Content Requirements**:
    *   MUST start with an H2 heading for the lesson title.
    *   Major sections within the lesson MUST use H2 headings.
    *   Subsections within the lesson MUST use H3 headings.
    *   Content should be concise (~500 words).
    *   All factual claims MUST be verifiable and include citations (APA style).
    *   Inclusion of diagrams/code examples as specified in the plan (details to be refined).
*   **Validation Rules**:
    *   Word count approximately 500 words.
    *   Correct heading hierarchy (H2 for lesson, H3 for subsections).
    *   Citations present and formatted correctly.
    *   No plagiarism.

## Versioning Strategy

*   Content will be versioned through the Git repository.
*   Docusaurus provides versioning capabilities for documentation; this can be utilized if future iterations require managing multiple versions of the textbook. (Currently out of scope but noted for future planning).

## Error Taxonomy

*   **Formatting Errors**: Incorrect heading hierarchy, missing meta descriptions, incorrect word count.
*   **Content Errors**: Factual inaccuracies, missing required topics, plagiarism.
*   **Build Errors**: Docusaurus build failures (e.g., broken links, invalid Markdown).
*   **Citation Errors**: Missing citations, incorrect APA formatting.
