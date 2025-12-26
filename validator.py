"""
Pipeline validation and compatibility checks for the RAG retrieval pipeline.
"""

from typing import List, Dict, Any
import statistics
from retriever import RAGRetriever
from models import ValidationResult
from utils import generate_uuid


class RAGValidator:
    """Handles pipeline validation and compatibility checks."""

    def __init__(self, retriever: RAGRetriever):
        """
        Initialize the validator with a retriever instance.

        Args:
            retriever: Instance of RAGRetriever to validate
        """
        self.retriever = retriever

    def validate_embedding_compatibility(self) -> bool:
        """
        Validate that the embedding model used for retrieval matches the one used for ingestion.

        Returns:
            True if compatible, False otherwise
        """
        print("Validating embedding compatibility...")
        return self.retriever.validate_embedding_compatibility()

    def validate_result_data_model(self, result_data: Dict) -> bool:
        """
        Implement validation result data model validation.

        Args:
            result_data: Dictionary containing validation results to validate

        Returns:
            True if valid, False otherwise
        """
        required_keys = [
            "validation_passed",
            "test_queries_run",
            "queries_results",
            "overall_accuracy",
            "avg_relevance_score",
            "total_retrieved_chunks",
            "issues_found"
        ]

        # Check if all required keys exist
        for key in required_keys:
            if key not in result_data:
                print(f"Validation result missing required key: {key}")
                return False

        # Validate data types
        if not isinstance(result_data["validation_passed"], bool):
            print("validation_passed should be boolean")
            return False

        if not isinstance(result_data["test_queries_run"], int) or result_data["test_queries_run"] < 0:
            print("test_queries_run should be non-negative integer")
            return False

        if not isinstance(result_data["queries_results"], list):
            print("queries_results should be a list")
            return False

        if not isinstance(result_data["overall_accuracy"], (int, float)) or not 0.0 <= result_data["overall_accuracy"] <= 1.0:
            print("overall_accuracy should be a float between 0.0 and 1.0")
            return False

        if not isinstance(result_data["avg_relevance_score"], (int, float)) or not 0.0 <= result_data["avg_relevance_score"] <= 1.0:
            print("avg_relevance_score should be a float between 0.0 and 1.0")
            return False

        if not isinstance(result_data["total_retrieved_chunks"], int) or result_data["total_retrieved_chunks"] < 0:
            print("total_retrieved_chunks should be non-negative integer")
            return False

        if not isinstance(result_data["issues_found"], list):
            print("issues_found should be a list")
            return False

        print("Validation result data model validated successfully")
        return True

    def create_multi_query_validation(self, test_queries: List[str]) -> Dict[str, Any]:
        """
        Create multi-query validation function.

        Args:
            test_queries: List of test queries to validate against

        Returns:
            Validation results dictionary
        """
        print(f"Creating multi-query validation with {len(test_queries)} test queries...")

        validation_results = {
            "validation_passed": True,
            "test_queries_run": len(test_queries),
            "queries_results": [],
            "overall_accuracy": 0.0,
            "avg_relevance_score": 0.0,
            "total_retrieved_chunks": 0,
            "issues_found": [],
            "query_consistency_score": 0.0
        }

        all_relevance_scores = []
        total_chunks = 0

        for query in test_queries:
            print(f"\nTesting query: '{query}'")

            try:
                # Retrieve chunks for the query
                chunks = self.retriever.retrieve_chunks(query, top_k=3)

                query_result = {
                    "query": query,
                    "retrieved_chunks": len(chunks),
                    "chunks": chunks,
                    "avg_relevance_score": 0.0,
                    "issues": []
                }

                if chunks:
                    chunk_scores = [c["relevance_score"] for c in chunks]
                    avg_score = statistics.mean(chunk_scores) if chunk_scores else 0.0
                    query_result["avg_relevance_score"] = avg_score
                    all_relevance_scores.extend(chunk_scores)
                    total_chunks += len(chunks)

                    # Check if relevance scores are acceptable
                    for chunk in chunks:
                        if chunk["relevance_score"] < 0.5:
                            query_result["issues"].append(
                                f"Low relevance score ({chunk['relevance_score']:.3f}) for chunk: {chunk['content'][:100]}..."
                            )
                else:
                    query_result["issues"].append("No chunks retrieved for this query")
                    validation_results["validation_passed"] = False

                validation_results["queries_results"].append(query_result)

            except Exception as e:
                error_msg = f"Error processing query '{query}': {str(e)}"
                validation_results["issues_found"].append(error_msg)
                validation_results["validation_passed"] = False
                print(f"Error: {error_msg}")

        # Calculate overall metrics
        if all_relevance_scores:
            validation_results["avg_relevance_score"] = statistics.mean(all_relevance_scores)
            validation_results["total_retrieved_chunks"] = total_chunks

            # Calculate consistency across queries
            if len(all_relevance_scores) > 1:
                mean_score = statistics.mean(all_relevance_scores)
                variance = sum((x - mean_score) ** 2 for x in all_relevance_scores) / len(all_relevance_scores)
                std_dev = variance ** 0.5
                # Higher consistency if lower deviation
                validation_results["query_consistency_score"] = max(0.0, 1.0 - std_dev)

            # Simple accuracy calculation based on average relevance
            validation_results["overall_accuracy"] = min(1.0, validation_results["avg_relevance_score"] * 2)  # Scale to 0-1 range

        print(f"\nMulti-query validation completed:")
        print(f"- Queries run: {validation_results['test_queries_run']}")
        print(f"- Total chunks retrieved: {validation_results['total_retrieved_chunks']}")
        print(f"- Average relevance score: {validation_results['avg_relevance_score']:.3f}")
        print(f"- Query consistency score: {validation_results['query_consistency_score']:.3f}")
        print(f"- Overall accuracy: {validation_results['overall_accuracy']:.3f}")
        print(f"- Passed: {validation_results['validation_passed']}")

        if validation_results["issues_found"]:
            print(f"- Issues found: {len(validation_results['issues_found'])}")

        return validation_results

    def validate_relevance_scoring(self, query: str, expected_sources: List[str] = None, top_k: int = 5) -> Dict[str, Any]:
        """
        Implement relevance scoring validation.

        Args:
            query: Query to validate relevance scoring for
            expected_sources: Optional list of expected source URLs that should be retrieved
            top_k: Number of results to retrieve

        Returns:
            Dictionary with relevance validation results
        """
        print(f"Validating relevance scoring for query: '{query}'")

        relevance_validation = {
            "query": query,
            "expected_sources": expected_sources or [],
            "top_k_requested": top_k,
            "retrieved_chunks": [],
            "relevance_scores": [],
            "avg_relevance_score": 0.0,
            "sources_found": [],
            "recall_rate": 0.0,
            "precision_at_k": 0.0,
            "validation_passed": True,
            "issues": []
        }

        try:
            # Retrieve chunks for the query
            chunks = self.retriever.retrieve_chunks(query, top_k=top_k)

            relevance_validation["retrieved_chunks"] = chunks
            relevance_validation["relevance_scores"] = [c["relevance_score"] for c in chunks]

            if chunks:
                relevance_validation["avg_relevance_score"] = statistics.mean([c["relevance_score"] for c in chunks])

                # Track which expected sources were found
                if expected_sources:
                    found_sources = []
                    for chunk in chunks:
                        if chunk["source_url"] in expected_sources:
                            found_sources.append(chunk["source_url"])

                    relevance_validation["sources_found"] = found_sources

                    # Calculate recall rate: found / expected
                    if expected_sources:
                        relevance_validation["recall_rate"] = len(found_sources) / len(expected_sources)

                    # Calculate precision at k: relevant retrieved / total retrieved
                    relevant_retrieved = len([c for c in chunks if c["relevance_score"] >= 0.5])  # threshold
                    relevance_validation["precision_at_k"] = relevant_retrieved / len(chunks) if chunks else 0.0

                    # Check if expected sources were found
                    if expected_sources and not found_sources:
                        relevance_validation["issues"].append("Expected sources not found in results")
                        relevance_validation["validation_passed"] = False

                # Check if relevance scores are reasonable
                low_score_chunks = [c for c in chunks if c["relevance_score"] < 0.3]
                if low_score_chunks:
                    relevance_validation["issues"].append(f"{len(low_score_chunks)} chunks with low relevance scores (< 0.3)")

            print(f"Relevance scoring validation completed:")
            print(f"- Average relevance score: {relevance_validation['avg_relevance_score']:.3f}")
            print(f"- Recall rate: {relevance_validation['recall_rate']:.3f}")
            print(f"- Precision at K: {relevance_validation['precision_at_k']:.3f}")
            print(f"- Sources found: {len(relevance_validation['sources_found'])}/{len(relevance_validation['expected_sources'])}")

        except Exception as e:
            error_msg = f"Error validating relevance scoring for query '{query}': {str(e)}"
            relevance_validation["issues"].append(error_msg)
            relevance_validation["validation_passed"] = False
            print(f"Error: {error_msg}")

        return relevance_validation

    def run_validation_pipeline(self, test_queries: List[str], expected_sources: List[str] = None) -> Dict[str, Any]:
        """
        Create validation pipeline that runs multiple test queries.

        Args:
            test_queries: List of test queries to run
            expected_sources: Optional list of expected source URLs

        Returns:
            Dictionary with complete validation pipeline results
        """
        print(f"Running validation pipeline with {len(test_queries)} test queries...")

        pipeline_results = {
            "pipeline_validation_passed": True,
            "test_queries_run": len(test_queries),
            "expected_sources": expected_sources or [],
            "multi_query_validation": {},
            "relevance_validations": [],
            "overall_metrics": {
                "avg_relevance_score": 0.0,
                "avg_precision": 0.0,
                "avg_recall": 0.0,
                "consistency_score": 0.0,
                "accuracy_score": 0.0
            },
            "issues_found": [],
            "validation_summary": {}
        }

        relevance_scores = []
        precisions = []
        recalls = []

        # Run multi-query validation
        multi_validation = self.create_multi_query_validation(test_queries)
        pipeline_results["multi_query_validation"] = multi_validation
        pipeline_results["pipeline_validation_passed"] = multi_validation["validation_passed"]

        # Run individual relevance validations
        for query in test_queries:
            relevance_val = self.validate_relevance_scoring(query, expected_sources)
            pipeline_results["relevance_validations"].append(relevance_val)

            # Collect metrics for overall calculation
            if relevance_val["relevance_scores"]:
                relevance_scores.extend(relevance_val["relevance_scores"])
            if relevance_val["precision_at_k"] is not None:
                precisions.append(relevance_val["precision_at_k"])
            if relevance_val["recall_rate"] is not None:
                recalls.append(relevance_val["recall_rate"])

            # Collect any issues
            if relevance_val["issues"]:
                pipeline_results["issues_found"].extend(relevance_val["issues"])

        # Calculate overall metrics
        if relevance_scores:
            pipeline_results["overall_metrics"]["avg_relevance_score"] = statistics.mean(relevance_scores)
        if precisions:
            pipeline_results["overall_metrics"]["avg_precision"] = statistics.mean(precisions)
        if recalls:
            pipeline_results["overall_metrics"]["avg_recall"] = statistics.mean(recalls)

        # Calculate consistency score based on multi-query validation
        pipeline_results["overall_metrics"]["consistency_score"] = multi_validation.get("query_consistency_score", 0.0)
        pipeline_results["overall_metrics"]["accuracy_score"] = multi_validation.get("overall_accuracy", 0.0)

        # Update overall validation status if individual validations failed
        for rel_val in pipeline_results["relevance_validations"]:
            if not rel_val["validation_passed"]:
                pipeline_results["pipeline_validation_passed"] = False
                break

        pipeline_results["validation_summary"] = {
            "total_test_queries": len(test_queries),
            "total_issues_found": len(pipeline_results["issues_found"]),
            "pipeline_passed": pipeline_results["pipeline_validation_passed"],
            "avg_relevance": pipeline_results["overall_metrics"]["avg_relevance_score"],
            "avg_precision": pipeline_results["overall_metrics"]["avg_precision"],
            "avg_recall": pipeline_results["overall_metrics"]["avg_recall"]
        }

        print(f"\nPipeline validation completed:")
        print(f"- Test queries: {pipeline_results['test_queries_run']}")
        print(f"- Issues found: {len(pipeline_results['issues_found'])}")
        print(f"- Pipeline passed: {pipeline_results['pipeline_validation_passed']}")
        print(f"- Avg relevance: {pipeline_results['overall_metrics']['avg_relevance_score']:.3f}")
        print(f"- Avg precision: {pipeline_results['overall_metrics']['avg_precision']:.3f}")
        print(f"- Avg recall: {pipeline_results['overall_metrics']['avg_recall']:.3f}")

        return pipeline_results

    def test_validation_with_queries(self, query_types: List[str]) -> Dict[str, Any]:
        """
        Test validation functionality with various query types.

        Args:
            query_types: List of different types of queries to test

        Returns:
            Dictionary with test results
        """
        print(f"Testing validation functionality with {len(query_types)} different query types...")

        test_results = {
            "query_types_tested": len(query_types),
            "query_types": query_types,
            "individual_results": [],
            "summary": {
                "successful_validations": 0,
                "failed_validations": 0,
                "avg_processing_time": 0.0,
                "most_common_issue": "",
                "success_rate": 0.0
            }
        }

        successful_count = 0
        failed_count = 0
        issues = []

        for query_type in query_types:
            print(f"\nTesting query type: {query_type}")

            # Create sample queries based on the type
            if query_type == "factual":
                test_queries = ["What are robotics fundamentals?", "Define artificial intelligence"]
            elif query_type == "conceptual":
                test_queries = ["How does machine learning work?", "Explain neural networks"]
            elif query_type == "procedural":
                test_queries = ["How to implement a controller?", "Steps for data preprocessing"]
            else:
                test_queries = [f"Sample {query_type} query", f"Another {query_type} example"]

            try:
                # Run validation for this query type
                result = self.run_validation_pipeline(test_queries)
                test_results["individual_results"].append({
                    "query_type": query_type,
                    "validation_result": result,
                    "success": result["pipeline_validation_passed"]
                })

                if result["pipeline_validation_passed"]:
                    successful_count += 1
                else:
                    failed_count += 1

                # Collect issues
                if result["issues_found"]:
                    issues.extend(result["issues_found"])

            except Exception as e:
                test_results["individual_results"].append({
                    "query_type": query_type,
                    "error": str(e),
                    "success": False
                })
                failed_count += 1
                issues.append(f"Error with {query_type} queries: {str(e)}")

        # Calculate summary statistics
        total_tests = successful_count + failed_count
        test_results["summary"]["successful_validations"] = successful_count
        test_results["summary"]["failed_validations"] = failed_count
        test_results["summary"]["success_rate"] = successful_count / total_tests if total_tests > 0 else 0.0

        # Find most common issue
        if issues:
            from collections import Counter
            issue_counts = Counter(issues)
            test_results["summary"]["most_common_issue"] = issue_counts.most_common(1)[0][0] if issue_counts else ""

        print(f"\nValidation testing completed:")
        print(f"- Query types tested: {test_results['query_types_tested']}")
        print(f"- Successful validations: {test_results['summary']['successful_validations']}")
        print(f"- Failed validations: {test_results['summary']['failed_validations']}")
        print(f"- Success rate: {test_results['summary']['success_rate']:.2%}")
        if test_results["summary"]["most_common_issue"]:
            print(f"- Most common issue: {test_results['summary']['most_common_issue']}")

        return test_results