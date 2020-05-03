To run:

\$env:FLASK_APP = "image_scraper.py"
flask run

Todo:

- Fetch in background
  - Send result in real-time over web socket as they're fetched
- Paginate output
  - Create iterable using yield, then limit iterations
- Standardize url vs src
- Fix results being different each time
