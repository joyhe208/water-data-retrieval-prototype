import pandas as pd
import numpy as np
import json
import os
from os import path
import snowflake.connector
import config
from config import *
from abc import *
import re
import sqltranslate
from sqltranslate import *

#######################Get Formatted Data Module#############################
# semi-abstract parent class for querying data in different formats
# data is saved in a specific format that can be sent to front-end Javascript systems, 
# held in data field
#############################################################################
class GetFormattedData(metaclass = ABCMeta):
    def __init__(self, filename):
       self.filename = filename
       #self.data = self.accessData()
    
    @abstractmethod
    def accessData(self):
        pass

    def returnData(self):
        return self.data

class GetTableData(GetFormattedData):
    def __init__(self,filename):
        super().__init__(filename)

    def accessData(self):
        with open(self.filename,'r') as f:
            df = pd.read_csv(f)
        values = []
        for i in range(len(df)):
            dataEntry = {}
            for column in df.columns:
                dataEntry[column] = df.loc[i,column]
            values.append(dataEntry)
        return values
    
class GetJsonData(GetFormattedData):
    def __init__(self,filename):
        super().__init__(filename)
    def accessData(self):
        with open(self.filename,"r") as f:
            return json.load(f)
    

class GetDatabaseTableData(GetTableData):
    def __init__(self,filename,config, params):
        self.query = run(params) #make sqltranslate object using this function from sqltranslate package
        self.ctx = snowflake.connector.connect(
            user= config['user'],
            password= config['password'],
            account= config['account'],
            warehouse=config['warehouse'],
            database=config['database'],
            schema=config['schema']
        )
        self.cs = self.ctx.cursor()
        self.executeCommand()
        super().__init__(filename)
        

    def executeCommand(self):
        records = self.cs.execute(self.query.command())
        with open(self.filename,'w') as f:
            records.fetch_pandas_all().to_csv(self.filename)

