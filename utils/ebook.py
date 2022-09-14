from ebooklib import epub
import os

# Encoding
Taiwan = "zh-TW"
class Ebook(object):
    def __init__(self):
        # Initialize ebook
        self.book = epub.EpubBook()
        self.book.set_language(Taiwan)
        # the index of the chapter
        self.index = 0
        # basic spine and toc
        self.book.spine = []
        self.book.toc = []

        # for this class
        self.has_cover = False
        self.unique_img_page = False
        self.chapter_spine = []
        self.chapter_toc = []
        
    def _set_css(self):
        """set CSS style for this book 
        """
        # define CSS style
        style = 'BODY {color: white;}' 
        nav_css = epub.EpubItem(uid= "style_nav" , file_name= "style/nav.css" , media_type= "text/css" , content=style)
        self.book.add_item(nav_css)

    def _add_nav(self):
        """add navigation
        """
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

    def add_chapter(self,title:str, content:str):
        """add chapter
        Args:
            tilte: the title of the chapter
            content: the content of the chapter
        """
        page_file_name = '{}.xhtml'.format(self.index)
        # Add new page
        chapter = epub.EpubHtml(title=title, file_name=page_file_name, lang= Taiwan)
        chapter.set_content("<h1>%s%s%s" % (title ,r'</h>' ,content))
        
        self.book.add_item(chapter) # add item into book directory
        self.chapter_spine.append(chapter) # add item into book
        self.chapter_toc.append(epub.Link(page_file_name, title, str(self.index))) # Set nav
        self.index += 1

    def set_cover(self, img_path:str):
        cover_img = open(img_path,'rb').read()
        self.book.set_cover("cover.jpg", content=cover_img, create_page=True)
        self.book.items[-1].is_linear = True
        self.has_cover = True
        
    def _add_img(self, img_path:str):
        if '.jpg' not in img_path:
            raise ValueError("img_path should be a jpeg file!")
        file_name = os.path.basename(img_path)
        img = epub.EpubImage()
        img.file_name = file_name
        img.media_type = 'image/jpeg'
        img.content = open(img_path,'rb').read()
        self.book.add_item(img)

    def add_image_page(self, img_dir:str, unique=False):
        """Add image page for this book
        Args:
            img_dir: the directory containing images
            unique: if True, then this page will be add into 2-th page of this book(first page will be cover); if False, then this page will be add as normal page
        """
        if self.unique_img_page == True and unique:
            raise ValueError("One book should have one unique iamge page!")
        img_template = '<img src="{}"><br><br>'
        # Add new page for images
        if unique:
            self.unique_img_page = True
            page_file_name = 'imgs.xhtml'
            title = "彩頁"
            page_id = "imgs"
        else:
            page_file_name =   '{}.xhtml'.format(self.index)
            title = "彩頁{}".format(self.index)
            self.index += 1
            page_id = self.index
        img_page = epub.EpubHtml(title=title, file_name=page_file_name, lang=Taiwan)
        img_page.id = page_id
        content = f'<h1>{title}' + r'</h>'
        # Add images into the page
        imgs = os.listdir(img_dir)
        for i in range(0, len(imgs)):
            file_name = f'{i}.jpg'
            path = os.path.join(img_dir, file_name)
            self._add_img(path)
            content += img_template.format(file_name)
        img_page.set_content(content)
        # Add Items
        self.book.add_item(img_page)
        if not unique:
            self.chapter_spine.append(img_page)
            self.chapter_toc.append(epub.Link(page_file_name, title, str(self.index))) # Set nav

    def write(self, output_path:str, author:str=""):
        """Output file(.epub)
        Args:
            output_path: the path of output file
        """
        # Set spine and toc
        spine = []
        toc = []
        if self.has_cover:
            spine.append("cover")
        if self.unique_img_page:
            spine.append("imgs")
            toc.append(epub.Link("imgs.xhtml","彩頁",'imgs'))
        
        spine.append('nav')
        toc.append(epub.Link("nav.xhtml","目錄",'nav'))
        spine += self.chapter_spine
        toc += self.chapter_toc
        self.book.spine = spine
        self.book.toc = toc
        # Set author
        if author == "":
            author = "Novel Epub Creator Robot"
        self.book.add_author(author)
        # Set title
        file_name = os.path.basename(output_path)
        title = file_name.replace('.epub','')
        self.book.set_title(title)
        # Set identifier
        self.book.set_identifier(title + ' ' + author)
        # Set toc and spine
        self.chapter_toc

        # Set css style and add navigation
        self._set_css()
        self._add_nav()
        # If output_path contains path, then create them
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        if '.epub' not in output_path:
            output_path += '.epub'

        epub.write_epub(output_path, self.book)