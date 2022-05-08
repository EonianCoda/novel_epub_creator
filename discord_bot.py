import discord
import configparser
from utils.database import Database
from utils.download import Downloader, create_metadata
from utils.convert import read_file, simple2Trad, create_ebook,translate_and_convert
from utils.config import TMP_TXT_PATH, LINE_BOT_TEMPLATE_FILE_PATH, get_OUTPUT_PATH,GOOGLE_DRIVE_PATH
from utils.google_drive import upload
from utils.config import SOURCE_NAME


DOWNLOADER = Downloader()
client = discord.Client()
config = configparser.ConfigParser()
config.read('./.keys/config.ini')

def count_length(input_string:str) ->int:
    """Count the real length of input string(the length of non-ascill string is 2)
    """
    length = 0
    for s in input_string:
        if ord(s) < 128:
            length += 1
        else:
            length += 2
    return length

def link_message(id,novel_name,novel_link):
    return mention(id)+'\n小說名稱《{}\n下載連結：\n{}'.format(novel_name,novel_link)
def mention(id):
    myid = '<@{}>'.format(id)
    return myid
def full_number(number):
    fn = ''
    for i in number:
        fn += chr(ord(i)+0xfee0)
    return fn

@client.event
async def on_ready():
    print('目前登入身份：',client.user)

@client.event
async def on_message(message):
    database = Database()
    user = message.author
    channel = message.channel
    if message.author == client.user:
        return
   
    if message.content.startswith('搜尋'):
        data = message.content.split(" ")

        result = DOWNLOADER.search(data[1])
        if result == None :
            await channel.send(mention(user.id)+"搜尋不到此小說!!")
        else:
            #排版
            max_book_len = max([len(i['novel_name']) for i in result])
            max_src_len = max([len(SOURCE_NAME[i['source_idx']]) for i in result])
            formated_str = '|\t{0:\u3000<%ds}\t{1:\u3000<%ds}\t{2:\u3000<%ds}\t|' % (4,max_book_len,max_src_len)
            name = [formated_str.format(full_number(str(idx+1)),book['novel_name'],SOURCE_NAME[book['source_idx']]) for idx,book in enumerate(result)]
            border_line = '—'*len(name[0])+'\n'
            await channel.send(mention(user.id)+'\n'+border_line+
                                formated_str.format('標籤','小說名稱','資料來源')+'\n'+
                               '\n'.join(i for i in name)+'\n'+
                                border_line+'要下載哪一個？')
            
            def check(m):
                return   user == m.author and m.channel == channel
            msg = await client.wait_for('message',check=check)
            book = result[int(msg.content)-1]
            novel_name, novel_idx, source_idx = book['novel_name'],book['novel_idx'],book['source_idx']
            
            book_id = database.get_download(str(('{}.epub'.format(novel_name),source_idx)))
            if book_id!= None:
                await channel.send(link_message(user.id,novel_name,GOOGLE_DRIVE_PATH.format(book_id)))
                return

            await channel.send('正在下載《{}》！'.format(novel_name))
            DOWNLOADER.download(create_metadata(novel_name, novel_idx, source_idx))
            if translate_and_convert(TMP_TXT_PATH, get_OUTPUT_PATH(novel_name)):
                file_name = "{}.epub".format(novel_name)
                file = (file_name,source_idx)
                novel_link = upload(file =file, local_file_path=get_OUTPUT_PATH(novel_name))
            await channel.send(link_message(user.id,novel_name,novel_link))
   
if __name__ == "__main__"  : 
    client.run(config.get('discord-bot', 'TOKEN'))