"""
RAG Chatbot Agent with Qdrant retrieval integration.

This module implements an AI Agent that integrates Qdrant-based retrieval
to answer questions grounded in the book's content using the OpenAI Agents SDK.
"""
import os
import json
import argparse
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI

gemini_Api_key = os.getenv("Gemini_Api_Key")

provider = AsyncOpenAI(
    api_key= gemini_Api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.5-flash",
    openai_client= provider
)



# Import required libraries
try:
    from agents import Agent, Runner, function_tool
    import qdrant_client
    from qdrant_client.http import models
    import cohere
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install required dependencies: pip install openai-agents qdrant-client cohere python-dotenv")
    raise

# Import existing modules
try:
    from config import config
    from retriever import RAGRetriever
    from models import RetrievedChunk, QueryRequest
    from errors import RetrievalError, ValidationError
    from utils import get_current_timestamp, generate_uuid
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure existing modules are available in the project")
    raise

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGAgent:
    """
    AI Agent that integrates Qdrant-based retrieval to answer questions grounded in book content.
    """

    def __init__(self):
        """Initialize the RAG Agent with OpenAI Agents SDK, Qdrant, and Cohere clients."""
        # Initialize OpenAI API key
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            # Try to use OpenRouter API key as fallback
            self.openai_api_key = os.getenv("OPENROUTER_API_KEY")
            if not self.openai_api_key:
                raise ValueError("Either OPENAI_API_KEY or OPENROUTER_API_KEY environment variable is required")

        # Initialize Qdrant client via existing retriever
        self.retriever = RAGRetriever()

        # Create the RAG Agent using the OpenAI Agents SDK with function tools
        self.agent = Agent(
            name="RAG Chatbot Assistant",
            instructions="You are a helpful assistant that answers questions based on retrieved document chunks. Always ground your responses in the provided context and do not hallucinate information not present in the context.",
            tools=[self.qdrant_retrieval_tool],
            model= model  # Using a capable model for complex reasoning
        )

        print(f"RAG Agent initialized with name: {self.agent.name}")

    @function_tool
    def qdrant_retrieval_tool(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Retrieve relevant document chunks from Qdrant based on query.

        Args:
            query: The query text to search for
            top_k: Number of results to return (default: 5)

        Returns:
            List of retrieved chunks with metadata
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Check if Qdrant connection is healthy before attempting retrieval
                if not self.retriever.handle_connection_failures():
                    logger.error("Qdrant connection is not healthy and could not be re-established")
                    if attempt == max_retries - 1:  # Last attempt
                        return []
                    # Wait before retrying (exponential backoff)
                    import time
                    wait_time = (2 ** attempt) + 0.1  # Add small random component
                    time.sleep(wait_time)
                    continue  # Skip to next attempt

                # Use the existing retriever to get chunks
                chunks = self.retriever.retrieve_chunks_with_retry(query, top_k=top_k)
                return chunks
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed in qdrant_retrieval: {str(e)}")
                if attempt == max_retries - 1:  # Last attempt
                    # Attempt to handle connection failures one final time
                    if not self.retriever.handle_connection_failures():
                        logger.error("Qdrant connection failed and could not be re-established")
                    return []

                # Wait before retrying (exponential backoff)
                import time
                wait_time = (2 ** attempt) + 0.1  # Add small random component
                time.sleep(wait_time)

        return []

    def qdrant_retrieval(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Retrieve relevant document chunks from Qdrant based on query (wrapper for tool use).
        This is a wrapper that can be used directly without the agent framework.
        """
        # Directly call the underlying retrieval functionality without the function_tool decorator
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Check if Qdrant connection is healthy before attempting retrieval
                if not self.retriever.handle_connection_failures():
                    logger.error("Qdrant connection is not healthy and could not be re-established")
                    if attempt == max_retries - 1:  # Last attempt
                        return []
                    # Wait before retrying (exponential backoff)
                    import time
                    wait_time = (2 ** attempt) + 0.1  # Add small random component
                    time.sleep(wait_time)
                    continue  # Skip to next attempt

                # Use the existing retriever to get chunks
                chunks = self.retriever.retrieve_chunks_with_retry(query, top_k=top_k)
                return chunks
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed in qdrant_retrieval: {str(e)}")
                if attempt == max_retries - 1:  # Last attempt
                    # Attempt to handle connection failures one final time
                    if not self.retriever.handle_connection_failures():
                        logger.error("Qdrant connection failed and could not be re-established")
                    return []

                # Wait before retrying (exponential backoff)
                import time
                wait_time = (2 ** attempt) + 0.1  # Add small random component
                time.sleep(wait_time)

        return []

    async def query_async(self, user_query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Process a user query and return a grounded response using the OpenAI Agents SDK.

        Args:
            user_query: The user's query/question
            top_k: Number of chunks to retrieve (default: 5)

        Returns:
            Dictionary containing the response and retrieved chunks
        """
        print(f"Processing query: '{user_query}'")

        # Validate the query complexity before processing
        is_valid, issues = self._validate_query_complexity(user_query)
        if not is_valid:
            logger.warning(f"Query validation failed: {', '.join(issues)}")
            return {
                "response": f"Your query could not be processed: {', '.join(issues)}",
                "retrieved_chunks": [],
                "query": user_query,
                "timestamp": datetime.now().isoformat(),
                "retrieval_count": 0
            }

        # Run the agent with the user query
        try:
            import asyncio
            result = await Runner.run(self.agent, user_query)
            response_content = result.final_output
        except Exception as e:
            logger.error(f"Error running agent: {e}")
            response_content = f"Error processing your query: {str(e)}"

        # Retrieve chunks using the tool directly to include in response
        retrieved_chunks = self.qdrant_retrieval(user_query, top_k)

        # Prepare the response
        agent_response = {
            "response": response_content,
            "retrieved_chunks": retrieved_chunks,
            "query": user_query,
            "timestamp": datetime.now().isoformat(),
            "retrieval_count": len(retrieved_chunks)
        }

        return agent_response

    def query(self, user_query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Process a user query and return a grounded response using the OpenAI Agents SDK.
        This is a synchronous wrapper for the async method.

        Args:
            user_query: The user's query/question
            top_k: Number of chunks to retrieve (default: 5)

        Returns:
            Dictionary containing the response and retrieved chunks
        """
        import asyncio
        return asyncio.run(self.query_async(user_query, top_k))

    def _validate_query_complexity(self, query_text: str, max_length: int = 1000) -> tuple[bool, List[str]]:
        """
        Add validation for complex or long queries.

        Args:
            query_text: Query text to validate
            max_length: Maximum allowed query length

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []

        if not query_text or len(query_text.strip()) == 0:
            issues.append("Query text is empty")
            return False, issues

        # Check length
        if len(query_text) > max_length:
            issues.append(f"Query length ({len(query_text)}) exceeds maximum allowed length ({max_length})")

        # Check for excessive special characters that might indicate a malformed query
        special_char_ratio = sum(1 for c in query_text if not c.isalnum() and not c.isspace()) / len(query_text)
        if special_char_ratio > 0.5:  # More than 50% special characters
            issues.append(f"Query has high ratio of special characters ({special_char_ratio:.2%})")

        # Check for SQL injection patterns (basic check)
        sql_patterns = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'UNION', '--', ';']
        for pattern in sql_patterns:
            if pattern.lower() in query_text.lower():
                issues.append(f"Potential SQL injection pattern detected: {pattern}")

        # Check for script tags (basic check)
        if '<script' in query_text or 'javascript:' in query_text:
            issues.append("Potential script injection detected")

        is_valid = len(issues) == 0
        if not is_valid:
            logger.warning(f"Query validation failed with issues: {', '.join(issues)}")

        return is_valid, issues

    def validate_response_against_chunks(self, response: str, chunks: List[Dict]) -> bool:
        """
        Validate that the response is grounded in the retrieved chunks.

        Args:
            response: The agent's response
            chunks: The retrieved chunks used for the response

        Returns:
            True if response is grounded in chunks, False otherwise
        """
        # Simple validation: check if response contains content from chunks
        response_lower = response.lower()

        # Look for content from any of the chunks in the response
        for chunk in chunks:
            content = chunk.get("content", "")
            if len(content) > 10:  # Only check substantial chunks
                # Check if a significant portion of the chunk appears in the response
                content_words = content.lower().split()
                if len(content_words) > 0:
                    # Check if at least some content from the chunk appears in response
                    found_content = any(word in response_lower for word in content_words[:10])
                    if found_content:
                        return True

        # If no chunk content was found in response, it might be hallucinated
        return False

    def close(self):
        """Clean up resources."""
        # No specific cleanup needed for the OpenAI Agents SDK agent
        # The agent doesn't maintain persistent connections that need cleanup
        pass


def main():
    """Main function to run the RAG agent."""
    parser = argparse.ArgumentParser(description="RAG Chatbot Agent with Qdrant retrieval integration")
    parser.add_argument("query", nargs="?", help="Query to ask the agent")
    parser.add_argument("--top-k", type=int, default=5, help="Number of chunks to retrieve (default: 5)")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    # Configure logging based on verbose flag
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        print("Verbose logging enabled")
    else:
        logging.getLogger().setLevel(logging.INFO)
        logger.setLevel(logging.INFO)

    # Initialize the agent
    try:
        agent = RAGAgent()
    except ValueError as e:
        logger.error(f"Error initializing agent: {e}")
        print(f"Error initializing agent: {e}")
        return

    logger.info(f"Agent initialized successfully with top_k={args.top_k}")

    if args.interactive or not args.query:
        # Interactive mode
        print("RAG Agent ready! Ask your questions (type 'quit' to exit):")
        while True:
            try:
                user_input = input("\n> ").strip()
                if user_input.lower() in ['quit', 'exit', 'q']:
                    logger.info("User requested to quit")
                    break
                if not user_input:
                    continue

                logger.info(f"Processing user query: {user_input[:50]}{'...' if len(user_input) > 50 else ''}")
                response = agent.query(user_input, top_k=args.top_k)
                print(f"\n{response['response']}")

                if response['retrieved_chunks']:
                    logger.info(f"Retrieved {len(response['retrieved_chunks'])} chunks for query")
                    print(f"\nUsed {len(response['retrieved_chunks'])} document chunks:")
                    for i, chunk in enumerate(response['retrieved_chunks'][:2]):  # Show first 2 chunks
                        print(f"  {i+1}. {chunk['content'][:200]}...")
                else:
                    logger.warning("No relevant document chunks found for query")
                    print("\nNo relevant document chunks found.")

            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received, exiting")
                print("\nGoodbye!")
                break
            except Exception as e:
                logger.error(f"Error processing query: {e}")
                print(f"Error processing query: {e}")
    else:
        # Single query mode
        logger.info(f"Processing single query: {args.query[:50]}{'...' if len(args.query) > 50 else ''}")
        response = agent.query(args.query, top_k=args.top_k)
        print(f"Response: {response['response']}")

        if response['retrieved_chunks']:
            logger.info(f"Retrieved {len(response['retrieved_chunks'])} chunks for query")
            print(f"\nUsed {len(response['retrieved_chunks'])} document chunks:")
            for i, chunk in enumerate(response['retrieved_chunks']):
                print(f"  {i+1}. {chunk['content'][:200]}...")
        else:
            logger.warning("No relevant document chunks found for query")
            print("\nNo relevant document chunks found.")

    # Clean up
    agent.close()
    logger.info("Agent session completed and resources cleaned up")

#  function
if __name__ == "__main__":
    main()

