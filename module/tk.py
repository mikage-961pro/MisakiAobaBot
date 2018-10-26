# Python function
import datetime as dt
from datetime import datetime,tzinfo,timedelta
from datetime import time as stime#specific time
import time
import os
from random import randrange
from string import Template
from functools import wraps
from urllib import request
from urllib.parse import parse_qs
from telegram import Bot, Chat, Sticker, ReplyKeyboardMarkup, Message
from telegram.callbackquery import CallbackQuery
from telegram.error import *
from bs4 import BeautifulSoup as bs
import requests
# ---error log setting
import logging
logging.basicConfig(format='[%(asctime)s](%(levelname)s) %(name)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# do once var
do_once_value=True

# Record bot init time
init_time = datetime.now()
quote_search={} # Use on /quote
reply_pair={} # Use on catch reply
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

def user_admin_value(t_msg):
    """Dectect user if admin, return boolen value"""
    if isinstance(t_msg, Message):
        var_type="Message"
    elif isinstance(t_msg, CallbackQuery):
        var_type="Query"
    else:
        raise TypeError("Var is not telegram.Message or telegram.callbackquery.CallbackQuery type.")
        return
    uid=t_msg.from_user.id


    try:
        if var_type=="Message":
            adminlist=t_msg.chat.get_administrators()
        elif var_type=="Query":
            adminlist=t_msg.message.chat.get_administrators()
        for i in adminlist:
            if uid==i.user.id:
                return True
    except TelegramError as e:
        if e=="There is no administrators in the private chat":
            logger.info('(%s):%s','user_admin_value',e)
        return True
    except:
        logger.warning('Unknown error in [user_admin_value] function.')
        return False

# decorator
def wait_for_timeOut(func):
    """Reply a msg for timeOut"""
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        """Dectect bot if admin, if True, del cmd"""
        try:
            return func(bot, update, *args, **kwargs)
        except TelegramError as e:
            if e=="Timed out":
                bot.send_message(chat_id=update.message.chat_id,
                    text='請稍候...')
        except TimedOut:
            bot.send_message(chat_id=update.message.chat_id,
                text='請稍候...')
    return wrapped

# decorator
def wait_for_modify(func):
    """Reply a msg for timeOut"""
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        """Dectect bot if admin, if True, del cmd"""
        try:
            return func(bot, update, *args, **kwargs)
        except TelegramError as e:
            if e=="Message is not modified":
                bot.send_message(chat_id=update.message.chat_id,
                    text='請稍候...')
    return wrapped


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
    bot_count=0
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

def timePrint():
    return datetime.now().strftime("%y/%m/%d %H:%M:%S")

def utc8now():
    return (datetime.now()+timedelta(hours=8)).strftime("%y/%m/%d %H:%M:%S")

def utc8now_datetime():
    return datetime.now()+timedelta(hours=8)

def if_int_negative(interval):
    if interval<0:
        return True
    else:
        return False

def formula(key,text,if_list=False,parameter_preword='-',sep_word=' '):
    """
    To make function has add function.
    Ex. If /funcion -h
    Help funcion will return true.
    Or
    Ex. /funcion -f=123
    will return '123'

    this funcion support many formula
    if user input /funcion -f=123 -d -w=abc
    formula('f',text) will return '123'
    """
    # key is what you want to dectect
    key_len=len(key)
    key_total=parameter_preword+key
    key_position=text.find(key_total)
    value=False
    if key_position>=0:
        start_point=key_position+key_len+1
        if start_point>(len(text)-1):
            value=True
        else:
            try:
                if text[start_point] == '=':
                    start_point+=1
                    return_value=""
                    while(start_point<len(text)):
                        if text[start_point]==sep_word:
                            break
                        return_value+=text[start_point]
                        start_point+=1
                    value=return_value
                    if if_list:
                        """input data like -data=a,b,c"""
                        value=[]
                        for i in return_value.split(','):
                            value.append(i)
                elif text[start_point] == sep_word:
                    value=True
                else:
                    value=False
            finally:
                pass
    return value

def url_valid(url):
    try:
        code = request.urlopen(url).code
    except:
        return False
    return True

def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

def htmlPharseTester(str):
    """This function is to fix Can't parse entities problem like (*>△<)"""
    right_mouth=False
    for i in str:
        if i=="<":
            right_mouth=True
        if i==">":
            right_mouth=False
    return not right_mouth

def picLinker(url):
    """Deal with twitter multi pic and pixiv header issue"""
    """case twitter"""
    if 'twitter' in url:
        try:
            twi=requests.get(url)
        except:
            return url
        else:
            soap=bs(twi.content, "lxml")
            metalink=soap.find_all('meta',{'property':'og:image'})
            for i in metalink:
                picLink.append(i.attrs['content'])
            return randList(picLink)
            
    if 'pixiv' in url:
        
        illustId_qs=url[url.find('illust_id='):]
        illustId=parse_qs(illustId_qs)['illust_id'][0]
        img=pixivGet_img(illustId)
        if img:
            return img
        else:
            return url
    return url

################################pixiv
        
se = requests.session()
headers = {
    'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/62.0.3202.89 Chrome/62.0.3202.89 Safari/537.36'
}

def pixivGet_img(illustId):  
    #login
    pixiv_login(pixiv_id,password)
    
    img_url = 'https://www.pixiv.net/member_illust.php?mode=manga&illust_id='+illustId
    get_url='https://www.pixiv.net/ajax/illust/'+illustId
    html = se.get(get_url, headers=headers, timeout=10)
    img_info=json.loads(html.text)
    img_src = img_info['body']['urls']['original']    
    img_orig_src=img_src
    src_headers = headers
    src_headers['Referer'] = img_url
    try:
        img=se.get(img_orig_src, headers=src_headers).content
        return img
    except:
        return False
    
    
    
def pixiv_login(pixiv_id,password):
    base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
    login_url = 'https://accounts.pixiv.net/api/login?lang=zh'
    post_key_html = se.get(base_url, headers=headers).text
    post_key_soup = BeautifulSoup(post_key_html, 'lxml')
    post_key = post_key_soup.find('input', {'name': 'post_key'})['value']
    data = {
        'pixiv_id': pixiv_id,
        'password': password,
        'post_key': post_key
    }
    se.post(login_url, data=data, headers=headers)