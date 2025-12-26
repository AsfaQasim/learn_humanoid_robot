# Data Model: RAG Chatbot – Spec 3: Agent creation with retrieval integration

## Overview
Data models for the AI Agent that integrates Qdrant-based retrieval to answer questions grounded in the book's content.

## Core Entities

### AgentRequest
**Description**: Represents a request to the AI agent
- **query**: string (required) - The user's query/question
- **user_id**: string (optional) - Identifier for the user (if needed for future features)
- **metadata**: object (optional) - Additional request metadata

**Validation rules**:
- query must be non-empty
- query length must be less than 1000 characters

### AgentResponse
**Description**: Represents the response from the AI agent
- **response**: string (required) - The agent's response to the user's query
- **retrieved_chunks**: array[RetrievedChunk] (required) - List of chunks used to generate the response
- **confidence**: number (optional) - Confidence score for the response (0-1)
- **sources**: array[string] (optional) - List of source identifiers used
- **timestamp**: string (required) - ISO timestamp of the response

**Validation rules**:
- response must be non-empty
- confidence must be between 0 and 1 if provided

### RetrievedChunk
**Description**: Represents a chunk of content retrieved from Qdrant
- **id**: string (required) - Unique identifier for the chunk
- **content**: string (required) - The text content of the chunk
- **relevance_score**: number (required) - Score indicating relevance to the query (0-1)
- **source_url**: string (optional) - URL where the content originated
- **section**: string (optional) - Section identifier from the original document
- **heading**: string (optional) - Heading or title of the section
- **metadata**: object (optional) - Additional metadata from the original document

**Validation rules**:
- content must be non-empty
- relevance_score must be between 0 and 1
- id must be unique within the response

### AgentToolDefinition
**Description**: Definition of the Qdrant retrieval tool for the agent
- **name**: string (required) - Name of the tool ("qdrant_retrieval")
- **description**: string (required) - Description of what the tool does
- **parameters**: object (required) - Parameters the tool accepts
  - **type**: string - Type of parameters object ("object")
  - **properties**: object - Individual parameters
    - **query**: object - Query to search for
      - **type**: string - Parameter type ("string")
      - **description**: string - Description of the parameter
    - **top_k**: object - Number of results to return
      - **type**: string - Parameter type ("integer")
      - **description**: string - Description of the parameter
      - **default**: number - Default value (5)
  - **required**: array[string] - Required parameter names

**Validation rules**:
- name must be unique among tools
- parameters must follow OpenAI function calling format

## State Transitions

### Agent Query Processing
1. **Received**: Agent receives a query from the user
2. **Processing**: Agent determines if Qdrant retrieval is needed
3. **Retrieving**: Agent calls Qdrant retrieval tool
4. **Generating**: Agent generates response using retrieved context
5. **Validating**: Agent validates response is grounded in retrieved content
6. **Responded**: Agent returns final response to user

## Relationships

- AgentRequest → (processed by) → AgentResponse
- AgentResponse → (contains) → [0..n] RetrievedChunk
- AgentToolDefinition → (used by) → Agent

## API Contracts

### Agent Query Endpoint
**Method**: POST
**Path**: `/agent/query` (hypothetical - not building API endpoints per constraints)
**Request Body**: AgentRequest
**Response**: AgentResponse

### Tool Function Contract
**Function Name**: qdrant_retrieval
**Purpose**: Retrieve relevant document chunks from Qdrant based on query
**Input**: Query string and optional top_k parameter
**Output**: Array of RetrievedChunk objects