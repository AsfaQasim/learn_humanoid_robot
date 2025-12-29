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

    # Try method 3: query() with query_vector parameter
    if has_query:
        try:
            logger.info("Using query() method with query_vector")
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

            results = client.query(**kwargs)
            logger.info(f"query() returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"query() with query_vector failed: {e}")

    # Last resort: error
    logger.error(f"No compatible search method found on Qdrant client. Available attributes: {[attr for attr in dir(client) if not attr.startswith('_')][:20]}")
    raise AttributeError(f"Qdrant client does not have any compatible search method (search, query_points, or query)")
