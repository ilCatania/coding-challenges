# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from sitemap.items import SitemapItem
from urllib.parse import urlparse


class SitemapMakerSpider(scrapy.Spider):
    name = 'sitemap_maker'

    def __init__(self, category=None, *args, **kwargs):
        super(SitemapMakerSpider, self).__init__(*args, **kwargs)
        # restrict allowed domain to that of start_url
        su = kwargs.get('start_url')
        if su:
            self.start_urls = [su]
        self.allowed_domains = [urlparse(u).netloc for u in self.start_urls]

    def parse(self, response):
        links = LinkExtractor(allow_domains=self.allowed_domains)\
            .extract_links(response)
        paths = set(urlparse(l.url).path for l in links)
        yield from (response.follow(p, callback=self.parse) for p in paths)
        yield SitemapItem(path=urlparse(response.url).path, links=paths)
