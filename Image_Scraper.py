import requests
import lxml.html
import cssselect
import uuid

top_url = "https://misscolle.com"
top_url_response = requests.get(top_url)

url = "https://misscolle.com/aoyama2018"
url_response = requests.get(url)

images = []

#TOPページの中のHTMLをrootに格納。
top_html = top_url_response.text
top_root = lxml.html.fromstring(top_html)

html = url_response.text
root = lxml.html.fromstring(html)

for img in root.xpath("//*[@id='contest-header-image']/img"):
   print(top_url + img.get("src"))
   images.append(top_url + img.get("src"))

for target in images:
    re = requests.get(target)
    with open('/Users/YUSUKE/Desktop/Mscolle.com/imgs/' + target.split('/')[-1], 'wb') as f: # imgフォルダに格納
      # .contentで画像データとして書き込む
      f.write(re.content)

# スクレイピング終了確認
print("画像保存が完了しました。")
