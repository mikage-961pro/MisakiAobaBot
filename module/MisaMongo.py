# coding=utf-8
#operation involve mongodb will be placed here
from string import Template
import os
import datetime
# ---MongoDB
import pymongo
from pymongo import MongoClient
from bson import ObjectId

# ---error log setting
import logging
logging.basicConfig(format='[%(asctime)s](%(levelname)s) %(name)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

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

def randget_t(Collection='quote_main',size=1,after=None):
    #where after is a datetime object ,in this case, it'll select data 'after' the date.
    op_ins=db[Collection]
    dummy_id=ObjectId.from_datetime(after)
    pipeline=[{'$match': {"_id": {"$gt": dummy_id}}},{'$sample': {'size': size}}]
    #result = collection.find({"_id": {"$gt": dummy_id}})
    selected=op_ins.aggregate(pipeline)
    result=[]
    for i in selected:
        result.append(i)
    return result    
    
def randget_idol(idol,Collection='ml_idol_pic_colle',size=1):
    op_ins=db[Collection]
    if idol=='all':
        pipeline=[{'$sample': {'size': size}}]
    else:
        pipeline=[{'$match': { 'name':idol }},{'$sample': {'size': size}}]
    selected=op_ins.aggregate(pipeline)
    result=[]
    for i in selected:
        result.append(i)
        print(i)
    return result

def room_state_getter(Collection='room_state',room_id=-1001290696540):
    op_ins=db[Collection]
    result=op_ins.find({"room_id":room_id}).sort('update_time',pymongo.DESCENDING).limit(1)
    try:
        return result[0]
    except IndexError:
        logger.warning("(%s):No result."'room_state_getter')
        return None

def db_quote_finder(key,Collection='quote_main'):
    op_ins=db[Collection]
    cmd_cursor=op_ins.find({})
    all_cont=[]
    result=[]
    for i in cmd_cursor:
        all_cont.append(i)
    for i in all_cont:
        index=i.values()
        for j in index:
            try:
                pos=j.find(key)
            except:
                pass
            else:
                if pos!=-1:
                    result.append(i)
                    break
    return result
    '''
    op_ins=db[Collection]
    pipeline={ '$text': { '$search': key }}
    selected=op_ins.find(pipeline)
    result=[]
    for i in selected:
        result.append(i)
    return result
'''
def insert_data(Collection,dict):
    op_ins=db[Collection]
    return op_ins.insert_one(dict)

def updata_data(Collection,dict,newdict):
    op_ins=db[Collection]
    return op_ins.update_one(dict,newdict,upsert=True)

def display_alldata(Collection):
    op_ins=db[Collection]
    ins=op_ins.find()
    return ins

def display_data(Collection,pipeline,key):
    """If no result, return true"""
    op_ins=db[Collection]
    ins=op_ins.find_one(pipeline)
    if ins is None:
        return True
    try:
        return ins[key]
    except KeyError:
        return True

def display_data2(Collection,pipeline,key):
    """If no result, return None"""
    op_ins=db[Collection]
    ins=op_ins.find_one(pipeline)
    if ins is None:
        return None
    try:
        return ins[key]
    except KeyError:
        return None

def modify_data(Collection,pipeline=None,key=None,update_value=None):
    op_ins=db[Collection]

    if pipeline is not None:
        pass
    else:
        return

    ins=op_ins.find_one(pipeline)
    if ins is not None:
        op_ins.update_one(pipeline,
        {'$set':{key:update_value}})
    else:
        dict=pipeline
        pipeline[key]=update_value
        op_ins.insert_one(dict)

def modify_many_data(Collection,pipeline=None,key=None,update_value=None):
    op_ins=db[Collection]

    if pipeline is not None:
        pass
    else:
        return

    op_ins.update_many(pipeline,
    {'$set':{key:update_value}})
