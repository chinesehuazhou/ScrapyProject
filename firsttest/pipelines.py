# -*- coding: utf-8 -*-

import os
import urllib.request
from twisted.enterprise import adbapi
from pymongo import MongoClient
import MySQLdb.cursors

from firsttest import settings
from firsttest.items import DoubanTopMoviesItem

# 自定义方法下载图片
class FirsttestPipeline(object):
    # 电影封面命名：序号加电影名
    def _createmovieImageName(self, item):
        lengh = len(item['topid'])
        return [item['topid'][i] + "-" + item['title_ch'][i] + ".jpg" for i in range(lengh)]

    # 另一种命名法，取图片链接中名字
    # def _createImagenameByURL(self, image_url):
    #     file_name = image_url.split('/')[-1]
    #     return file_name

    def process_item(self, item, spider):
        namelist = self._createmovieImageName(item)
        dir_path = '%s/%s' % (settings.IMAGES_STORE, spider.name)
        # print('dir_path', dir_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        for i in range(len(namelist)):
            image_url = item['image_urls'][i]
            file_name = namelist[i]
            file_path = '%s/%s' % (dir_path, file_name)
            if os.path.exists(file_path):
                print("重复，跳过：" + image_url)
                continue
            with open(file_path, 'wb') as file_writer:
                print("正在下载："+image_url)
                conn = urllib.request.urlopen(image_url)
                file_writer.write(conn.read())
            file_writer.close()
        return item

# 保存内容至MYSQL数据库
class DoubanmoviePipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset=settings['MYSQL_CHARSET'],
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数
        return cls(dbpool)

    # pipeline默认调用
    def process_item(self, item, spider):
        # 调用插入的方法
        query=self.dbpool.runInteraction(self._conditional_insert,item)
        # 调用异常处理方法
        query.addErrback(self._handle_error,item,spider)
        return item

    def _conditional_insert(self, tx, item):
        sql = "insert into doubantopmovie(topid,title_ch,rating_num,rating_count) values(%s,%s,%s,%s)"
        lengh = len(item['topid'])
        for i in range(lengh):
            params = (item["topid"][i], item["title_ch"][i], item["rating_num"][i], item["rating_count"][i])
            tx.execute(sql, params)

    def _handle_error(self, e):
        print(e)


# 保存内容至MONGODB数据库
class MongoDBPipeline( object):
    mongo_uri_no_auth = 'mongodb://localhost:27017/' # 没有账号密码验证
    database_name = 'yun'
    table_name = 'coll'
    client = MongoClient(mongo_uri_no_auth)  # 创建了与mongodb的连接
    db = client[database_name]
    table = db[table_name]  # 获取数据库中表的游标

    def process_item(self, item, spider):
        valid = True
        for data in item:
          if not data:
              valid = False
              raise DropItem("Missing {0}!".format(data))
        if valid:
              self.table.insert(dict(item))
        return item


from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem

# 用Scrapy内置的ImagesPipeline类下载图片
class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_name = request.url.split('/')[-1]
        return 'doubanmovie2/%s' % (image_name)

    # 从item获取url，返回request对象给pipeline处理
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    # pipeline处理request对象，完成下载后，将results传给item_completed
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        # print(image_paths)
        if not image_paths:
            raise DropItem("Item contains no images")
        # item['image_paths'] = image_paths
        return item