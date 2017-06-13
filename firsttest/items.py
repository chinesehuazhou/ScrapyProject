# -*- coding: utf-8 -*-

import scrapy

class FirsttestItem(scrapy.Item):
    image_urls = scrapy.Field()


class DoubanTopMoviesItem(scrapy.Item):
    title_ch = scrapy.Field()
    # 本想按title-title-other 取出3个名字，但有的只有title-other，例如霸王别姬。所以只取一个名字
    # title_en = scrapy.Field()
    # title_ht = scrapy.Field()
    # detail = scrapy.Field()
    rating_num = scrapy.Field()
    rating_count = scrapy.Field()
    # quote = scrapy.Field()
    image_urls = scrapy.Field()
    topid = scrapy.Field()


class StackItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()