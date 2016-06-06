import re

def stock_symbol(stock):
    if type(stock) == list:
        print("STOCK: {0}".format(stock))
        stock = str(stock[0])
    try:
        a = re.search(r'\((.*)\)', stock).group()
        if " " in a:
            return re.search(r'\((.*)\)', a.split(' ')[-1]).group(1)
        else:
            return re.search(r'\((.*)\)', stock).group(1)
    except TypeError:
        print ("TYpeError with stock: {0} that has type: {1}").format(stock,type(stock))
    except AttributeError:
        print ("AttributeError with stock: {0} that has type: {1}").format(stock,type(stock))

def convert_exchange_names(exchange_name, current_exchange):
    if exchange_name == '' or exchange_name == 'exchange':
        exchange_name = None
        country = None
    elif 'Nasdaq' in exchange_name or current_exchange == 'NASDAQ':
        exchange_name = 'NASDAQ'
        country = 'USA'
    elif 'NASDAQ' in exchange_name:
        exchange_name = 'NASDAQ'
        country = 'USA'
    elif 'NYSE' in exchange_name or current_exchange == 'NYSE':
        exchange_name = 'NYSE'
        country = 'USA'
    elif 'HKSE' in exchange_name:
        exchange_name = 'HKSE'
        country = 'CHI'
    elif 'Toronto' in exchange_name or current_exchange == 'TSX':
        exchange_name = 'TSX'
        country = 'CAN'
    elif 'TSX' in exchange_name:
        exchange_name = 'TSX'
        country = 'CAN'
    elif 'SNP' in exchange_name:
        exchange_name = 'SNP'
        country = 'USA'
    elif 'S&P 500' in exchange_name:
        exchange_name = 'SNP'
        country = 'USA'
    elif 'Toronto' in exchange_name:
        exchange_name = 'TSX'
        country = 'CAN'
    elif 'London' in exchange_name or current_exchange == 'LSE':
        exchange_name = 'LSE'
        country = 'GBR'
    return exchange_name
