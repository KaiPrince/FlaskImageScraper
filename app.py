"""
* Project Name: FlaskImageScraper
* File Name: app.py
* Programmer: Kai Prince
* Date: Sun, May 03, 2020
* Description: This file contains the main entry point for the app.
"""

import gunicorn
from flask import Flask
from image_scraper import views

app = Flask(__name__)
app.add_url_rule("/", view_func=views.request_form, methods=["GET", "POST"])
app.add_url_rule(
    "/scrape/<path:source>", view_func=views.results, methods=["GET", "POST"]
)
