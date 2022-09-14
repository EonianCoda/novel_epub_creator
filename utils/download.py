import urllib
from urllib.request import urlopen, Request
from urllib.parse import quote
from urllib import parse
import os
import shutil
import string
import glob
import patoolib
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


from utils.database import Database 
from utils.config import TMP_DIRECTORY, TMP_TXT_PATH, TMP_RAR_PATH, TMP_ZIP_PATH, USE_DATABASE, reset_TMP_DIRECTORY
from utils.convert import simple2Trad, Trad2simple

import requests
from requests.cookies import RequestsCookieJar
import pickle
import time
import threading
WENKU8_COOKIE_FILE = "wenku8_cookie.pickle"



def open_url(url, decode=True, post_data=None, return_response=False):
    """
    Args:
        url: url
        decode: boolean, whether decode the html
    Return: if decode is True, then return BeautifulSoup, else return bytes
    """
    
    headers={'User-Agent':UserAgent().chrome}
    request = Request(url, headers=headers, data=post_data)

    # decode html for search
    response = urlopen(request)
    if return_response:
        return response

    content = response.read()
    # for download file 
    if not decode:
        return content
    else:
        encodings = ['utf-8','gb2312','gb18030']
        for encoding in encodings:
            try:
                html = content.decode(encoding)
                return BeautifulSoup(html, 'html.parser')
            except UnicodeDecodeError:
                continue
        html = content.decode('gb18030','ignore')
        return BeautifulSoup(html, 'html.parser')

def download_file(url, output_path:str):
    if os.path.dirname(output_path) == TMP_DIRECTORY:
        reset_TMP_DIRECTORY()
    file = open_url(url, decode=False)
    with open(output_path, 'wb') as f:
        f.write(file)

def extract_and_move_file(is_rar=True):
    if is_rar:
        file_path = TMP_RAR_PATH
    else:
        file_path = TMP_ZIP_PATH

    patoolib.extract_archive(file_path, outdir=TMP_DIRECTORY)
    files = glob.glob(os.path.join(TMP_DIRECTORY,'*.txt'))
    shutil.move(files[0], TMP_TXT_PATH)

def encode_chinese(data, is_post_data=False, encoding="utf-8"):
    SAFE_LETTER = string.digits + string.ascii_letters + string.punctuation
    # is post data
    if is_post_data:
        return parse.urlencode(data, encoding=encoding).encode()
    # is url
    else:
        return quote(data, safe=SAFE_LETTER)

def create_metadata(novel_name:str, novel_idx:int, source_idx:str=None, author:str=None):
    """Create metadata for downloader
    Args:
        novel_name: the name of the novel
        novel_idx: the index of the novel
    """
    metadata = {'novel_name': novel_name, 
                'novel_idx': int(novel_idx), 
                'source_idx': source_idx,
                'author': author}
    return metadata

def all_match(metadatas:list, keyword:str):
    for metadata in metadatas:
        if keyword == metadata['novel_name']:
            return True
    return False

class Downloader(object):
    def __init__(self, search_all_source=False, use_database=USE_DATABASE):
        self.downloader = {'Zxcs': Zxcs_downloader(),     # 知軒藏書
                            'Mijjxswco':Mijjxswco_downloader(),  # 久久小說下載網
                            'Ijjxs':Ijjxs_downloader(), # 愛久久小說下載網
                            # 'Qiuyewx':Qiuyewx_downloader(), # 平板电子书网
                            #'Qinkan':Qinkan_downloader(),  # 請看小說網
                            'Xsla':Xsla_downloader(), }  # 八零电子书 (Too slow)
        self.search_all_source = search_all_source
        self.use_database = use_database
        if self.use_database:
            self.database = Database()
    def search(self, key_word:str) -> list:
        """Search novel by key word
        Args:
            key_word: the key word for search
        Return:
            a list of all result's metadatas
        """
        # If use database, then search database by keyword
        if self.use_database:
            result = self.database.get_search(key_word)
            # If find, then return
            if result != None:
                return result
        novels_metadata = []
        for source_idx, downloader in self.downloader.items():
            metadatas = downloader.search(key_word)
            if metadatas != None:
                # add source_idx
                for metadata in metadatas:
                    metadata['source_idx'] = source_idx
                novels_metadata.extend(metadatas)

        if len(novels_metadata) != 0:
            if self.use_database:
                self.database.add_search(key_word, novels_metadata)
            return novels_metadata
        else:
            if self.use_database:
                self.database.add_search(key_word, None)
            return None

    def download(self, metadata:dict) -> bool:
        """
        Args:
            metadata: tuple of a book's metadata
        Return:
            If success downloader, return True, else return False
        """
        source_idx = metadata['source_idx']
        try:
            self.downloader[source_idx].download(metadata)
        # Site can't be reached or no response
        except urllib.error.URLError as e:
            print(f"Some error in download, {e}")
            return False
        return True

class Japanese_downloader(object):
    def __init__(self, search_all_source=False, use_database=USE_DATABASE):
        self.downloader = {'Wenku8': Wenku8_downloader(),}     # 輕小說文庫
        self.search_all_source = search_all_source
        self.use_database = use_database
        if self.use_database:
            self.database = Database(is_japanese=True)
    def search(self, key_word:str) -> list:
        """Search novel by key word
        Args:
            key_word: the key word for search
        Return:
            a list of all result's metadatas
        """
        # If use database, then search database by keyword
        if self.use_database:
            result = self.database.get_search(key_word)
            # If find, then return
            if result != None:
                return result
        novels_metadata = []
        for source_idx, downloader in self.downloader.items():
            metadatas = downloader.search(key_word)
            if metadatas != None:
                # add source_idx
                for metadata in metadatas:
                    metadata['source_idx'] = source_idx
                novels_metadata.extend(metadatas)

        if len(novels_metadata) != 0:
            if self.use_database:
                self.database.add_search(key_word, novels_metadata)
            return novels_metadata
        else:
            if self.use_database:
                self.database.add_search(key_word, None)
            return None

    def download(self, metadata:dict) -> bool:
        """
        Args:
            metadata: tuple of a book's metadata
        Return:
            If success downloader, return True, else return False
        """
        source_idx = metadata['source_idx']
        try:
            self.downloader[source_idx].download(metadata)
        # Site can't be reached or no response
        except urllib.error.URLError as e:
            print(f"Some error in download, {e}")
            return False
        return True


class Zxcs_downloader(object):
    """Download novel from websit: http://zxcs.me/ (知軒藏書)
    """
    def __init__(self):
        self.base_url = "http://zxcs.me/index.php?keyword={}&page={}"
        self.search_url = lambda key, p : encode_chinese(self.base_url.format(Trad2simple(key),p))
    def __str__(self) -> str:
        return "Zxcs"
    def search_page(self, key_word:str, page=1):
        """Search novel with key word for one page
        Return:
            if not found return None, else return dict: {novel_name:novel_idx}
        """
        soup = open_url(self.search_url(key_word, page))
        # No Result
        if soup.find('dl',id="plist") == None:
            return None
        link_list = [element.find('dt').find('a') for element in soup.find_all('dl',id="plist")] 
        # Get novel name and their index
        novels_metadata = []
        for l in link_list:
            novel_name = l.text.split('》')[0][1:]
            novel_name = simple2Trad(novel_name)
            url = l.get('href')
            novel_idx = url.split('/')[-1]
            novels_metadata.append(create_metadata(novel_name, novel_idx))
            
        pages = soup.find('div',id="pagenavi").find_all('a')
        if pages == []:
            num_pages = 1
        else:
            num_pages = int(pages[-1].get('href').split('=')[-1])
        
        return novels_metadata, num_pages

    def search(self, key_word:str):
        result = self.search_page(key_word, page=1)
        if result == None:
            return None

        novels_metadatas, num_pages = result
        if num_pages != 1:
            for i in range(num_pages):
                result = self.search_page(key_word, i)
                if result == None:
                    continue
                novels_metadata, _ = result
                novels_metadatas.extend(novels_metadata)
        return novels_metadatas

    def download(self, metadata:dict):
        # Get download link
        novel_name, novel_idx = metadata['novel_name'], metadata['novel_idx']
        # Get download link
        download_url = "http://zxcs.me/download.php?id={}".format(novel_idx)
        soup = open_url(download_url)
        files = soup.find_all("span",class_="downfile")

        flag = False
        for file_url in files:
            try:
                file_url = file_url.find('a').get('href')
                file_url = encode_chinese(file_url)
                # Download rar
                download_file(file_url, TMP_RAR_PATH)
                extract_and_move_file()
                flag = True
                break
            except urllib.error.URLError:
                continue
        if flag:
            return True
        else:
            return False

class Ijjxs_downloader(object):
    """Download novel from websit: https://www.ijjxs.com/ (愛久久小說下載網)
    """
    def __init__(self):
        self.base_url = "https://www.ijjxs.com"
        self.search_url = self.base_url + '/e/search/index.php'
    def __str__(self) -> str:
        return "Ijjxs"
    def search(self, key_word:str):
        post_data = {'keyboard':Trad2simple(key_word),'show':'title,writer'}
        post_data = encode_chinese(post_data, is_post_data=True)
        soup = open_url(self.search_url, post_data=post_data)

        results = soup.find_all('a',class_='searchtitle')
        if results == []:
            return None
        novels_metadata = []
        for result in results:
            novel_name = result.text
            url = result.get('href')
            novel_idx = url.split('/')[-1].split('.')[0]
            novels_metadata.append(create_metadata(novel_name, novel_idx))

        return novels_metadata

    def download(self, metadata:dict):
        # Get download link
        novel_name, novel_idx = metadata['novel_name'], metadata['novel_idx']
        novel_name = Trad2simple(novel_name)

        download_url = f"{self.base_url}/txt/{novel_idx}.html"
        soup = open_url(download_url)
        download_url = soup.find('li', class_="downAddress_li").find('a').get('href')
        download_url = self.base_url + download_url
        soup = open_url(download_url)
        # Download txt
        download_url = self.base_url + soup.find('a',class_="strong green").get('href')
        download_file(download_url, TMP_TXT_PATH)

class Mijjxswco_downloader(object):
    """Download novel from websit: https://m.ijjxsw.co/ (久久小說下載網)
    """
    def __init__(self):
        self.base_url = "https://m.ijjxsw.co/"
        self.search_url = self.base_url + 'search/'
    def __str__(self) -> str:
        return "Mijjxswco"
    def search(self, key_word:str):
        post_data = {'searchkey' : Trad2simple(key_word)}
        post_data = encode_chinese(post_data, is_post_data=True)
        soup = open_url(self.search_url, post_data=post_data)

        results = soup.find_all('div',class_="list_a")
        if results == []:
            return None
        
        results = [element.find_all('a')[1] for element in results]
        novels_metadata = []
        for result in results:
            novel_name = simple2Trad(result.text)
            url = result.get('href')
            novel_idx = url.split('/')[-1].split('.')[0]
            novels_metadata.append(create_metadata(novel_name, novel_idx))
            
        return novels_metadata
    def download(self, metadata:dict):
        # Get download link
        novel_name, novel_idx = metadata['novel_name'], metadata['novel_idx']
        novel_name = Trad2simple(novel_name)

        download_url = "https://m.ijjxsw.co/api/txt_down.php?articleid={}&amp;articlename={}".format(novel_idx, novel_name)
        download_url = encode_chinese(download_url)

        # Download txt
        download_file(download_url, TMP_TXT_PATH)

class Qiuyewx_downloader(object):
    """Download novel from websit: https://www.qiuyewx.com/ (平板電子書網)
    """
    def __init__(self):
        self.base_url = "https://www.qiuyewx.com/"
        self.search_url = self.base_url + 'modules/article/search.php'
    def __str__(self) -> str:
        return "Qiuyewx"
    def search(self, key_word:str):
        post_data = {'searchkey':Trad2simple(key_word)}
        post_data = encode_chinese(post_data, is_post_data=True)
        soup = open_url(self.search_url, post_data=post_data)

        results = soup.find_all('div', class_="zhuopin")
        if results == []:
            return None

        novels_metadata = []
        for result in results:
            result = result.find('div',class_="book_info").find('a')
            novel_name = result.text
            url = result.get('href')
            novel_idx = url.split('/')[-1].split('.')[0]
            novels_metadata.append(create_metadata(simple2Trad(novel_name), novel_idx))

        return novels_metadata

    def download(self, metadata:dict):
        # Get download link
        novel_name, novel_idx = metadata['novel_name'], metadata['novel_idx']
        novel_name = Trad2simple(novel_name)

        download_url = "https://txt.qiuyewx.com/zip/{}/{}.txt".format(novel_idx, novel_name)
        download_url = encode_chinese(download_url)

        # Download txt
        download_file(download_url, TMP_TXT_PATH)

class Qinkan_downloader(object):
    """Download novel from websit: http://www.qinkan.net/ (請看小說網)
    """
    def __init__(self):
        self.base_url = "http://www.qinkan.net/"
        self.search_url = 'http://www.qinkan.net/e/search/index.php'
    def __str__(self) -> str:
        return "Qinkan"
    def search_page(self, url:str):
        soup = open_url(url)
        results = soup.find('div', class_="listBoxs").find('ul').find_all('li')
        novels_metadata = []

        for result in results:
            novel_name = simple2Trad(result.find('a').text)
            novel_name = novel_name.split('》')[0][1:]
            url = result.find('a').get('href')
            novel_idx = url.split('/')[-1].split('.')[0]
            novels_metadata.append(create_metadata(novel_name, novel_idx))
        return novels_metadata

    def search(self, key_word:str):
        # Encoding post data
        post_data = {'tbname':'txt', 'tempid':'1','keyboard':Trad2simple(key_word), 'show':'title,smalltext,writer'}
        post_data = encode_chinese(post_data, is_post_data=True, encoding='gb2312')

        response = open_url(self.search_url, post_data=post_data, return_response=True)
        # Get response url for anther page
        url = response.geturl()

        # Search fail
        if "index.php" in url:
            return None

        soup = BeautifulSoup(response.read().decode('gb18030'), 'html.parser')
        results = soup.find('div', class_="listBoxs").find('ul').find_all('li')
        if results == []:
            return None

        num_novels = int(soup.find('h1').find('strong').text)
        num_pages = int((num_novels - 1) / 30) + 1
        paged_url = (url.split('-')[0] + '-{}-' + url.split('-')[-1])

        novel_metadatas = []
        # Search pages
        for i in range(num_pages):
            metadatas = self.search_page(paged_url.format(i))
            novel_metadatas.extend(metadatas)
            # Max pages = 15
            if i == 15:
                break
        return novel_metadatas

    def download(self, metadata:dict):
        # Get download link
        novel_name, novel_idx = metadata['novel_name'], metadata['novel_idx']
        novel_name = Trad2simple(novel_name)
        download_url = "http://www.qinkan.net/book/{}.html".format(novel_idx)
        soup = open_url(download_url)

        # Download file
        download_url = soup.find_all('a',class_="downButton")[1].get('href')
        download_url = download_url.strip()
        file_extension = download_url.split('.')[-1]
        download_url = encode_chinese(download_url)
        if file_extension == 'txt':
            download_file(download_url, TMP_TXT_PATH)
            return
        # Is rar or zip
        if file_extension == 'zip':
            file_path = TMP_ZIP_PATH
        elif file_extension == 'rar':
            file_path = TMP_RAR_PATH
        # Extract and 
        download_file(download_url, file_path)
        patoolib.extract_archive(file_path, outdir=TMP_DIRECTORY)
        for file_path in glob.glob(os.path.join(TMP_DIRECTORY,'*.txt')):
            if novel_name in file_path:
                shutil.move(file_path, TMP_TXT_PATH)
                break

class Xsla_downloader(object):
    """Download novel from websit:https://www.80xs.la/ (八零電子書)
    """
    def __init__(self):
        self.base_url = "https://www.80xs.la/"
        self.search_url = self.base_url + 'modules/article/search.php'
    def __str__(self) -> str:
        return "Xsla"
    def search(self, key_word:str):
        post_data = {'searchkey' : Trad2simple(key_word)}
        post_data = encode_chinese(post_data, is_post_data=True)
        soup = open_url(self.search_url, post_data=post_data)

        results = soup.find_all('div',class_="list_a")
        if results == []:
            return None
        
        results = soup.find_all('li',class_="storelistbt5a")
        novels_metadata = []
        for result in results:
            result = result.find('a',class_="bookname")
            novel_name = simple2Trad(result.text.split('》')[0][1:])
            url = result.get('href')
            novel_idx = url.split('/')[-1].split('.')[0]
            novels_metadata.append(create_metadata(novel_name, novel_idx))
            
        return novels_metadata
    def download(self, metadata:dict):
        # Get download link
        novel_name, novel_idx = metadata['novel_name'], metadata['novel_idx']
        novel_name = Trad2simple(novel_name)
        download_url = "https://dz.80xs.la/{}/{}.zip".format(novel_idx, novel_name)
        download_url = encode_chinese(download_url)

        # Download zip
        download_file(download_url, TMP_ZIP_PATH)
        extract_and_move_file(is_rar=False)

class Wenku8_downloader(object):
    """Download novel from websit: https://www.wenku8.net/ (輕小說文庫)
    """
    def __init__(self):
        self.base_url = "https://www.wenku8.net/modules/article/search.php?searchtype=articlename&searchkey={}&page={}"
        self.search_url = lambda key, p : self.base_url.format(quote(Trad2simple(key).encode('gbk')), p)
        self.latex_book_url = "https://www.wenku8.net/modules/article/toplist.php?sort=lastupdate"
        self._load_cookie()

    @staticmethod
    def _dump_cookie():
        cookie = "Input your cookie"
        temp = cookie.split('\n')[1:-1]
        cookies = []
        for c in temp:
            cookies.append(c.split('\t'))
        cookie_jar = RequestsCookieJar()
        for c in cookies:
            cookie_jar.set(c[0], c[1], domain=c[2])

        with open(WENKU8_COOKIE_FILE,'wb') as f:
            pickle.dump(cookie_jar, f)

    def _load_cookie(self):
        if not os.path.isfile(WENKU8_COOKIE_FILE):
            raise ValueError("Weku8 cookie file does not exist!")
        #Load cookie
        with open(WENKU8_COOKIE_FILE,'rb') as f:
            self.cookie = pickle.load(f)
    def __str__(self) -> str:
        return "Wenku8"

    def open_url(self, url, decode=True, post_data=None, return_response=False, use_cookie=True, return_url=False):
        """
        Args:
            url: url
            decode: boolean, whether decode the html
        Return: if decode is True, then return BeautifulSoup, else return bytes
        """
        
        headers={'User-Agent':UserAgent().edge}
        # decode html for search

        if use_cookie:
            response = requests.get(url, cookies=self.cookie, headers=headers)
        else:
            response = requests.get(url, headers=headers)
        if return_response:
            return response

        content = response.content
        # for download file 
        if not decode:
            return content
        else:
            encodings = ['utf-8','gb2312','gb18030']
            for encoding in encodings:
                try:
                    html = content.decode(encoding)
                    if return_url:
                        return BeautifulSoup(html, 'html.parser'), response.url
                    else:
                        return BeautifulSoup(html, 'html.parser')
                except UnicodeDecodeError:
                    continue
            html = content.decode('gb18030','ignore')
            if return_url:
                return BeautifulSoup(html, 'html.parser'), response.url
            else:
                return BeautifulSoup(html, 'html.parser')

    def search_page(self, key_word:str, page=1):
        """Search novel with key word for one page
        Return:
            if not found return None, else return dict: {novel_name:novel_idx}
        """
        soup, url = self.open_url(self.search_url(key_word, page), return_url=True)

        # Only one result
        if ".net/book/" in url:
            novel_name = simple2Trad(soup.find('table').find('b').text)
            author = soup.find('table').find_all('td')[4].text.split('：')[1]
            novel_idx = url.split('/')[-1].split('.')[0]

            novels_metadata = [create_metadata(novel_name, novel_idx,author=author)]
            return novels_metadata, 1

        link_list = soup.find('table').find_all('b')
        if link_list == []:
            return None
        # Get authors
        authors = []
        targets = soup.find('table').find_all('p')
        for i in range(0, len(targets), 5):
            authors.append(targets[i].text.split('/')[0][3:])

        # Get novel name and their index
        novels_metadata = []
        for author, l in zip(authors, link_list):
            l = l.find('a')
            novel_name = simple2Trad(l.get('title'))
            url = l.get('href')
            novel_idx = url.split('/')[-1].split('.')[0]
            novels_metadata.append(create_metadata(novel_name, novel_idx,author=simple2Trad(author)))
            
        num_pages = soup.find("div", id="pagelink").find_all('a')[-1].text
        
        return novels_metadata, int(num_pages)
    def search(self, key_word:str):
        result = self.search_page(key_word, page=1)
        if result == None:
            return None

        novels_metadatas, num_pages = result
        if num_pages != 1:
            for i in range(1, num_pages + 1):
                time.sleep(5)
                result = self.search_page(key_word, i)
                if result == None:
                    continue
                novels_metadata, _ = result
                novels_metadatas.extend(novels_metadata)
        return novels_metadatas
    def download_file(self, url, file_name:str, output_dir:str):
        file = self.open_url(url, decode=False, use_cookie=False)
        with open(os.path.join(output_dir,file_name), 'wb') as f:
            f.write(file)

    def download(self, metadata:dict, download_img=True):
        novel_name, novel_idx = metadata['novel_name'], metadata['novel_idx']
        # Get download link
        download_url = "https://www.wenku8.net/modules/article/packshow.php?id={}&type=txt".format(novel_idx)
        soup = self.open_url(download_url)
        files = soup.find("table",class_="grid").find_all('tr')[1:]


        threading.Semaphore(3)
        threads = []
        
        reset_TMP_DIRECTORY()
        for i, f in enumerate(files):
            chapter_name = simple2Trad(f.find('td').text)
            file_name =  f"{novel_name} {chapter_name}.txt"
            url =  f.find_all('a')[2].get('href')

            # Create directory for this chapter
            path = os.path.join(TMP_DIRECTORY, str(i))
            os.makedirs(path, exist_ok = True)

            t = threading.Thread(target=self.download_file, args=(url, file_name, path))
            threads.append(t)
        
        for t in threads:
            t.start() 
        for t in threads:
            t.join()
        if download_img:
            self.download_imgs(metadata)

    def download_img(self, url:str, idx:int):
        soup = self.open_url(url, use_cookie=False)
        imgs = soup.find_all("div", class_="divimage")
        imgs = [img.find('a').get('href') for img in imgs]
        
        # Create directory for storing images
        img_path = os.path.join(TMP_DIRECTORY, str(idx), 'imgs')
        os.makedirs(img_path, exist_ok = True)
        for i, img in enumerate(imgs):
            self.download_file(img, f"{i}.jpg", img_path)
            #time.sleep(0.1)
        return len(imgs)
        
    def download_imgs(self, metadata:dict):
        novel_name, novel_idx = metadata['novel_name'], metadata['novel_idx']
        url = "https://www.wenku8.net/book/{}.htm".format(novel_idx)
        soup = self.open_url(url, use_cookie=False)

        index_url = soup.find('div',id="content").find_all("a")[4].get('href')
        soup = self.open_url(index_url, use_cookie=False)
        chapter_titles = soup.find('table').find_all('td',class_="vcss")
        chapter_titles = [c.text for c in chapter_titles]
        num_chapters = len(chapter_titles)

        from collections import defaultdict
        all_titles = soup.find('table').find_all('td')
        idx = 0
        img_urls = defaultdict(list)
        for t in all_titles:
            if idx < len(chapter_titles) and t.text == chapter_titles[idx]:
                idx += 1
            if t.text == "插圖" or t.text == "插图":
                img_urls[idx - 1].append(t.find('a').get('href'))

        base_url = '/'.join(index_url.split('/')[:-1]) 
        base_url += '/'

        threading.Semaphore(3)
        threads = []
        for chapter_idx in range(num_chapters):
            if len(img_urls[chapter_idx]) == 0:
                continue
            # Download img one by one
            url = base_url + img_urls[chapter_idx][0]
            t = threading.Thread(target=self.download_img, args=(url, chapter_idx))
            threads.append(t)


        for t in threads:
            t.start() 
        for t in threads:
            t.join()