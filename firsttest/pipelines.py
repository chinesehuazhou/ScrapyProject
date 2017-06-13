# -*- coding: utf-8 -*-

import os
import urllib.request
from twisted.enterprise import adbapi
from pymongo import MongoClient
import MySQLdb.cursors

from firsttest import settings
from firsttest.items import DoubanTopMoviesItem

class FirsttestPipeline(object):
    def _createmovieImageName(self, items):
        namelist = []
        lengh = len(items['topid'])
        for i in range(lengh):
            namelist.append(items['topid'][i] + "-" + items['title_ch'][i] + ".jpg")
        return namelist

    def _createImagenameByURL(self, image_url):
        list_name = image_url.split('/')
        file_name = list_name[len(list_name) - 1]
        return file_name

    def process_item(self, item, spider):
        namelist = self._createmovieImageName(item)
        # print(namelist)
        dir_path = '%s/%s' % (settings.IMAGES_STORE, spider.name)  # 存储路径
        # print('dir_path', dir_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        for i in range(len(namelist)):
            image_url = item['image_urls'][i]
            file_name = namelist[i]
            # print(image_url)
            file_path = '%s/%s' % (dir_path, file_name)
            if os.path.exists(file_name):
                continue
            with open(file_path, 'wb') as file_writer:
                print("正在下载："+image_url)
                conn = urllib.request.urlopen(image_url)  # 下载图片
                file_writer.write(conn.read())
            file_writer.close()
        return item

class DoubanmoviePipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。返回数据库连接池dbpool
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
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
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy...
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

    # pipeline默认调用
    def process_item(self, item, spider):
        query=self.dbpool.runInteraction(self._conditional_insert,item)#调用插入的方法
        query.addErrback(self._handle_error,item,spider)#调用异常处理方法
        return item

    def _conditional_insert(self, tx, item):
        sql = "insert into doubantopmovie(topid,title_ch,rating_num,rating_count) values(%s,%s,%s,%s)"
        lengh = len(item['topid'])
        for i in range(lengh):
            params = (item["topid"][i], item["title_ch"][i], item["rating_num"][i], item["rating_count"][i])
            tx.execute(sql, params)

    def _handle_error(self, e):
        print(e)


class MongoDBPipeline( object):
    # client = MongoClient('localhost',27017)
    mongo_uri_no_auth = 'mongodb://localhost:27017/'  # mongo没有账号密码验证的时候用这个
    database_name = 'yun'
    table_name = 'coll'  # 你要查询的表名，请自行替换你需要的表名
    client = MongoClient(mongo_uri_no_auth)  # 创建了与mongodb的连接
    db = client[database_name]
    table = db[table_name]  # 获取数据库中表的游标

    def process_item(self, item, spider):
        valid = True
        # print(item)
        for data in item:
          if not data:
              valid = False
              raise DropItem("Missing {0}!".format(data))
        if valid:
              self.table.insert(dict(item))
        return item