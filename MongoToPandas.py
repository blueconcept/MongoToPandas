from pymongo import MongoClient
import pandas as pd

class MongoToPython():
    '''
    API for Mongo to Python
    '''
    
    def __init__(self, database_name, host=None, post=None):
        '''
        INPUT: String, host=String, post=String
        DESCRIPTION: Initializes MongoClient and assigns database
        OUTPUT: None
        '''
        if host==None and post==None:
            self.client = MongoClient()
        else:
            self.client = MongoClient(host, port)
        self.db = self.client[database_name]

    def query_all(self, collection_name, dict_requirements=None):
        '''
        INPUT: String, dict_requirements=String
        DESCRIPTION: Generator for a Mongo Query
        OUTPUT: Dictionary
        '''
        docs = self.db[collection_name]
        if dict_requirements == None:
            for doc in docs.find({}):
                yield doc
        else:
            for doc in docs.find(dict_requirements):
                yield doc

    def mongo_to_lists(self, collection_name, column_names, dict_requirements=None):
        '''
        INPUT: String, List of Strings, dict_req=Dictionary
        DESCRIPTION: Takes queries and converts to a combined list or list
        OUTPUT: List of Lists
        '''
        list_of_columns = []
  
        for query in self.query_all(collection_name, dict_requirements):
            row = []
            for i in xrange(len(column_names)):
                row.append(query[column_names[i]])
            list_of_columns.append(row)
            
        return list_of_columns

    def mongo_to_df(self, collection_name, column_names, dict_requirements=None):
        '''
        INPUT: String, List of Strings, dict_req=Dictionary
        DESCRIPTION: Like mongo_to_lists but returns a dataframe
        OUTPUT: pandas.DataFrame
        '''
        lst = self.mongo_to_lists(collection_name, column_names, dict_requirements=dict_requirements)
        df = pd.DataFrame(data=lst)
        df.columns = column_names
        return df

    def query_for_each(self, collection_name, iterable, matching_field, columns):
        '''
        INPUT: String, iterable of strings, String, List 
        DESCRIPTION: Does a query for each item
        OUTPUT: Pandas DataFrame
        '''
        dicts_of_dicts = { col:{} for col in columns}
        
        i = 0
        for item in iterable:
            for query in mongo.query_all(collection_name, dict_requirements={matching_field:item}):
                for col in columns:
                    dicts_of_dicts[col][i] = query[col]
                i += 1
        return pd.DataFrame(dicts_of_dicts)
    
    def get_collection_keys(self, collection_name):
        '''
        INPUT: String
        DESCRIPTION: Gets the keys for the first item in the mongodb WARNING!: is not gauranteed to get all keys in collection
        OUTPUT: List 
        '''
        return self.db[collection_name].find_one({}).keys()
    
    def get_one(self, collection_name, key, value):
        '''
        INPUT: String, String, String
        DESCRIPTION: Get's the first document with a matching key value
        OUTPUT: Dictionary
        '''
        return db[collection_name].find_one({key:value})