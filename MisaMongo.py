# coding=utf-8
#operation involve mongodb will be placed here
from string import Template
import os
# ---MongoDB
import pymongo
from pymongo import MongoClient

url = "mongodb://$dbuser:$dbpassword@ds149732.mlab.com:49732/heroku_jj2sv6sm"
mongo_us = 'admin'
mongo_ps = os.environ['MONGO_PSW']
temp=Template(url)
mongo_url=temp.substitute(dbuser=mongo_us,dbpassword=mongo_ps)
client = MongoClient(mongo_url)
db = client['heroku_jj2sv6sm']

def randget(Collection='quote_main',size=1):
    op_ins=db[Collection]
    pipeline=[{'$sample': {'size': size}}]
    selected=op_ins.aggregate(pipeline)
    result=[]
    for i in selected:
        result.append(i)
    
    return result
def insert_data(Collection,dict):
    op_ins=db[Collection]
    op_ins.insert_one(dict)

def display_data(Collection,pipeline,key):
    op_ins=db[Collection]
    ins=op_ins.find_one(pipeline)
    if ins is None:
        return None
    return ins[key]

def modify_data(Collection,pipeline=None,key=None,update_value=None):
    op_ins=db[Collection]

    if pipeline is not None:
        pass
    else:
        return
    
    ins=op_ins.find_one(pipeline)
    if ins is not None:
        op_ins.update_one(pipline,
        {'$set':{key:update_value}})
    else:
        dict=pipeline
        pipeline[key]=update_value
        op_ins.insert_one(dict)
    