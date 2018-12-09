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
for item in root.xpath("//*[@id='summary']/table/tbody/tr"):
      for contest_name in item.xpath(".//th"):
        print(contest_name.text)
