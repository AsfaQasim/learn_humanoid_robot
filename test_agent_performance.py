"""
Performance test for the RAG Chatbot Agent.
"""
import time
import unittest
from unittest.mock import patch, Mock
from agent import RAGAgent


class TestRAGAgentPerformance(unittest.TestCase):
    """Performance tests for the RAGAgent class."""

    @patch('agent.Agent')
    @patch('agent.RAGRetriever')
    def test_response_time_under_2_seconds(self, mock_retriever, mock_agent_class):
        """Test that agent responses are returned within 2 seconds."""
        # Setup mocks
        mock_agent_instance = Mock()
        mock_agent_instance.name = "test-agent-name"
        mock_agent_class.return_value = mock_agent_instance

        # Mock the Runner.run response structure
        mock_result = Mock()
        mock_result.final_output = "This is a test response from the agent."

        # Mock Runner.run to return the result
        with patch('agent.Runner') as mock_runner:
            mock_runner.run.return_value = mock_result

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

            # Create agent instance
            agent = RAGAgent()

            # Measure response time
            start_time = time.time()
            response = agent.query("test query", top_k=1)
            end_time = time.time()

            response_time = end_time - start_time

            # Verify response time is under 2 seconds
            self.assertLess(response_time, 2.0, f"Response time {response_time:.2f}s exceeded 2 seconds")

            # Verify that a response was returned
            self.assertIn("response", response)
            self.assertIn("retrieved_chunks", response)


if __name__ == '__main__':
    unittest.main()