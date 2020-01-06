import scrapy


class PubmedSpider(scrapy.Spider):
    name = "eager"
    max_paper = 31875646 # the latest article in trending
    good_paper = 0
    target_paper = 50000

    def start_requests(self):
        base_url = 'https://www.ncbi.nlm.nih.gov/pubmed/'

        for id in range(self.max_paper,1,-1):
            url = base_url + str(id)
            if self.good_paper == self.target_paper:
                return None
            yield scrapy.Request(url=url, callback=self.parse)

    # Now we will parse all the pages for ever until we hit a 404
    # we will keep the following data:
    # title of the article
    # urls of the pubmed article
    # list of authors
    # abstract
    # DOI of article
    def parse(self, response):
        # need to get the title 
        title = ''
        abstract = ''
        authors = ''
        doi = ''

        
        abstract_selector = response.css('.abstr div p::text')
        # If there is nothing in the selector for the abstract there is no use for this dataset
        if not abstract_selector:
            return {}

        abstract = "".join(abstract_selector.getall())
        
        # Get the title if there is one (it should)
        title_selector = response.css('.abstract h1::text')
        if title_selector:
            title = title_selector[0].get()

        # Get the authors if there are some
        authors_selector = response.css('.auths a::text')
        if authors_selector:
            authors = authors_selector.getall()

        # Get the doi if possible
        doi_selector = response.css('.rprtid dd a::attr(href)')
        if doi_selector:
            doi = doi_selector[0].get()
        
        # Yield the scraped info
        scraped_info = {
                #key:value
                'title': title,
                'url' : response.url,
                'authors' : authors,
                'abstract' : abstract,
                'doi' : doi,
            }

        self.good_paper = self.good_paper + 1
        print("NUMBER OF GOOD PAPER = " + str(self.good_paper))
        yield scraped_info
    