from bs4 import BeautifulSoup
import urllib.request
import datetime
import csv

ngay_out_2017 = datetime.datetime(year=2017, month=2, day=15)
ngay_out_2018 = datetime.datetime(year=2018, month=2, day=15)

headers = {
    "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063"
}

webpage = "https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130428&end=20190320"
request = urllib.request.Request(url=webpage, headers=headers)
websource = urllib.request.urlopen(request)
soup = BeautifulSoup(websource.read(), "html.parser")
tbody = soup.find_all("tbody")
tbody =  tbody[0]
tr_list = tbody.find_all("tr")
tr_list = tr_list[1:]

with open('btc.csv','w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Date','Open','High','Low','Close','Volume','Market Cap'])
    for tr in tr_list:
        td = tr.find_all("td")
        writer.writerow([td[0].text,td[1].text,td[2].text,td[3].text,td[4].text,td[5].text,td[6].text])

