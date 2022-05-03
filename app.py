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

def add_option(result,temp):
    
    for book_name in result:
        opt =  {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
                "type": "message",
                "label": book_name,
                "text": book_name
            }
        }
        temp['footer']['contents'].append(opt)

    return 
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
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        try :
            action, data = event.message.text.split(',')
            if action == '搜尋':
                result = DOWNLOADER.search(data)
                if result == None :
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='NONO')
                    )
                else:
                    temp =  json.load(open(LINE_BOT_TEMPLATE_FILE_PATH,'r',encoding='utf-8'))
                    temp['body']['contents'][0]['text'] = data
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
                        temp['footer']['contents'].append(opt)
                    FlexMessage = temp
                    line_bot_api.reply_message(event.reply_token,FlexSendMessage(data, FlexMessage))
            elif action == '下載':
                novel_name, novel_idx, source_idx = data.split('&')
                DOWNLOADER.download(create_metadata(novel_name, novel_idx, source_idx))
                # Success
                if translate_and_convert_novel(novel_name):
                    # upload file
                    file_name = "{}.epub".format(novel_name)
                    link = upload(filename=file_name, local_file_path=get_OUTPUT_PATH(novel_name))
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text =link))
                # Fail
                else:
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text ='下載錯誤'))
            else :
                message = '請先使用[搜尋,XXX]並選擇欲下載的書目'
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text =message))
        except Exception as e:
            print(e)
            message = '錯囉，請先使用[搜尋,XXX]並選擇欲下載的書目'
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text =message))
        
if __name__ == "__main__":
    app.run()