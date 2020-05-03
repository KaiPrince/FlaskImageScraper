"""
* Project Name: FlaskImageScraper
* File Name: image_scraper.py
* Programmer: Kai Prince
* Date: Sat, May 02, 2020
* Description: This file contains a webscaper that gathers images and presents
*  them in a paginated display.
"""

from flask import Flask, render_template, request, redirect, url_for
from constants import recursion_depth_limit, recursion_spread_limit
from service import get_images, get_links, clean_url
from itertools import islice

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def request_form():
    if request.method == "POST":
        scrape_url = request.form["url"]
        return redirect(url_for("results", source=scrape_url))

    return render_template("index.html")


@app.route("/scrape/<path:source>", methods=["GET", "POST"])
def results(source):

    images = set()
    images.update(recursive_scrape(clean_url(source)))

    return render_template("results.html", source=source, images=images)


def recursive_scrape(url, recursion_depth=0):
    """ Recursive functions that consumes a URL string, 
        and produces a set of image URLs. 
    """
    print("Scraping " + url + "...")
    images = set()
    images_from_page = get_images(url)
    images.update(images_from_page)

    if recursion_depth >= recursion_depth_limit:
        return images

    links = get_links(url)
    for link in islice(links, recursion_spread_limit):
        descendant_images = recursive_scrape(link, recursion_depth + 1)
        images.update(descendant_images)

    return images
