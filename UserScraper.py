#importの設定
import requests
import lxml.html
import cssselect

##****** TOPページのFooterから、URL一覧を取得する。 ******##
#TOPページのurlをrに格納
top_url = "https://misscolle.com"
top_url_response = requests.get(top_url)

#TOPページの中のHTMLをrootに格納。
top_html = top_url_response.text
top_root = lxml.html.fromstring(top_html)
contests_url = []
profiles_url = []

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
    print(contest_url)

##****** Contestに出ているユーザーをスクレイピングする ******##
    #TOPページの中のHTMLをrootに格納。
    contest_response = requests.get(contest_url)
    contest_html = contest_response.text
    contest_root = lxml.html.fromstring(contest_html)

    #プロフィールの部分を取得
    for profile in contest_root.xpath("//div[@class='entry']"):

    #名前の取得
     for name in profile.xpath(".//h3"):
      print(name.text)

    #Twitterを取得
     for icon_box in profile.xpath(".//div[@class='icon-box']"):
      for twitter_url in icon_box.xpath(".//a[1]"):
       print(twitter_url.get("href"))

    #Instagramを取得
     for icon_box in profile.xpath(".//div[@class='icon-box']"):
      for instagram_url in icon_box.xpath(".//a[3]"):
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

      for birthday in profile_root.xpath("//*[@id='info']/dl[1]/dd"):
            print(birthday.text)

      for birthplace in profile_root.xpath("//*[@id='info']/dl[2]/dd"):
            print(birthplace.text)

      for height in profile_root.xpath("//*[@id='info']/dl[3]/dd"):
            print(height.text)

      for blood in profile_root.xpath("//*[@id='info']/dl[4]/dd"):
            print(blood.text)

      for columns in profile_root.xpath("//ul[@class='columns js-masonry']"):
        for lis in columns.xpath(".//li"):
           for quetion in lis.xpath(".//h3"):
             print(quetion.text.replace(" ", "").replace("\n", ""))

           for answer in lis.xpath(".//p"):
             print(answer.text.replace(" ", "").replace("\n", ""))
