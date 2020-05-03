"""
* Project Name: FlaskImageScraper
* File Name: sockets.py
* Programmer: Kai Prince
* Date: Sun, May 03, 2020
* Description: This file contains functions for the websocket.
"""

from flask import render_template
from flask_socketio import emit
from image_scraper.app_service import collect_page_media


def collect_and_emit(html, src):
    collected_media = collect_page_media(html, src)
    response = render_template("components/media_page.html", page=collected_media)
    emit("page", {"data": response})
    return collected_media
