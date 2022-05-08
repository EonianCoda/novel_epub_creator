import os, json
from utils.config import SEARCH_RESULTS_JSON, DATABASE_DIRECTORY,DOWNLOAD_RESULTS_JSON

class Database(object):
    def __init__(self):
        self.search_results = dict()
        self.download_results = dict()

        # init database directory
        os.makedirs(DATABASE_DIRECTORY, exist_ok=True)

        if os.path.exists(SEARCH_RESULTS_JSON):
            with open(SEARCH_RESULTS_JSON, 'r', encoding='utf-8') as f:
                self.search_results = json.load(f)
        if os.path.exists(DOWNLOAD_RESULTS_JSON):
            with open(DOWNLOAD_RESULTS_JSON,'r', encoding='utf-8') as f:
                self.download_results= json.load(f)


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
        with open(SEARCH_RESULTS_JSON, 'w', encoding='utf-8') as f:
            json.dump(self.search_results, f, ensure_ascii=False)

    def _write_download_file(self):
        with open(DOWNLOAD_RESULTS_JSON, 'w', encoding='utf-8') as f:
            json.dump(self.download_results, f, ensure_ascii=False)
            f.write('\n')
   

    