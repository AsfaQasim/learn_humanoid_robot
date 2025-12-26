"""
Test suite for the RAG Chatbot Agent with Qdrant retrieval integration.
"""
import unittest
import os
from unittest.mock import Mock, patch, MagicMock
from agent import RAGAgent
from config import config


class TestRAGAgent(unittest.TestCase):
    """Test cases for the RAGAgent class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Mock the OpenAI API key to avoid actual API calls during testing
        os.environ["OPENAI_API_KEY"] = "test-key"
        os.environ["COHERE_API_KEY"] = "test-key"
        os.environ["QDRANT_URL"] = "https://test.qdrant.io"

    @patch('agent.Agent')
    @patch('agent.RAGRetriever')
    def test_agent_initialization(self, mock_retriever, mock_agent_class):
        """Test that the agent initializes correctly with required components."""
        # Mock the Agent class
        mock_agent_instance = Mock()
        mock_agent_instance.name = "test-agent-name"
        mock_agent_class.return_value = mock_agent_instance

        # Mock the retriever
        mock_retriever_instance = Mock()
        mock_retriever.return_value = mock_retriever_instance

        # Initialize the agent
        agent = RAGAgent()

        # Verify that the agent was initialized properly
        self.assertIsNotNone(agent)
        self.assertEqual(agent.agent.name, "test-agent-name")
        mock_agent_class.assert_called_once()

    @patch('agent.Agent')
    @patch('agent.RAGRetriever')
    def test_qdrant_retrieval_success(self, mock_retriever, mock_agent_class):
        """Test that qdrant_retrieval returns expected chunks when successful."""
        # Setup mocks
        mock_agent_instance = Mock()
        mock_agent_instance.name = "test-agent-name"
        mock_agent_class.return_value = mock_agent_instance

        # Mock retriever with successful retrieval
        mock_retriever_instance = Mock()
        mock_retriever_instance.handle_connection_failures.return_value = True
        mock_retriever_instance.retrieve_chunks_with_retry.return_value = [
            {
                "rank": 1,
                "id": "test-id-1",
                "content": "Test content 1",
                "relevance_score": 0.8,
                "source_url": "http://example.com",
                "section": "Test Section",
                "heading": "Test Heading",
                "metadata": {},
                "retrieved_at": "2023-01-01T00:00:00"
            }
        ]
        mock_retriever.return_value = mock_retriever_instance

        agent = RAGAgent()

        # Test the retrieval
        result = agent.qdrant_retrieval("test query", top_k=1)

        # Verify the result
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["content"], "Test content 1")
        self.assertEqual(result[0]["relevance_score"], 0.8)

        # Verify that the retriever methods were called
        mock_retriever_instance.handle_connection_failures.assert_called()
        mock_retriever_instance.retrieve_chunks_with_retry.assert_called_with("test query", top_k=1)

    @patch('agent.Agent')
    @patch('agent.RAGRetriever')
    def test_qdrant_retrieval_with_connection_failure(self, mock_retriever, mock_agent_class):
        """Test that qdrant_retrieval handles connection failures gracefully."""
        # Setup mocks
        mock_agent_instance = Mock()
        mock_agent_instance.name = "test-agent-name"
        mock_agent_class.return_value = mock_agent_instance

        # Mock retriever with connection failure
        mock_retriever_instance = Mock()
        mock_retriever_instance.handle_connection_failures.return_value = False  # Simulate failure
        mock_retriever.return_value = mock_retriever_instance

        agent = RAGAgent()

        # Test the retrieval
        result = agent.qdrant_retrieval("test query", top_k=1)

        # Verify the result is empty due to connection failure
        self.assertEqual(result, [])

        # Verify that the connection handling was called
        mock_retriever_instance.handle_connection_failures.assert_called()

    def test_query_validation_empty(self):
        """Test that empty queries are properly validated."""
        agent = RAGAgent.__new__(RAGAgent)  # Create without calling __init__ to avoid API calls

        # Test empty query
        is_valid, issues = agent._validate_query_complexity("")
        self.assertFalse(is_valid)
        self.assertIn("Query text is empty", issues)

        # Test whitespace-only query
        is_valid, issues = agent._validate_query_complexity("   ")
        self.assertFalse(is_valid)
        self.assertIn("Query text is empty", issues)

    def test_query_validation_long_query(self):
        """Test that overly long queries are properly validated."""
        agent = RAGAgent.__new__(RAGAgent)  # Create without calling __init__ to avoid API calls

        # Create a query longer than the default 1000 character limit
        long_query = "a" * 1001

        is_valid, issues = agent._validate_query_complexity(long_query)
        self.assertFalse(is_valid)
        self.assertTrue(any("exceeds maximum allowed length" in issue for issue in issues))

    def test_query_validation_special_characters(self):
        """Test that queries with excessive special characters are validated."""
        agent = RAGAgent.__new__(RAGAgent)  # Create without calling __init__ to avoid API calls

        # Create a query with 60% special characters (more than the 50% threshold)
        special_query = "!@#$%^&*()" * 20 + "normal text"  # Should exceed 50% threshold

        is_valid, issues = agent._validate_query_complexity(special_query)
        self.assertFalse(is_valid)
        self.assertTrue(any("high ratio of special characters" in issue for issue in issues))

    def test_query_validation_sql_injection(self):
        """Test that queries with potential SQL injection are validated."""
        agent = RAGAgent.__new__(RAGAgent)  # Create without calling __init__ to avoid API calls

        # Test a query with SQL injection pattern
        sql_query = "SELECT * FROM users"

        is_valid, issues = agent._validate_query_complexity(sql_query)
        self.assertFalse(is_valid)
        self.assertTrue(any("SQL injection pattern detected" in issue for issue in issues))

    def test_query_validation_script_injection(self):
        """Test that queries with potential script injection are validated."""
        agent = RAGAgent.__new__(RAGAgent)  # Create without calling __init__ to avoid API calls

        # Test a query with script injection pattern
        script_query = "<script>alert('test')</script>"

        is_valid, issues = agent._validate_query_complexity(script_query)
        self.assertFalse(is_valid)
        self.assertTrue(any("script injection detected" in issue for issue in issues))


class TestRAGAgentIntegration(unittest.TestCase):
    """Integration tests for the RAG Agent (these would require actual API keys)."""

    def test_agent_end_to_end_flow(self):
        """Test the complete flow from query to response (skipped for CI)."""
        # This test would require valid API keys, so we skip it in automated tests
        self.skipTest("Requires valid API keys for end-to-end testing")


if __name__ == '__main__':
    unittest.main()