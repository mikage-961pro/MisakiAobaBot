# coding=utf-8

################################################
#                   Global                     #
################################################
# import
from telegram import (Bot, Chat, Sticker, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,JobQueue
from telegram.ext.dispatcher import run_async
import datetime as dt
from datetime import datetime,tzinfo,timedelta
from datetime import time as stime#specific time
import logging
import time
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from global_words import GLOBAL_WORDS
from random import randrange

init_time = -1

bot_name='@MisakiAobaBot'
token = os.environ['TELEGRAM_TOKEN']
spreadsheet_key=os.environ['SPREAD_TOKEN']
# token will taken by heroku
# Please use test token when dev
# WARNING!!! Please use quarter space instead of tab
# This will cause fatal error
# ---TOKEN---
updater = Updater(token,workers=16)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

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
    #bool func to check auth
    adminlist=update.message.chat.get_administrators()
    is_admin=False
    for i in adminlist:
        if update.message.from_user.id==i.user.id:
            is_admin=True
    return is_admin

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
        spreadsheet.add_worksheet(worksheet_name,len(values),2)
        worksheet=spreadsheet.worksheet(worksheet_name)
        worksheet.insert_row(values,2)
    else:
        worksheet.insert_row(values,2)
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

def help(bot, update):
    """Send a message when the command /help is issued."""
    if update.message.date > init_time:
        if randrange(1000)<30:
            bot.send_message(chat_id=update.message.chat_id, text="ぜ")
        else:
            bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_help, 
                        parse_mode=ParseMode.HTML)

def tbgame(bot, update):
    """Send a message when the command /tbgame is issued."""
    if update.message.date > init_time:
        bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_tbgame, 
                        parse_mode=ParseMode.HTML)

@run_async
def rule(bot, update):
    """Send a message when the command /rule is issued."""
    if update.message.date > init_time:
        if randrange(1000)<30:
            bot.send_message(chat_id=update.message.chat_id, text="ぜ")
        else:
            msg=bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_rule, 
                            parse_mode=ParseMode.HTML)
            time.sleep(60)
            bot.delete_message(chat_id=update.message.chat_id, message_id=msg.message_id)

def state(bot, update):
    """Send a message when the command /state is issued."""
    if update.message.date > init_time:
        bot.send_message(chat_id=update.message.chat_id,
        text='目前室內人數：{}'.format(str(bot.get_chat_members_count(update.message.chat.id)))+'\n'+
        GLOBAL_WORDS.word_state,parse_mode=ParseMode.HTML)

@run_async
def config(bot, update, args):
    """Send a message when the command /config is issued."""
    if update.message.date > init_time:
        word_kachikoi_name=GLOBAL_WORDS.word_kachikoi_1.replace('$name',' '.join(args))
        if not args:
            bot.send_message(chat_id=update.message.chat_id, text="本功能目前沒有毛用")
        else:
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

@run_async
def nanto(bot, update, args):
    """Send a message when the command /nanto is issued."""
    if update.message.date > init_time:
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
            
def which(bot, update, args):
    """Send a message when the command /which is issued."""
    if update.message.date > init_time:
        if not args:
            text="請輸入要給我決定的事情♪\n記得用〔＃〕分開喔！"
            msg=bot.send_message(chat_id=update.message.chat_id, text=text)
        else:
            things=' '.join(args).split('#')
            result=things[randrange(len(things))]
            text="わたしは〜♬［$res］が良いと思うよ〜えへへ。".replace('$res',result)
            msg=bot.send_message(chat_id=update.message.chat_id, text=text)


def dice(bot,update,args):
    """Send a message when the command /dice is issued."""
    dice=['⚀','⚁','⚂','⚃','⚄','⚅']
    count=[0,0,0,0,0,0]
    text=''
    if update.message.date > init_time:
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
                bot.send_message(chat_id=update.message.chat_id,text='できました！！')
            else:
                bot.send_message(chat_id=update.message.chat_id,text='失敗しました、能力不足ですね')
            
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

@run_async
def notiger(bot, update):
    """Send a message when the command /notiger is issued."""
    if update.message.date > init_time:
        msg=bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_notiger, 
                    parse_mode=ParseMode.HTML)
        time.sleep(10)
        bot.delete_message(chat_id=update.message.chat_id, message_id=msg.message_id)

def echo(bot, update):
    """Echo the user message."""
    bot.send_message(chat_id=update.message.chat_id, text=update.message.sticker.file_id)

def echo2(bot, update):
    """Echo the user message."""
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def unknown(bot, update):
    if update.message.text.find('MisakiAobaBot')!=-1:
        bot.send_message(chat_id=update.message.chat_id, text="すみません、よく分かりません。")

################################################
#                not command                   #
################################################
def key_word_reaction(bot,update):
    test=update.message.text
    dalao_check=test.find('大佬')!=-1 or\
        test.find('大老')!=-1 or\
        test.find('dalao')!=-1 or\
        test.find('ㄉㄚˋㄌㄠˇ')!=-1 or\
        test.find('巨巨')!=-1
    if dalao_check and randrange(100)<20:
        bot.send_message(chat_id=update.message.chat_id,text='你才大佬！你全家都大佬！')
def aisatu(bot, update):
    if update.message.new_chat_members != None:
        for u in update.message.new_chat_members:
            if u.is_bot == False:
                text='$usernameさん、ようこそ事務所へ！\n輸入 /help 可以尋求幫助'
                # text = text.replace('$username',u.first_name.encode('utf-8'))
                text = text.replace('$username',u.first_name)
                bot.send_message(chat_id=update.message.chat_id,text=text)

    if update.message.left_chat_member != None:
        if update.message.left_chat_member.is_bot == False:
            text='まだ会いましょう！$usernameさん！'
            # text = text.replace('$username',update.message.left_chat_member.first_name.encode('utf-8'))
            text = text.replace('$username',update.message.left_chat_member.first_name)
            bot.send_message(chat_id=update.message.chat_id,text=text)

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
   
def bot_historian(bot,update):
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
    # dp.add_handler(CommandHandler("title", title, pass_args=True))

    # ---Message answer---
    #dp.add_handler(MessageHandler(Filters.sticker, echo))
    #dp.add_handler(MessageHandler(Filters.text, echo2))
    #dp.add_handler(MessageHandler(Filters.command, unknown))
    dp.add_handler(MessageHandler(Filters.text, key_word_reaction))
    dp.add_handler(MessageHandler(Filters.all, bot_historian))
    dp.add_handler(MessageHandler(Filters.all, aisatu))
    
    # <function end>

    # log all errors
    dp.add_error_handler(error)
    
    # Start the Bot
    updater.start_polling()

    # IDLE
    updater.idle()


################################################
#                   program                    #
################################################
if __name__ == '__main__':
    main()
