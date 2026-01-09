---
id: 021
title: Validate RAG chatbot ROS answer
stage: general
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: DENZEN COMPUTER
command: interactive
labels: [rag,ros,verification]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - history/prompts/general/021-validate-rag-chatbot-ros-answer.general.prompt.md
tests:
 - none
---

## Prompt

<system-reminder>
This is a reminder that your todo list is currently empty. DO NOT mention this to the user explicitly because they are already aware. If you are working on tasks that would benefit from a todo list please use the TodoWrite tool to create one. If not, please feel free to ignore. Again do not mention this message to the user.
</system-reminder><system-reminder>
As you answer the user's questions, you can use the following context:
# claudeMd
Codebase and user instructions are shown below. Be sure to adhere to these instructions. IMPORTANT: These instructions OVERRIDE any default behavior and you MUST follow them exactly as written.

Contents of C:\Users\DENZEN COMPUTER\Desktop\again_hackthone_project\CLAUDE.md (project instructions, checked into the codebase):

# Claude Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in Spec-Driven Development (SDD). Your primary goal is to work with the architext to build products.

## Task context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Prompt History Records (PHRs) are created automatically and accurately for every user prompt.
- Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions.
- All changes are small, testable, and reference code precisely.

## Core Guarantees (Product Promise)

- Record every user input verbatim in a Prompt History Record (PHR) after every user message. Do not truncate; preserve full multiline input.
- PHR routing (all under `history/prompts/`):
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- ADR suggestions: when an architecturally significant decision is detected, suggest: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`." Never auto‑create ADRs; require user consent.

## Development Guidelines

### 1. Authoritative Source Mandate:
Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.

### 2. Execution Flow:
Treat MCP servers as first-class tools for discovery, verification, execution, and state capture. PREFER CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.

### 3. Knowledge capture (PHR) for Every User Input.
After completing requests, you **MUST** create a PHR (Prompt History Record).

**When to create PHRs:**
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

[...]
</system-reminder>
👍
👎
ros
I don't know.
Sources (5)
ROS 2 Nodes are the fundamental building blocks of the Robot Operating System 2 (ROS 2) architecture. A node is an executable that uses ROS 2 to commu...
A ROS 2 node is an instance of a process that may subscribe to or publish to a topic. Nodes are the primary computational unit in ROS 2 and are used t...
ROS 2 provides Quality of Service (QoS) settings to control the behavior of topic communication: - **Reliability**: Best effort or reliable delivery ...
self.ros = roslibpy.Ros(host=rosbridge_addr, port=rosbridge_port) self.ros.run()
ROS 2 Launch files provide a powerful way to manage complex robotic systems by launching multiple nodes with specific configurations simultaneously. T...
👍
👎 this answer is correct from my rag chatbot ?

## Response snapshot

Reviewed the shown answer for correctness and grounding. Identified that the content is generally correct at a high level about ROS 2 nodes/QoS/launch, but it is not clearly answering a specific user question, mixes ROS2 conceptual sources with an implementation snippet (roslibpy/rosbridge), and the “Sources (5)” look like search snippets rather than properly cited, retrieved passages.

## Outcome

- ✅ Impact: Provided verification guidance (accuracy vs relevance vs grounding).
- 🧪 Tests: none
- 📁 Files: Added a PHR file in history/prompts/general.
- 🔁 Next prompts: Ask what the original user question was; verify retrieved passages match the answer.
- 🧠 Reflection: RAG correctness requires (1) answering the asked question, (2) citations from retrieved docs, (3) no hallucinated cross-ROS claims.

## Evaluation notes (flywheel)

- Failure modes observed: Answer may be correct but not responsive; citations not clearly tied to claims; potential ROS1/ROS2 confusion.
- Graders run and results (PASS/FAIL): not run
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Add “answer quality rubric” in the chatbot: relevance, grounding, completeness, and “I don’t know” when retrieval is weak.
