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

class CasePartSpider(scrapy.Spider):
    name = "case"
    base_url = 'https://pcpartpicker.com/'
    
    # This slug is what will trigger the fetching of the data
    magic_slug = "fetch/?page=%d&xslug=&location=&search=&qid=1&scr=1&scr_vw=1263&scr_vh=319&scr_dw=1280&scr_dh=720&scr_daw=1280&scr_dah=680&scr_ddw=1263&scr_ddh=5806&ms=1578965341903"
   
    type_part = "products/case/"

    start_urls = [
        base_url + type_part + magic_slug,
    ]


    link_regex = "product.*\w{1}"
    page_regex = 'page=[0-9]*'

    def parse(self, response):
        
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
            new_slug = self.magic_slug % (i)
            page_url = self.base_url + self.type_part + '/' + new_slug
            yield scrapy.Request(page_url, callback=self.parse_page)
        

    def parse_page(self, response):
        # Get all links in the page
        all_links = response.css("a::attr(href)").getall()
        for link in all_links:
            
            # Check if it is a content link
            link_search = re.compile(self.link_regex)
            result = link_search.findall(link)
            if result != []:
                product_url = self.base_url + result[0]
                yield scrapy.Request(product_url, callback=self.parse_cpu)
    
    def parse_cpu(self, response):
        '''
            will parse the product page for specification on the computer part
            need to be called like this:
            >>> yield scrapy.Request(product_url, callback=self.parse_cpu)
        '''
        # Default of scraped info (nothing in it)
        scraped_info = {}

        specs_list = []
        specs = response.css("div.specs").getall()
        if len(specs) > 0:
            all_specs = specs[0]
            soup = BeautifulSoup(all_specs, 'html.parser')
            specs_list = soup.find_all("div", {"class": "group group--spec"})
        else:
            return {}
        
        
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


            