"""
* Project Name: FlaskImageScraper
* File Name: image_scraper.py
* Programmer: Kai Prince
* Date: Sat, May 02, 2020
* Description: This file contains a webscaper that gathers images and presents
*  them in a paginated display.
"""

from flask import redirect, render_template, request, url_for
from image_scraper.app_service import collect_page_media, recursive_scrape
from utils.scraper import clean_url, get_images, get_links, get_videos


def request_form():
    if request.method == "POST":
        scrape_url = request.form["url"]
        return redirect(url_for("results", source=scrape_url))

    return render_template("index.html")


def results(source):
    url = clean_url(source)

    collected_media = recursive_scrape(url, collect_page_media)

    return render_template(
        "results.html", source=source, collected_media=collected_media
    )
