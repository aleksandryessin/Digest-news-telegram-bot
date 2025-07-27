def filter_links_by_substring(links, substring, case_sensitive=False, exact_match=False):
    """
    Filter a list of links by a given substring.
    
    Args:
        links (list): List of URLs/links to filter
        substring (str): Substring to search for in the links
        case_sensitive (bool): Whether the search should be case sensitive (default: False)
        exact_match (bool): Whether to match the entire link exactly (default: False)
        
    Returns:
        list: Filtered list of links containing the substring
    """
    if not links or not substring:
        return []
    
    filtered_links = []
    
    # Prepare substring for comparison
    search_string = substring if case_sensitive else substring.lower()
    
    for link in links:
        # Prepare link for comparison
        compare_link = link if case_sensitive else link.lower()
        
        if exact_match:
            if compare_link == search_string:
                filtered_links.append(link)
        else:
            if search_string in compare_link:
                filtered_links.append(link)
    
    return filtered_links


def filter_links_by_multiple_substrings(links, substrings, case_sensitive=False, match_all=False):
    """
    Filter links by multiple substrings.
    
    Args:
        links (list): List of URLs/links to filter
        substrings (list): List of substrings to search for
        case_sensitive (bool): Whether the search should be case sensitive (default: False)
        match_all (bool): If True, link must contain ALL substrings. If False, ANY substring (default: False)
        
    Returns:
        list: Filtered list of links
    """
    if not links or not substrings:
        return []
    
    filtered_links = []
    
    for link in links:
        compare_link = link if case_sensitive else link.lower()
        search_strings = substrings if case_sensitive else [s.lower() for s in substrings]
        
        if match_all:
            # Link must contain ALL substrings
            if all(substring in compare_link for substring in search_strings):
                filtered_links.append(link)
        else:
            # Link must contain ANY substring
            if any(substring in compare_link for substring in search_strings):
                filtered_links.append(link)
    
    return filtered_links


def filter_links_by_domain(links, domain, include=True):
    """
    Filter links by domain.
    
    Args:
        links (list): List of URLs/links to filter
        domain (str): Domain to filter by (e.g., 'techcrunch.com')
        include (bool): If True, include links from this domain. If False, exclude them (default: True)
        
    Returns:
        list: Filtered list of links
    """
    if not links or not domain:
        return []
    
    filtered_links = []
    domain_lower = domain.lower()
    
    for link in links:
        link_lower = link.lower()
        
        # Check if link contains the domain
        has_domain = domain_lower in link_lower
        
        if include and has_domain:
            filtered_links.append(link)
        elif not include and not has_domain:
            filtered_links.append(link)
    
    return filtered_links


# Example usage and demonstrations
if __name__ == "__main__":
    # Sample links for testing
    sample_links = [
        "https://techcrunch.com/2025/01/22/ai-referrals-to-top-websites/",
        "https://techcrunch.com/2025/01/20/ai-companions-threat-love-evolution/",
        "https://techcrunch.com/2025/01/20/google-web-guide-search-experiment/",
        "https://techcrunch.com/2025/01/19/ai-slop-fake-reports-bug-bounty/",
        "https://techcrunch.com/2025/01/18/google-ai-overviews-2b-users/",
        "https://example.com/ai-news",
        "https://wired.com/story/artificial-intelligence-future/",
        "https://techcrunch.com/tag/ai/",
        "https://techcrunch.com/tag/startups/"
    ]
    
    print("=== Filter Links by Substring Demo ===")
    print(f"Total sample links: {len(sample_links)}")
    
    # Filter by 'ai' (case insensitive)
    ai_links = filter_links_by_substring(sample_links, "ai")
    print(f"\nLinks containing 'ai': {len(ai_links)}")
    for link in ai_links:
        print(f"  - {link}")
    
    # Filter by 'Google' (case sensitive)
    google_links = filter_links_by_substring(sample_links, "Google", case_sensitive=True)
    print(f"\nLinks containing 'Google' (case sensitive): {len(google_links)}")
    for link in google_links:
        print(f"  - {link}")
    
    # Filter by multiple substrings
    multi_links = filter_links_by_multiple_substrings(sample_links, ["ai", "google"])
    print(f"\nLinks containing 'ai' OR 'google': {len(multi_links)}")
    for link in multi_links:
        print(f"  - {link}")
    
    # Filter by domain
    tc_links = filter_links_by_domain(sample_links, "techcrunch.com")
    print(f"\nLinks from techcrunch.com: {len(tc_links)}")
    for link in tc_links:
        print(f"  - {link}")
    
    # Exclude domain
    non_tc_links = filter_links_by_domain(sample_links, "techcrunch.com", include=False)
    print(f"\nLinks NOT from techcrunch.com: {len(non_tc_links)}")
    for link in non_tc_links:
        print(f"  - {link}") 