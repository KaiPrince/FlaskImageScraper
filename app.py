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
from flask_socketio import SocketIO, emit
from image_scraper.sockets import scrape_and_emit

app = Flask(__name__)
socketio = SocketIO(app)

app.add_url_rule("/", view_func=views.request_form, methods=["GET", "POST"])
app.add_url_rule(
    "/scrape/<path:source>", view_func=views.results, methods=["GET", "POST"]
)


@socketio.on("connect")
def socket_connected():
    print("connected!")


@socketio.on("start_scrape")
def start_scrape(url):
    if url:
        scrape_and_emit(url)


if __name__ == "__main__":
    socketio.run(app, debug=True)
