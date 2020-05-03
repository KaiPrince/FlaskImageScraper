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
from image_scraper.app_service import recursive_scrape

from threading import Event


def scrape_and_emit(src: str, stop_flag: Event = None):

    for page, complete in recursive_scrape(src, collect_page_media):
        response = render_template(
            "components/media_page.html", page=page, complete=complete
        )
        emit("page", {"data": response})

        if stop_flag and stop_flag.isSet():
            print("stopping")
            return

    emit("scrape-complete")
