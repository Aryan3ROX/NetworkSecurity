import os
import sys
import json
from dotenv import load_dotenv
load_dotenv()

import certifi
ca = certifi.where()

MONGODB_URL = os.getenv('MONGODB_URL')

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_convertor(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGODB_URL)
            self.database = self.mongo_client[database]
            self.collection = self.database[collection]

            result = self.collection.insert_many(self.records)
            return len(result.inserted_ids)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__ == "__main__":
    FILE_PATH = r"Network_Data\phishingData.csv"
    DATABASE = "NETWORK_SECURITY"
    Collection = "NetworkData"
    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json_convertor(FILE_PATH)
    no_of_records = networkobj.insert_data_mongodb(records,DATABASE,Collection)
    print(no_of_records)