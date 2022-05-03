from urllib.request import urlopen, Request
from urllib.parse import quote
from urllib import parse
import os, shutil, string

from bs4 import BeautifulSoup
from opencc import OpenCC
import patoolib

from utils.config import TMP_DIRECTORY, TMP_TXT_PATH, TMP_RAR_PATH, reset_TMP_DIRECTORY

T2S = OpenCC('t2s') # Tradtional to Simple
S2T = OpenCC('s2twp') # Simple to Traditional


def open_url(url, decode=True, encoding='utf-8',post_data=None):
    """
    Args:
        url: url
        decode: boolean, whether decode the html
    Return: if decode is True, then return BeautifulSoup, else return bytes
    """
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
    request = Request(url, headers=headers, data=post_data)

    # decode html for search
    content = urlopen(request).read()

    # for download file
    if not decode:
        return content
    else:
        return BeautifulSoup(content.decode(encoding), 'html.parser')
        
    
def download_file(url, output_path:str):
    file = open_url(url, decode=False)
    with open(output_path, 'wb') as f:
        f.write(file)

def extract_and_move_file():
    reset_TMP_DIRECTORY()
    patoolib.extract_archive(TMP_RAR_PATH, outdir=TMP_DIRECTORY)
    files = os.listdir(TMP_DIRECTORY)
    shutil.move(os.path.join(TMP_DIRECTORY, files[0]), TMP_TXT_PATH)

def encode_chinese(data, is_post_data=False):
    # is post data
    if is_post_data:
        return parse.urlencode(data).encode()
    # is url
    else:
        return quote(data, safe=string.printable)

def create_metadata(novel_name:str, novel_idx:int, source_idx:int=None):
    """Create metadata for downloader
    Args:
        novel_name: the name of the novel
        novel_idx: the index of the novel
    """
    if source_idx != None:
        source_idx = int(source_idx)

    metadata = {'novel_name': novel_name, 
                'novel_idx': int(novel_idx), 
                'source_idx': source_idx}
    return metadata

class Downloader(object):
    def __init__(self, search_all_source=False):
        self.downloader = [Zxcs_downloader(), 
                            Ijjxsw_downloader()]
        self.search_all_source = search_all_source
    def search(self, key_word:str):
        """Search novel by key word
        Returns:
            source_idx, novel_dict
        """
        novels_metadatas = []
        for source_idx, downloader in enumerate(self.downloader):
            novels_metadata = downloader.search(key_word)
            if novels_metadata != None:
                for metadata in novels_metadata:
                    metadata['source_idx'] = source_idx
                novels_metadatas.extend(novels_metadata)
                # If get results, then return
                if self.search_all_source == False:
                    return novels_metadatas

        if len(novels_metadatas) != 0:
            return novels_metadatas
        else:
            return None
    def download(self, metadata:dict):
        source_idx = metadata['source_idx']
        self.downloader[source_idx].download(metadata)

class Zxcs_downloader(object):
    """Download novel from websit: http://zxcs.me/
    """
    def __init__(self):
        self.base_url = "http://zxcs.me/index.php?keyword={}&page={}"
        self.search_url = lambda key, p : encode_chinese(self.base_url.format(T2S.convert(key),p))

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
            novel_name = S2T.convert(novel_name)
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
                novels_metadata, _ = self.search_page(key_word, i)
                novels_metadatas.extend(novels_metadata)
        return novels_metadatas


    def download(self, metadata:dict):
        # Get download link
        novel_name, novel_idx = metadata['novel_name'], metadata['novel_idx']
        # Get download link
        download_url = "http://zxcs.me/download.php?id={}".format(novel_idx)
        soup = open_url(download_url)
        files = soup.find_all("span",class_="downfile")
        file_url = files[0].find('a').get('href')

        # Download rar
        download_file(file_url, TMP_RAR_PATH)
        extract_and_move_file()

class Ijjxsw_downloader(object):
    """Download novel from websit: https://m.ijjxsw.co/
    """
    def __init__(self):
        self.base_url = "https://m.ijjxsw.co/"
        self.search_url = self.base_url + 'search/'

    def search(self, key_word:str):
        post_data = {'searchkey' : T2S.convert(key_word)}
        post_data = encode_chinese(post_data, is_post_data=True)
        soup = open_url(self.search_url, post_data=post_data)

        results = soup.find_all('div',class_="list_a")
        if results == None:
            return None
        
        results = [element.find_all('a')[1] for element in results]
        novels_metadata = []
        for result in results:
            novel_name = S2T.convert(result.text)
            url = result.get('href')
            novel_idx = url.split('/')[-1].split('.')[0]
            novels_metadata.append(create_metadata(novel_name, novel_idx))
            
        return novels_metadata
    def download(self, metadata:dict):
        # Get download link
        novel_name, novel_idx = metadata['novel_name'], metadata['novel_idx']
        novel_name = T2S.convert(novel_name)

        download_url = "https://m.ijjxsw.co/api/txt_down.php?articleid={}&amp;articlename={}".format(novel_idx, novel_name)
        download_url = encode_chinese(download_url)

        # Download txt
        reset_TMP_DIRECTORY()
        download_file(download_url, TMP_TXT_PATH)