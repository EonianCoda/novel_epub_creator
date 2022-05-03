from opencc import OpenCC
import re, os
from utils.ebook import Ebook
from utils.config import MAX_CHAPTER_NAME_LEN

FINDS = [u'第(\d)+[章卷]',
        '第[一二三四五六七八九十千百零兩]+[章卷]',
        '序章']

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
    encodings = ['gbk','big5','utf-8']
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


def get_search(line:str):
    if len(line) > MAX_CHAPTER_NAME_LEN:
        return False
    for f in FINDS:
        search = re.search(f, line, re.DOTALL)
        if search != None:
            return search
    return False
    
def create_ebook(lines:list, output_name:str):
    """Create an Ebook
    Args:
        book_name : the name of the book(inner name)
        output_name : the name of the output file(.epub)
    Return: list of the chapter names of the book
    """
    # Create new book
    book_name = os.path.basename(output_name).replace('.epub','')
    book = Ebook(name=book_name)

    content = "<p>" # the content of the chapter
    chapter_name = "" # the name of the chapter
    chapter_names = []
    for line in lines:
        if len(line.strip()) != 0:
            # Fine whether this line is the name of the chapter
            if get_search(line):
                # If True, mean find the next chapter, then add current chapter into the book
                if chapter_name:
                    content += "</p>"
                    book.add_chapter(chapter_name, content)
                    content = "<p>"
                chapter_name = line
                chapter_names.append(chapter_name)
                continue
            content += "<br>" + line + "<br>"
    # Add last chpater into the book
    content += "</p>"
    book.add_chapter(chapter_name, content)

    # Output book
    book.write(output_name)
    return chapter_names





