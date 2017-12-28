Site map grap generator
=======================

Crawls a website and produces a network graph of its links.

# Configuration

This project requires python version 3.5 or greater. To start, `cd` into
the project directory. Optionally enable `venv`:

```bash
python3 -m venv venv
source venv/bin/activate
```

Make sure you have all the required packages:

```bash
pip install -r requirements.txt
```

# Running

Run the crawler with the following command, replacing the example domain with
yours:

```bash
scrapy crawl -a start_url=https://example.com sitemap_maker
```

If the crawler completes successfully, a network graph should open in your browser.
