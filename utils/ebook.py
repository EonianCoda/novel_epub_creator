from ebooklib import epub
import os

# Encoding
Taiwan = "zh-TW"


class Ebook(object):
    def __init__(self, author="Ebook_creator", name=""):
        
        # main body
        self.book = epub.EpubBook()
        self.book.set_identifier(author)
        self.book.set_language(Taiwan)
        
        # name of the book
        self.name = name
        # basic spine
        self.book.spine = ['nav']
        # table of content
        self.table = []
        # the index of the chapter
        self.index = 0
        
        # define CSS style
        style = 'BODY {color: white;}' 
        self.nav_css = epub.EpubItem(uid= "style_nav" , file_name= "style/nav.css" , media_type= "text/css" , content=style)
        
        # add default NCX and Nav file
        self.book.items = [epub.EpubNcx(),epub.EpubNav(),self.nav_css]
        
        self.book.toc = []
      
    def add_chapter(self,title:str, content:str):
        """add chapter
        Args:
            tilte: the title of the chapter
            content: the content of the chapter
        """
        chapter = epub.EpubHtml(title = title , file_name = str(self.index) + '.xhtml' , lang= Taiwan)
        chapter.set_content("<h1>%s%s%s" % (title ,r'</h>' ,content))
        
        self.book.add_item(chapter)
        
        self.book.spine.append(chapter)
        self.book.toc.append(epub.Link(str(self.index) + '.xhtml', title , str(self.index)))
        self.index += 1

    def clear(self):
        """Clear all variable
        """
        self.table = []
        self.index = 0
        
        
        self.book.spine = ['nav']
        self.book.toc = []
        # add default NCX and Nav file and CSS file
        self.book.items = [epub.EpubNcx(),epub.EpubNav(),self.nav_css]
        
    def write(self, file_name:str=None):
        """Output file(.epub)
        Args:
            file_name: the name of output file
        """
        # If file_name contains path, then create them
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        if file_name == None or '.epub' not in file_name:
            file_name = self.name + '.epub'


        self.book.set_title(self.name)
        epub.write_epub(file_name  , self.book, {})

        
        

       
        
        
    






