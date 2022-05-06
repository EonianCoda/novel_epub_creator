import discord
import configparser
from utils.download import Downloader, create_metadata
from utils.convert import read_file, simple2Trad, create_ebook,translate_and_convert
from utils.config import TMP_TXT_PATH, LINE_BOT_TEMPLATE_FILE_PATH, get_OUTPUT_PATH
from utils.google_drive import upload
from utils.config import WEB_NAME
DOWNLOADER = Downloader()
client = discord.Client()
config = configparser.ConfigParser()
config.read('./.keys/config.ini')
@client.event
async def on_ready():
    print('目前登入身份：',client.user)

@client.event
async def on_message(message):
   
    if message.author == client.user:
        return
   
    if message.content.startswith('搜尋'):
        # user = message.user
        channel = message.channel
        data = message.content.split(" ")
        print(data)
        result = DOWNLOADER.search(data[1])
        if result == None :
            await channel.send("搜尋不到此小說!!")
        else:
            name = [[i['novel_name'],WEB_NAME[i['source_idx']]] for i in result]
            await channel.send('\n'.join(str(i) for i in name))
            await channel.send('要下載哪一個?')
            # def check(m):
            #     return   user == m.author and m.channel == channel
            msg = await client.wait_for('message')
            book = result[int(msg.content)-1]
            novel_name, novel_idx, source_idx = book['novel_name'],book['novel_idx'],book['source_idx']
            await channel.send('正在下載{}!'.format(novel_name))
            DOWNLOADER.download(create_metadata(novel_name, novel_idx, source_idx))
            if translate_and_convert(TMP_TXT_PATH, get_OUTPUT_PATH(novel_name)):
                # upload file
                file_name = "{}.epub".format(novel_name)
                link = upload(filename=file_name, local_file_path=get_OUTPUT_PATH(novel_name))
            await channel.send('{}連結:{}'.format(novel_name,link))

client.run(config.get('discord-bot', 'TOKEN'))