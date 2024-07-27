import firebase_admin
import os
import logging
from firebase_admin import credentials
from firebase_admin import db
from dotenv import load_dotenv
from scrapy.exceptions import CloseSpider

class HoroscopeScraperPipeline:
    def __init__(self):
        load_dotenv()             
        try:           
            cred = credentials.Certificate(os.getenv('FIREBASE_CERTIFICATE'))
            firebase_admin.initialize_app(cred, {'databaseURL': os.getenv('FIREBASE_URL')})
            self.ref = db.reference(os.getenv('COLLECTION_NAME')) 
        except Exception as e:
            raise CloseSpider(f"Failed to initialize Firebase: {e}")          
    def process_item(self, item, spider):
        self.ref.push(item)
        return item  