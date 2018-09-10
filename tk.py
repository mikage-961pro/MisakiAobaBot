# Python function
import datetime as dt
from datetime import datetime,tzinfo,timedelta
from datetime import time as stime#specific time
import time
import os
from random import randrange
from string import Template
from functools import wraps

from telegram import Bot, Chat, Sticker, ReplyKeyboardMarkup

# MongoDB
import pymongo
from pymongo import MongoClient

url = "mongodb://$dbuser:$dbpassword@ds149732.mlab.com:49732/heroku_jj2sv6sm"
mongo_us = 'admin'
mongo_ps = os.environ['MONGO_PSW']
temp=Template(url)
mongo_url=temp.substitute(dbuser=mongo_us,dbpassword=mongo_ps)
client = MongoClient(mongo_url)
db = client['heroku_jj2sv6sm']
collect = db['misaki_setting']

# ---Google Database
import gspread
from oauth2client.service_account import ServiceAccountCredentials
spreadsheet_key=os.environ['SPREAD_TOKEN']

# ---postgresql
from postgre import dbDump,dbrandGet,dbGet


# do once var
do_once_value=True

# Record bot init time
init_time = datetime.now()
################################################
#                   tool kits                  #
################################################
# decorator
def do_once(function):
    """decorator for function do once"""
    global do_once_value
    if do_once_value:
        do_once_value=False
        return function

def c_tz(datetime,tz):
    t=datetime+timedelta(hours=tz)#轉換時區 tz為加減小時

def is_admin(bot,update):
    """Dectect user if admin, return boolen value"""
    is_admin=False
    try:
        if update.message.chat.type=='private':
            return is_admin
        else:
            adminlist=update.message.chat.get_administrators()
            for i in adminlist:
                if update.message.from_user.id==i.user.id:
                    is_admin=True
            return is_admin
    except:
        if update.callback_query.message.chat.type=='private':
            return is_admin

def bot_is_admin(bot,update):
    """Dectect bot if admin, return boolen value"""
    bot_auth=False
    if update.message.chat.type=='private':
        return bot_auth
    else:
        adminlist=update.message.chat.get_administrators()
        me=bot.get_me()
        for b in adminlist:
                if me.id==b.user.id:
                    bot_auth=True
        return bot_auth

def room_member_num(bot,update):
    # count member number
    total_count=bot.get_chat_members_count(update.message.chat.id)
    bot_count=2
    human_count=total_count-bot_count
    return human_count

# decorator
def del_cmd(func):
    """This decorator is used to prevent the command input before init"""
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        """Dectect bot if admin, if True, del cmd"""
        if bot_is_admin(bot,update):
            try:
                bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
            except:
                pass
        return func(bot, update, *args, **kwargs)
    return wrapped

def del_cmd_func(bot, update):
    """Dectect bot if admin, if True, del cmd"""
    if bot_is_admin(bot,update):
        try:
            bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
        except:
            pass

def randList(list):
    return list[randrange(len(list))]

# decorator
def do_after_root(func):
    """This decorator is used to prevent the command input before init"""
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        if update.message.date <= init_time:
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

# decorator
def admin_cmd(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        if not is_admin(bot,update):
            try:
                bot.send_message(chat_id=update.message.chat_id, text="Only admin can use this command.")
            except:
                bot.send_message(chat_id=update.callback_query.message.chat_id, text="Only admin can use this command.")
            return
        return func(bot, update, *args, **kwargs)
    return wrapped
def bool2text(v):
    if v:
        return '開啟'
    else:
        return '關閉'
# DB function
def db_switch_one_value(data_tag):
    dict={'tag': ''}
    dict['tag']=data_tag
    data_value = db.misaki_setting.find_one(dict)
    if data_value['value']:
        result = db.misaki_setting.update_one(
            dict,
            {'$set': {'value': False}},
            upsert=True)
        return False
    else:
        result = db.misaki_setting.update_one(
            dict,
            {'$set': {'value': True}},
            upsert=True)
        return True


def get_sheet(name):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key)
    try:
        worksheet=sheet.worksheet(name)
    except:
        sheet.add_worksheet(name,1,1)
        worksheet=sheet.worksheet(name)
        return worksheet
    else:
        return worksheet

def work_sheet_push(values,worksheet_name):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    #got from google api
    #attach mine for example
    #try to set in environ values but got fail
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_key)
    try:
        worksheet=spreadsheet.worksheet(worksheet_name)
    except:#there is no this worksheet
        spreadsheet.add_worksheet(worksheet_name,len(values),1)
        worksheet=spreadsheet.worksheet(worksheet_name)
        worksheet.insert_row(values,1)
    else:
        worksheet.insert_row(values,1)
#usage (values[list of string],worksheet_name[string])
#put a list of value and push to worksheet

def work_sheet_pop(key,woksheet_name):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    #got from google api
    #attach mine for example
    #try to set in environ values but got fail
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_key)
    worksheet=spreadsheet.worksheet(worksheet_name)
    cell=get_cell(key,worksheet)
    if cell!=None:
        row=worksheet.row_values(cell.row)
        worksheet.delete_row(cell.row)
    else:
        return None

def set_config(id,command):

    worksheet=get_sheet('config')
    user_id=id
    try:
        #find chat_id
        cell=worksheet.find(str(user_id))
    except:
        #ERROR:not found
        #creat new record
        worksheet.insert_row([user_id,command], 1)
    else:
        #replace record
        setting=worksheet.cell(cell.row,cell.col+1).value
        if setting.find(command)!=-1:
            setting=setting.replace(command,'')
        else:
            setting=setting+command
        worksheet.update_cell(cell.row,cell.col+1,setting)
    global config_buffer
    global config_buffer_Plock
    if config_buffer_Plock==True:
        time.sleep(0.5)
    config_buffer_Plock=True
    config_buffer=worksheet.get_all_values()
    config_buffer_Plock=False

def get_config(id,setting):
    global config_buffer
    global config_buffer_Plock
    if config_buffer_Plock==True:
        time.sleep(0.5)
    for i in config_buffer:
        if i[0].find(str(id))!=-1:
            if i[1].find(setting)!=-1:
                return True
            else:
                return False
    return False
