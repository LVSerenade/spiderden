import scrapy

class MusicItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    file_name = scrapy.Field()

class MusighSpider(scrapy.Spider):
    name = "audio"
    start_urls = ['http://musigh.com/']

    # Now we will parse all the pages for ever until we hit a 404
    def parse(self, response):
        # Get all link to music
        audio_links = response.css('audio source::attr(src)').getall()
        for audio_link in audio_links:
            yield self.parse_item(audio_link)
    
        # Get the next url
        next_url = response.css('.older a::attr(href)')[0].get()
        yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_item(self, audio_link):
        item = MusicItem()
        item['file_urls'] = [audio_link]
        name = audio_link.split('?')[0].split('/')[-1]
        item['file_name'] = name
        return item
    