import os
import json
from os.path import exists
from utils.config import DOWNLOAD_JAPANESE_RESULTS_JSON, SEARCH_JAPANESE_RESULTS_JSON, SEARCH_RESULTS_JSON, DATABASE_DIRECTORY, DOWNLOAD_RESULTS_JSON, DATABASE_VERSION, delete_if_exist

class Database(object):
    @property
    def __version__(self):
        return 1.0

    def __init__(self, is_japanese=False):
        self.search_results = dict()
        self.download_results = dict()
        # init database directory
        os.makedirs(DATABASE_DIRECTORY, exist_ok=True)

        # Check database version
        if exists(DATABASE_VERSION):
            with open(DATABASE_VERSION, 'r', encoding='utf-8') as f:
                cur_version = float(f.read())
            # If local database version is older than current version, then delete it
            if self.__version__ > cur_version:
                self._del_file
                cur_version = self.__version__
                with open(DATABASE_VERSION, 'w', encoding='utf-8') as f:
                    f.write(f'{cur_version}')
        else:
            self._del_file()
            cur_version = self.__version__
            with open(DATABASE_VERSION, 'w', encoding='utf-8') as f:
                f.write(f'{cur_version}')

        if not is_japanese:
            self.search_result_json = SEARCH_RESULTS_JSON
            self.download_results_json = DOWNLOAD_RESULTS_JSON
        else:
            self.search_result_json = SEARCH_JAPANESE_RESULTS_JSON
            self.download_results_json = DOWNLOAD_JAPANESE_RESULTS_JSON

        if exists(self.search_result_json):
            with open(self.search_result_json, 'r', encoding='utf-8') as f:
                self.search_results = json.load(f)
        if exists(self.download_results_json):
            with open(self.download_results_json,'r', encoding='utf-8') as f:
                self.download_results= json.load(f)

    def _del_file(self):
        delete_if_exist(self.search_result_json)
        delete_if_exist(self.download_results_json)
    def add_search(self, key:str, result: list, overwrite=True):
        """Add a new search result to database
        Args:
            key: the key word of the search
            result: the result of the search
            overwrite: 
                If False, check the database whether the key word exists or not. if not, then add result to the database  
        """
        if overwrite or self.search_results.get(key) != None:
            self.search_results[key] = result
            self._write_search_file()
    def get_search(self, key:str) -> list:
        return self.search_results.get(key, None)
   
    def add_download(self, key:tuple, metadata:dict):
        if self.download_results.get(key) == None:
            self.download_results[key] = metadata
            self._write_download_file()     

    def get_download(self, key:str) ->list:
        return self.download_results.get(key, None)

    def _write_search_file(self):
        with open(self.search_result_json, 'w', encoding='utf-8') as f:
            json.dump(self.search_results, f, ensure_ascii=False)

    def _write_download_file(self):
        with open(self.download_results_json, 'w', encoding='utf-8') as f:
            json.dump(self.download_results, f, ensure_ascii=False)
            f.write('\n')
   

    