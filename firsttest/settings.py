# -*- coding: utf-8 -*-

BOT_NAME = 'firsttest'
SPIDER_MODULES = ['firsttest.spiders']
NEWSPIDER_MODULE = 'firsttest.spiders'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 32

DOWNLOAD_DELAY = 3
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

COOKIES_ENABLED = False

#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,
    'firsttest.middlewares.RotateUserAgentMiddleware':50,
}

ITEM_PIPELINES = {
    # 'firsttest.pipelines.FirsttestPipeline': 300,
    # 'firsttest.pipelines.MyImagesPipeline': 400,
    'firsttest.pipelines.DoubanmoviePipeline':600,
    # 'firsttest.pipelines.MongoDBPipeline':900,
}

AUTOTHROTTLE_MAX_DELAY = 60

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# CRITICAL、 ERROR、WARNING、INFO、DEBUG
LOG_LEVEL = 'INFO'

IMAGES_STORE='C:\新建文件夹'
# IMAGES_EXPIRES = 90     # 过期天数，90天内抓过的不再抓
# IMAGES_MIN_HEIGHT = 110 # 过滤图片大小
# IMAGES_MIN_WIDTH = 110

MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_DBNAME = 'world'
MYSQL_USER = 'dhz'
MYSQL_PASSWD = '666'
MYSQL_CHARSET = 'utf8'   # 编码要加上，否则可能出现中文乱码问题

MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'yun'
MONGODB_COLLECTION = 'coll'