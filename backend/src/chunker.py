"""
Text chunking module for the RAG ingestion pipeline.
Handles splitting text into appropriately sized chunks with overlap.
"""

from typing import List, Dict, Tuple
import re
from transformers import AutoTokenizer
from .models.data_models import DocumentChunk
from .config import config
from .utils import sanitize_text
from .errors import ChunkingError
from .logging_config import logger


class TextChunker:
    """Handles text chunking with overlap and metadata preservation."""

    def __init__(self, chunk_size: int = None, overlap: int = None):
        """
        Initialize the chunker with configuration.

        Args:
            chunk_size: Size of each chunk (default from config)
            overlap: Overlap between chunks (default from config)
        """
        self.chunk_size = chunk_size or config.CHUNK_SIZE
        self.overlap = overlap or config.CHUNK_OVERLAP
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

    def chunk_text(self, text: str, source_url: str, section: str, heading: str,
                   metadata: Dict = None) -> List[DocumentChunk]:
        """
        Chunk text into appropriately sized pieces with overlap.

        Args:
            text: Text to chunk
            source_url: Source URL for metadata
            section: Section information for metadata
            heading: Heading information for metadata
            metadata: Additional metadata to include

        Returns:
            List of DocumentChunk objects
        """
        if not text or len(text.strip()) == 0:
            raise ChunkingError("Cannot chunk empty text")

        # Clean the text
        clean_text = sanitize_text(text)

        # Split text into chunks
        chunks = self._split_text_with_overlap(clean_text)

        # Create DocumentChunk objects
        document_chunks = []
        for i, chunk_text in enumerate(chunks):
            chunk_metadata = {
                "source_url": source_url,
                "section": section,
                "heading": heading,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }

            # Add any additional metadata
            if metadata:
                chunk_metadata.update(metadata)

            document_chunk = DocumentChunk(
                id="",
                content=chunk_text,
                source_url=source_url,
                section=section,
                heading=heading,
                metadata=chunk_metadata
            )

            document_chunks.append(document_chunk)

        logger.info(f"Text chunked into {len(document_chunks)} chunks")
        return document_chunks

    def _split_text_with_overlap(self, text: str) -> List[str]:
        """
        Split text into chunks with overlap using token-based approach.

        Args:
            text: Text to split

        Returns:
            List of text chunks
        """
        # First, split by paragraphs to maintain semantic boundaries
        paragraphs = self._split_by_paragraphs(text)

        chunks = []
        current_chunk = ""
        current_tokens = 0

        for paragraph in paragraphs:
            # Tokenize the paragraph to estimate token count
            paragraph_tokens = len(self.tokenizer.encode(paragraph))

            # If adding this paragraph would exceed chunk size
            if current_tokens + paragraph_tokens > self.chunk_size and current_chunk:
                chunks.append(current_chunk.strip())

                # Add overlap by taking part of the previous chunk
                if self.overlap > 0:
                    # Calculate overlap based on characters for simplicity
                    overlap_start = max(0, len(current_chunk) - self.overlap * 10)  # Rough approximation
                    current_chunk = current_chunk[overlap_start:] + paragraph
                    current_tokens = len(self.tokenizer.encode(current_chunk))
                else:
                    current_chunk = paragraph
                    current_tokens = paragraph_tokens
            else:
                # Add paragraph to current chunk
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph
                current_tokens += paragraph_tokens

            # If current chunk is getting too large, force a split
            if current_tokens > self.chunk_size:
                # Split the current chunk into smaller pieces
                sub_chunks = self._force_split_chunk(current_chunk, current_tokens)
                for sub_chunk in sub_chunks[:-1]:  # Add all but the last to chunks
                    chunks.append(sub_chunk)

                # Keep the last sub-chunk as current for potential overlap
                current_chunk = sub_chunks[-1] if sub_chunks else ""
                current_tokens = len(self.tokenizer.encode(current_chunk))

        # Add the final chunk if it's not empty
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def _split_by_paragraphs(self, text: str) -> List[str]:
        """
        Split text by paragraphs to maintain semantic boundaries.

        Args:
            text: Text to split

        Returns:
            List of paragraphs
        """
        # Split by double newlines first
        paragraphs = text.split('\n\n')

        # Clean up paragraphs
        cleaned_paragraphs = []
        for para in paragraphs:
            clean_para = sanitize_text(para)
            if clean_para:  # Only add non-empty paragraphs
                cleaned_paragraphs.append(clean_para)

        return cleaned_paragraphs

    def _force_split_chunk(self, chunk: str, token_count: int) -> List[str]:
        """
        Force split a chunk that's too large into smaller pieces.

        Args:
            chunk: Chunk to split
            token_count: Estimated token count of the chunk

        Returns:
            List of smaller chunks
        """
        # Calculate target size for sub-chunks
        num_sub_chunks = max(2, token_count // self.chunk_size + 1)
        target_size = len(chunk) // num_sub_chunks

        sub_chunks = []
        start = 0

        while start < len(chunk):
            end = start + target_size

            # Try to break at a sentence boundary if possible
            if end < len(chunk):
                # Look for sentence boundaries near the target
                for i in range(end, min(end + 50, len(chunk))):
                    if chunk[i] in '.!?':
                        end = i + 1
                        break
                else:
                    # If no sentence boundary found, break at word boundary
                    for i in range(end, min(end + 50, len(chunk))):
                        if chunk[i] == ' ':
                            end = i
                            break

            sub_chunk = chunk[start:end].strip()
            if sub_chunk:
                sub_chunks.append(sub_chunk)

            start = end

        return sub_chunks

    def validate_chunk(self, chunk: DocumentChunk) -> bool:
        """
        Validate a document chunk.

        Args:
            chunk: DocumentChunk to validate

        Returns:
            True if valid, False otherwise
        """
        if not chunk.content or len(chunk.content.strip()) == 0:
            return False

        if len(chunk.content) > self.chunk_size * 2:  # Allow some flexibility
            logger.warning(f"Chunk with ID {chunk.id} is larger than expected")

        return True

    def chunk_document_chunks(self, document_chunks: List[DocumentChunk]) -> List[DocumentChunk]:
        """
        Chunk a list of document chunks (useful for re-chunking already chunked content).

        Args:
            document_chunks: List of DocumentChunk objects to re-chunk

        Returns:
            List of re-chunked DocumentChunk objects
        """
        all_chunks = []
        for doc_chunk in document_chunks:
            chunks = self.chunk_text(
                text=doc_chunk.content,
                source_url=doc_chunk.source_url,
                section=doc_chunk.section,
                heading=doc_chunk.heading,
                metadata=doc_chunk.metadata
            )
            all_chunks.extend(chunks)

        return all_chunks