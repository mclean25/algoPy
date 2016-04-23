# -*- coding: utf-8 -*-
from urllib import urlencode
from urlparse import urlparse, urlunparse, parse_qs
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
		url = item['url']
		u = urlparse(url)
		query = parse_qs(u.query)
		query.pop('lookup', None)
		u = u._replace(query=urlencode(query, True))
		unique_url = urlunparse(u)
		if unique_url in self.urls_seen:
		    raise DropItem("Duplicate Item found (%s)" % unique_url)
		elif "lookup" in url:
		    raise DropItem("contains lookup (%s)" % unique_url)
		else:
		    self.urls_seen.add(unique_url)
		return item