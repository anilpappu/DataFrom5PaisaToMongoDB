#!/usr/bin/env python
# coding: utf-8

# In[1]:


from py5paisa import FivePaisaClient
cred={
    "APP_NAME":"5P694",
    "APP_SOURCE":"5367",
    "USER_ID":"ulGCnUw6",
    "PASSWORD":"ggnwhMA",
    "USER_KEY":"M0Y3qsUA5nGw5OfyKxGoxg8",
    "ENCRYPTION_KEY":"3iRMtiWCUwyMMETjte3LAoM"
    }


# In[2]:


get_ipython().run_cell_magic('writefile', 'keys.conf', '[KEYS]\nAPP_NAME=5P55694\nAPP_SOURCE=5367\nUSER_ID=ulGinUw6\nPASSWORD=ggniVhMA\nUSER_KEY=M0Y3qsUJXwGxA5nGw5OfyKxGoxg8\nENCRYPTION_KEY=3iRMtiLFk7LrgToWCUwyMMETjte3LAoM')


# In[ ]:





# In[3]:



client = FivePaisaClient(email="jaal@gmail.com", passwd="Si23", dob="19021309",cred=cred)
client.login()


# In[ ]:





# In[4]:


import pandas as pd
from pymongo import MongoClient
import pymongo
import json
import warnings
warnings.filterwarnings('ignore')


# In[5]:


df=pd.read_csv(r'scripmaster-csv-format.csv')


# In[ ]:





# In[6]:


historic_df=client.historical_data('N','C',3045,'1m','2021-05-25','2021-06-16')
print(historic_df)


# In[34]:


class hist_data:
    #historic_df=pd.DataFrame()
    def __init__(self,exch,exty,name,timef,year):
        self.name=name
        cashdf=df[(df.Exch==exch)& (df.ExchType==exty)]
        cashdf['Name']=cashdf['Name'].str.strip()
        scrip=cashdf[cashdf['Name']==name]['Scripcode'].iat[0]
        historic_df1=client.historical_data(exch,exty,scrip,timef,f'{year}-01-01',f'{year}-06-30')
        historic_df2=client.historical_data(exch,exty,scrip,timef,f'{year}-07-01',f'{year}-12-31')
        #print(historic_df1)
        self.historic_df=historic_df1.append(historic_df2,ignore_index = True)
     
    def hist_show(self):
        print(self.historic_df)

class hist_data_csv(hist_data):
    
    def data_to_csv(self):
        self.historic_df.to_csv(f"{self.name}_csv.csv")
    
class import_mongo(hist_data_csv):
    db_url='mongodb://localhost:27017'
    db_name='data_base'
    
    def mongoimport(self):
        #def mongoimport(self,db_name, coll_name, db_url):
        self.data_to_csv()
        self.csv_path=f"{self.name}_csv.csv"
        self.coll_name=f"{self.name}_coll"
        
        client = MongoClient(self.db_url)
        db = client[self.db_name]  
        coll = db[self.coll_name]
        data = pd.read_csv(self.csv_path)
        df_=pd.DataFrame(data)
        posts = df_.to_dict(orient="record")
        #print(posts)
        coll.insert_many(posts)
        coll.create_index([("_id", pymongo.ASCENDING)])
    
    def insert_one(self,dict):
        client = MongoClient(self.db_url)
        db = client[self.db_name]  
        self.coll = db[self.coll_name]
        self.coll.insert_one(dict)
        
    def read(self,dict):
        client = MongoClient(self.db_url)
        db = client[self.db_name]  
        self.coll = db[self.coll_name]
        print(self.coll.find_one(dict))
        
    def update_one(self,dict1,data2):
        client = MongoClient(self.db_url)
        db = client[self.db_name]  
        self.coll = db[self.coll_name]
        self.coll.update_one(dict1,data2)
    
    def delete_one(self,dict):
        client = MongoClient(self.db_url)
        db = client[self.db_name]  
        self.coll = db[self.coll_name]
        self.coll.delete_one(dict)
        
        
               
#obj_SBIN=hist_data('N','C','SBIN','1d','2020')
#obj_RELIANCE=hist_data('N','C','RELIANCE','1d','2020')
#obj_TCS=hist_data('N','C','TCS','1d','2020')
#obj_LT=hist_data('N','C','LT','1d','2020')
#obj_IOC=hist_data('N','C','IOC','1d','2020')

#obj_SBIN=hist_data_csv('N','C','SBIN','1d','2020')
#obj_RELIANCE=hist_data_csv('N','C','RELIANCE','1d','2020')
#obj_TCS=hist_data_csv('N','C','TCS','1d','2020')
#obj_LT=hist_data_csv('N','C','LT','1d','2020')
#obj_IOC=hist_data_csv('N','C','IOC','1d','2020')

#obj_SBIN.data_to_csv()
#obj_RELIANCE.data_to_csv()
#obj_TCS.data_to_csv()
#obj_LT.data_to_csv()
#obj_IOC.data_to_csv()

obj_SBIN=import_mongo('N','C','SBIN','1d','2020')
obj_RELIANCE=import_mongo('N','C','RELIANCE','1d','2020')
obj_TCS=import_mongo('N','C','TCS','1d','2020')
obj_LT=import_mongo('N','C','LT','1d','2020')
obj_IOC=import_mongo('N','C','IOC','1d','2020')

obj_SBIN.mongoimport()
di={"Open":334.7}
obj_SBIN.read(di)

#obj1.hist_show()

    


# In[58]:


class live_data_to_mongo:
    db_url='mongodb://localhost:27017'
    db_name='live_data_base'
    post={}
    def __init__(self,exch,exty,name):
        self.exch=exch
        self.exty=exty
        self.name=name
        cashdf=df[(df.Exch==exch)& (df.ExchType==exty)]
        cashdf['Name']=cashdf['Name'].str.strip()
        self.scrip=cashdf[cashdf['Name']==name]['Scripcode'].iat[0]

    def live_mongo(self):
        req_list=[
            { "Exch":self.exch,"ExchType":self.exty,"ScripCode":int(self.scrip)},
            ]
        req_data=client.Request_Feed('mf','s',req_list)
        
        def on_message(ws, message):
            print(message)
            t=message.strip("[")
            self.post=json.loads(t.strip("]"))
            coll.insert_one(self.post)
            
        self.coll_name=f"{self.name}_coll"    
        client_mdb = MongoClient(self.db_url)
        db = client_mdb[self.db_name]  
        coll = db[self.coll_name]
        client.connect(req_data)

        client.receive_data(on_message)

        
        

           #data = pd.read_csv(csv_path)
           #df_=pd.DataFrame(data)
            #posts = df_.to_dict(orient="record")
        #print(type(post))
        
        #coll.create_index([("_id", pymongo.ASCENDING)])


# In[60]:


obj34=live_data_to_mongo('N','C','RELIANCE')
obj34.live_mongo()


# In[ ]:





# In[ ]:




