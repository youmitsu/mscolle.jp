#importの設定
import requests
import lxml.html
import cssselect
import pymysql
import uuid

#Left,Right,middleを定義
def left(text, n):
  return text[:n]

def right(text, n):
  return text[-n:]

def mid(text, n, m):
  return text[n-1:n+m-1]

#TOPページのurlをrに格納
top_url = "https://misscolle.com"
top_url_response = requests.get(top_url)

#TOPページの中のHTMLをrootに格納。
top_html = top_url_response.text
top_root = lxml.html.fromstring(top_html)
contests_url = []
profiles_url = []
contest_images = []
profile_images = []

#SQLのログイン情報を記載
connector = pymysql.connect(
   host='127.0.0.1',
   db='mscolle',
   user='root',
   passwd='root',
   charset='utf8',
)

#cursorでSQLにログインが可能な状態にする。
cursor = connector.cursor()

##****** TOPページのFooterから、URL一覧を取得する。 ******##
#フッター内のxpath内のデータを取得。
for a in top_root.xpath("body/footer/div/div/ul/li/a"):

#contests_urlの配列にURLを追加
  contests_url.append(top_url + a.get("href"))

##****** https://misscolle.com/versionsから過去のミスコン一覧ページを取得する。 ******##
#過去のミスコン一覧をroot2に格納
versions_url = "https://misscolle.com/versions"
versions_url_response = requests.get(versions_url)
versions_html = versions_url_response.text
versions_root = lxml.html.fromstring(versions_html)

#root2の中からurlを取得。
for item in versions_root.xpath(".//ul[@class='columns']"):
  for a in item.xpath(".//a"):
    aa = a.get("href")
    if aa.startswith("http://"):
      contests_url.append(aa)
    else:
      contests_url.append(top_url + aa)

#contests_urlの配列にURLを追加
for contest_url in contests_url:
    #contest URL *
    print(contest_url)

    #開催年度の取得 *
    print(right(contest_url,4))

##****** Contestのページのスクレピング******##
    #TOPページの中のHTMLをrootに格納。
    contest_response = requests.get(contest_url)
    contest_html = contest_response.text
    contest_root = lxml.html.fromstring(contest_html)

    #contest_idの取得


    #contest_imageの取得　*
    for contest_img in contest_root.xpath("//*[@id='contest-header-image']/img"):
       print(top_url + contest_img.get("src"))
       contest_images.append(top_url + contest_img.get("src"))

    for target in contest_images:
        re = requests.get(target)
    with open('/Users/YUSUKE/Desktop/Mscolle.com/contest_imgs/' + str(uuid.uuid1()) + target.replace("?v=121001", "").split("/")[-1], 'wb') as f: # imgフォルダに格納
          # .contentで画像データとして書き込む
                f.write(re.content)

    #Contestの中身を取得
    for item in contest_root.xpath("//*[@id='summary']"):
        for entry in item.xpath(".//table/*"):
    #コンテスト名

    #大学名

    #主催団体名

    #実施学園祭

    #実施日

    #場所

    #団体Twitter

    #WEB投票開始日

    #WEB投票終了日

            for th in entry.xpath(".//th"):
                print(th.text)
            for td in entry.xpath(".//td"):
                print(td.text)



##****** プロフィールのスクレピング******##
    #プロフィールの部分を取得
    for profile in contest_root.xpath("//div[@class='entry']"):

    #profile_idの取得



    #contest_idの取得



    #エントリーNoの取得
     for entry_no in profile.xpath(".//span[1]"):
      print(entry_no.text.replace("ENTRY 0", ""))

    #名前の取得
     for name in profile.xpath(".//h3"):
      print(name.text)

    #TwitterのURLを取得
     for icon_box in profile.xpath(".//div[@class='icon-box']"):
      for twitter_url in icon_box.xpath(".//a[contains(@class, 'twitter')]"):
       print(twitter_url.get("href"))

    #InstagramのURLを取得
     for icon_box in profile.xpath(".//div[@class='icon-box']"):
      for instagram_url in icon_box.xpath(".//a[contains(@class, 'instagram')]"):
       print(instagram_url.get("href"))

    #グランプリflgの取得
     for grandprix_flg in profile.xpath(".//span[2]"):
       if grandprix_flg.text == "グランプリ":
          grandprix_flg = 1
       elif grandprix_flg.text == "準グランプリ":
          grandprix_flg = 2
       else:
          grandprix_flg = 0
     print(grandprix_flg)

    #ProfileのURLの取得
     for profile_directory in profile.xpath(".//div/ul/li[1]/a"):
      print(top_url + profile_directory.get("href"))
      profile_url = top_url + profile_directory.get("href")

    ##Profile URLの中から、ユーザー情報を取得。
      profile_response = requests.get(profile_url)
      profile_html = profile_response.text
      profile_root = lxml.html.fromstring(profile_html)

      #profileの写真を取得
      for profile_img in profile_root.xpath("//*[@id='main-photo']/img"):
         print(top_url + profile_img.get("src"))
         profile_images.append(top_url + profile_img.get("src"))

      for target in profile_images:
          re = requests.get(target)
      with open('/Users/YUSUKE/Desktop/Mscolle.com/profile_imgs/' + str(uuid.uuid1()) + target.replace("?v=121001", "").split("/")[-1], 'wb') as f: # imgフォルダに格納
          # .contentで画像データとして書き込む
            f.write(re.content)

      #学部を取得
      for faculty in profile_root.xpath("//*[@id='info']/span[2]"):
            print(faculty.text.replace(" ", "").replace("\n", ""))

      #誕生日を取得
      for birthday in profile_root.xpath("//*[@id='info']/dl[1]/dd"):
            print(birthday.text)

      #出身地を取得
      for birthplace in profile_root.xpath("//*[@id='info']/dl[2]/dd"):
            print(birthplace.text)

      #身長を取得
      for height in profile_root.xpath("//*[@id='info']/dl[3]/dd"):
            print(height.text)

      #血液型を取得
      for blood in profile_root.xpath("//*[@id='info']/dl[4]/dd"):
            print(blood.text)

##詳細のユーザー情報を取得
    #詳細の質問のアイテムを取得
      for columns in profile_root.xpath("//ul[@class='columns js-masonry']"):
        for lis in columns.xpath(".//li"):
    #question_idを取得



    #questionを取得
           for quetion in lis.xpath(".//h3"):
             print(quetion.text.replace(" ", "").replace("\n", ""))

    #answerを取得
           for answer in lis.xpath(".//p"):
             print(answer.text.replace(" ", "").replace("\n", ""))

    #profile_idを取得
