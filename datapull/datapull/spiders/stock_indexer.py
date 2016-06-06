# -*- coding: utf-8 -*-
import scrapy, json
from datapull.exchange_links import *
from datapull.items import YahooItem
from datapull.scrapy_functions import *
from time import strptime, time
from datetime import datetime


class StockIndexer(scrapy.Spider):

    name = "stock_indexer"
    allowed_domains = ["finance.yahoo.com", "http://eoddata.com/", "ca.finance.yahoo.com"]
    start_urls = ['http://finance.yahoo.com/q/hp?s=CAT']

    def __init__(self, *args, **kwargs):
        super(StockIndexer, self).__init__(*args,**kwargs)
        self.exchange = kwargs.get('exchange')
        print (self.exchange)
        links = []
        for link in exchange_links[str(self.exchange)]:
            links.append(link)
        self.start_urls = links

    def parse(self, response):

        if "eoddata" in response.url:
            companyList1 = response.xpath('//tr[@class="ro"]/td/a/text()').extract()
            companyList2 = response.xpath('//tr[@class="re"]/td/a/text()').extract()
            companyList = companyList1 + companyList2
            for company in companyList:
                print("Scraping Company: {0}".format(company))
                if "TSX" in response.url:
                    go = 'http://finance.yahoo.com/q/hp?s={0}.TO'.format(company)
                elif "LSE" in response.url:
                    go = 'http://finance.yahoo.com/q/hp?s={0}.L'.format(company)
                elif "HKEX" in response.url:
                    go = 'http://finance.yahoo.com/q/hp?s={0}.HK'.format(company)
                elif "AMS" in response.url:
                    go = 'http://finance.yahoo.com/q/hp?s={0}.AS'.format(company)
                else:
                    go = 'http://finance.yahoo.com/q/hp?s={0}'.format(company)
                print("Go: {0}".format(go))
                yield scrapy.Request(go, self.stocks1)
        elif "http://finance.yahoo.com/q?s=CAT" in response.url:
            go = 'http://finance.yahoo.com/q/hp?s=CAT'
            yield scrapy.Request(go, self.stocks1)
        elif 'http://finance.yahoo.com/q/hp?s=CAT' in response.url:
            go = 'http://finance.yahoo.com/q/hp?s=CAT'
            yield scrapy.Request(go, self.stocks1)
        else:
            rows = response.xpath('//table[@class="yfnc_tableout1"]//table/tr')[1:]
            for row in rows:
                company = row.xpath('.//td[1]/b/a/text()').extract()
                go = 'http://finance.yahoo.com/q/hp?s={0}'.format(company)
                yield scrapy.Request(go, self.stocks1)

    def stocks1(self, response):

        date_format = '%Y-%m-%d'
        print ("in stocks1")
        if 'item' in response.meta:
            # If the response contains a 'item' from a previous page unwrap it
            item = response.meta['item']

        else:
            # if it contains no such item, it's the first page, so let's create it
            item = YahooItem()
            item['dates'] = []
            item['opens'] = []
            item['highs'] = []
            item['lows'] = []
            item['closes'] = []
            item['volumes'] = []
            item['adjcloses'] = []

        # This grabs the stock data from the page
        returns_page = []
        rows = response.xpath('//table[@class="yfnc_datamodoutline1"]//table/tr')[1:]
        if rows:
            print("there is rows")
        for row in rows:
            cells = row.xpath('.//td/text()').extract()
            try:
                vals = {}
                vals['open'] = cells[1]
                vals['high'] = cells[2]
                vals['low'] = cells[3]
                vals['close'] = cells[4]
                vals['volume'] = cells[5]
                vals['adjclose'] = cells[6]
                for key in vals:
                    if "," in vals[key]:
                        vals[key] = vals[key].replace(",","")
                unf_date = str(cells[0])
                month = strptime(unf_date[:3],'%b').tm_mon
                day = unf_date[4:6].replace(',','')
                year = unf_date[-4:]
                vals['date'] = str(datetime.strptime(str(year) + '-' + str(month) + '-' + str(day), date_format).date())
                try:
                    float(vals['open'])
                except ValueError:
                    continue
                else:
                    if vals['date'] not in item['dates']:
                        item['opens'].append(vals['open'])
                        item['highs'].append(vals['high'])
                        item['lows'].append(vals['low'])
                        item['closes'].append(vals['close'])
                        item['volumes'].append(vals['volume'])
                        item['adjcloses'].append(vals['adjclose'])
                        item['dates'].append(vals['date'])
            except ValueError:
                continue
            except IndexError:
                # print "index Error with cells: {0}".format(cells)
                continue

        # Check if there is a 'Next' link
        xpath_Next_Page = './/a[contains(.,"Next")]/@href'
        if response.xpath(xpath_Next_Page):
            # No need to calculate offset values. Just take the link ...
            next_page_href = response.xpath(xpath_Next_Page).extract()[0]
            url_next_page = 'http://finance.yahoo.com' + next_page_href
            # ... build the request ...
            request = scrapy.Request(url_next_page, callback=self.stocks1)
            # ... and add the item with the collected values to the request
            request.meta['item'] = item
            yield request
        else:
            # items = []
            if item['adjcloses']:
                print("adjusted close")
                item['name'] = response.xpath('//div[@class="title"]/h2/text()').extract()
                if item['name']:
                    item['url'] = response.url
                    print("ITEM: {0}".format(item))
                    item['symbol'] = stock_symbol(item['name'])
                    item['dates'] = json.dumps(item['dates'])
                    item['opens'] = json.dumps(item['opens'])
                    item['highs'] = json.dumps(item['highs'])
                    item['lows'] = json.dumps(item['lows'])
                    item['closes'] = json.dumps(item['closes'])
                    item['volumes'] = json.dumps(item['volumes'])
                    item['adjcloses'] = json.dumps(item['adjcloses'])
                    item['exchange'] = convert_exchange_names(response.xpath('//span[@class="rtq_exch"]/text()').extract(),"")
                    # item['ind_sharpe'] = ((numpy.average(rates) - risk_free_rate) / numpy.std(rates))
                    # item['dates'] = dates
                    # items.append(item)
                    yield item
                else:
                    print("Couldn't extract data at URL: {0}".format(response.url))
