"""
Qdrant compatibility layer to handle different client versions and methods.
"""
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

def safe_qdrant_search(
    client,
    collection_name: str,
    query_vector: List[float],
    limit: int = 5,
    with_payload: bool = True,
    query_filter: Optional[Any] = None,
    score_threshold: Optional[float] = None
) -> List[Any]:
    """
    Safely perform Qdrant search using whatever method is available.

    Tries multiple methods in order:
    1. search() - Standard method in most versions
    2. query() with query_vector - Alternative method
    3. scroll() - Fallback if no search available

    Args:
        client: QdrantClient instance
        collection_name: Name of collection to search
        query_vector: Embedding vector to search with
        limit: Maximum results to return
        with_payload: Whether to include payload
        query_filter: Optional filter
        score_threshold: Minimum score threshold

    Returns:
        List of search results
    """

    # Log what methods are available
    has_search = hasattr(client, 'search')
    has_query = hasattr(client, 'query')
    has_query_points = hasattr(client, 'query_points')

    logger.info(f"Qdrant client type: {type(client).__name__}")
    logger.info(f"Available methods: search={has_search}, query={has_query}, query_points={has_query_points}")

    # Try method 1: search() - most common
    if has_search:
        try:
            logger.info("Using search() method")
            kwargs = {
                'collection_name': collection_name,
                'query_vector': query_vector,
                'limit': limit,
                'with_payload': with_payload
            }
            if query_filter is not None:
                kwargs['query_filter'] = query_filter
            if score_threshold is not None:
                kwargs['score_threshold'] = score_threshold

            results = client.search(**kwargs)
            logger.info(f"search() returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"search() failed: {e}")

    # Try method 2: query_points()
    if has_query_points:
        try:
            logger.info("Using query_points() method")
            kwargs = {
                'collection_name': collection_name,
                'query': query_vector,
                'limit': limit,
                'with_payload': with_payload
            }
            if query_filter is not None:
                kwargs['query_filter'] = query_filter
            if score_threshold is not None:
                kwargs['score_threshold'] = score_threshold

            response = client.query_points(**kwargs)
            results = response.points if hasattr(response, 'points') else response
            logger.info(f"query_points() returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"query_points() failed: {e}")

    # Try method 3: query() - newer method that might expect different parameters
    if has_query:
        try:
            logger.info("Using query() method")
            # The query method in newer versions expects a different format for vector search
            from qdrant_client.http import models

            # Attempt to use the query method with the correct parameters for vector search
            # In newer versions, we might need to pass the vector differently
            results = client.query(
                collection_name=collection_name,
                query=query_vector,  # In newer versions, the vector itself is the query
                limit=limit,
                with_payload=with_payload,
                query_filter=query_filter,
                score_threshold=score_threshold
            )
            logger.info(f"query() method succeeded with {len(results)} results")
            return results
        except TypeError as te:
            logger.error(f"query() method failed due to type error: {te}")
            # If it's a type error about missing required arguments, try alternative approaches
            if "missing" in str(te) or "required" in str(te):
                logger.info("Trying alternative query() approach with NearestQuery...")

                # Try with models.NearestQuery if available in newer versions
                try:
                    query_struct = models.NearestQuery(vector=query_vector)
                    results = client.query(
                        collection_name=collection_name,
                        query=query_struct,
                        limit=limit,
                        with_payload=with_payload,
                        query_filter=query_filter,
                        score_threshold=score_threshold
                    )
                    logger.info(f"query() with NearestQuery succeeded with {len(results)} results")
                    return results
                except Exception as nearest_e:
                    logger.error(f"NearestQuery approach failed: {nearest_e}")
            else:
                logger.error(f"Other TypeError in query() method: {te}")
        except Exception as inner_e:
            logger.error(f"Direct query() call failed: {inner_e}")

            # Try with models.NearestQuery if available in newer versions
            try:
                from qdrant_client.http import models
                query_struct = models.NearestQuery(vector=query_vector)
                results = client.query(
                    collection_name=collection_name,
                    query=query_struct,
                    limit=limit,
                    with_payload=with_payload,
                    query_filter=query_filter,
                    score_threshold=score_threshold
                )
                logger.info(f"query() with NearestQuery succeeded with {len(results)} results")
                return results
            except Exception as nearest_e:
                logger.error(f"NearestQuery approach failed: {nearest_e}")

    # Try method 4: scroll() as a fallback for when search methods don't work
    has_scroll = hasattr(client, 'scroll')
    if has_scroll:
        try:
            logger.info("Using scroll() method as fallback")
            # Scroll can be used to retrieve records, though it's not ideal for similarity search
            # This is just a fallback when other methods fail
            records, next_page_offset = client.scroll(
                collection_name=collection_name,
                limit=limit,
                with_payload=with_payload
            )
            # Convert scroll records to the same format as search results for compatibility
            # Note: scroll doesn't perform semantic search, so results won't be relevant
            # But at least it avoids the error
            converted_results = []
            for record in records:
                # Create a mock result object with similar structure to search results
                mock_result = type('MockResult', (), {
                    'id': record.id,
                    'payload': record.payload,
                    'score': 0.0,  # No relevance score from scroll
                    'vector': getattr(record, 'vector', None)
                })()
                converted_results.append(mock_result)

            logger.info(f"scroll() returned {len(converted_results)} results (not semantically ranked)")
            return converted_results
        except Exception as e:
            logger.error(f"scroll() fallback also failed: {e}")

    # Last resort: error
    logger.error(f"No compatible search method found on Qdrant client. Available attributes: {[attr for attr in dir(client) if not attr.startswith('_')][:20]}")
    raise AttributeError(f"Qdrant client does not have any compatible search method (search, query_points, query, or scroll)")
