# -*- coding: utf-8 -*-

import scrapy

class DoubanTopMoviesItem(scrapy.Item):
    title_ch = scrapy.Field()     # 中文标题
    # title_en = scrapy.Field()   # 外文名字
    # title_ht = scrapy.Field()   # 港台名字
    # detail = scrapy.Field()     # 导演主演等信息
    rating_num = scrapy.Field()   # 分值
    rating_count = scrapy.Field() # 评论人数
    # quote = scrapy.Field()      # 短评
    image_urls = scrapy.Field()   # 封面图片地址
    topid = scrapy.Field()        # 排名序号
    # image_paths = scrapy.Field() # 图片保存地址
