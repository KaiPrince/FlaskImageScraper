"""
* Project Name: FlaskImageScraper
* File Name: scraper.py
* Programmer: Kai Prince
* Date: Sat, May 02, 2020
* Description: This file contains scraper service functions.
"""

from requests import get, post
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import mimetypes
import re


def get_videos(url):
    """ Returns full links to all videos on a page. """
    video_links = set()

    page = get_page(url)
    if not page:
        return video_links
    html = BeautifulSoup(page, "html.parser")

    image_tags = html.find_all(["video", "source"])
    for tag in image_tags:
        if "src" not in tag.attrs:
            continue
        link = urljoin(url, tag["src"])
        if is_url_video(link):
            video_links.add(link)

    link_tags = html.find_all("a")
    for tag in link_tags:
        if "href" not in tag.attrs:
            continue

        href = tag["href"]
        if is_url_video(href):
            video_links.add(urljoin(url, href))

    return video_links


def is_url_video(url):
    mimetype, _encoding = mimetypes.guess_type(url)
    return mimetype and mimetype.startswith("video")


def get_links(url):
    """ Returns a list of all the links on a page. """
    links = set()

    page = get_page(url)
    if not page:
        return links
    html = BeautifulSoup(page, "html.parser")

    anchor_tags = html.find_all("a")
    for tag in anchor_tags:
        if "href" not in tag.attrs:
            continue
        if not tag["href"].endswith("/"):
            continue
        link = urljoin(url, tag["href"])
        links.add(link)

    return links


def get_images(url) -> set:
    """ Returns full links to all images on a page. """
    image_links = set()

    page = get_page(url)
    if not page:
        return image_links
    html = BeautifulSoup(page, "html.parser")

    image_tags = html.find_all("img")
    for tag in image_tags:
        if "src" not in tag.attrs:
            continue
        link = urljoin(url, tag["src"])
        image_links.add(link)

    link_tags = html.find_all("a")
    for tag in link_tags:
        if "href" not in tag.attrs:
            continue

        href = tag["href"]
        if is_url_image(href):
            image_links.add(urljoin(url, href))

    return image_links


def is_url_image(url):
    mimetype, _encoding = mimetypes.guess_type(url)
    return mimetype and mimetype.startswith("image")


def get_page(url):
    """ Make a HTTP GET request to a given url, and return the response. """

    response = simple_get(clean_url(url))

    return response


def clean_url(url):
    parsed_url = urlparse(url, "http")
    if parsed_url.netloc:
        return parsed_url.geturl()
    else:
        return "http://www." + url


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except (RequestException, KeyError) as e:
        log_error("Error during requests to {0} : {1}".format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers["Content-Type"].lower()
    return (
        resp.status_code == 200
        and content_type is not None
        and content_type.find("html") > -1
    )


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)
