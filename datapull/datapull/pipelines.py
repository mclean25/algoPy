
from scrapy.exceptions import DropItem
from scrapy import log
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class YahooPipeline(object):
    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        unique_url = item['url']
        if unique_url in self.urls_seen:
            raise DropItem("Duplicate Item found (%s)" % unique_url)
        elif "lookup" in url:
            raise DropItem("contains lookup (%s)" % unique_url)
        else:
            self.urls_seen.add(unique_url)
        return item
