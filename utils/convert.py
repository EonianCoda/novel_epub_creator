from opencc import OpenCC
import re 
import os
from utils.ebook import Ebook
from utils.config import MAX_CHAPTER_NAME_LEN, FINDS

class Ebook_creater(object):
    def __init__(self, white_list:list=[], black_list=[], max_chapter_name_len:int=-1):
        self.white_list = white_list
        self.black_list = black_list
        self.max_chapter_name_len = max_chapter_name_len

        if len(self.white_list) == 0:
            self.white_list = FINDS
        if isinstance(black_list, str):
            if black_list != "":
                black_list = [black_list]
            else:
                black_list = []
        if self.max_chapter_name_len == -1:
            self.max_chapter_name_len = MAX_CHAPTER_NAME_LEN
        
    def in_black_list(self, line:str):
        for f in self.black_list:
            if f in line:
                return True
        return False
    def get_search(self, line:str):
        if len(line) > self.max_chapter_name_len:
            return False
        for f in self.white_list:
            search = re.search(f, line, re.DOTALL)
            if search != None:
                return search
        return False
    
    def create_ebook(self, lines:list, output_name:str, author:str="", imgs_path:str=""):
        """Create an Ebook
        Args:
            book_name : the name of the book(inner name)
            output_name : the name of the output file(.epub)
        Return: 
            list of the chapter names of the book
        """
        # Create new book
        #book_name = os.path.basename(output_name).replace('.epub','')
        book = Ebook()

        content = "<p>" # the content of the chapter
        chapter_name = "" # the name of the chapter
        chapter_names = []
        for line in lines:
            if len(line.strip()) != 0:
                # Fine whether this line is the name of the chapter
                if self.get_search(line) and not self.in_black_list(line):
                    # If True, mean find the next chapter, then add current chapter into the book
                    if chapter_name:
                        content += "</p>"
                        book.add_chapter(chapter_name, content)
                        content = "<p>"
                    chapter_name = line
                    chapter_names.append(chapter_name)
                    continue
                line = line.strip()
                content += "<br>" + line + "<br>"
        # Add last chpater into the book
        content += "</p>"
        book.add_chapter(chapter_name, content)

        if imgs_path != "":
            book.set_cover( os.path.join(imgs_path, "0.jpg"))
            book.add_image_page(imgs_path, True)

        # Output book
        book.write(output_name, author)
        return chapter_names

def translate_and_convert(input_path:str, output_path:str, white_list:list=[], black_list=[], max_chapter_name_len:int=-1, author:str="",imgs_path:str=""):
    content = read_file(input_path)
    if content == None:
        raise UnicodeDecodeError
    content = simple2Trad(content)
    lines = content.splitlines(True)

    ebook_creater = Ebook_creater(white_list, black_list, max_chapter_name_len)
    return ebook_creater.create_ebook(lines, output_path,author, imgs_path)


# def translate_and_convert_japanese(input_path:str, output_path:str, white_list:list=[], black_list=[], max_chapter_name_len:int=-1):
#     content = read_file(input_path)
#     if content == None:
#         raise UnicodeDecodeError
#     content = simple2Trad(content)
#     lines = content.splitlines(True)

#     ebook_creater = Ebook_creater(white_list, black_list, max_chapter_name_len)
#     return ebook_creater.create_ebook(lines, output_path)

def simple2Trad(content:str):
    """Translate Simplified Chinese to tradtional Chinese
    Args:
        content: str, string for converted
    """
    cc = OpenCC('s2twp')
    content = cc.convert(content)
    return content

def Trad2simple(content:str):
    """Translate tradtional Chinese to Simplified Chinese
    Args:
        content: str, string for converted
    """
    cc = OpenCC('t2s')
    content = cc.convert(content)
    return content

def read_file(file_name:str):
    """Read file
    """
    encodings = ['gbk','big5','utf-8','gb2312','gb18030']
    flag = False
    for encoding in encodings:
        try:
            f = open(file_name, 'r', encoding=encoding)
            content = f.read()
            flag = True
        except UnicodeDecodeError:
            continue
        finally:
            f.close()

    return content if flag else None





