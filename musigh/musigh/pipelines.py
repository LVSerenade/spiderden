# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import scrapy
from urllib.parse import urlparse
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem

class MusighPipeline(FilesPipeline):
            
    def get_media_requests(self, item, info):
        for image_url in item['file_urls']:
            yield scrapy.Request(image_url, meta={'file_name': item['file_name']})

    def item_completed(self, results, item, info):
        image_paths = [item['file_name'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['files'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):
        return request.meta['file_name']