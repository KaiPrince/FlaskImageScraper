"""
* Project Name: FlaskImageScraper
* File Name: app_service.py
* Programmer: Kai Prince
* Date: Sun, May 03, 2020
* Description: This file contains service functions for the image_scraper app.
"""

import mimetypes
import re
from contextlib import closing
from itertools import islice
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from requests import get, post
from requests.exceptions import RequestException

from utils.scraper import (
    clean_url,
    scrape_images,
    scrape_links,
    scrape_videos,
    get_page,
)

from .constants import recursion_depth_limit, recursion_spread_limit


def collect_page_media(html, src):

    if not html:
        return None

    images = scrape_images(html)
    images = list(map(lambda image: urljoin(src, image), images))

    videos = scrape_videos(html)
    videos = list(map(lambda video: urljoin(src, video), videos))

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


def recursive_scrape(
    url: str, scrape_func: callable, recursion_depth: int = 0
) -> (list, bool):
    """ Recursive functions that consumes a URL string, 
        and produces a list of image URLs. 
    """
    print("Scraping " + url + "...")
    scrape_results = []

    page = get_page(url)
    if not page:
        return scrape_results
    html = BeautifulSoup(page, "html.parser")

    results_from_page = scrape_func(html, url)

    links = get_downstream_links(html, url)

    complete = not links and len(links) <= recursion_spread_limit
    scrape_results.append((results_from_page, complete))

    if recursion_depth < recursion_depth_limit:

        links_to_scrape = islice(links, recursion_spread_limit)
        for link in links_to_scrape:
            descendant_results = recursive_scrape(
                link, scrape_func, recursion_depth + 1
            )
            scrape_results.extend(descendant_results)

    return scrape_results


def get_downstream_links(html, url: str) -> set:
    links = scrape_links(html)
    links = set(map(lambda link: urljoin(url, link), links))

    upstream_links = {link for link in links if link in url}
    links.difference_update(upstream_links)
    return links
