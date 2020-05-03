"""
* Project Name: FlaskImageScraper
* File Name: app_service.py
* Programmer: Kai Prince
* Date: Sun, May 03, 2020
* Description: This file contains service functions for the image_scraper app.
"""

from itertools import islice

from constants import recursion_depth_limit, recursion_spread_limit
from service import clean_url, get_images, get_links, get_videos
from urllib.parse import urljoin, urlparse


def collect_page_media(src):
    images = get_images(src)
    videos = get_videos(src)

    if images or videos:
        page_url = src
        page_title = urlparse(src).path
        return {
            "page_url": page_url,
            "page_title": page_title,
            "images": images,
            "videos": videos,
        }
    else:
        return None


def recursive_scrape(url: str, scrape_func: callable, recursion_depth: int = 0):
    """ Recursive functions that consumes a URL string, 
        and produces a set of image URLs. 
    """
    print("Scraping " + url + "...")
    scrape_results = []
    results_from_page = scrape_func(url)
    scrape_results.append(results_from_page)

    if recursion_depth >= recursion_depth_limit:
        return scrape_results

    links = get_links(url)
    upstream_links = {link for link in links if link in url}
    links.difference_update(upstream_links)
    for link in islice(links, recursion_spread_limit):
        descendant_images = recursive_scrape(link, scrape_func, recursion_depth + 1)
        scrape_results.extend(descendant_images)

    return scrape_results
