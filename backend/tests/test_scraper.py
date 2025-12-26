"""
Unit tests for the scraper module.
"""

import pytest
from unittest.mock import Mock, patch
from src.scraper import DocumentScraper
from src.models.data_models import DocumentChunk, MetadataRecord


class TestDocumentScraper:
    """Test class for DocumentScraper."""

    def test_scraper_initialization(self):
        """Test that scraper initializes correctly."""
        scraper = DocumentScraper()
        assert scraper.session is not None
        assert 'User-Agent' in scraper.session.headers

    def test_validate_and_sanitize_url_valid(self):
        """Test URL validation and sanitization with valid URL."""
        scraper = DocumentScraper()
        url = "https://example.com"
        result = scraper.validate_and_sanitize_url(url)
        assert result == url

    def test_validate_and_sanitize_url_invalid(self):
        """Test URL validation with invalid URL."""
        scraper = DocumentScraper()
        url = "not-a-url"

        with pytest.raises(Exception):  # ValidationError
            scraper.validate_and_sanitize_url(url)

    def test_extract_content_with_metadata(self):
        """Test content extraction with metadata."""
        from bs4 import BeautifulSoup

        scraper = DocumentScraper()
        html_content = """
        <html>
            <head><title>Test Title</title></head>
            <body>
                <h1>Main Heading</h1>
                <h2>Sub Heading</h2>
                <div class="content">This is the main content.</div>
                <nav>Navigation</nav>
            </body>
        </html>
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        content, section, heading = scraper.extract_content_with_metadata(soup, "https://example.com")

        assert "This is the main content." in content
        assert "Test Title" in section
        assert "Main Heading" in heading
        assert "Navigation" not in content  # Navigation should be removed

    @patch('src.scraper.requests.Session.get')
    def test_scrape_single_url(self, mock_get):
        """Test scraping a single URL."""
        # Mock the response
        mock_response = Mock()
        mock_response.content = b'<html><body><p>Test content</p></body></html>'
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        scraper = DocumentScraper()
        metadata, chunks = scraper.scrape_single_url("https://example.com/test")

        assert isinstance(metadata, MetadataRecord)
        assert len(chunks) >= 0  # At least one chunk should be created
        if chunks:
            assert isinstance(chunks[0], DocumentChunk)
            assert "Test content" in chunks[0].content

    def test_validate_url_function(self):
        """Test the validate_url utility function."""
        from src.utils import validate_url

        assert validate_url("https://example.com") == True
        assert validate_url("http://example.com") == True
        assert validate_url("not-a-url") == False
        assert validate_url("") == False
        assert validate_url(None) == False