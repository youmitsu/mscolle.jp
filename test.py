#importでrequests、cssselectとlxmlを持ってくる。
import requests
import lxml.html
import cssselect

#TOPページのurlをtop_urlに格納
url = "https://misscolle.com/aoyama2018"
r = requests.get(url)

#TOPページの中のHTMLをrootに格納。
html = r.text
root = lxml.html.fromstring(html)

#フッター内のxpath内のデータを取得。
for item in root.xpath("//*[@id='summary']"):
    for entry in item.xpath(".//table/*"):
        for th in entry.xpath(".//th"):
            print(th.text)
        for td in entry.xpath(".//td"):
            if(td.text is None):
                for tdd in td.xpath(".//text()"):
                    print(tdd)
            else:
                print(td.text)
