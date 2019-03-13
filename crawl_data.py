from bs4 import BeautifulSoup
import urllib.request
import datetime
import csv

ngay_out_2017 = datetime.datetime(year=2017, month=2, day=15)
ngay_out_2018 = datetime.datetime(year=2018, month=2, day=15)

headers = {
    "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063"
}

webpage = "https://coinmarketcap.com/currencies/ethereum-classic/historical-data/?start=20170101&end=20180131"
request = urllib.request.Request(url=webpage, headers=headers)
websource = urllib.request.urlopen(request)
soup = BeautifulSoup(websource.read(), "html.parser")

with open('data.csv','w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Date','min_price','price','max_price',])
exit()
# ti le nam 2017 den luc can tinh
ratio_list_max_2017 = list()
ratio_list_min_2017 = list()
tr_list = soup.find_all("tr")
tr = tr_list[len(tr_list) - 1]
while (True):
    gia_truoc_max = float(tr.find_all("td")[2].text)
    gia_truoc_min = float(tr.find_all("td")[3].text)
    tr = tr.find_previous("tr")
    gia_sau_max = float(tr.find_all("td")[2].text)
    gia_sau_min = float(tr.find_all("td")[3].text)
    ratio_list_max_2017.append(gia_sau_max / gia_truoc_max)
    ratio_list_min_2017.append(gia_sau_min / gia_truoc_min)
    get_date = datetime.datetime.strptime(tr.find_all("td")[0].text, "%b %d, %Y")
    if get_date == ngay_out_2017:
        break

# Tinh toan cho nam nay
tr = tr_list[len(tr_list) - 2 - 365]
# check luc out
x = 0
# check ratio list
y = 0
get_date = None
do_lech_max = 0
do_lech_min = 0
future_max = float(tr_list[1].find_all("td")[2].text)
future_min = float(tr_list[1].find_all("td")[3].text)
while (True):
    if tr is tr_list[1]:
        x = x + 1
        if x == (ngay_out_2018 - get_date).days:
            break
        future_max = future_max * (ratio_list_max_2017[y])
        future_min = future_min * (ratio_list_min_2017[y])
    else:
        gia_current_max = float(tr.find_all("td")[2].text)
        gia_current_min = float(tr.find_all("td")[3].text)
        gia_predict_max = (ratio_list_max_2017[y] - do_lech_max) * float(
            (tr.find_previous("tr")).find_all("td")[2].text)
        gia_predict_min = (ratio_list_min_2017[y] - do_lech_min) * float(
            (tr.find_previous("tr")).find_all("td")[3].text)
        do_lech_max = (do_lech_max + (gia_predict_max - gia_current_max) / gia_current_max) / 2
        do_lech_min = (do_lech_min + (gia_predict_min - gia_current_min) / gia_current_min) / 2
        get_date = datetime.datetime.strptime(tr.find_all("td")[0].text, "%b %d, %Y")
        tr = tr.find_previous("tr")
    y = y + 1
print((future_max - do_lech_max * future_max), "\n", (future_min - do_lech_min * future_min))
