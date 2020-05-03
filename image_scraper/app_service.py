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

from . import constants


def collect_page_media(html, src) -> dict:

    images = scrape_images(html)
    images = list(map(lambda image: urljoin(src, image), images))

    videos = scrape_videos(html)
    videos = list(map(lambda video: urljoin(src, video), videos))

    page_url = src
    page_title = urlparse(src).path
    return {
        "page_url": page_url,
        "page_title": page_title,
        "images": images,
        "videos": videos,
    }


def recursive_scrape(
    url: str, scrape_func: callable, recursion_depth: int = 0
) -> (dict, bool):
    """ Recursive functions that consumes a URL string, 
        and produces a list of image URLs. 
    """
    print("Scraping " + url + "...")

    page = get_page(url)
    if not page:
        yield
    html = BeautifulSoup(page, "html.parser")

    results_from_page = scrape_func(html, url)

    links = get_downstream_links(html, url)

    hit_recursion_limit = recursion_depth >= constants.recursion_depth_limit

    # An incomplete result will have a "show more" link
    # An exception is made for the first page (depth=0)
    more_recursion = hit_recursion_limit and links
    more_spread = len(links) > constants.recursion_spread_limit and recursion_depth
    complete = not more_recursion and not more_spread
    yield (results_from_page, complete)

    if not hit_recursion_limit:

        spread_limit = (
            constants.recursion_spread_limit
            if recursion_depth
            else constants.recursion_spread_limit * 2
        )
        links_to_scrape = islice(links, spread_limit)
        for link in links_to_scrape:
            yield from recursive_scrape(link, scrape_func, recursion_depth + 1)


def get_downstream_links(html, url: str) -> set:
    links = scrape_links(html)
    links = set(map(lambda link: urljoin(url, link), links))

    upstream_links = {link for link in links if link in url}
    links.difference_update(upstream_links)
    return links
