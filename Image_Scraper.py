# coding:utf-8

import requests
from bs4 import BeautifulSoup

url = 'https://programming-beginner-zeroichi.jp/'
# スクレイピングするユーザーエージェントを指定
headers = {'User-Agent':'Mozilla/5.0'}
soup = BeautifulSoup(requests.get(url,headers=headers).content,'lxml')
images = [] # 画像リストの空配列

for img in soup.find_all('img', class_="img", limit=5):
    # コンソールへスクレイピング対象の画像URLを表示。特段必須ではない
    print(img.get("src"))
    # imagesの空配列へsrcを登録
    images.append(img.get("src"))

# imagesからtargetに入れる
for target in images:
    re = requests.get(target)
    with open('/Users/YUSUKE/Desktop/Mscolle.com/imgs/' + target.split('/')[-1], 'wb') as f: # imgフォルダに格納
      # .contentで画像データとして書き込む
      f.write(re.content)

# スクレイピング終了確認
print("画像保存が完了しました。")
