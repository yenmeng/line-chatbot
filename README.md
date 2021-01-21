# line-chatbot
simple chatbot for using [line-bot-sdk-python](https://github.com/line/line-bot-sdk-python) deployed on [heruko](https://dashboard.heroku.com/)<br><br>
功能：一個可以promote自己的聊天機器人<br>
掃描QRcode可以加入好友(my chatbot implementaion)<br>
![](https://i.imgur.com/eMsER89.png)
## 開始之前
* 使用[Chatbot developer console](https://developers.line.me/en/)<br>
* 使用[Line Messaging API](https://developers.line.me/en/docs/messaging-api/getting-started/)取得CHANNEL_ACCESS_TOKEN和CHANNEL_SECRET加入app.py<br>
* 基本設定參考[官方tutorial](https://developers.line.me/en/docs/messaging-api/building-sample-bot-with-heroku/)<br>
## 實作功能
[註]因為隱私問題，app.py中有關個人的內容皆用alt_text取代，但修改alt_text的部分後就可以跑了<br>
### 加入好友
* 當有好有新加入時會有歡迎的訊息，傳送貼圖＋文字以及一個 `QuickReplyButton` 可以開啟下一個回覆<br><br>
![](https://i.imgur.com/e57yWhum.jpg)
### 訊息回覆
* 為了讓內容清楚呈現，所以用了各種 `ButtonsTemplate`及`ImageCarouselTemplate` 的選單<br>
* 點選選單中的項目會得到對應的回覆，可能是文字或是圖片或是前往連結<br>
* 用了python的str.find以及re.search去做訊息文字的matching，讓如果輸入到一些關鍵字就可以得到對應的回覆，不一定只能從選單<br>
* 如果訊息不在回覆的規則中，則送出default回覆，也就是文字＋profile選單，提供可以回答的問題<br><br>
![](https://i.imgur.com/GdCWIwdl.png?1)<br>
### Rich Menu
* rich menu的部分好像不能直接寫，因此用了[Line Business ID](https://account.line.biz/login?redirectUri=https%3A%2F%2Fmanager.line.biz%2F%3Fstatus%3Dsuccess)建立圖文選單<br>
若是真的不知道問什麼問題可以點選<br>
共有三個項目:<br>
  * About Me(傳送profile選單)
  * GitHub(連結到github)
  * 純屬娛樂的功能，分享一些我近日看到的迷因
## 一些網站
* [Line貼圖](https://developers.line.biz/media/messaging-api/sticker_list.pdf)
* [emoji unicode](https://unicode.org/emoji/charts/full-emoji-list.html)
* [line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)
