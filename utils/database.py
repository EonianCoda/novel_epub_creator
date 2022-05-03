import os
from utils.config import *
import pickle
##TODO
class Database(object):
    def __init__(self):
        self.search_results = dict()
        self.download_results = dict()
        os.mkdir('database')

        if os.path.exists(SEARCH_RESULTS_PICKLE):
            with open(SEARCH_RESULTS_PICKLE, 'rb') as f:
                self.search_results = pickle.load(f)

        if os.path.exists(DOWNLOAD_RESULTS_PICKLE):
            with open(DOWNLOAD_RESULTS_PICKLE, 'rb') as f:
                self.download_results = pickle.load(f)        

    def add_search(self, key:str, results:dict):
        #source_idx, novel_dict
        pass
    def add_download(self, key:str, metadata:dict):
        self.download_results[key] = metadata

    def write(self):
        with open(DOWNLOAD_RESULTS_PICKLE, 'rw') as f:
            pickle.dump(self.download_results, f)
        with open(SEARCH_RESULTS_PICKLE, 'rw') as f:
            pickle.dump(self.search_results, f) 
    