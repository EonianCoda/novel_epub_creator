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

def integrate_japanese_epubs(files:list, chapter_names:list, output_path:str):
    """
    Args:
        files: list of the path of the file
        chapter_names: the names of the chapters
        output_path: the path of output file
    """
    ebook = epub.EpubBook()
    ebook.set_language(Taiwan)
    ebook.toc = []
    all_items = []


    cover_img_content = None
    author = ""
    for book_idx, (file, name) in enumerate(zip(files, chapter_names)):
        book = epub.read_epub(file)
        if author != "":
            author = book.get_metadata('DC','creator')[0][0]
        items = []
        toc = []
        spine = []
        # add images
        for item in book.items:
            if isinstance(item, epub.EpubImage):
                item.id = f"{book_idx}_{item.id}" 
                item.file_name = f"{book_idx}_{item.file_name}"
                items.append(item)
                if cover_img_content != None:
                    cover_img_content = copy.deepcopy(item.content)
        num_imgs = len(items)
        for link in book.toc:
            uid = link.uid
            if uid == 'imgs':
                img_template = '<img src="{}"><br><br>'
                item = epub.EpubHtml(title='彩頁', file_name=f'{book_idx}_imgs.xhtml', lang=Taiwan)
                item.id = f"{book_idx}_imgs"
                content = f'<h1>彩頁' + r'</h>'
                for i in range(num_imgs):
                    content += img_template.format(f"{book_idx}_{i}.jpg")
                item.set_content(content)
                items.append(item)
                toc.append(epub.Link(item.file_name, '彩頁', item.id))
                spine.append(item.id)
            elif uid.isnumeric():
                item = book.get_item_with_id(f"chapter_{uid}")
                item.id = f"{book_idx}_{item.id}" 
                item.file_name = f"{book_idx}_{item.file_name}"
                items.append(item)

                if link.title == None or link.title.strip() == "":
                    toc.append(epub.Link(item.file_name, name, item.id))
                else:
                    toc.append(epub.Link(item.file_name, link.title, item.id))
                spine.append(item.id)
        
        all_items += items
        ebook.spine += spine
        ebook.toc.append((epub.Section(name, href=f"{book_idx}_0.xhtml"), tuple(toc)))

    for item in all_items:
        ebook.add_item(item)
    # Set spine and toc
    ebook.spine = ['nav'] + ebook.spine
    ebook.toc = [epub.Link("nav.xhtml","目錄",'nav')] + ebook.toc

    # Set Cover
    if cover_img_content != None:
        ebook.set_cover("cover.jpg", content=cover_img_content, create_page=False)

    if author == "":
        author = "Novel Epub Creator Robot"
    ebook.add_author(author)
    # Set title
    file_name = os.path.basename(output_path)
    title = file_name.replace('.epub','')
    ebook.set_title(title)
    # Set identifier
    ebook.set_identifier(title + ' ' + author)

    # define CSS style
    style = 'BODY {color: white;}' 
    nav_css = epub.EpubItem(uid= "style_nav" , file_name= "style/nav.css" , media_type= "text/css" , content=style)
    ebook.add_item(nav_css)
    # Add navigation
    ebook.add_item(epub.EpubNcx())
    ebook.add_item(epub.EpubNav())
    epub.write_epub(output_path, ebook)