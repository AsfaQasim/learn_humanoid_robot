# Tasks: RAG Chatbot Integration

**Input**: Design documents from `specs/2-rag-chatbot-integration/`

## Phase 1: Setup

**Purpose**: Project initialization and basic structure.

- [x] T001 Create `backend` and `frontend` directories.
- [x] T002 [P] Initialize a new FastAPI project in `backend`.
- [x] T003 [P] Initialize a new React project in `frontend`.
- [x] T004 [P] Configure linting and formatting tools for both projects.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

- [x] T005 [P] Setup database schema for `ChatSession`, `UserQuery`, and `ChatbotResponse` in `backend/src/models/`.
- [x] T006 [P] Setup Neon Serverless Postgres connection in `backend/src/database.py`.
- [x] T007 [P] Setup Qdrant Cloud connection in `backend/src/vector_store.py`.
- [x] T008 [P] Implement data ingestion script in `backend/scripts/ingest_data.py` to process and store book content in Qdrant.
- [x] T009 [P] Create basic chat interface in `frontend/src/components/Chat.js`.

---

## Phase 3: User Story 1 - General Content Questions (Priority: P1) 🎯 MVP

**Goal**: A user can ask the chatbot a question about the book's content and receive a relevant answer.

**Independent Test**: Ask a question about a specific topic in the book and verify the answer is accurate and relevant.

### Implementation for User Story 1

- [x] T010 [US1] Create API endpoint `/chat` in `backend/src/api/chat.py` to handle chat requests.
- [x] T011 [US1] Implement RAG retrieval logic in `backend/src/services/rag_service.py` to fetch relevant content from Qdrant.
- [x] T012 [US1] Implement response generation logic in `backend/src/services/rag_service.py` using Free Gemini API.
- [x] T013 [US1] Connect the frontend chat interface to the `/chat` endpoint.

---

## Phase 4: User Story 2 - Selected Text Questions (Priority: P2)

**Goal**: A user can select a passage of text and ask a question about it.

**Independent Test**: Select a paragraph, ask a question about it, and confirm the answer is based only on the selected text.

### Implementation for User Story 2

- [x] T014 [US2] Add functionality to the frontend to capture selected text and send it with the chat request.
- [x] T015 [US2] Modify the `/chat` endpoint in `backend/src/api/chat.py` to accept selected text.
- [x] T016 [US2] Update the RAG retrieval logic in `backend/src/services/rag_service.py` to use the selected text as context.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories.

- [x] T017 [P] Implement logging for all API requests and responses in `backend/src/main.py`.
- [x] T018 [P] Implement user feedback mechanism in the frontend and a `/feedback` endpoint in the backend.
- [x] T019 [P] Add error handling and loading states to the frontend.
- [x] T020 [P] Write comprehensive documentation in `README.md` for both frontend and backend.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion.
- **User Stories (Phase 3 & 4)**: Depend on Foundational phase completion.
- **Polish (Phase 5)**: Can be done in parallel with other phases after the foundational phase is complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2).
- **User Story 2 (P2)**: Depends on User Story 1.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently.

### Incremental Delivery

1. Complete Setup + Foundational.
2. Add User Story 1 → Test independently → Deploy/Demo (MVP).
3. Add User Story 2 → Test independently → Deploy/Demo.
4. Add Polish features.
