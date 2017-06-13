# !/usr/bin/env python
# -*- coding:utf-8 -*-
""""
爬取豆瓣top250电影，图片保存在本地，其它信息保存在mysql和mongodb中
"""
import scrapy
import re
from firsttest.items import DoubanTopMoviesItem

class SpDoubanSpider(scrapy.Spider):
    name = 'doubanmovie'
    allowed_domains = ["douban.com"]
    base_url = "https://movie.douban.com/top250"
    # start_urls = [base_url]

    # 共有10页，格式固定。可替代start_urls 及下面的翻页
    def start_requests(self):
        for i in range(0, 226, 25):
            url = self.base_url + "?start=%d&filter=" % i
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        items = DoubanTopMoviesItem()
        items['title_ch'] = response.xpath('//div[@class="hd"]//span[@class="title"][1]/text()').extract()

        # 替换掉html标签中的空格
        # en_list = response.xpath('//div[@class="hd"]//span[@class="title"][2]/text()').extract()
        # items['title_en'] = [en.replace('\xa0/\xa0','').replace('  ','') for en in en_list]
        # ht_list = response.xpath('//div[@class="hd"]//span[@class="other"]/text()').extract()
        # items['title_ht'] = [ht.replace('\xa0/\xa0','').replace('  ','') for ht in ht_list]
        # detail_list = response.xpath('//div[@class="bd"]/p[1]/text()').extract()
        # print(detail_list)
        # items['detail'] = [detail.replace('  ', '').replace('\xa0', '').replace('\n', '') for detail in detail_list]

        items['rating_num'] = response.xpath('//div[@class="star"]/span[2]/text()').extract()
        # 评价数格式：“XXX人评价”。用正则表达式取出XXX数字
        count_list = response.xpath('//div[@class="star"]/span[4]/text()').extract()
        items['rating_count'] = [re.findall('\d+',count)[0] for count in count_list]
        items['image_urls'] = response.xpath('//div[@class="pic"]/a/img/@src').extract()
        items['topid'] = response.xpath('//div[@class="pic"]/em/text()').extract()
        # 注意：有的电影没有quote！！！！！！！！！！
        # items['quote'] = response.xpath('//span[@class="inq"]/text()').extract()
        # print(len(items['topid']))
        # print(len(items['title_ch']))
        # print(len(items['rating_num']))
        # print(len(items['image_urls']))
        # print(len(items['rating_count']))
        # print(items['topid'])
        # print(items['title_ch'])
        # print(items['rating_num'])
        # print(items['image_urls'])
        # print(items['rating_count'])
        yield items

        # 后页，继续爬取
        new_url = response.xpath('//link[@rel="next"]/@href').extract_first()
        if new_url:
            next_url = self.base_url+new_url
            yield scrapy.Request(next_url, callback=self.parse)
