import re, os, glob

def check_file(n):
    if "_ver_" not in n:
        n = n + "_ver_1"
    while os.path.exists(n):
        c = n.split('_')
        i = int(c[-1]) + 1
        if len(c[:-1])>1:
            b = c[0]
            for x in range(len(c[:-1])):
                b = b + "_" + c[x]
        else:
            b = c[0]
        n = b + "_" + i
    return n

def last_data_file(key):
    with cd("datapull/data"):
        return key + "_ver_" + str(max([filename.split('_')[-1].split('.')[0] for filename in glob.glob('*.csv') if filename.split('_')[0] == key])) + ".csv"


def stock_symbol(stock):
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


def get_change_in(y, ln=False, percentage=True, ascending=True):
    """
    returns change in 1-d numpy array
    if percentage == True, returns percentage change, else actual dollar or amount difference
    ascending means [older - > newer], else [newer - > older]
    """
    if ascending == True:
        if percentage == True:
            if ln == True:
                with np.errstate(divide='ignore',invalid='ignore'):
                    change = np.log(y[1:]/y[:-1])
                    change[change == np.inf] = 0
                    change = np.nan_to_num(change)
            else:
                with np.errstate(divide='ignore',invalid='ignore'):
                    change = (y[1:]/y[:-1])-1
                    change[change == np.inf] = 0
                    change = np.nan_to_num(change)
        else: # get amount change
            change = (y[1:]-y[:-1])
    else:
        if percentage == True:
            if ln == True:
                with np.errstate(divide='ignore',invalid='ignore'):
                    change = np.log(y[:-1]/y[1:])
                    change[change == np.inf] = 0
                    change = np.nan_to_num(change)
            else:
                with np.errstate(divide='ignore',invalid='ignore'):
                    change = (y[:-1]/y[1:])-1
                    change[change == np.inf] = 0
                    change = np.nan_to_num(change)
        else:
            change = (y[:-1]-y[1:])
    return change


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

class cd:
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)
    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)
    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
