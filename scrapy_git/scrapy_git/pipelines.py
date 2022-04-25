import pymongo


class MongoDBPipeline:
    def process_item(self, item, spider):
        self.connection = pymongo.MongoClient(
            'localhost',
            27017,
        )
        db = self.connection['ScrapyGit']
        self.collection = db['repositories']
        self.collection.insert_one(dict(item))
        return item
