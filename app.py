"""
* Project Name: FlaskImageScraper
* File Name: app.py
* Programmer: Kai Prince
* Date: Sun, May 03, 2020
* Description: This file contains the main entry point for the app.
"""


from itertools import islice

import gunicorn
from flask import Flask, redirect, render_template, request, url_for
from app_service import collect_page_media, recursive_scrape
from constants import recursion_depth_limit, recursion_spread_limit
from service import clean_url, get_images, get_links, get_videos

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
