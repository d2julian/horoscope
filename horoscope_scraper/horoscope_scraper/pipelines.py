from itemadapter import ItemAdapter
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import logging

class HoroscopeScraperPipeline:
    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item        

    def open_spider(self, spider):
        load_dotenv()        
        uri = os.getenv('MONGODB_URI')
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client[os.getenv('DB_NAME')] 
        self.collection = self.db[os.getenv('COLLECTION_NAME')] 
        try:
            self.client.admin.command('ping')
        except Exception as e:
             logging.error(f'Mongo error: {e}')
             
    def close_spider(self, spider):  
        self.client.close()        