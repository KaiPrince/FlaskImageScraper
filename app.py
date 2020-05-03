"""
* Project Name: FlaskImageScraper
* File Name: app.py
* Programmer: Kai Prince
* Date: Sun, May 03, 2020
* Description: This file contains the main entry point for the app.
"""


from flask import Flask
import gunicorn
import image_scraper

app = Flask(__name__)
