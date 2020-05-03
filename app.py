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

from threading import Lock, Thread, Event

app = Flask(__name__)
socketistop_flagadd_url_rule("/", view_func=views.request_form, methods=["GET", "POST"])
app.add_url_rule(
    "/scrape/<path:source>", view_func=views.results, methods=["GET", "POST"]
)


# Controls background task
scrape_thread: Thread = None
scrape_thread_lock = Lock()
sstop_flagd_stop = Event()


@socketio.on("connect")
def socket_connected():
    print("connected!")
    scrape_thread_stop.clear()


@socketio.on("start_scrape")
def start_scrape(url):
    if not url:
        return

    global scrape_thread
    with scrape_thread_lock:
        print("starting thread")
        scrape_thread = socketio.start_background_task(
            scrape_and_emit(url, scrape_thread_stop)
        )


@socketio.on("disconnect")
def stop_scrape():
    print("disconnected")
    scrape_thread_stop.set()
    scrape_thread.join()


if __name__ == "__main__":
    socketio.run(app, debug=True)
