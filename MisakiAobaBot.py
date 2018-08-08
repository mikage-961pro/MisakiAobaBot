# coding=utf-8

################################################
#                   Import                     #
################################################

# Telegram
from telegram import (Bot, Chat, Sticker, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,JobQueue
from telegram.ext.dispatcher import run_async

# Python function
import datetime as dt
from datetime import datetime,tzinfo,timedelta
from datetime import time as stime#specific time
import logging
import time
import os
from random import randrange
import random
import json
# Database
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# User Module
from global_words import GLOBAL_WORDS

################################################
#                     init                     #
################################################

# ---BOT SETTING---
bot_name='@MisakiAobaBot'
token = os.environ['TELEGRAM_TOKEN']
spreadsheet_key=os.environ['SPREAD_TOKEN']
# token will taken by heroku
updater = Updater(token,workers=16)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Record bot init time
init_time = -1

# Buffer of key_word dic , fomat : list of dic
kw_j_buffer=[]
################################################
#                     class                    #
################################################
class remind():
    def __init__(self,stime,text,day=7):
        self.stime=dt.datetime.strptime(stime, '%H:%M').time()
        #str to stime()
        self.text=text
        self.day=day
################################################
#                   tool kits                  #
################################################
def c_tz(datetime,tz):
    t=datetime+timedelta(hours=tz)#轉換時區 tz為加減小時
    return t#datetime object

#key of spread sheet
def get_cell(key_word,worksheet):
    try:
        cell=worksheet.find(key_word)
    except:#not find
        return None
    else:
        return cell

def is_admin(bot,update):
    """Dectect user if admin, return boolen value"""
    is_admin=False
    if update.message.chat.type=='private':
        return is_admin
    else:
        adminlist=update.message.chat.get_administrators()
        for i in adminlist:
            print(i.user.id)
            if update.message.from_user.id==i.user.id:
                is_admin=True
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

def del_cmd(bot,update):
    """Dectect bot if admin, if True, del cmd"""
    if bot_is_admin(bot,update):
        try:
            bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
        except:
            pass

def yuunou(bot,update):
    """misaki is good"""
    if randrange(100) <3:
        bot.send_photo(chat_id=update.message.chat_id, photo=open('yuunou.jpg', 'rb'))

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
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key)
    worksheet=sheet.worksheet('config')
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

def get_config(id,setting):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key)
    worksheet=sheet.worksheet('config')
    user_id=id
    try:
        #find chat_id
        cell=worksheet.find(str(user_id))
    except:
        return False
    else:
        config=worksheet.cell(cell.row,cell.col+1).value
        if config.find(setting)!=-1:
            return True
        else:
            return False
        
################################################
#                   command                    #
################################################
"""
All cmd function need to add
if update.message.date > init_time:
at first to prevent too many cmd before root
"""

def start(bot, update):
    """Send a message when the command /start is issued."""
    if update.message.date > init_time:
        bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_start,
                        parse_mode=ParseMode.HTML)
        yuunou(bot,update)

def help(bot, update):
    """Send a message when the command /help is issued."""
    if update.message.date > init_time:
        del_cmd(bot,update)
        if randrange(1000)<30:
            bot.send_message(chat_id=update.message.chat_id, text="ぜ")
        else:
            bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_help, 
                        parse_mode=ParseMode.HTML)
            yuunou(bot,update)

def tbgame(bot, update):
    """Send a message when the command /tbgame is issued."""
    if update.message.date > init_time:
        del_cmd(bot,update)
        bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_tbgame, 
                        parse_mode=ParseMode.HTML)
        yuunou(bot,update)

@run_async
def rule(bot, update):
    """Send a message when the command /rule is issued."""
    if update.message.date > init_time:
        del_cmd(bot,update)
        if randrange(1000)<30:
            bot.send_message(chat_id=update.message.chat_id, text="ぜ")
        else:
            msg=bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_rule, 
                            parse_mode=ParseMode.HTML)
            time.sleep(60)
            bot.delete_message(chat_id=update.message.chat_id, message_id=msg.message_id)
            yuunou(bot,update)

def sendmsg(bot, update, args):
    """Send a message to chat when the command /sendmsg is issued."""
    """Only for admin use"""
    t_pw='misakiisgood'
    if update.message.date > init_time:
        if not args:
            bot.send_message(chat_id=update.message.chat_id, text="Please enter message and password.")
        else:
            t=' '.join(args).split('#')
            if t[0] != t_pw:
                bot.send_message(chat_id=update.message.chat_id, text="Uncorrect password.")
            else:
                text=t[1]
                bot.send_message(chat_id='-1001290696540', text=text)

def state(bot, update):
    """Send a message when the command /state is issued."""
    if update.message.date > init_time:
        total_count=bot.get_chat_members_count(update.message.chat.id)
        bot_count=3
        human_count=total_count-bot_count
        bot.send_message(chat_id=update.message.chat_id,
        text='目前室內人數：{}'.format(str(human_count))+'\n'+
        GLOBAL_WORDS.word_state,parse_mode=ParseMode.HTML)

@run_async
def config(bot, update, args):
    """Send a message when the command /config is issued."""
    if update.message.date > init_time:
        word_kachikoi_name=GLOBAL_WORDS.word_kachikoi_1.replace('$name',' '.join(args))
        if not args:
            bot.send_message(chat_id=update.message.chat_id, text="本功能目前沒有毛用")
        elif word_kachikoi_name.find('安靜')!=-1:
            set_config(update.message.from_user.id,'s')
            return
        else:
            del_cmd(bot,update)
            msg_1=bot.send_message(chat_id=update.message.chat_id, text=word_kachikoi_name,
            parse_mode=ParseMode.HTML)
            time.sleep(6)
            bot.delete_message(chat_id=update.message.chat_id, message_id=msg_1.message_id)
            msg_2=bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_kachikoi_2,
            parse_mode=ParseMode.HTML)
            time.sleep(6)
            bot.delete_message(chat_id=update.message.chat_id, message_id=msg_2.message_id)
            msg_3=bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_kachikoi_3,
            parse_mode=ParseMode.HTML)
            time.sleep(6)
            bot.delete_message(chat_id=update.message.chat_id, message_id=msg_3.message_id)
            yuunou(bot,update)

@run_async
def nanto(bot, update, args):
    """Send a message when the command /nanto is issued."""
    if update.message.date > init_time:
        del_cmd(bot,update)
        if not args:
            msg_1=bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_nanto_1)
            time.sleep(1)
            msg_2=bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_nanto_2)
            time.sleep(0.5)
            msg_3=bot.send_sticker(chat_id=update.message.chat_id, sticker="CAADBQADGgADT1ZbIFSw_UAI28HiAg")
            time.sleep(2)
            msg_4=bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_nanto_4)
            time.sleep(10)
            bot.delete_message(chat_id=update.message.chat_id, message_id=msg_4.message_id)
            bot.delete_message(chat_id=update.message.chat_id, message_id=msg_3.message_id)
            bot.delete_message(chat_id=update.message.chat_id, message_id=msg_2.message_id)
            bot.delete_message(chat_id=update.message.chat_id, message_id=msg_1.message_id)
        else:
            if '#' in ' '.join(args):  
                input_text=' '.join(args).split('#')
                text="なんとっ!$username居然$text了！".replace('$text',input_text[1]).replace('$username',input_text[0])
                msg_1=bot.send_message(chat_id=update.message.chat_id, text=text)
                time.sleep(1)
                msg_2=bot.send_sticker(chat_id=update.message.chat_id, sticker="CAADBQADGgADT1ZbIFSw_UAI28HiAg")
                time.sleep(5)
                text="明日も$textすると、きっといいことがあると思いますよぉ～。えへへぇ♪".replace('$text',input_text[1])
                msg_3=bot.send_message(chat_id=update.message.chat_id, text=text)
                time.sleep(30)
                bot.delete_message(chat_id=update.message.chat_id, message_id=msg_3.message_id)
                bot.delete_message(chat_id=update.message.chat_id, message_id=msg_2.message_id)
                bot.delete_message(chat_id=update.message.chat_id, message_id=msg_1.message_id)
            else:
                input_text=' '.join(args)
                text="なんとっ!居然$text了！".replace('$text',input_text)
                msg_1=bot.send_message(chat_id=update.message.chat_id, text=text)
                time.sleep(1)
                msg_2=bot.send_sticker(chat_id=update.message.chat_id, sticker="CAADBQADGgADT1ZbIFSw_UAI28HiAg")
                time.sleep(5)
                text="明日も$textすると、きっといいことがあると思いますよぉ～。えへへぇ♪".replace('$text',input_text)
                msg_3=bot.send_message(chat_id=update.message.chat_id, text=text)
                time.sleep(30)
                bot.delete_message(chat_id=update.message.chat_id, message_id=msg_3.message_id)
                bot.delete_message(chat_id=update.message.chat_id, message_id=msg_2.message_id)
                bot.delete_message(chat_id=update.message.chat_id, message_id=msg_1.message_id)
        yuunou(bot,update)
            
def which(bot, update, args):
    """Send a message when the command /which is issued."""
    if update.message.date > init_time:
        if not args:
            text="請輸入要給我決定的事情♪\n記得用〔＃〕分開喔！"
            bot.send_message(chat_id=update.message.chat_id, text=text)
        else:
            things=' '.join(args).split('#')
            result=things[randrange(len(things))]
            text="わたしは〜♬［$res］が良いと思うよ〜えへへ。".replace('$res',result)
            bot.send_message(chat_id=update.message.chat_id, text=text)
            yuunou(bot,update)

def dice(bot,update,args):
    """Send a message when the command /dice is issued."""
    dice=['⚀','⚁','⚂','⚃','⚄','⚅']
    count=[0,0,0,0,0,0]
    text=''
    if update.message.date > init_time:
        bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
        if not args:
            #dice 1
                msg=bot.send_message(chat_id=update.message.chat_id, text=dice[randrange(6)])
        else:
            dice_num=' '.join(args)
            try:
                num=int(dice_num)
            except:
                #value error
                return
            else:
                if num>100:
                    return
                else:
                    for i in range(0,num):
                        j=randrange(6)
                        text=text+dice[j]
                        count[j]=count[j]+1
                    msg=bot.send_message(chat_id=update.message.chat_id, text=text)
                    text=''
                    for i in range(0,6):
                        text=text+dice[i]+str(count[i])+'個\n'
                    if num>20:
                        msg1=bot.send_message(chat_id=update.message.chat_id, text=text)
                        time.sleep(5)
                        bot.delete_message(chat_id=update.message.chat_id, message_id=msg.message_id)
                        bot.delete_message(chat_id=update.message.chat_id, message_id=msg1.message_id)
                    
@run_async
def tiger(bot, update):
    word_tiger_1="<pre>あー</pre>"
    word_tiger_2="<pre>👏</pre>"
    word_tiger_3="<pre>👏👏</pre>"
    word_tiger_4="<pre>ジャージャー！</pre>"
    word_tiger_5="<pre>タイガー！</pre>"
    word_tiger_6="<pre>ファイヤー！</pre>"
    word_tiger_7="<pre>サイバー！</pre>"
    word_tiger_8="<pre>ファイバー！</pre>"
    word_tiger_9="<pre>ダイバー！</pre>"
    word_tiger_10="<pre>バイバー！</pre>"
    word_tiger_11="<pre>ジャージャー！</pre>"
    word_tiger_12="<pre>ファイボー！ワイパー！</pre>"
    if update.message.date > init_time:
        del_cmd(bot,update)
        messg = bot.send_message(chat_id=update.message.chat_id, text=word_tiger_1,
            parse_mode=ParseMode.HTML)
        time.sleep(0.5)
        messg = bot.editMessageText(chat_id=update.message.chat_id, text=word_tiger_2, message_id=messg.message_id,
            parse_mode=ParseMode.HTML)
        time.sleep(0.25)
        messg = bot.editMessageText(chat_id=update.message.chat_id, text=word_tiger_3, message_id=messg.message_id,
            parse_mode=ParseMode.HTML)
        time.sleep(0.25)
        messg = bot.editMessageText(chat_id=update.message.chat_id, text=word_tiger_4, message_id=messg.message_id,
            parse_mode=ParseMode.HTML)
        time.sleep(1.2)
        messg = bot.editMessageText(chat_id=update.message.chat_id, text=word_tiger_5, message_id=messg.message_id,
            parse_mode=ParseMode.HTML)
        time.sleep(0.6)
        messg = bot.editMessageText(chat_id=update.message.chat_id, text=word_tiger_6, message_id=messg.message_id,
            parse_mode=ParseMode.HTML)
        time.sleep(0.6)
        messg = bot.editMessageText(chat_id=update.message.chat_id, text=word_tiger_7, message_id=messg.message_id,
            parse_mode=ParseMode.HTML)
        time.sleep(0.6)
        messg = bot.editMessageText(chat_id=update.message.chat_id, text=word_tiger_8, message_id=messg.message_id,
            parse_mode=ParseMode.HTML)
        time.sleep(0.6)
        messg = bot.editMessageText(chat_id=update.message.chat_id, text=word_tiger_9, message_id=messg.message_id,
            parse_mode=ParseMode.HTML)
        time.sleep(0.6)
        messg = bot.editMessageText(chat_id=update.message.chat_id, text=word_tiger_10, message_id=messg.message_id,
            parse_mode=ParseMode.HTML)
        time.sleep(0.6)
        messg = bot.editMessageText(chat_id=update.message.chat_id, text=word_tiger_11, message_id=messg.message_id,
            parse_mode=ParseMode.HTML)
        time.sleep(1.2)
        messg = bot.editMessageText(chat_id=update.message.chat_id, text=word_tiger_12, message_id=messg.message_id,
            parse_mode=ParseMode.HTML)
        time.sleep(5)
        bot.delete_message(chat_id=update.message.chat_id, message_id=messg.message_id)
        yuunou(bot,update)

@run_async
def notiger(bot, update):
    """Send a message when the command /notiger is issued."""
    if update.message.date > init_time:
        del_cmd(bot,update)
        msg=bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_notiger, 
                    parse_mode=ParseMode.HTML)
        time.sleep(10)
        bot.delete_message(chat_id=update.message.chat_id, message_id=msg.message_id)
        yuunou(bot,update)

def title(bot,update,args):
    """Change tilte when the command /title OOO is issued."""
    if update.message.date > init_time:
        title = ' '.join(args)
        adminlist=update.message.chat.get_administrators()
        is_admin=False
        
        me=bot.get_me()
        bot_auth=False
        
        for i in adminlist:
            if update.message.from_user.id==i.user.id:
                is_admin=True
                
        for b in adminlist:
                if me.id==b.user.id:
                    bot_auth=True
        
        if is_admin==True:
            if bot_auth==True:
                bot.set_chat_title(chat_id=update.message.chat_id, title=title)
                bot.send_message(chat_id=update.message.chat_id,text='できました！！\nOK~~')
            else:
                bot.send_message(chat_id=update.message.chat_id,text='失敗しました.....\nFail.....')
            
        else:
            bot.send_message(chat_id=update.message.chat_id,text='申し訳ございませんが、このコマンドは、管理者しか使いません\nOops!Only admin can change title.')

#mention that bot need to be an admin of sgroup
#should change automatically and get title from DB,though JOBquece
#function for test

def set_remind_time(bot,update,args):
    if update.message.date > init_time:
        #do not test public cause there's no auth check yet
        #check auth
        #if is_admin(bot,update)==True:
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
        #got from google api
        #attach mine for example
        #try to set in environ values but got fail
        client = gspread.authorize(creds)
        sheet = client.open_by_key(spreadsheet_key)
        if not args:
            return
        
        text=' '.join(args)
        l_text=text.split('%%')
        tsheet=sheet.worksheet('time')
        cell=get_cell(l_text[0],tsheet)
        if cell==None:
            tsheet.insert_row([l_text[0],l_text[1],l_text[2],update.message.from_user.id], 2)
        else:
            tsheet.update_cell(cell.row,cell.col+1,l_text[1])
            tsheet.update_cell(cell.row,cell.col+2,l_text[2])
            tsheet.update_cell(cell.row,cell.col+3,update.message.from_user.id)

            
def quote(bot,update):
    #daily quote
    if get_config(update.message.from_user.id,'q')==True:
        del_cmd(bot,update)
        return
    else:
        set_config(update.message.from_user.id,'q')
        del_cmd(bot,update)
    worksheet=get_sheet('quote_main')
    quote=worksheet.get_all_values()
    num=random.randint(0,len(quote)-1)
    text='<pre>'+quote[num][0]+'</pre>\n'+'-----<b>'+quote[num][1]+'</b> より'
    msg=bot.send_message(chat_id=update.message.chat_id,text=text,parse_mode='HTML')

# other command
def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def unknown(bot, update):
    if update.message.text.find('MisakiAobaBot')!=-1:
        bot.send_message(chat_id=update.message.chat_id, text="すみません、よく分かりません。")

################################################
#                not command                   #
################################################
def find_word_TAKEVER(sentence,key_words, echo=None, prob=1000, els=None,photo =None, video=None,sticker=None, allco=False):
    #sentence:sentence user send
    # words: words need to reaction
    # echo: msg send after reaction
    # prob: probability, if not, send els msg
    # els: if not in prob
    list_r=['','']
    #represent type of return
    # a random number from 0 to 99
    num = randrange(1000)
    key_words_value=False
    for check in key_words:
        if allco == False:
             if sentence.find(check)!=-1:
                key_words_value=True
        if allco == True:
            if sentence.find(check)!=-1:
                key_words_value=True
            else:
                key_words_value=False
                break

    if echo != None:
        if key_words_value==True and num<prob:
            list_r[0]='t'
            list_r[1]=echo
            return list_r
        if key_words_value==True and num>=prob and els!=None:
            list_r[0]='t'
            list_r[1]=els
            return list_r
    elif photo!=None:
        if key_words_value==True and num<prob:
            list_r[0]='p'
            list_r[1]=photo[randrange(len(photo))]
            return list_r
    elif video != None:
        if key_words_value==True and num<prob:
            list_r[0]='v'
            list_r[1]=video[randrange(len(video))]
            return list_r
    elif sticker != None:
        if key_words_value==True and num<prob:
            list_r[0]='s'
            list_r[1]=stickerrandrange(len(sticker))
            return list_r
    return None

def key_word_reaction_json(word):
    global kw_j_buffer
    list_k=[]
    for i in kw_j_buffer:
        temp_t=find_word_TAKEVER(word,i['key_words'],echo=i['echo'],prob=i['prob'],els=i['els'],allco=i['allco'],photo =i['photo'], video=i['video'],sticker=i['sticker'])
        if temp_t != None:
            list_k.append(temp_t)
    return list_k


def key_word_reaction(bot,update):
    def find_word(words, echo=None, prob=1000, els=None,photo =None, video=None, allco=False, passArg=[]):
        # words: words need to reaction
        # echo, photo, video: msg send after reaction
        # prob: probability, if not, send els msg (1 for 0.1%)
        # els: if not in prob
        # allco: if words are all correct will go
        # passArg: if true, the function will never go; default is false
        key_words=update.message.text
        cid=update.message.chat_id
        # a random number from 0 to 999
        num = randrange(1000)
        key_words_value=False
        for check in words:
            if allco == False:
                "one word correct will go"
                if key_words.find(check)!=-1:
                    key_words_value=True
            if allco == True:
                "all word correct will go"
                if key_words.find(check)!=-1:
                    key_words_value=True
                else:
                    key_words_value=False
                    break
        for fp in passArg:
            if fp==True:
                key_words_value=False       
        if echo != None:
            if key_words_value==True and num<prob:
                bot.send_message(chat_id=cid,text=echo)
            if key_words_value==True and num>=prob and els!=None:
                if els.find('https://')!=-1:
                    bot.send_video(chat_id=cid, video=els)
                else:
                    bot.send_message(chat_id=cid,text=els)
        elif video != None:
            if key_words_value==True and num<prob:
                try:
                    vd=video[randrange(len(video))]
                    bot.send_video(chat_id=cid, video=vd)
                except:
                    bot.send_video(chat_id=cid, video=video)
        elif photo != None:
            if key_words_value==True and num<prob:
                bot.send_photo(chat_id=cid, photo=photo)
        if key_words_value:
            yuunou(bot,update)
        return key_words_value
    
    if get_config(update.message.from_user.id,'s') != True:
        react=y=key_word_reaction_json(update.message.text)
        for i in react:
            if i!=None:
                if i[0]=='t':
                    bot.send_message(chat_id=update.message.chat_id, text=i[1])
                elif i[0]=='p':
                    bot.send_photo(chat_id=update.message.chat_id, photo=i[1])
                elif i[0]=='s':
                    bot.send_sticker(chat_id=update.message.chat_id, sticker=i[1])
                elif i[0]=='v':
                    bot.send_video(chat_id=update.message.chat_id, video=i[1])
                


    # word_pass
    misaki_pass=find_word(words=['#美咲請安靜'])
    try_pass=find_word(words=['天','ナンス','もちょ'],allco=True)

    # long url
    pic_ten=['https://i.imgur.com/XmWYqS1.mp4',
    'https://imgur.com/LYBnOzo.mp4',
    'https://i.imgur.com/denCUYX.mp4']
    pic_trys=['https://img.gifmagazine.net/gifmagazine/images/2289135/original.mp4',
    'https://i.imgur.com/b9s69iK.mp4',
    'https://img.gifmagazine.net/gifmagazine/images/1333179/original.mp4']

    # word_echo
    find_word(passArg=[misaki_pass],words=['大老','dalao','ㄉㄚˋㄌㄠˇ','巨巨','Dalao','大 佬'],echo='你才大佬！你全家都大佬！', prob=200)
    find_word(passArg=[misaki_pass],words=['依田','芳乃'], echo='ぶおおー')
    find_word(passArg=[misaki_pass],words=['青羽','美咲'], echo='お疲れ様でした！')
    find_word(passArg=[misaki_pass],words=['ころあず'], echo='ありがサンキュー！')
    find_word(passArg=[misaki_pass],words=['この歌声が'], echo='MILLLLLIIIONNNNNN',els='UNIIIIIOOONNNNN',prob=500)
    find_word(passArg=[misaki_pass],words=['天','ナンス','もちょ'],video=pic_trys,allco=True)
    find_word(passArg=[misaki_pass,try_pass],words=['麻倉','もも','もちょ'], echo='(●･▽･●)',els='(o・∇・o)もちー！もちもちもちもちもちーーーもちぃ！',prob=900)
    find_word(passArg=[misaki_pass,try_pass],words=['夏川','椎菜','ナンス'], echo='(*>△<)<ナーンナーンっ',els='https://imgur.com/AOfQWWS.mp4',prob=300)
    find_word(passArg=[misaki_pass,try_pass],words=['雨宮','てん','天ちゃん'], video=pic_ten)
    find_word(passArg=[misaki_pass,try_pass],words=['天'], prob=15, video=pic_ten)
    find_word(passArg=[misaki_pass],words=['終わり','結束','沒了','完結'], echo='終わりだよ(●･▽･●)')
    find_word(passArg=[misaki_pass],words=['小鳥'], echo='もしかして〜♪ 音無先輩についてのお話ですか')
    find_word(passArg=[misaki_pass],words=['誰一百'], echo='咖嘎雅哭')
    find_word(passArg=[misaki_pass],words=['咖嘎雅哭'], echo='吼西米～那咧')
    find_word(passArg=[misaki_pass],words=['vertex'], echo='IDOL!')
    find_word(passArg=[misaki_pass],words=['高木','社長','順二朗'], echo='あぁ！社長のことを知りたい！')
    find_word(passArg=[misaki_pass],words=['天海','春香'], echo='天海さんのクッキーはとっても美味しいですね〜')
    find_word(passArg=[misaki_pass],words=['閣下'], echo='え！？もしかして春香ちゃん！？',els='恐れ、平れ伏し、崇め奉りなさいのヮの！',prob=900)
    find_word(passArg=[misaki_pass],words=['如月','千早'], echo='如月さんの歌は素晴らしい！',els='静かな光は蒼の波紋 VERTEX BLUE!!!!',prob=720)
    find_word(passArg=[misaki_pass],words=['72'],prob=100, echo='こんな言えば如月さんは怒ってしまうよ！')
    find_word(passArg=[misaki_pass],words=['星井','美希'], echo='あの...星井さんはどこかで知っていますか？')
    find_word(passArg=[misaki_pass],words=['高槻','やよい'], echo="ζ*'ヮ')ζ＜うっうー ")
    find_word(passArg=[misaki_pass],words=['萩原','雪歩'], echo='あ、先のお茶は萩原さんからの')
    find_word(passArg=[misaki_pass],words=['秋月','律子'], echo='律子さんは毎日仕事するで、大変ですよね〜')
    find_word(passArg=[misaki_pass],words=['三浦','あずさ'], echo='え？あずささんは今北海道に！？')
    find_word(passArg=[misaki_pass],words=['水瀬','伊織'], echo='このショコラは今朝水瀬さんからの、みな一緒に食べろう！')
    find_word(passArg=[misaki_pass],words=['菊地','真'], echo='真さんは今、王子役の仕事をしていますよ。',els='真さんは今、ヒーロー役の仕事をしていますよ～～激しい光は黒の衝撃 VERTEX BLACK!!!!',prob=700,allco=True)
    find_word(passArg=[misaki_pass],words=['我那覇','響'], echo='ハム蔵はどこでしょうか？探していますね',els='弾ける光は浅葱の波濤 VERTEX LIGHTBLUE!!',prob=700,allco=True)
    find_word(passArg=[misaki_pass],words=['四条','貴音'], echo='昨日〜貴音さんがわたしに色々な美味しい麺屋を紹介しました！',els='秘めたり光は臙脂の炎 VERTEX CARMINE〜〜',prob=700)
    find_word(passArg=[misaki_pass],words=['亜美'], echo='亜美？あそこよ')
    find_word(passArg=[misaki_pass],words=['真美'], echo='真美？いないよ')
    find_word(passArg=[misaki_pass],words=['双海'], echo='亜美真美？先に外へ行きました')
    find_word(passArg=[misaki_pass],words=['なんなん'], photo=open('nannnann.jpg', 'rb'))

    ###################################
    #          quote collector        #
    ###################################
    record=False
    test=update.message.text
    if test.find(' #名言')!=-1 or test.find('#名言 ')!=-1:
        if update.message.reply_to_message==None and update.message.from_user.is_bot==False:
            test=test.replace(' #名言','').replace('#名言 ','')
            qlist=[test,update.message.from_user.first_name]
            work_sheet_push(qlist,'quote_main')
            record=True
    if test.find('#名言')!=-1 and record==False:
        if update.message.reply_to_message is not None and update.message.reply_to_message.from_user.is_bot==False:
            qlist=[update.message.reply_to_message.text,update.message.reply_to_message.from_user.first_name]
            work_sheet_push(qlist,'quote_main')
            
    
    ###################################
    #          bot_historian          #
    ###################################
    #refresh token
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key)
    worksheet=sheet.worksheet('last_message_misaki')
    chat_id=update.message.chat_id
    #record all message_id
    lmessage_id=update.message.message_id
    list=[str(chat_id),lmessage_id]
    try:
        #find chat_id
        cell=worksheet.find(str(chat_id))
    except:
        #ERROR:not found
        #creat new record
        worksheet.insert_row(list, 2)
    else:
        #replace record
        worksheet.update_cell(cell.row,cell.col+1,lmessage_id)

def message_callback(bot, update):

    ###################################
    #              aisatu             #
    ###################################
    if update.message.new_chat_members != None:
        for u in update.message.new_chat_members:
            if u.is_bot == False:
                text='$usernameさん、ようこそ事務所へ！\n輸入 /help 可以尋求幫助'
                # text = text.replace('$username',u.first_name.encode('utf-8'))
                text = text.replace('$username',u.first_name)
                bot.send_message(chat_id=update.message.chat_id,text=text)
                yuunou(bot,update)

    if update.message.left_chat_member != None:
        if update.message.left_chat_member.is_bot == False:
            text='まだ会いましょう！$usernameさん！'
            # text = text.replace('$username',update.message.left_chat_member.first_name.encode('utf-8'))
            text = text.replace('$username',update.message.left_chat_member.first_name)
            bot.send_message(chat_id=update.message.chat_id,text=text)
            yuunou(bot,update)

    
def mission_callback(bot,job):
    # somaction

    # 玩人狼玩到忘記每日
    bot.send_message(chat_id='-1001290696540',text=GLOBAL_WORDS.word_do_mission)
    
def group_history(bot,job):
    ######################
    #put in your group id#
    ######################
    chat_id=-1001290696540
    ######################
    #put in your group id#
    ######################    
    time = datetime.now().strftime("%y/%m/%d %H:%M:%S")#+0 time

    #refresh token
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key)
    #get last_message_id
    worksheet=sheet.worksheet('last_message_misaki')
    c=get_cell(str(chat_id),worksheet)
    message_id=worksheet.cell(c.row,c.col+1).value
    count=bot.get_chat_members_count(chat_id)
    #create record and save it
    list=[str(chat_id),time,message_id,str(count)]
    work_sheet_push(list,'server')
    #get info 'now'
    worksheet=sheet.worksheet('server')
    w=get_cell(str(chat_id),worksheet)
    #calculate
    water=int(worksheet.cell(w.row,w.col+2).value)-int(worksheet.cell(w.row+1,w.col+2).value)
    human=int(worksheet.cell(w.row,w.col+3).value)-int(worksheet.cell(w.row+1,w.col+3).value)
    rate='在過去的幾個小時內，本群組增加了$water則訊息、加入$human位成員'
    rate=rate.replace('$water',str(water))
    rate=rate.replace('$human',str(human))
    bot.send_message(chat_id=-1001290696540,text=rate)
   
def daily_reset(bot,job):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key)
    user_config=sheet.worksheet('config').get_all_values()
    for i in user_config:
        if i[1].find('q') != -1:
            set_config(i[0],'q')

def key_word_j_buffer(bot,job):
    global kw_j_buffer
    kw_j_buffer=[]
    #clean buffer
    k=[]
    key_word_j=get_sheet('key_word_j_m')
    try:
        k=key_word_j.get_all_values()
    except:
        return
    else:
        for i in k:
            temp=json.loads(i[0])
            kw_j_buffer.append(temp)
################################################
#                   main                       #
################################################
def main():
    """Start the bot."""
    # ---Record init time---
    global init_time
    init_time = datetime.now()

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # <function start>

    # ---daily jobs---
    # mission_callback every 22:30 daily
    updater.job_queue.run_daily(mission_callback,stime(14,30))
    # mission_show record every 8 hours
    m_history=[stime(7,0,0),stime(15,0,0),stime(23,0,0)]
    for t in m_history:
        #plug in mission time with loop
        updater.job_queue.run_daily(group_history,t)
    #mission refresh daily gasya
    updater.job_queue.run_daily(daily_reset,stime(14,59,59))
    #refresh buffer
    updater.job_queue.run_repeating(key_word_j_buffer, interval=60, first=0)
    # ---Command answer---
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("rule", rule))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("tbgame", tbgame))
    dp.add_handler(CommandHandler("state", state))
    dp.add_handler(CommandHandler("config", config, pass_args=True))
    dp.add_handler(CommandHandler("set_remind_time", set_remind_time, pass_args=True))
    dp.add_handler(CommandHandler("nanto", nanto, pass_args=True))
    dp.add_handler(CommandHandler("tiger", tiger))
    dp.add_handler(CommandHandler("notiger", notiger))
    dp.add_handler(CommandHandler("which", which, pass_args=True))
    dp.add_handler(CommandHandler("dice", dice, pass_args=True))
    dp.add_handler(CommandHandler("quote",quote))
    dp.add_handler(CommandHandler("sendmsg", sendmsg, pass_args=True))
    # dp.add_handler(CommandHandler("title", title, pass_args=True))

    # ---Message answer---
    dp.add_handler(MessageHandler(Filters.text, key_word_reaction))
    dp.add_handler(MessageHandler(Filters.all, message_callback))
    
    # <function end>

    # log all errors
    dp.add_error_handler(error)
    
    # Start the Bot
    updater.start_polling(clean=True)

    # IDLE
    updater.idle()


################################################
#                   program                    #
################################################
if __name__ == '__main__':
    main()
