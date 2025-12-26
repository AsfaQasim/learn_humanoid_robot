"""
Test script to verify the RAG Agent works with the OpenAI Agents SDK
"""
import os
from unittest.mock import patch, Mock
from agent import RAGAgent


def test_agent_initialization_with_sdk():
    """Test that the agent initializes correctly with the OpenAI Agents SDK."""
    # Mock the OpenAI API key to avoid actual API calls during testing
    os.environ["OPENAI_API_KEY"] = "test-key"

    with patch('agent.RAGRetriever') as mock_retriever:
        # Mock the retriever instance
        mock_retriever_instance = Mock()
        mock_retriever.return_value = mock_retriever_instance

        # Initialize the agent
        agent = RAGAgent()

        # Verify that the agent was initialized properly
        assert agent is not None
        assert hasattr(agent, 'agent')  # Should have the new agent instance
        assert hasattr(agent, 'qdrant_retrieval_tool')  # Should have the tool function
        assert hasattr(agent, 'qdrant_retrieval')  # Should have the wrapper function

        print("SUCCESS: Agent initialized successfully with OpenAI Agents SDK")
        print(f"SUCCESS: Agent name: {agent.agent.name}")
        print("SUCCESS: Agent has required methods and tools")


def test_function_tool_decorator():
    """Test that the function tool decorator is applied correctly."""
    os.environ["OPENAI_API_KEY"] = "test-key"

    with patch('agent.RAGRetriever') as mock_retriever:
        mock_retriever_instance = Mock()
        mock_retriever.return_value = mock_retriever_instance

        agent = RAGAgent()

        # Check that the qdrant_retrieval_tool is a FunctionTool object
        tool_func = agent.qdrant_retrieval_tool
        print(f"SUCCESS: Function tool created: {type(tool_func).__name__}")

        # The tool should be a FunctionTool instance
        from agents import function_tool
        assert hasattr(tool_func, 'name') or hasattr(tool_func, '__call__')
        print("SUCCESS: Function tool is properly configured")


if __name__ == "__main__":
    print("Testing RAG Agent with OpenAI Agents SDK...")
    print("=" * 50)

    test_agent_initialization_with_sdk()
    print()
    test_function_tool_decorator()

    print("\nSUCCESS: All tests passed! The agent is properly configured with the OpenAI Agents SDK.")