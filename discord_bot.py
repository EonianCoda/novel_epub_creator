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

def convert2fullwidth(input_string:str)->str:
    output = []
    for s in input_string:
        if s.isascii():
            output.append(chr(0xFEE0 + ord(s)))
        elif s == '"' or s == "'":
            continue
        else:
            output.append(s)
    return "".join(output)

def generate_result_lines(result:list) -> str:
    max_len_of_book = max([len(m['novel_name']) for m in result])
    max_len_of_src = max([len(SOURCE_NAME[i['source_idx']]) for i in result])
    gap = chr(12288) * 2
    len_line = 1 + 4 * 2 + max_len_of_book *2 + max_len_of_src * 2 + len(gap) * 2 * 2
    formatted_str = "` {idx:{space}<4}  {novel_name:{space}<{max_len_of_book}}{gap}{source:{space}<{max_len_of_src}}{gap}`"
    
    msgs = []
    msgs.append('下載列表：')
    header_line = formatted_str.format(idx='索引',
                            novel_name='小說名稱', 
                            max_len_of_book = max_len_of_book,
                            source = '資料來源',
                            max_len_of_src = max_len_of_src,
                            gap=gap,
                            space=chr(12288),
                            )
    msgs.append(header_line)
    msgs.append('`' + "─" * len_line + '`')
    for i, metadata in enumerate(result):
        novel_name, source_idx = metadata['novel_name'], metadata['source_idx']
        line = formatted_str.format(idx=convert2fullwidth(str(i + 1)),
                                novel_name=convert2fullwidth(novel_name), 
                                max_len_of_book = max_len_of_book,
                                source = SOURCE_NAME[source_idx],
                                max_len_of_src = max_len_of_src,
                                gap=gap,
                                space=chr(12288),
                                )
        msgs.append(line)
    return msgs

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
            lines = generate_result_lines(result)
            # Contain header lines
            header_msg = "\n".join(lines[:3]) + '\n'
            len_line = len(lines[3]) + 1
            cur_idx = 0
            line_len_limit = 2000
            while cur_idx < (len(lines) - 3):
                msg = ""
                # Add header
                if cur_idx == 0:
                    next_idx = cur_idx + int((line_len_limit - len(header_msg)) / len_line) - 1
                    msg = header_msg 
                else:
                    next_idx = cur_idx + int(line_len_limit / len_line) - 1
                msg += "\n".join(lines[3 + cur_idx: 3 + next_idx])
                await channel.send(msg)
                cur_idx = next_idx

            await channel.send(mention_msg(user.id, '亲，請問要下載哪個?'))

            # Get the answer of the user
            msg = await client.wait_for('message', check=lambda m: (user == m.author and m.channel == channel))
            if not msg.content.isnumeric() or int(msg.content) > len(result) or int(msg.content) <= 0:
                await channel.send(mention_msg(user.id, "亲，您的索引不在单上呢，请再试试"))
                return
            
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
            success = DOWNLOADER.download(create_metadata(novel_name, novel_idx, source_idx))
            # downloader error
            if not success:
                await channel.send(mention_msg(user.id,"亲，下載失敗，請換個來源试试"))
                return

            # Translate and convert novel
            try:
                result = translate_and_convert(TMP_TXT_PATH, get_OUTPUT_PATH(novel_name))
            except UnicodeDecodeError:
                await channel.send(mention_msg(user.id,"亲，檔案解碼失敗，請換個來源试试"))
                return
            #TODO Catch chapter error
            if result == []:
                pass
            # Upload file into google drive
            novel_link = upload(file=download_metedata, local_file_path=get_OUTPUT_PATH(novel_name))
            await channel.send(link_message(user.id, novel_name, novel_link))
   
if __name__ == "__main__"  : 
    client.run(config.get('discord-bot', 'TOKEN'))