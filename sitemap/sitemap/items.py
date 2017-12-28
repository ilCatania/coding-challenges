from scrapy import Item, Field


class SitemapItem(Item):
    path = Field()
    links = Field()
