Project: Physical AI & Humanoid Robotics Textbook  
Module 1: The Robotic Nervous System (ROS 2)

Objective:
Execute the full plan and tasks to generate final publish-ready content for Module 1.

Implementation Requirements:
- Use /sp.constitution, /sp.specify, /sp.plan, and /sp.tasks as strict constraints.
- Produce:
  1. Fully written chapters (4–5 total)
  2. 3 lessons per chapter
  3. Meta descriptions for each chapter
  4. Code examples (ROS 2, Python, URDF)
  5. Diagrams in Mermaid/Markdown
  6. Docusaurus-ready Markdown files
- All writing must be original, accurate, and reproducible.

Implementation Steps:

1. **Assemble Outline**
   - Import structure from /sp.plan and expand into full chapter/lesson map.

2. **Generate Chapter Content**
   - Write each chapter (~500 words) using strict H1/H2/H3 hierarchy.
   - Add meta description (<160 chars).

3. **Generate Lesson Content**
   - Write 3 lessons per chapter (~150–180 words each).
   - Ensure clarity, pedagogy, and correctness.

4. **Insert ROS 2 Examples**
   - Generate Node creation code, Topic publishing code, Services, Parameters.
   - Add validated rclpy bridging examples.

5. **Insert URDF Examples**
   - Include minimal humanoid URDF (torso, head, arms, legs).
   - Ensure it loads without errors in ROS 2 + RViz.

6. **Insert Diagrams**
   - Add middleware flow diagrams, node graphs, URDF trees.
   - Use clean Mermaid syntax.

7. **Run Technical Verification**
   - Ensure all commands, APIs, and file paths accurately reflect ROS 2 (Humble/Foxy).

8. **Format to Docusaurus**
   - Produce `module-1.md` or folder-based chapters for Docusaurus.
   - Ensure sidebar navigation compatibility.

9. **Quality Review**
   - Check for:
     - Clarity  
     - Consistency  
     - SEO  
     - Zero plagiarism  
     - Source accuracy  

10. **Final Output**
    - Return final, ready-to-publish Markdown for Module 1.
    - Include all chapters, lessons, diagrams, and code blocks.

Output Format:
Return only the final executed module content in clean Docusaurus Markdown.  
No extra reasoning or commentary in the output.
