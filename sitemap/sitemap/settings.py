# -*- coding: utf-8 -*-

# Scrapy settings for sitemap project
BOT_NAME = 'sitemap'

SPIDER_MODULES = ['sitemap.spiders']
NEWSPIDER_MODULE = 'sitemap.spiders'

FEED_EXPORTERS = {
    'networkx-graph': 'sitemap.exporters.NetworkGraphExporter'
}

FEED_FORMAT="networkx-graph"
FEED_URI="file:///tmp/sitemap.html"

ROBOTSTXT_OBEY = True

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
