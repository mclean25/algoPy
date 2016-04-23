import numpy as np
import os, itertools, glob, string, sys, csv, json
from datetime import datetime
from preferences import *
from functions import *

csv.field_size_limit(sys.maxsize) # maximizes ability to read massive csv files
csv.field_size_limit(sys.maxsize) # Done twice intentionally

headers = ['adjcloses', 'volumes']
dollar_vlaues = ['adjcloses', 'volumes', 'opens', 'lows', 'highs', 'closes']

def download_data(exchange_settings):
	with cd("datapull"):
		for key in exchange_settings:
			if exchange_settings[key] == True:
				fname = check_file("data/"+key)
				os.system("scrapy crawl stock_indexer -o {0}.csv -t csv -a exchange={1}".format(fname, key))

# download_data(exchange_settings)

class Equity(object):
	def __init__(self, stock):
		self.symbol = stock['symbol']
		self.exchange = stock['exchange']
		self.dates = stock['dates'][::-1]
		self.first_trade = self.dates[0]
		self.last_trade = self.dates[-1]
		
	def ffill(self, stock):
		"""
		Forward fills stock data to allow symmetry between different stock exchanges
		"""
		global trading_dates, headers
		start = trading_dates.index(self.first_trade)
		end = trading_dates.index(self.last_trade)
		for day in trading_dates[start:end]:
			if day not in self.dates:
				pos = trading_dates[start:end].index(day)
				self.dates.insert(pos,day)
				for key in headers:
					stock[key].insert(pos, stock[key][pos-1])
		self.dates = self.dates
		self.volume = np.array(json.loads(stock['volumes']))[::-1]
		self.adjcloses = np.array(json.loads(stock['adjcloses']))[::-1]
		return

	def rates(self):
		self.rates = get_change_in(self.adjcloses,ln=True)
		return



def load_universe():
	date_format = '%Y-%m-%d'
	trading_dates = set()
	unf_stocks = {}
	# Load each exchange's stocks
	for key in exchange_settings:
		if exchange_settings[key] == True:
			# with cd("data/"+last_data_file(key)):
			with open("datapull/data/"+last_data_file(key), 'rb') as csvfile:
				reader = csv.DictReader(csvfile)
				sid = 0 # stock id
				for row in reader:
					sid +=1
					row['dates'] = [datetime.strptime(str(x), date_format).date() for x in json.loads(row['dates'])]
					[trading_dates.add(x) for x in row['dates']]
					unf_stocks[sid] = row
	trading_dates = sorted([datetime.strptime(str(x), date_format).date() for x in trading_dates], reverse=True)
	return unf_stocks, trading_dates # these are unfilled stocks
	# stock = {}
	# for key in unf_stocks:
	# 	# key in this case will be the stocks sid
	# 	stock[key] = equity(unf_stocks[key])


def create_equities():
	unf_stocks, trading_dates = load_universe()
	equities = {}
	for key in unf_stocks:
		equities[unf_stocks[key]['sid']] = Equity(unf_stocks[key]).ffill()
		return equities
