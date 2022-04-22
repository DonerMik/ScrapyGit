# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo

from logging import log
from . import settings
from scrapy.exceptions import DropItem

import pymongo
from itemadapter import ItemAdapter


import pymongo



from  . import settings

from scrapy.exceptions import DropItem



class MongoDBPipeline(object):

    def __init__(self):
        self.connection = pymongo.MongoClient(
            'localhost',
            27017,
        )
        db = self.connection['ScrapyGit']
        self.collection = db['repositories']

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item
