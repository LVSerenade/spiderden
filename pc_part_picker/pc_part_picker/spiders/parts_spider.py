import scrapy
import re
from bs4 import BeautifulSoup

def get_data(soup):
    spec_value = soup.find("ul")
    
    if spec_value != None:
        spec_value = spec_value.text.replace('\n',' ').strip().lower()
    else:
        spec_value = soup.find("p")
        if spec_value != None:
            spec_value = spec_value.text.strip().lower()

    return spec_value

class AllPartSpider(scrapy.Spider):
    # Here we overide the default behavior
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI' : 'all_parts.json'
    }

    name = "parts"
    base_url = 'https://pcpartpicker.com'
    
    # This slug is what will trigger the fetching of the data
    magic_slug = "fetch/?page=%d&xslug=&location=&search=&qid=1&scr=1&scr_vw=1263&scr_vh=319&scr_dw=1280&scr_dh=720&scr_daw=1280&scr_dah=680&scr_ddw=1263&scr_ddh=5806&ms=1578965341903"


    start_urls = [
        base_url + "/products/"
    ]

    link_regex = "product.*\w{1}"
    page_regex = 'page=[0-9]*'

    def parse(self, response):
        
        # Get all links in the page
        all_part_type_links = response.css('.wrapper__pageContent a::attr(href)').getall()
        

        max_num_page = -1
        for link in all_part_type_links:
            part_type = link.split('/')[2]
            part_type_url = self.base_url + link + self.magic_slug
            yield scrapy.Request(part_type_url, callback=self.parse_part_type, cb_kwargs=dict(part_type=part_type))

    def parse_part_type(self, response, part_type):
        
        # Get all links in the page
        all_links = response.css("a::attr(href)").getall()

        max_num_page = -1
        for link in all_links:
            
            # Check if it is a next page link            
            page_search = re.compile(self.page_regex)
            result = page_search.findall(link)
            if result != []:
                num_page = int(result[0].split('=')[-1])
                if(num_page > max_num_page):
                    max_num_page = num_page

        # Iterate over all the pages for this product
        for i in range(1,max_num_page+1):
            page_url = response.url % (i)
            print(page_url)
            yield scrapy.Request(page_url, callback=self.parse_page, cb_kwargs=dict(part_type=part_type))
        

    def parse_page(self, response, part_type):
        # Get all links in the page
        all_links = response.css("a::attr(href)").getall()
        for link in all_links:
            
            # Check if it is a content link
            link_search = re.compile(self.link_regex)
            result = link_search.findall(link)
            if result != []:
            
                product_url = self.base_url + '/' + result[0]
                yield scrapy.Request(product_url, callback=self.parse_part, cb_kwargs=dict(part_type=part_type))
    
    def parse_part(self, response, part_type):
        # Default of scraped info (nothing in it)
        scraped_info = {
        }

        specs_list = []
        specs = response.css("div.specs").getall()
        if len(specs) > 0:
            all_specs = specs[0]
            soup = BeautifulSoup(all_specs, 'html.parser')
            specs_list = soup.find_all("div", {"class": "group group--spec"})
        else:
            return {}

        scraped_info['part_type'] = part_type
        
        # Gather the specification for this part
        for spec in specs_list:
            soup = BeautifulSoup(str(spec), 'html.parser')

            # Get the type and the value (h3 and p respectively)
            spec_type = soup.find("h3").text.lower()
            spec_value = get_data(soup)

            # Assign it at the right spot in the dictionary
            scraped_info[spec_type] = spec_value

        # Gather the prices for this part
        prices = response.css('.td__finalPrice a::text')
        if prices != None:
            scraped_info['prices'] = prices.getall()
        
        # Rating for this part
        raw_rating = response.css('.wrapper__pageTitle--rating section::text').extract()
        ratings = [rating.strip() for rating in raw_rating if rating.strip() != ""]
        if len(ratings) != 0:
            scraped_info['rating'] = ratings[0]

        # Reviews for this parts
        reviews = response.css('.partReviews__writeup p::text')
        if reviews != None:
            scraped_info['reviews'] = reviews.getall()

        yield scraped_info


            