import discord
import configparser
from utils.database import Database
from utils.download import Downloader, create_metadata
from utils.convert import translate_and_convert
from utils.config import TMP_TXT_PATH, SOURCE_NAME, GOOGLE_DRIVE_PATH, get_OUTPUT_PATH
from utils.google_drive import upload

DOWNLOADER = Downloader()
client = discord.Client()
config = configparser.ConfigParser()
config.read('./.keys/config.ini')

def convert2fullwidth(input_string:str) ->str:
    output = []
    for s in input_string:
        if s.isascii():
            output.append(chr(0xFEE0 + ord(s)))
        else:
            output.append(s)
    return "".join(output)

def generate_search_result_msg(result:list) -> str:
    max_len_of_book = max([len(m['novel_name']) for m in result])
    max_len_of_src = max([len(SOURCE_NAME[i['source_idx']]) for i in result])
    gap = "   "
    len_line = 3 * 2 + max_len_of_book *2 + max_len_of_src * 2 + len(gap) * 2
    msgs = ["```",
            '下載列表:',
        "╔" + "═" * len_line + "╗",]

    formatted_str = "║ {idx:{space}<3}  {novel_name:{space}<{max_len_of_book}}{gap}{source:{space}<{max_len_of_src}}{gap}║"
    line = formatted_str.format(idx='索引',
                            novel_name='小說名稱', 
                            max_len_of_book = max_len_of_book,
                            source = '資料來源',
                            max_len_of_src = max_len_of_src,
                            gap=gap,
                            space=chr(12288),
                            )
    msgs.append(line)
    msgs.append("║" + "═" * len_line + "║")
    for i, metadata in enumerate(result):
        novel_name, source_idx = metadata['novel_name'], metadata['source_idx']
        line = formatted_str.format(idx=convert2fullwidth(str(i)),
                                novel_name=convert2fullwidth(novel_name), 
                                max_len_of_book = max_len_of_book,
                                source = SOURCE_NAME[source_idx],
                                max_len_of_src = max_len_of_src,
                                gap=gap,
                                space=chr(12288),
                                )
        msgs.append(line)
    msgs.append("╚" + "═" * len_line + "╝")
    msgs.append("```")
    return '\n'.join(msgs)


def mention_msg(user_id:int, msg:str="") -> str:
    """Mention people with id
    Args:
        user_id: id of people
        msg: the message sended
    Return:
        the message which   is sended
    """
    return  f'<@{user_id}>\n{msg}'

def link_message(user_id:str, novel_name:str, novel_link:str) -> str:
    msg = f'小說名稱：**《{novel_name}》**\n' + f'下載連結：{novel_link}'
    return mention_msg(user_id, msg)

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
            await channel.send(mention_msg(user.id, "搜尋不到此小說!"))
        else:
            # Send search result
            await channel.send(mention_msg(user.id, generate_search_result_msg(result) + '請問要下載哪個?'))

            # Get the answer of the user
            msg = await client.wait_for('message', check=lambda m: (user == m.author and m.channel == channel))
            # TODO Error
            if not msg.isnumeric() or int(msg.content) > len(result):
                pass
                # return
            
            book = result[int(msg.content) - 1]
            novel_name, novel_idx, source_idx = book['novel_name'],book['novel_idx'],book['source_idx']
            
            # Search database
            # If this novel exists, then interrupt and send the link to user
            download_metedata = (f'{novel_name}.epub', source_idx)
            book_id = database.get_download(str(download_metedata))
            if book_id!= None:
                await channel.send(link_message(user.id, novel_name, GOOGLE_DRIVE_PATH.format(book_id)))
                return

            # Download novel
            await channel.send('正在下載《{}》！'.format(novel_name))
            DOWNLOADER.download(create_metadata(novel_name, novel_idx, source_idx))
            # Translate and convert novel
            if translate_and_convert(TMP_TXT_PATH, get_OUTPUT_PATH(novel_name)):
                # Upload file into google drive
                novel_link = upload(file=download_metedata, local_file_path=get_OUTPUT_PATH(novel_name))
            await channel.send(link_message(user.id, novel_name, novel_link))
   
if __name__ == "__main__"  : 
    client.run(config.get('discord-bot', 'TOKEN'))