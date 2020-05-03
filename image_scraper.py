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
from service import get_images, get_links, clean_url, get_videos
from itertools import islice
from app_service import recursive_scrape, collect_page_media

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def request_form():
    if request.method == "POST":
        scrape_url = request.form["url"]
        return redirect(url_for("results", source=scrape_url))

    return render_template("index.html")


@app.route("/scrape/<path:source>", methods=["GET", "POST"])
def results(source):
    url = clean_url(source)

    collected_media = recursive_scrape(url, collect_page_media)

    return render_template(
        "results.html", source=source, collected_media=collected_media
    )
