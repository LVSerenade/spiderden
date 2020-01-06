import scrapy
import re

class PCPartSpider(scrapy.Spider):
    name = "parts"
    base_url = 'https://pcpartpicker.com/products/'
    
    # This slug is what will trigger the fetching of the data
    magic_slug = "fetch/?page=%d&xslug=&location=&search=&qid=1&scr=1&scr_vw=1263&scr_vh=319&scr_dw=1280&scr_dh=720&scr_daw=1280&scr_dah=680&scr_ddw=1263&scr_ddh=4097&ms=1578350483758"
   
    start_urls = [
        base_url + "cpu/" + magic_slug,
    ]

    type_part = "cpu"


    link_regex = "/product.*\w{1}"
    page_regex = 'page=[0-9]*'

    def parse(self, response):
        
        # Get all links in the page
        all_links = response.css("a::attr(href)").getall()

        max_num_page = 0
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
                print(self.product_counter)
    
    def parse_product(self, response):
        print("yehaaaw")


            