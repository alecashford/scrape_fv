import finviz
import time
import datetime
import re
import csv
import math

market_holidays = [datetime.datetime.strptime(i, "%Y-%m-%d").date() for i in [
    "2020-01-01",
    "2020-01-20",
    "2020-02-17",
    "2020-04-10",
    "2020-05-25",
    "2020-07-03",
    "2020-09-07",
    "2020-11-26",
    "2020-12-25",
    "2021-01-01",
]]

todays_date = datetime.datetime.today().date()

a_holiday = todays_date in market_holidays
a_weekend = todays_date.weekday() > 4


def normalize_value(field):
    if bool(re.search('^-$', field)):
        return None
    elif bool(re.search('^-?\d*\.\d*%$', field)):
        return round(float(field.rstrip('%')) / 100.0, 4)
    elif bool(re.search('^-?\d*\.\d*[BMKT]$', field)):
        mapping = {"K": 1000, "M": 1000000,
                   "B": 1000000000, "T": 1000000000000}
        multiple = mapping[field[-1]]
        multiple = multiple * -1 if bool(re.search('^-', field)) else multiple
        field = re.sub(r'[-BMKT]', '', field)
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


tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
market_open = tomorrow.replace(hour=6, minute=0, second=0, microsecond=0)


def sleepx(remaining):
    right_now = datetime.datetime.now()
    time_delta = (market_open - right_now).total_seconds()
    exact_wait = time_delta / remaining
    time_to_sleep = math.floor(exact_wait) if math.floor(
        exact_wait) > 1 else exact_wait
    print(f'Sleeping {time_to_sleep} seconds')
    time.sleep(time_to_sleep)


filename = "stock-metrics-" + datetime.datetime.today().strftime('%Y-%m-%d') + ".csv"


if __name__ == '__main__':
    if a_holiday or a_weekend:
        exit()

    for i in range(0, 5):
        try:
            stock_list = finviz.Screener(filters=[]).data
            time.sleep(5)
            break
        except:
            time.sleep(5)

    headers_written = False

    with open(filename, 'w') as file:
        for idx, stock in enumerate(stock_list):
            for i in range(0, 3):
                try:
                    metrics = normalize(finviz.get_stock(stock["Ticker"]))
                    metrics["ticker"] = stock["Ticker"]
                    metrics["company"] = stock["Company"]
                    metrics["sector"] = stock["Sector"]
                    metrics["industry"] = stock["Industry"]
                    metrics["country"] = stock["Country"]
                    if not headers_written:
                        writer = csv.DictWriter(file, metrics.keys())
                        writer.writeheader()
                        headers_written = True
                    writer.writerow(metrics)
                    print(stock["Ticker"])
                    sleepx(len(stock_list) - idx + 1)
                    break
                except:
                    sleepx(len(stock_list) - idx + 1)
