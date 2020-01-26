import requests
import finviz
from bs4 import BeautifulSoup
import time
import datetime
import re
import csv

def normalize_value(field):
    if bool(re.search('^-$', field)):
        return None
    elif bool(re.search('^-?\d*\.*\d*%$', field)):
        return round(float(field.rstrip('%')) / 100.0, 4)
    elif bool(re.search('^-?\d*\.*\d*[BMK]$', field)):
        if field[-1] == "K":
            multiple = 1000
        elif field[-1] == "M":
            multiple = 1000000
        elif field[-1] == "B":
            multiple = 1000000000
        field = re.sub(r'[MBK]', '', field)
        whole_part = int(field.split(".")[0])
        fractional_part = int(field.split(".")[1])
        return int((whole_part * multiple) + (fractional_part * (multiple / 100)))
    elif bool(re.search('^-?\d*\.\d*$', field)):
        return round(float(field), 4)
    elif bool(re.search('^-?\d*$', field)):
        return int(field)
    elif bool(re.search('\d,\d', field)):
        return int(re.sub(r',', '', field))
    elif field == "Yes":
        return True
    elif field == "No":
        return False
    else:
        return field


def normalize_key(label):
    label = re.sub(r'[\ \/]', '_', label).lower()
    label = re.sub(r'[()\.]', '', label)
    return re.sub(r'%', 'percent', label)

def normalize(d):
    return {normalize_key(k): normalize_value(v) for (k, v) in d.items()}

stock_list = finviz.Screener(filters=[]).data

filename = "stock-metrics-" + datetime.datetime.today().strftime('%Y-%m-%d') + ".csv"

with open(filename, 'w') as file:
    headers = normalize(finviz.get_stock(stock_list[0]["Ticker"]))
    headers["ticker"] = stock_list[0]["Ticker"]
    headers["company"] = stock_list[0]["Company"]
    headers["sector"] = stock_list[0]["Sector"]
    headers["industry"] = stock_list[0]["Industry"]
    headers["country"] = stock_list[0]["Country"]
    writer = csv.DictWriter(file, headers.keys())
    writer.writeheader()
    for stock in stock_list:
        metrics = normalize(finviz.get_stock(stock["Ticker"]))
        metrics["ticker"] = stock["Ticker"]
        metrics["company"] = stock["Company"]
        metrics["sector"] = stock["Sector"]
        metrics["industry"] = stock["Industry"]
        metrics["country"] = stock["Country"]
        writer.writerow(metrics)
        print(stock["Ticker"])
        time.sleep(2)
