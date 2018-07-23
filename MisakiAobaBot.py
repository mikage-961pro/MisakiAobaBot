# coding=utf-8

################################################
#                   Global                     #
################################################
# import
from telegram import (Bot, Chat, Sticker, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,JobQueue
from datetime import datetime,tzinfo,timedelta
from datetime import time as stime#specific time
import logging
import time
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from global_words import GLOBAL_WORDS

init_time = -1

bot_name='@MisakiAobaBot'
token = os.environ['TELEGRAM_TOKEN']
spreadsheet_key=os.environ['SPREAD_TOKEN']
# token will taken by heroku
# Please use test token when dev
# WARNING!!! Please use quarter space instead of tab
# This will cause fatal error

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

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
    worksheet = client.open_by_key(spreadsheet_key)
    try:
        worksheet=sheet.worksheet(worksheet_name)
    except:#there is no this worksheet
        sheet.add_worksheet(woksheet_name,len(values),2)
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
    worksheet = client.open_by_key(spreadsheet_key)
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
        bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_help, 
                        parse_mode=ParseMode.HTML)

def tbgame(bot, update):
    """Send a message when the command /tbgame is issued."""
    if update.message.date > init_time:
        bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_tbgame, 
                        parse_mode=ParseMode.HTML)

def rule(bot, update):
    """Send a message when the command /rule is issued."""
    if update.message.date > init_time:
        bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_rule, 
                        parse_mode=ParseMode.HTML)

def state(bot, update):
    """Send a message when the command /state is issued."""
    if update.message.date > init_time:
        bot.send_message(chat_id=update.message.chat_id,
        text='目前室內人數：{}'.format(str(bot.get_chat_members_count(update.message.chat.id)))+'\n'+
        GLOBAL_WORDS.word_state,parse_mode=ParseMode.HTML)

def config(bot, update,args):
    """Send a message when the command /config is issued."""
    if update.message.date > init_time:
        word_kachikoi_name=GLOBAL_WORDS.word_kachikoi_1.replace('$name',' '.join(args))
        if not args:
            bot.send_message(chat_id=update.message.chat_id, text="本功能目前沒有毛用")
        else:
            bot.send_message(chat_id=update.message.chat_id, text=word_kachikoi_name,
            parse_mode=ParseMode.HTML)
            time.sleep(9)
            bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_kachikoi_2,
            parse_mode=ParseMode.HTML)
            time.sleep(9)
            bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_kachikoi_3,
            parse_mode=ParseMode.HTML)

def nanto(bot, update):
    """Send a message when the command /nanto is issued."""
    if update.message.date > init_time:
        bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_nanto_1)
        time.sleep(1)
        bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_nanto_2)
        time.sleep(0.5)
        bot.send_sticker(chat_id=update.message.chat_id, sticker="CAADBQADGgADT1ZbIFSw_UAI28HiAg")
        time.sleep(2)
        bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_nanto_4)

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

def notiger(bot, update):
    """Send a message when the command /notiger is issued."""
    if update.message.date > init_time:
        bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_notiger, 
                    parse_mode=ParseMode.HTML)
                  
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
    bot.send_message(chat_id='-1001290696540',text='做每日')
################################################
#                   main                       #
################################################
def main():
    """Start the bot."""
    # ---Record init time---
    global init_time
    init_time = datetime.now()

    # ---TOKEN---
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # <function start>

    # ---daily jobs---
    # mission_callback every 22:30 daily
    updater.job_queue.run_daily(mission_callback,stime(14,30))

    # ---Command answer---
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("rule", rule))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("tbgame", tbgame))
    dp.add_handler(CommandHandler("state", state))
    dp.add_handler(CommandHandler("config", config, pass_args=True))
    dp.add_handler(CommandHandler("set_remind_time", set_remind_time, pass_args=True))
    dp.add_handler(CommandHandler("nanto", nanto))
    dp.add_handler(CommandHandler("notiger", notiger))
    # dp.add_handler(CommandHandler("title", title, pass_args=True))

    # ---Message answer---
    #dp.add_handler(MessageHandler(Filters.sticker, echo))
    #dp.add_handler(MessageHandler(Filters.text, echo2))
    #dp.add_handler(MessageHandler(Filters.command, unknown))
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
