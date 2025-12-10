# Tasks: Module 1 Content Specification

**Input**: Design documents from `/specs/1-module-content-spec/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` a
t repository root (adjusted to `scripts/content-generator/` as per plan.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for the content generator

- [ ] T001 Create project structure for content generator in `scripts/content-generator/`
- [ ] T002 [P] Initialize Python project and create `requirements.txt` in `scripts/content-generator/`
- [ ] T003 [P] Configure `pytest` for testing in `scripts/content-generator/`
- [ ] T004 Create `scripts/content-generator/main.py` for orchestration
- [ ] T005 Create `scripts/content-generator/config.py` for LLM and other configurations
- [ ] T006 Create `scripts/content-generator/content_analyzer.py` for analyzing existing content
- [ ] T007 Create `scripts/content-generator/content_writer.py` for generating and formatting content

---

## Phase 2: Foundational (Core Content Generation System)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Implement LLM API client in `scripts/content-generator/content_writer.py` using Google Gemini API.
- [ ] T009 Implement basic Markdown parsing/generation utility functions (e.g., for H1, H2, H3, word count) in `scripts/content-generator/content_writer.py`.
- [ ] T010 Implement function to read existing lesson headlines from Docusaurus structure (e.g., `frontend/docs/1-robotics-module-one/...`) in `scripts/content-generator/content_analyzer.py`.
- [ ] T011 Implement function to write generated Markdown content to specified file paths in `scripts/content-generator/content_writer.py`.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Generate Optimized Lesson Content (Priority: P1) 🎯 MVP

**Goal**: Automatically generate content for individual lessons, adhering to headline relevance and a 500-word limit with H1, H2, H3 structure.

**Independent Test**: Generate content for a single lesson (`frontend/docs/1-robotics-module-one/chapter-1/lesson-1.md`) and verify headline adherence, word count, and heading structure manually or with simple scripts.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️
> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**
- [ ] T012 [P] [US1] Unit test for `content_writer.py`'s content generation logic (e.g., word count, heading application) in `scripts/content-generator/tests/test_content_writer.py`.
- [ ] T013 [P] [US1] Integration test for `main.py` to generate a single lesson's content, verifying output file existence and basic structure in `scripts/content-generator/tests/test_main.py`.

### Implementation for User Story 1

- [ ] T014 [US1] Implement core lesson content generation logic in `scripts/content-generator/content_writer.py` using the chosen LLM (Google Gemini API).
- [ ] T015 [US1] Implement logic to ensure generated lesson content does not exceed 500 words, potentially involving truncation or summarization.
- [ ] T016 [US1] Implement logic to incorporate H1, H2, H3 headings into the generated lesson content, based on semantic analysis or predefined structure.
- [ ] T017 [US1] Integrate `content_analyzer.py` to fetch lesson headlines and `content_writer.py` to save the generated lesson content via `scripts/content-generator/main.py`.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Generate Optimized Chapter Content (Priority: P2)

**Goal**: Ensure aggregated content for each chapter adheres to a 1500-2000 word limit.

**Independent Test**: Aggregate generated content for all lessons within a chapter and verify the total word count is within the 1500-2000 word range.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️
> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**
- [ ] T018 [P] [US2] Unit test for chapter word count aggregation logic in `scripts/content-generator/tests/test_content_analyzer.py` or `test_main.py`.
- [ ] T019 [P] [US2] Integration test for `main.py` to generate and validate a full chapter's content against word count limits in `scripts/content-generator/tests/test_main.py`.

### Implementation for User Story 2

- [ ] T020 [US2] Implement logic in `scripts/content-generator/content_analyzer.py` or `main.py` to aggregate word counts for all lessons within a chapter.
- [ ] T021 [US2] Implement logic to adjust content across lessons within a chapter (if necessary and feasible) to meet the 1500-2000 word target, while respecting individual lesson limits. (This may involve suggesting content expansion/reduction points).

**Checkpoint**: All user stories should now be independently functional

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T022 Update documentation for the content generator in `scripts/content-generator/README.md`.
- [ ] T023 Code cleanup and refactoring across `scripts/content-generator/`.
- [ ] T024 Error handling and logging improvements for the content generation process.
- [ ] T025 Performance optimization for LLM calls (e.g., batching, caching).
- [ ] T026 Add CLI arguments to `main.py` for specifying module/chapter/lesson to process.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on User Story 1 being able to generate individual lesson content.

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Core generation logic before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All tasks marked [P] can run in parallel within their respective phases.
- Once the Foundational phase completes, User Story 1 tasks can begin. User Story 2 tasks may require US1 content generation capabilities to be in place.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently (single lesson generation).
5. Deploy/demo if ready (show automatic lesson content generation).

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP for lesson generation!)
3. Add User Story 2 → Test independently → Deploy/Demo (Chapter word count validation)
4. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Lesson content generation)
   - Developer B: User Story 2 (Chapter content validation and adjustment logic)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
