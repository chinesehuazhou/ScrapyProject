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
    start_urls = [base_url]

    # 共有10页，格式固定。重写start_requests方法，等价于tart_urls及翻页
    # def start_requests(self):
    #     for i in range(0, 226, 25):
    #         url = self.base_url + "?start=%d&filter=" % i
    #         yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        item = DoubanTopMoviesItem()
        item['title_ch'] = response.xpath('//div[@class="hd"]//span[@class="title"][1]/text()').extract()

        # 本想按title-title-other 取出3个名字，但有的只有title-other，例如霸王别姬。所以只取一个名字
        # en_list = response.xpath('//div[@class="hd"]//span[@class="title"][2]/text()').extract()
        # item['title_en'] = [en.replace('\xa0/\xa0','').replace('  ','') for en in en_list]
        # ht_list = response.xpath('//div[@class="hd"]//span[@class="other"]/text()').extract()
        # item['title_ht'] = [ht.replace('\xa0/\xa0','').replace('  ','') for ht in ht_list]
        # detail_list = response.xpath('//div[@class="bd"]/p[1]/text()').extract()
        # item['detail'] = [detail.replace('  ', '').replace('\xa0', '').replace('\n', '') for detail in detail_list]
        # 注意：有的电影没有quote！！！！！！！！！！
        # item['quote'] = response.xpath('//span[@class="inq"]/text()').extract()

        item['rating_num'] = response.xpath('//div[@class="star"]/span[2]/text()').extract()
        # 评价数格式：“XXX人评价”。用正则表达式只需取出XXX数字
        count_list = response.xpath('//div[@class="star"]/span[4]/text()').extract()
        item['rating_count'] = [re.findall('\d+',count)[0] for count in count_list]
        item['image_urls'] = response.xpath('//div[@class="pic"]/a/img/@src').extract()
        item['topid'] = response.xpath('//div[@class="pic"]/em/text()').extract()

        yield item

        # 取下一页链接，继续爬取
        # new_url = response.xpath('//link[@rel="next"]/@href').extract_first()
        # if new_url:
        #     next_url = self.base_url+new_url
        #     yield scrapy.Request(next_url, callback=self.parse)


######-------初始start_urls加LinkExtractor 链接提取器方法--------#####
    # from scrapy.spiders import CrawlSpider, Rule
    # from scrapy.linkextractors import LinkExtractor
    # class SpDoubanSpider(CrawlSpider):
        # 略
    # 引入链接提取器，等价于注释前的翻页
    # rules = [Rule(LinkExtractor(allow=(r'https://movie.douban.com/top250\?start=\d+.*')),
    #                callback='parse_item', follow=True)
    #           ]
    # def parse_item(self, response):
    #     # item 解析部分，略
    #     yield item
######-------初始start_urls加LinkExtractor 链接提取器方法--------#####
