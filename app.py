# from __future__ import unicode_literals
import configparser, os, json
from flask import Flask, request, abort
# LineBot
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,FlexSendMessage
# Utils
from utils.download import Downloader, create_metadata
from utils.convert import read_file, simple2Trad, create_ebook
from utils.config import TMP_TXT_PATH, LINE_BOT_TEMPLATE_FILE_PATH, get_OUTPUT_PATH
from utils.google_drive import upload

# Global Variable
DOWNLOADER = Downloader()

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('config.ini')
line_bot_api = LineBotApi(config.get('line-bot', 'CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(config.get('line-bot', 'CHANNEL_SECRET'))

def translate_and_convert_novel(novel_name:str):
    content = simple2Trad(read_file(TMP_TXT_PATH))
    with open(TMP_TXT_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    with open(TMP_TXT_PATH, "r", encoding = 'utf-8') as f:
        lines = f.readlines()
    # Create novel epub
    chapters = create_ebook(lines, get_OUTPUT_PATH(novel_name))
    # create fail
    if chapters == []:
        return False
    else:
        return True

def reply_text_message(event, msg:str):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text =msg))

# def add_option(result,temp):
#     for book_name in result:
#         opt =  {
#             "type": "button",
#             "style": "link",
#             "height": "sm",
#             "action": {
#                 "type": "message",
#                 "label": book_name,
#                 "text": book_name
#             }
#         }
#         temp['footer']['contents'].append(opt)
#     return 


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    global DOWNLOADER
    if event.source.user_id == "Udeadbeefdeadbeefdeadbeefdeadbeef":
        return

    try:
        action, data = event.message.text.split(',')
        if action == '搜尋':
            result = DOWNLOADER.search(data)
            if result == None :
                reply_text_message("搜尋不到此小說!!")
            else:
                # Create form
                form = json.load(open(LINE_BOT_TEMPLATE_FILE_PATH, 'r',encoding='utf-8'))
                form['body']['contents'][0]['text'] = data # Set title
                # Add option
                for metadata in result:
                    opt =  {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": metadata['novel_name'],
                            "text": '下載,{}&{}&{}'.format(metadata['novel_name'], metadata['novel_idx'], metadata['source_idx'])
                        }
                    }
                    form['footer']['contents'].append(opt)
                
                FlexMessage = form
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(data, FlexMessage))
        elif action == '下載':
            novel_name, novel_idx, source_idx = data.split('&')
            DOWNLOADER.download(create_metadata(novel_name, novel_idx, source_idx))
            # Success
            if translate_and_convert_novel(novel_name):
                # upload file
                file_name = "{}.epub".format(novel_name)
                link = upload(filename=file_name, local_file_path=get_OUTPUT_PATH(novel_name))
                reply_text_message(event, link)
            # Fail
            else:
                reply_text_message(event, '下載過程發生錯誤')
        else:
            reply_text_message(event, '請使用正確的指令:"搜尋,XXX"，接著選擇想下載的小說')
    except Exception as e:
        reply_text_message(event, '發生不明錯誤!\n{}'.format(e))
        print(e)
    
if __name__ == "__main__":
    app.run()