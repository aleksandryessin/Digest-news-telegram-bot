import re

def extract_links(html_content):
    """
    Extract all links from HTML content using regex.
    
    Args:
        html_content (str): HTML content as string
        
    Returns:
        list: List of URLs found in the HTML
    """
    # Pattern to match href attributes in anchor tags
    pattern = r'<a[^>]*\s+href\s*=\s*["\']([^"\']+)["\'][^>]*>'
    links = re.findall(pattern, html_content, re.IGNORECASE)
    return links

# Example usage
if __name__ == "__main__":
    # Example with HTML string
    html = """
    <html>
        <body>
            <a href="https://example.com">Example</a>
            <a href="/relative/path">Relative Link</a>
            <a href="mailto:test@example.com">Email</a>
        </body>
    </html>
    """
    
    links = extract_links(html)
    print("Extracted links:", links) 