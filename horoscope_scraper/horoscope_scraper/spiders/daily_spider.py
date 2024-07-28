import scrapy
import logging
from .constants import *
from datetime import datetime
class DailySpider(scrapy.Spider):
    name = "daily_spider"
    custom_settings = {
        'ITEM_PIPELINES': {
            'horoscope_scraper.pipelines.HoroscopeDailyScraperPipeline': 1,
        }
    }
    def start_requests(self):
        base_url = BASE_PATH
        for zodiac in ZODIACS_LIST:
            url = base_url + zodiac
            yield scrapy.Request(url=url, callback=self.parse, meta={'zodiac': zodiac, 'url': url})

    def parse(self, response):
        zodiac = response.meta['zodiac']  
        url = response.meta['url']
        paragraphs = response.css('div.horoscope-box.zigzag-box p::text').extract()
        daily_horoscope = paragraphs[0]  

        zodiac_compatibility_elements = []    
        ul_zodiac_compatibility_elements = response.css('div.span-4.span-s-6 div.module-matches ul.list-unstyled.list-inline')
        for ul in ul_zodiac_compatibility_elements:
            element = ul.css('li:nth-of-type(1) h4::text').get()
            zodiac_compatible = ul.css('li:nth-of-type(2) a::text').get()
            zodiac_compatibility_element = {
                   'element': element,
                   'zodiac_compatible': zodiac_compatible,
             }              
            zodiac_compatibility_elements.append(zodiac_compatibility_element)               
        
        lucky_elements = []        
        ul_luck_elements = response.css('div.span-4.span-s-12 div.module-star-ratings ul.list-unstyled.list-inline')        
        for ul in ul_luck_elements:
            element = ul.css('li:nth-of-type(1) h4::text').get()          
            if element:
               number_fill_hearts =  ul.css('li:nth-of-type(2) i.icon-filled-star.highlight')   
               total_stars_filled = len(number_fill_hearts);
               total_stars_empty = 5 - len(number_fill_hearts);
               lucky_element = {
                   'lucky_element': element,
                   'total_stars_filled': total_stars_filled,
                   'total_stars_empty': total_stars_empty
               }              
               lucky_elements.append(lucky_element)   
            
        yield {
            'timestamp': datetime.now().isoformat(),
            'url': url,            
            'zodiac': zodiac,
            'horoscope': daily_horoscope,
            'zodiac_compatibility_elements': zodiac_compatibility_elements,
            'lucky_elements': lucky_elements,
        }
