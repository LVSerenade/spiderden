import scrapy
import re
from bs4 import BeautifulSoup

# Helper functions
def get_spec_value(soup):
    '''
        Wrapper function to get the spec value in the correct format whether it is
        a bullet point list (ul) or a single element (p). No other type of spec value
        was found. 
        This function accept a beautifulsoup soup which contain the spec value
        in an html format and return a string representing the value.
    '''

    # Try first if its a list, if not try if its a paragram
    spec_value = soup.find("ul")
    
    if spec_value != None:
        spec_value = spec_value.text.replace('\n',' ').strip().lower()
    else:
        spec_value = soup.find("p")
        if spec_value != None:
            spec_value = spec_value.text.strip().lower()

    return spec_value

class PartsSpider(scrapy.Spider):
    '''
        Parts Spider:
        Purpose of this spider is to go on the website https://pcpartpicker.com 
        and scrape all the current products on the plateforms.

        The spider output the data as a list of JSON object which correspond to every part. 
        The part have varying specs depending on their category so the fields in each JSON object is 
        different. 
        
        The output json 'all_parts.json' can be used with convert_csv to convert to
        N number of CSV files, which correspond to one file per part type. 
    '''

    name = "parts"
    base_url = 'https://pcpartpicker.com'

    # Here we overide the default behavior
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI' : 'all_parts.json'
    }
    
    # This slug is what will trigger the fetching of the data
    get_slug = "fetch/?page=%d&xslug=&location=&search=&qid=1&scr=1&scr_vw=1263&scr_vh=319&scr_dw=1280&scr_dh=720&scr_daw=1280&scr_dah=680&scr_ddw=1263&scr_ddh=5806&ms=1578965341903"

    # We scrape the products page which host the links to all other products page
    start_urls = [
        base_url + "/products/"
    ]

    # Helper regex to parse some link
    link_regex = "product.*\w{1}"
    page_regex = 'page=[0-9]*'


    def parse(self, response):
        '''
            Initial function to be called by Scrapy
            It will scrape the start_urls (here we only have one)
        '''    
        # Get all links in the page
        all_part_type_links = response.css('.wrapper__pageContent a::attr(href)').getall()
        
        # Go through all the links to the product categories and scrape them
        for link in all_part_type_links:
            # Get the type out of the link
            part_type = link.split('/')[2]
            # Create a url using the get_slug to get a useable list of products
            part_type_url = self.base_url + link + self.get_slug
            # Scrape the specific product category page
            yield scrapy.Request(part_type_url, callback=self.parse_part_type, cb_kwargs=dict(part_type=part_type))


    def parse_part_type(self, response, part_type):
        '''
            Function that will scrape the link to the specific product page (e.g. page 1 to 33)
            It will get the number of pages containing products and call the get_slug on each
            page.
        '''
        
        # Get all links in the page
        all_links = response.css("a::attr(href)").getall()

        # We have many page number possible, we will take the maximum one so that
        # we make sure we scrape all the data
        max_num_page = -1
        for link in all_links:
            
            # Check if it is a next page link            
            page_search = re.compile(self.page_regex)
            result = page_search.findall(link)

            # If the result is not empty we check if the page number is bigger than
            # what we already found
            if result != []:
                num_page = int(result[0].split('=')[-1])
                if(num_page > max_num_page):
                    max_num_page = num_page

        # Iterate over all the pages for this product since we know how much page it has
        for i in range(1,max_num_page+1):
            # Use the i to put it inse page=%d in the get_slug
            page_url = response.url % (i)
            yield scrapy.Request(page_url, callback=self.parse_page, cb_kwargs=dict(part_type=part_type))
        

    def parse_page(self, response, part_type):
        '''
            This parser function will go to a specific page number of a particular product type
            and scrape all the link to the actual product to be scraped.
        '''
        # Get all links in the page
        all_links = response.css("a::attr(href)").getall()
        for link in all_links:
            
            # Check if it is a content link
            link_search = re.compile(self.link_regex)
            result = link_search.findall(link)

            # If the result is a content link we go to that page to scrape the part
            if result != []:
                product_url = self.base_url + '/' + result[0]
                yield scrapy.Request(product_url, callback=self.parse_part, cb_kwargs=dict(part_type=part_type))
    
    def parse_part(self, response, part_type):
        '''
            this parser is the one scraping the data from the page and generating a JSON
            object that will be appended to the returned list of JSON.
        '''
        # Default of scraped info (nothing in it)
        scraped_info = {
        }

        # Get all the specs in an unformatted way (still in HTML)
        # If we can't find anything this part is malformed
        specs_list = []
        specs = response.css("div.specs").getall()
        if len(specs) > 0:
            all_specs = specs[0]
            soup = BeautifulSoup(all_specs, 'html.parser')
            specs_list = soup.find_all("div", {"class": "group group--spec"})
        else:
            return {}

        # Set the part type which will be usefull to seperate the JSON list into 
        # different CSV files
        scraped_info['part_type'] = part_type
        
        # Gather the specification for this part
        for spec in specs_list:
            soup = BeautifulSoup(str(spec), 'html.parser')

            # Get the type and the value (h3 and p respectively)
            spec_type = soup.find("h3").text.lower()
            spec_value = get_spec_value(soup)

            # Assign it at the right spot in the dictionary
            scraped_info[spec_type] = spec_value

        # Gather the prices for this part
        prices = response.css('.td__finalPrice a::text')
        if prices != None:
            scraped_info['prices'] = prices.getall()
        
        # Get the Rating for this part (it's an aggregate so it's just a string)
        raw_rating = response.css('.wrapper__pageTitle--rating section::text').extract()
        ratings = [rating.strip() for rating in raw_rating if rating.strip() != ""]
        if len(ratings) != 0:
            scraped_info['rating'] = ratings[0]

        # Get the reviews for this parts from the users
        reviews = response.css('.partReviews__writeup p::text')
        if reviews != None:
            scraped_info['reviews'] = reviews.getall()

        yield scraped_info


            