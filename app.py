import os
import sys
import random
import re

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)
YOUR_CHANNEL_ACCESS_TOKEN = 'YOUR_CHANNEL_ACCESS_TOKEN'
YOUR_CHANNEL_SECRET = 'YOUR_CHANNEL_SECRET'

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

#greetings
greeting_msg = ['greet1','greet2','greet3','greet4']
#profile
profile = TemplateSendMessage(
                alt_text='alt_text',
                template = ButtonsTemplate(
                            thumbnail_image_url="https://example.com/example.jpg",
                            title='About Me',
                            text='profile',
                            actions=[
                                MessageAction(
                                    label='自我介紹',
                                    text='簡單的自我介紹吧！'
                                ),
                                MessageAction(
                                    label='學業',
                                    text='想了解學業相關~'
                                ),
                                MessageAction(
                                    label='專業能力',
                                    text='你有什麼專業能力呢'
                                ),
                                MessageAction(
                                    label='興趣',
                                    text='你的興趣？'
                                )
                            ]
                )
            )
#pic
pic_url = ['url1','url2','url3','url4','url5','url6']
#text
intro_text = 'alt_text'
research_text = 'alt_text'
#course
course1 = ['course1','course2','course3','course4','course5']
course2 = ['course1','course2']
course3 = ['course1','course2','course3']

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

#加入好友greeting
@handler.add(FollowEvent)
def handle_follow(event):
    if isinstance(event.source, SourceUser):
        user_profile = line_bot_api.get_profile(event.source.user_id)
    message = [
        StickerSendMessage(
            package_id='11537',
            sticker_id='52002734'
        ),
        TextSendMessage(text=user_profile.display_name+'，您好！\n我是[NAME]\udbc0\udc84很高興認識您！'),
        TextSendMessage(
            text='有興趣的話來聊聊天吧~',
            quick_reply = QuickReply(
                            items=[
                                QuickReplyButton(
                                    action=MessageAction(
                                    label='好啊！',
                                    text='想知道更多！')
                                ),
                                QuickReplyButton(
                                    action=MessageAction(
                                    label='下次好了QQ',
                                    text='下次好了\udbc0\udc8e')
                                )
                            ]
                )
        )
    ]
    line_bot_api.reply_message(event.reply_token, message)

#處理收到訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.lower()
    #greeting
    if text.find('你好')!=-1 or text.find('哈囉')!=-1 or text.find('hello')!=-1 or text.find('hi')!=-1:
        idx = random.randint(0,3)
        message = TextSendMessage(text=greeting_msg[idx]+' 想問些什麼呢？')
    elif text.find('迷因')!=-1:
        idx = random.randint(0,5)
        message = ImageSendMessage(
                    original_content_url=pic_url[idx],
                    preview_image_url=pic_url[idx]
                )
    elif text.find('下次好了')!=-1 or text.find('掰')!=-1 or text.find('bye')!=-1:
        message = TextSendMessage(text='掰掰\U0001F44B\n歡迎隨時回來哦~')
    #skills
    elif text.find('專業能力-1')!=-1:
        message = [
                TextSendMessage(text='alt_text_1'),
                TextSendMessage(text='alt_text_2'),
                TextSendMessage(text='alt_text_3'),
                TextSendMessage(text='alt_text_4')
        ]
    elif text.find('專業能力-2')!=-1:
        message = [
                TextSendMessage(text='alt_text_1'),
                TextSendMessage(text='alt_text_2')
        ]
    elif text.find('專業')!=-1 or text.find('專長')!=-1 or text.find('能力')!=-1:
        message = TemplateSendMessage(
                alt_text='alt_text',
                template = ButtonsTemplate(
                            title='一些相關的專業能力！',
                            text='點選查看更多...',
                            actions=[
                                MessageAction(
                                    label='專業能力-1',
                                    text='alt_text'
                                ),
                                MessageAction(
                                    label='專業能力-2',
                                    text='alt_text'
                                )
                            ]
                )
            )
    #學業
    #course
    elif text=='課程類別1':
        course = ''
        for item in course1:
            course = course + '\U000027A1' + item + '\n'
        course = course[:-1]
        message = TextSendMessage(text=course)
    elif text=='課程類別2':
        course = ''
        for item in course2:
            course = course + '\U000027A1' + item + '\n'
        course = course[:-1]
        message = TextSendMessage(text=course)
    elif text=='課程類別3':
        course = ''
        for item in course3:
            course = course + '\U000027A1' + item + '\n'
        course = course[:-1]
        message = TextSendMessage(text=course)
    elif re.search('修+.*課+.*',text):
        message = [
                TextSendMessage(text='alt_text_1'),
                TextSendMessage(text='alt_text_2'),
                TemplateSendMessage(
                    alt_text='alt_text',
                    template=ImageCarouselTemplate(
                        columns=[
                            ImageCarouselColumn(
                                image_url='https://example.com/example.jpg',
                                action=MessageTemplateAction(
                                    label='view',
                                    text='課程類別1'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://example.com/example.jpg',
                                action=MessageTemplateAction(
                                    label='view',
                                    text='課程類別2'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://example.com/example.jpg',
                                action=MessageTemplateAction(
                                    label='view',
                                    text='課程類別3'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://example.com/example.jpg',
                                action=URITemplateAction(
                                    label='view',
                                    uri='link'
                                )
                            )
                        ]
                    )
                )
        ]
    #專題
    elif text.find('專題介紹2')!=-1:
        message = [
            TextSendMessage(text='alt_text'),
            TemplateSendMessage(
                alt_text='\udbc0\udc2dtemplate\udbc0\udc2d',
                template = ButtonsTemplate(
                            thumbnail_image_url="https://example.com/example.jpg",
                            title='alt_text',
                            text='alt_text',
                            actions=[
                                URIAction(
                                    label='alt_text',
                                    uri='alt_url'
                                ),
                                URIAction(
                                    label='alt_text',
                                    uri='alt_url'
                                )
                            ]
                )
            )
        ]
    elif text.find('專題')!=-1:
        message = [
            TextSendMessage(text='alt_text'),
            TemplateSendMessage(
                alt_text='alt_text',
                template = ButtonsTemplate(
                            thumbnail_image_url="https://example.com/example.jpg",
                            title='專題研究',
                            text='查看專題研究相關...',
                            actions=[
                                PostbackAction(
                                    label='專題介紹1',
                                    data='研究'
                                ),
                                MessageAction(
                                    label='專題介紹2',
                                    text='alt_text'
                                ),
                                URIAction(
                                    label='專題介紹3',
                                    uri='alt_url'
                                )
                            ]
                )
            )
        ]
    #系上活動
    elif re.search('系上.*活動',text):
        message = TextSendMessage(text='alt_text')
    elif text.find('學業')!=-1:
        message = TemplateSendMessage(
                alt_text='alt_text',
                template = ButtonsTemplate(
                            title='想了解學業哪個部分呢',
                            text='點選查看更多...',
                            actions=[
                                MessageAction(
                                    label='修課',
                                    text='alt_text'
                                ),
                                MessageAction(
                                    label='專題',
                                    text='alt_text'
                                ),
                                MessageAction(
                                    label='系上活動',
                                    text='alt_text'
                                )
                            ]
                )
            )
    #interest/hobbies
    elif text.find('興趣')!=-1:
        message = TemplateSendMessage(
                alt_text='alt_text',
                template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://example.com/example.jpg',
                        action=PostbackTemplateAction(
                            label='learn more',
                            data='興趣1'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://example.com/example.jpg',
                        action=PostbackTemplateAction(
                            label='learn more',
                            data='興趣2'
                        )
                    )
                ]
            )
        )
    #其他
    elif text.find('github')!=-1:
        message = [
            TextSendMessage(text='這裡是我的github連結~'),
            TextSendMessage(text='[GitHub Link]')
        ]
    elif text.find('介紹')!=-1:
        message = [
            TextSendMessage(text=intro_text),
            TextSendMessage(text='請多指教！'),
            TemplateSendMessage(
                alt_text='alt_text',
                template = ButtonsTemplate(
                            text='了解更多...',
                            actions=[
                                MessageAction(
                                    label='學業',
                                    text='說說學業的部分吧'
                                ),
                                MessageAction(
                                    label='專業能力',
                                    text='你有什麼專業能力呢？'
                                ),
                                MessageAction(
                                    label='興趣',
                                    text='你的興趣？'
                                )
                            ]
                )
            )
        ]
    elif text.find('認識')!=-1 or text.find('知道')!=-1 or text.find('了解')!=-1:
        message = [
            TextSendMessage(text='好啊 想知道什麼呢？'),
            profile
        ]
    else:
        message = [
            TextSendMessage(text='Hi！這裡有一些我可以回答的問題哦\U0001F636'),
            profile,
            TextSendMessage(text='或是點選下方選單\U0001F447')
        ]
    line_bot_api.reply_message(event.reply_token, message)

@handler.add(PostbackEvent)
def handle_postback(event):
    #興趣
    if event.postback.data == '興趣1':
        message = [
            TextSendMessage(text='alt_text_1'),
            TextSendMessage(text='alt_text_2'),
            TextSendMessage(text='alt_text_3'),
            TextSendMessage(text='alt_text_4')
        ]
    elif event.postback.data == '興趣2':
        message = [
            TextSendMessage(text='alt_text_1'),
            TextSendMessage(text='alt_text_2'),
            ImageSendMessage(
                    original_content_url='https://example.com/example.jpg',
                    preview_image_url='https://example.com/example.jpg'
            )
        ]
    #研究
    elif event.postback.data == '研究':
        message = TextSendMessage(text=research_text)
    else:
        message=''
    line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
