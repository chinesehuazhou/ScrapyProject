# !/usr/bin/env python
# -*- coding:utf-8 -*-
""""
学习教程：http://www.jianshu.com/p/d08a6d1e0204
爬取煎蛋网妹子图
"""
import scrapy
from firsttest.items import FirsttestItem
from scrapy.crawler import CrawlerProcess


class firsttest(scrapy.Spider):
    name = 'testf'
    allowed_domains = []
    start_urls = ["http://jandan.net/ooxx"]

    def parse(self, response):
        item = FirsttestItem()
        item['image_urls'] = response.xpath('//p//img//@src').extract()  # 提取图片链接
        # print('图片链接池：',item['image_urls'])
        yield item
        new_url = response.xpath('//a[@class="previous-comment-page"]//@href').extract_first()  # 翻页
        # print('下一页链接：',new_url)
        if new_url:
            yield scrapy.Request(new_url, callback=self.parse)