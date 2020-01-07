import scrapy
import re
from bs4 import BeautifulSoup

class PCPartSpider(scrapy.Spider):
    name = "parts"
    base_url = 'https://pcpartpicker.com/'
    
    # This slug is what will trigger the fetching of the data
    magic_slug = "fetch/?page=%d&xslug=&location=&search=&qid=1&scr=1&scr_vw=1263&scr_vh=319&scr_dw=1280&scr_dh=720&scr_daw=1280&scr_dah=680&scr_ddw=1263&scr_ddh=4097&ms=1578350483758"
   
    start_urls = [
        base_url + "products/cpu/" + magic_slug,
    ]

    type_part = "products/cpu"


    link_regex = "product.*\w{1}"
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
                yield scrapy.Request(product_url, callback=self.parse_cpu)
    
    def parse_cpu(self, response):
        # Default values
        title = ''
        manufacturer = ''
        model = ''
        part_id = ''
        num_core = ''
        core_clock = ''
        boost_clock = ''
        tdp = ''
        series = ''
        microarchitecture = ''
        core_family = ''
        socket = ''
        integrated_graphics = ''
        ecc_support = ''
        packaging = ''
        include_cpu_cooler = ''
        l1_cache = ''
        l2_cache = ''
        l3_cache = ''
        lithography = ''
        simultaneous_multithreading = ''

        title = response.css('h1.pageTitle::text').get()

        specs = response.css("div.specs").getall()
        if len(specs) > 0:
            all_specs = specs[0]
            soup = BeautifulSoup(all_specs, 'html.parser')
            specs_list = soup.find_all("div", {"class": "group group--spec"})



        scraped_info = {
            'title' : title,
            'manufacturer' : manufacturer,
            'model' : model,
            'part_id' : part_id,
            'num_core' : num_core,
            'core_clock' : core_clock,
            'boost_clock' : boost_clock,
            'tdp': tdp,
            'series' : series,
            'microarchitecture' : microarchitecture,
            'core_family' : core_family,
            'socket' : socket,
            'integrated_graphics' : integrated_graphics,
            'ecc_support' : ecc_support,
            'packaging' : packaging,
            'include_cpu_cooler' : include_cpu_cooler,
            'l1_cache' : l1_cache,
            'l2_cache' : l2_cache,
            'l3_cache' : l3_cache,
            'lithography' : lithography,
            'simultaneous_multithreading' : simultaneous_multithreading,
        }

        yield scraped_info
        print("yehaaaw")


            