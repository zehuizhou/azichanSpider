# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import pymysql
import pymongo
from azichan.settings import mongo_host,mongo_port,mongo_db_name,mongo_db_collection

class AzichanPipeline(object):
    def __init__(self):
        # self.conn = pymysql.connect(host='116.62.138.41', user='ceshi', passwd='ckXo09alG"jF', db='azichan', charset='utf8')
        # self.cursor = self.conn.cursor()
        host = mongo_host
        port = mongo_port
        dbname = mongo_db_name
        sheetname = mongo_db_collection
        client = pymongo.MongoClient(host=host, port=port)
        mydb = client[dbname]
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        # id = item['id']
        # title = item['title']
        # date = item['date']
        # transferor = item['transferor']
        # transferee = item['transferee']
        # assets = item['assets']
        # detailUrl = item['detailUrl']
        #
        # debetNumber = item['debetNumber']
        # debetIntroduction = item['debetIntroduction']
        # sql ="insert into dealdata(id,title,date,transferor,transferee,assets,detailUrl,debetNumber,debetIntroduction)\
        #  VALUES(%s,'%s','%s','%s','%s','%s','%s',%s,'%s')"%\
        #      (id, title, date, transferor, transferee, assets, detailUrl, debetNumber, debetIntroduction)
        # self.cursor.execute(sql)
        # self.conn.commit()
        data = dict(item)
        self.post.insert(data)

        return item

    def close_spider(self, spider):
        self.conn.close()
