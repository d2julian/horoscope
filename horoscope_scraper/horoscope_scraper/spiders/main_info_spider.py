import scrapy
import logging
from .constants import *
from datetime import datetime
class MainInfoSpider(scrapy.Spider):
    name = "main_info_spider"
    custom_settings = {
        'ITEM_PIPELINES': {
            'horoscope_scraper.pipelines.HoroscopeMainScraperPipeline': 1,
        }
    }    
    def start_requests(self):
        base_url = BASE_MAIN_INFO_PATH
        for zodiac in ZODIACS_LIST:
            url = base_url + zodiac + '-personalidad'
            yield scrapy.Request(url=url, callback=self.parse, meta={'zodiac': zodiac, 'url': url})

    def parse(self, response):
        zodiac = response.meta['zodiac']            
        url = response.meta['url']     
        characteristics = response.css('div.characteristics h3') 
        all_characteristics = []
        for c in characteristics:
            text = c.css('::text').getall()
            charac = {
                text[0] : text[1]
            }
            all_characteristics.append(charac)
        paragraphs = response.css('div.span-8.span-s-12 div.content p::text').extract()
        yield {
            'timestamp': datetime.now().isoformat(),
            'url': url,            
            'zodiac': zodiac,
            'personality': paragraphs[0] ,
            'strengths': paragraphs[1] ,
            'weaknesses': paragraphs[2] ,
            'attribute': paragraphs[3] ,
            'likes': paragraphs[4] ,
            'dislikes': paragraphs[5] ,
            'ideal': paragraphs[6],
            'all_characteristics': all_characteristics
        }        
