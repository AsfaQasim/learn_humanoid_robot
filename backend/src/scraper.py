"""
Web scraping module for the RAG ingestion pipeline.
Handles crawling and extracting clean text content from documentation URLs.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Tuple
import time
import urllib.parse
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET
from .config import config
from .models.data_models import DocumentChunk, MetadataRecord
from .utils import sanitize_text, validate_url, get_current_timestamp
from .errors import ScrapingError, NetworkError, ValidationError
from .logging_config import logger


class DocumentScraper:
    """Handles web scraping and content extraction from documentation URLs."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def scrape_urls(self, urls: List[str]) -> List[Tuple[MetadataRecord, List[DocumentChunk]]]:
        """
        Scrape multiple URLs and extract content.

        Args:
            urls: List of URLs to scrape

        Returns:
            List of tuples containing (metadata_record, list_of_document_chunks)
        """
        results = []
        for url in urls:
            try:
                # Validate URL
                if not validate_url(url):
                    raise ValidationError(f"Invalid URL: {url}")

                # Add rate limiting delay
                time.sleep(config.RATE_LIMIT_DELAY)

                # Scrape the URL
                metadata, chunks = self.scrape_single_url(url)
                results.append((metadata, chunks))

                logger.info(f"Successfully scraped {url} with {len(chunks)} chunks")

            except Exception as e:
                logger.error(f"Error scraping {url}: {str(e)}")
                raise ScrapingError(f"Failed to scrape {url}: {str(e)}")

        return results

    def scrape_single_url(self, url: str) -> Tuple[MetadataRecord, List[DocumentChunk]]:
        """
        Scrape a single URL and extract content.

        Args:
            url: URL to scrape

        Returns:
            Tuple containing (metadata_record, list_of_document_chunks)
        """
        try:
            # Make the request
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract content with metadata
            content, section, heading = self.extract_content_with_metadata(soup, url)

            # Create metadata record
            metadata_record = MetadataRecord(
                id="",
                source_url=url,
                section_title=section,
                heading_hierarchy=heading,
                created_at=get_current_timestamp(),
                chunk_count=1  # For now, we're creating one chunk per page
            )

            # Create document chunk
            chunk = DocumentChunk(
                id="",
                content=content,
                source_url=url,
                section=section,
                heading=heading,
                metadata={
                    "url": url,
                    "section": section,
                    "heading": heading,
                    "timestamp": get_current_timestamp().isoformat()
                }
            )

            return metadata_record, [chunk]

        except requests.RequestException as e:
            raise NetworkError(f"Network error while scraping {url}: {str(e)}")
        except Exception as e:
            raise ScrapingError(f"Error scraping {url}: {str(e)}")

    def extract_content_with_metadata(self, soup: BeautifulSoup, url: str) -> Tuple[str, str, str]:
        """
        Extract clean content with metadata from BeautifulSoup object.

        Args:
            soup: BeautifulSoup object containing parsed HTML
            url: Source URL for context

        Returns:
            Tuple containing (clean_content, section_title, heading_hierarchy)
        """
        # Remove navigation and other non-content elements
        for element in soup.find_all(['nav', 'header', 'footer', 'aside', 'script', 'style']):
            element.decompose()

        # Try to find the main content area with specific selectors for documentation sites
        content_selectors = [
            # Docusaurus-specific selectors
            '.main-wrapper .markdown',
            '.doc-wrapper .markdown',
            '.theme-doc-markdown',
            '.markdown',
            '.doc-content',
            '.docs-content',
            # General selectors
            'main',
            'article',
            '.main-content',
            '.content',
            '.documentation-content',
            '.post-content',
            '[role="main"]',
            '#content',
            '.container'
        ]

        content_element = None
        for selector in content_selectors:
            content_element = soup.select_one(selector)
            if content_element:
                break

        if content_element:
            # If we found a specific content area, use it
            content_text = content_element.get_text(separator=' ', strip=True)
        else:
            # Otherwise, use the body
            body = soup.find('body')
            content_text = body.get_text(separator=' ', strip=True) if body else soup.get_text(separator=' ', strip=True)

        # Clean up the content
        content_text = sanitize_text(content_text)

        # Extract title/section information
        title_element = soup.find('title')
        section_title = title_element.get_text().strip() if title_element else "Unknown Section"

        # Extract heading hierarchy
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        heading_hierarchy = " > ".join([h.get_text().strip() for h in headings[:3]]) if headings else "No Headings"

        return content_text, section_title, heading_hierarchy

    def validate_and_sanitize_url(self, url: str) -> str:
        """
        Validate and sanitize a URL.

        Args:
            url: URL to validate and sanitize

        Returns:
            Sanitized URL string
        """
        if not url:
            raise ValidationError("URL cannot be empty")

        # Basic validation
        if not validate_url(url):
            raise ValidationError(f"Invalid URL format: {url}")

        # Sanitize by parsing and reconstructing
        parsed = urllib.parse.urlparse(url)
        sanitized = urllib.parse.urlunparse(parsed)

        return sanitized

    def get_sitemap_urls(self, base_url: str) -> List[str]:
        """
        Extract all URLs from the sitemap.xml of a given base URL.

        Args:
            base_url: Base URL of the website

        Returns:
            List of URLs found in the sitemap
        """
        sitemap_urls = []

        # First, try to find sitemap at common locations
        sitemap_locations = [
            urllib.parse.urljoin(base_url, 'sitemap.xml'),
            urllib.parse.urljoin(base_url, 'sitemap_index.xml'),
            urllib.parse.urljoin(base_url, 'sitemap/sitemap.xml'),
            urllib.parse.urljoin(base_url, '/sitemap.xml'),
        ]

        for sitemap_url in sitemap_locations:
            try:
                response = self.session.get(sitemap_url, timeout=30)
                response.raise_for_status()

                # Parse the sitemap XML
                root = ET.fromstring(response.content)

                # Handle both regular sitemap and sitemap index
                if root.tag.endswith('sitemapindex'):
                    # This is a sitemap index, need to fetch individual sitemaps
                    for sitemap_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap/{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                        if sitemap_elem is not None:
                            individual_sitemap_url = sitemap_elem.text.strip()
                            sitemap_urls.extend(self._parse_individual_sitemap(individual_sitemap_url))
                else:
                    # This is a regular sitemap
                    sitemap_urls.extend(self._parse_regular_sitemap(response.content))

                logger.info(f"Found {len(sitemap_urls)} URLs in sitemap: {sitemap_url}")
                break  # Exit after finding the first valid sitemap

            except requests.RequestException as e:
                logger.debug(f"Sitemap not found at {sitemap_url}: {str(e)}")
                continue
            except ET.ParseError as e:
                logger.debug(f"Could not parse sitemap at {sitemap_url}: {str(e)}")
                continue

        # If no sitemap was found, try to discover documentation URLs by looking for patterns
        if not sitemap_urls:
            logger.info(f"No sitemap found for {base_url}, trying to discover documentation URLs...")
            discovered_urls = self._discover_documentation_urls(base_url)
            sitemap_urls.extend(discovered_urls)

        return sitemap_urls

    def _discover_documentation_urls(self, base_url: str) -> List[str]:
        """
        Discover documentation URLs by looking for common documentation patterns.

        Args:
            base_url: Base URL of the website

        Returns:
            List of discovered documentation URLs
        """
        discovered_urls = []

        # Common documentation URL patterns
        doc_patterns = [
            'docs/',
            'documentation/',
            'guide/',
            'manual/',
            'tutorials/',
            'api/',
            'reference/',
        ]

        # Check if any of the common documentation paths exist
        for pattern in doc_patterns:
            try:
                docs_url = urllib.parse.urljoin(base_url, pattern)
                response = self.session.get(docs_url, timeout=15)

                if response.status_code == 200:
                    logger.info(f"Found documentation section at: {docs_url}")

                    # Extract links from the documentation page
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Look for links that follow documentation patterns
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        full_url = urllib.parse.urljoin(base_url, href)

                        # Check if URL is a documentation page
                        if any(doc_pattern in full_url for doc_pattern in doc_patterns) and full_url.startswith(base_url):
                            if full_url not in discovered_urls:
                                discovered_urls.append(full_url)
            except requests.RequestException:
                continue

        # Also try to get URLs from the main page that look like documentation
        try:
            response = self.session.get(base_url, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Look for navigation links that might lead to documentation
                for link in soup.find_all(['a', 'nav', 'ul', 'li'], href=True):
                    if hasattr(link, 'attrs') and 'href' in link.attrs:
                        href = link['href']
                        full_url = urllib.parse.urljoin(base_url, href)

                        # Check if URL is a documentation page
                        if any(doc_pattern in full_url for doc_pattern in doc_patterns) and full_url.startswith(base_url):
                            if full_url not in discovered_urls:
                                discovered_urls.append(full_url)
        except requests.RequestException:
            pass

        # Try to find specific documentation patterns like robotics-module-one
        try:
            # Try common documentation structures
            common_doc_paths = [
                'docs/',
                'docs/robotics-module-one/',
                'docs/robotics-module-one/chapter-1/',
                'docs/robotics-module-one/chapter-2/',
                'docs/robotics-module-one/chapter-3/',
                'documentation/',
                'guide/',
                'manual/'
            ]

            for doc_path in common_doc_paths:
                try:
                    doc_url = urllib.parse.urljoin(base_url, doc_path)
                    response = self.session.get(doc_url, timeout=15)
                    if response.status_code == 200:
                        # Parse the page to find links
                        soup = BeautifulSoup(response.content, 'html.parser')
                        for link in soup.find_all('a', href=True):
                            href = link['href']
                            full_url = urllib.parse.urljoin(base_url, href)
                            # Add to discovered URLs if it's within the same domain
                            if full_url.startswith(base_url) and full_url not in discovered_urls:
                                discovered_urls.append(full_url)
                except requests.RequestException:
                    continue
        except Exception as e:
            logger.debug(f"Error discovering specific documentation patterns: {str(e)}")

        logger.info(f"Discovered {len(discovered_urls)} documentation URLs")
        return discovered_urls

    def _parse_regular_sitemap(self, sitemap_content: bytes) -> List[str]:
        """
        Parse a regular sitemap and extract URLs.

        Args:
            sitemap_content: Content of the sitemap.xml file

        Returns:
            List of URLs from the sitemap
        """
        urls = []
        try:
            root = ET.fromstring(sitemap_content)
            for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                if url_elem is not None and url_elem.text:
                    urls.append(url_elem.text.strip())
        except ET.ParseError as e:
            logger.error(f"Error parsing sitemap content: {str(e)}")

        return urls

    def _parse_individual_sitemap(self, sitemap_url: str) -> List[str]:
        """
        Fetch and parse an individual sitemap from a sitemap index.

        Args:
            sitemap_url: URL of the individual sitemap

        Returns:
            List of URLs from the sitemap
        """
        urls = []
        try:
            response = self.session.get(sitemap_url, timeout=30)
            response.raise_for_status()
            urls = self._parse_regular_sitemap(response.content)
        except requests.RequestException as e:
            logger.warning(f"Could not fetch individual sitemap {sitemap_url}: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing individual sitemap {sitemap_url}: {str(e)}")

        return urls

    def get_all_urls(self, base_url: str, include_sitemap: bool = True) -> List[str]:
        """
        Get all URLs to process, optionally including those from sitemap.

        Args:
            base_url: Base URL of the website
            include_sitemap: Whether to include URLs from sitemap.xml

        Returns:
            List of URLs to process
        """
        all_urls = [base_url]  # Always include the base URL

        if include_sitemap:
            sitemap_urls = self.get_sitemap_urls(base_url)
            # Filter out placeholder or invalid URLs
            valid_sitemap_urls = self._filter_valid_urls(sitemap_urls, base_url)
            all_urls.extend(valid_sitemap_urls)

        # Remove duplicates while preserving order
        unique_urls = []
        seen = set()
        for url in all_urls:
            if url not in seen:
                seen.add(url)
                unique_urls.append(url)

        return unique_urls

    def _filter_valid_urls(self, urls: List[str], base_url: str) -> List[str]:
        """
        Filter out placeholder or invalid URLs based on the base URL.

        Args:
            urls: List of URLs to filter
            base_url: Base URL to compare against

        Returns:
            List of valid URLs that belong to the same domain
        """
        import re
        from urllib.parse import urlparse

        # Parse the base URL to get the domain
        base_domain = urlparse(base_url).netloc.lower()

        valid_urls = []
        for url in urls:
            try:
                parsed_url = urlparse(url)
                url_domain = parsed_url.netloc.lower()

                # Only include URLs that are from the same domain or are subdomains
                if url_domain == base_domain or url_domain.endswith('.' + base_domain):
                    # Additional check: filter out common placeholder domains
                    if not any(placeholder in url_domain for placeholder in [
                        'example.com', 'your-docusaurus-site.example.com', 'your-website.com',
                        'example.org', 'test.com', 'placeholder.com'
                    ]):
                        valid_urls.append(url)
                else:
                    logger.info(f"Filtered out URL from different domain: {url}")
            except Exception as e:
                logger.warning(f"Could not parse URL {url}: {str(e)}")
                continue

        return valid_urls

    def crawl_and_extract(self, urls: List[str]) -> List[Tuple[MetadataRecord, List[DocumentChunk]]]:
        """
        Main function to orchestrate the scraping process.

        Args:
            urls: List of URLs to crawl and extract content from

        Returns:
            List of tuples containing (metadata_record, list_of_document_chunks)
        """
        logger.info(f"Starting to crawl {len(urls)} URLs")

        if not urls:
            logger.warning("No URLs provided to crawl")
            return []

        results = self.scrape_urls(urls)
        logger.info(f"Successfully crawled {len(results)} URLs")

        return results

    def close(self):
        """Close the session and clean up resources."""
        if hasattr(self, 'session'):
            self.session.close()