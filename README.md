# GHN_CRAWLER

Crawler made using Scrapy and Splash.

## Installation

Make sure you have a Splash server running in a docker. [Installation steps here!](https://splash.readthedocs.io/en/stable/install.html)


```bash
pip install -r requirements.txt
```

## Usage

Point SPLASH_URL in settings.py to your Splash server.

```bash
scrapy crawl crawler_name
```