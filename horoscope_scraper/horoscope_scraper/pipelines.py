import firebase_admin
import os
import logging
from firebase_admin import credentials
from firebase_admin import db
from dotenv import load_dotenv
from scrapy.exceptions import CloseSpider

def initialize_database(collection_name):
    load_dotenv()             
    print(f"collection_name: {collection_name}")
    try:           
        cred = credentials.Certificate(os.getenv('FIREBASE_CERTIFICATE'))
        firebase_admin.initialize_app(cred, {'databaseURL': os.getenv('FIREBASE_URL')})
        return db.reference(collection_name) 
    except Exception as e:
        raise CloseSpider(f"Failed to initialize Firebase: {e}")

class HoroscopeDailyScraperPipeline:
    def __init__(self):
        load_dotenv()   
        self.ref = initialize_database(os.getenv('COLLECTION_NAME_DAILY'))       
    def process_item(self, item, spider):
        self.ref.push(item)
        return item  
    
class HoroscopeMainScraperPipeline:
    def __init__(self):
        load_dotenv()   
        self.ref = initialize_database(os.getenv('COLLECTION_NAME_MAIN'))                  
    def process_item(self, item, spider):
        self.ref.push(item)
        return item      
    