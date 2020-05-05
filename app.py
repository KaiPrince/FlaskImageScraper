"""
* Project Name: FlaskImageScraper
* File Name: app.py
* Programmer: Kai Prince
* Date: Sun, May 03, 2020
* Description: This file contains the main entry point for the app.
"""

import gunicorn
from flask import Flask, request
from image_scraper import views
from flask_socketio import SocketIO, emit
from image_scraper.sockets import scrape_and_emit

from threading import Lock, Thread, Event

app = Flask(__name__)
socketio = SocketIO(app)

app.add_url_rule("/", view_func=views.request_form, methods=["GET", "POST"])
app.add_url_rule(
    "/scrape/<path:source>", view_func=views.results, methods=["GET", "POST"]
)


# Controls background task
scrape_tasks = {}


@socketio.on("connect")
def socket_connected():
    print("connected!", request.sid)
    scrape_tasks[request.sid] = {"thread": None, "lock": Lock(), "stop": Event()}


@socketio.on("start_scrape")
def start_scrape(url):
    if not url:
        return

    this_task = scrape_tasks[request.sid]
    with this_task["lock"]:
        print("starting thread")
        this_task["thread"] = socketio.start_background_task(
            scrape_and_emit(url, this_task["stop"])
        )


@socketio.on("disconnect")
def stop_scrape():
    print("disconnected", request.sid)
    this_task = scrape_tasks[request.sid]

    this_task["stop"].set()
    with this_task["lock"]:
        if this_task["thread"]:
            this_task["thread"].join()


if __name__ == "__main__":
    socketio.run(app, debug=True)
