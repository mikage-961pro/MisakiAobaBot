# coding=utf-8

bot_name='@MisakiAobaBot'
################################################
#              Global Setting                  #
################################################

### ---Module---

# ---Python function
import datetime as dt
from datetime import datetime,tzinfo,timedelta
from datetime import time as stime#specific time
import logging
import time
import os
from random import randrange
import random
import json
from string import Template
from functools import wraps

# ---Telegram
from telegram import Bot, Chat, Sticker, ReplyKeyboardMarkup,ForceReply
from telegram import ReplyKeyboardRemove, ParseMode
from telegram import InlineQueryResultArticle, InputTextMessageContent,InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,JobQueue,CallbackQueryHandler
from telegram.ext.dispatcher import run_async

token = os.environ['TELEGRAM_TOKEN']
updater = Updater(token,workers=16)
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# ---Google Database
import gspread
from oauth2client.service_account import ServiceAccountCredentials
spreadsheet_key=os.environ['SPREAD_TOKEN']

# ---postgresql
from postgre import dbDump,dbrandGet,dbGet

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
collect = db['misaki_setting']

# ---User Module
from global_words import GLOBAL_WORDS
from tk import do_once, del_cmd, do_after_root, admin_cmd, del_cmd_func
from tk import db_switch_one_value, bool2text, room_member_num, bot_is_admin, is_admin, c_tz
from tk import init_time
from tk import get_config, set_config, work_sheet_pop, work_sheet_push, get_sheet
import MisaMongo
# ---Buffers
#悲觀鎖
kw_j_buffer=[]
kw_j_buffer_Plock=False
config_buffer=[]
config_buffer_Plock=False
last_message_list=[]

################################################
#                   command                    #
################################################
@do_after_root
def start(bot, update):
    """Send a message when the command /start is issued."""
    bot.send_message(chat_id=update.message.chat_id,
                    text=GLOBAL_WORDS.word_start,
                    parse_mode=ParseMode.HTML)

@do_after_root
@del_cmd
def help(bot, update):
    """Send a message when the command /help is issued."""
    if randrange(1000)<30:
        bot.send_message(chat_id=update.message.chat_id, text="ぜ")
    else:
        bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_help,
                    parse_mode=ParseMode.HTML)

@do_after_root
@del_cmd
def tbgame(bot, update):
    """Send a message when the command /tbgame is issued."""
    bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_tbgame,
                    parse_mode=ParseMode.HTML)

@run_async
@do_after_root
@del_cmd
def rule(bot, update):
    """Send a message when the command /rule is issued."""
    if randrange(1000)<30:
        bot.send_message(chat_id=update.message.chat_id, text="ぜ")
    else:
        msg=bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_rule,
                        parse_mode=ParseMode.HTML)
        time.sleep(60)
        bot.delete_message(chat_id=update.message.chat_id, message_id=msg.message_id)

@do_after_root
def config(bot, update):
    """Send a message when the command /config is issued."""
    """Config is use to let user to turn on/off some function"""
    bot.send_message(chat_id=update.message.chat_id,
        text='何がご用事ですか？',
        reply_markup=main_menu_keyboard())

@run_async
@do_after_root
@del_cmd
def nanto(bot, update, args):
    """Send a message when the command /nanto is issued."""
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

@do_after_root
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

@do_after_root
def quote(bot,update):
    global config_buffer
    global config_buffer_Plock

    #daily quote
    if get_config(update.message.from_user.id,'q',config_buffer,config_buffer_Plock)==True:
        del_cmd_func(bot,update)
        return
    else:

        config_buffer=set_config(update.message.from_user.id,'q')

        del_cmd_func(bot,update)
    quote=MisaMongo.randget()[0]
    text='<pre>'+quote['quote']+'</pre>\n'+'-----<b>'+quote['said']+'</b> より'
    msg=bot.send_message(chat_id=update.message.chat_id,text=text,parse_mode='HTML')

@do_after_root
def randchihaya(bot,update):
    url=dbrandGet('randchihaya','url')
    bot.send_photo(chat_id=update.message.chat_id,photo=url)

@do_after_root
def randtsumugi(bot,update):
    url=dbrandGet('randtsumugi','url')
    bot.send_photo(chat_id=update.message.chat_id,photo=url)

@do_after_root
def sticker_matome(bot,update):
    link=dbGet('sticker',['setname','about'])
    slink=''
    for i in link:
        slink=slink+'<a href="https://telegram.me/addstickers/'+i[0]+'">'+i[1]+'</a>\n'
    try:
        bot.send_message(chat_id=update.message.from_user.id,text=slink,parse_mode='HTML')
    except:
        startme='<a href="https://telegram.me/MisakiAobaBot?start=sticker">請先在私訊START♪</a>'
        bot.send_message(chat_id=update.message.chat_id,text=startme,parse_mode='HTML')
    else:
        bot.send_message(chat_id=update.message.chat_id,text='看私訊～～♪')

@do_after_root
def savepic(bot, update):
    """Send a message when the command /savepic is issued."""
    """Send msg to ask user and save pic"""
    #f=ForceReply(force_reply=True, selective=False)
    rpl=bot.send_message(chat_id=update.message.chat_id,
        text='何がご用事ですか？',reply_markup=ForceReply)

################################################
#               not command                    #
################################################
def find_word_TAKEVER(sentence,key_words, echo=None, prob=1000, els=None,photo =None, video=None,sticker=None, allco=False,passArg=[]):
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
    for i in passArg:
        if i==True:
            key_words_value=False

    if echo != None:
        if key_words_value==True and num<prob:
            list_r[0]='t'
            list_r[1]=echo
            return list_r
        if key_words_value==True and num>=prob and els!=None:
            if els.find('http')!=-1:
                list_r[0]='v'
            else:
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
    lr=[None,key_words_value]
    return lr

def key_word_reaction_json(word):
    global kw_j_buffer
    global kw_j_buffer_Plock
    list_k=[]

    passArg={'misaki_pass':find_word_TAKEVER(word,['#美咲請安靜'])[1],'try_pass':find_word_TAKEVER(word,['天','ナンス','もちょ'],allco=True)[1]}
    if kw_j_buffer_Plock==True:
        time.sleep(1)
    #if buffer is refreshing
    for i in kw_j_buffer:
        pl=[]
        for j in i['passArg']:
            pl.append(passArg[j])
        temp_t=find_word_TAKEVER(word,i['key_words'],echo=i['echo'],prob=i['prob'],els=i['els'],allco=i['allco'],photo =i['photo'], video=i['video'],sticker=i['sticker'],passArg=pl)
        if temp_t != None:
            list_k.append(temp_t)
    return list_k


def key_word_reaction(bot,update):
    ###################################
    #        key word reaction        #
    ###################################
    def find_word(words, echo=None, prob=1000, els=None,photo=None,
        video=None, allco=False, passArg=[], echo_list=False):
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
                if echo_list:
                    ts=echo[randrange(len(echo))]
                    bot.send_message(chat_id=cid,text=ts)
                else:
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
                finally:
                    pass
        elif photo != None:
            if key_words_value==True and num<prob:
                bot.send_photo(chat_id=cid, photo=photo)
        return key_words_value

    # switch
    switch=MisaMongo.display_data('config',{'id':update.message.from_user.id},'reply')

    # word_pass
    try_pass=find_word(words=['天','ナンス','もちょ'],allco=True)


    # long url
    pic_ten=['https://i.imgur.com/XmWYqS1.mp4',
    'https://imgur.com/LYBnOzo.mp4',
    'https://i.imgur.com/denCUYX.mp4']
    pic_trys=['https://img.gifmagazine.net/gifmagazine/images/2289135/original.mp4',
    'https://i.imgur.com/b9s69iK.mp4',
    'https://img.gifmagazine.net/gifmagazine/images/1333179/original.mp4']

    # word_echo
    if switch == True:
        find_word(words=['大老','dalao','ㄉㄚˋㄌㄠˇ','巨巨','Dalao','大 佬'],echo='你才大佬！你全家都大佬！', prob=200)
        find_word(words=['依田','芳乃'], echo='ぶおおー')
        find_word(words=['青羽','美咲'], echo='お疲れ様でした！')
        find_word(words=['ころあず'], echo='ありがサンキュー！')
        find_word(words=['この歌声が'], echo='MILLLLLIIIONNNNNN',els='UNIIIIIOOONNNNN',prob=500)
        find_word(words=['天','ナンス','もちょ'],video=pic_trys,allco=True)
        find_word(passArg=[try_pass],words=['麻倉','もも','もちょ'], echo='(●･▽･●)',els='(o・∇・o)もちー！もちもちもちもちもちーーーもちぃ！',prob=900)
        find_word(passArg=[try_pass],words=['夏川','椎菜','ナンス'], echo='(*>△<)<ナーンナーンっ',els='https://imgur.com/AOfQWWS.mp4',prob=300)
        find_word(passArg=[try_pass],words=['雨宮','てん','天ちゃん'], video=pic_ten)
        find_word(passArg=[try_pass],words=['天'], prob=15, video=pic_ten)
        find_word(words=['終わり','結束','沒了','完結'], echo='終わりだよ(●･▽･●)')
        find_word(words=['小鳥'], echo='もしかして〜♪ 音無先輩についてのお話ですか')
        find_word(words=['誰一百'], echo='咖嘎雅哭')
        find_word(words=['咖嘎雅哭'], echo='吼西米～那咧')
        find_word(words=['vertex'], echo='IDOL!')
        find_word(words=['高木','社長','順二朗'], echo='あぁ！社長のことを知りたい！')
        find_word(words=['天海','春香'], echo='天海さんのクッキーはとっても美味しいですね〜')
        find_word(words=['閣下'], echo='え！？もしかして春香ちゃん！？',els='恐れ、平れ伏し、崇め奉りなさいのヮの！',prob=900)
        find_word(words=['如月','千早'], echo='如月さんの歌は素晴らしい！',els='静かな光は蒼の波紋 VERTEX BLUE!!!!',prob=720)
        find_word(words=['72'],prob=10, echo='こんな言えば如月さんは怒ってしまうよ！')
        find_word(words=['星井','美希'], echo='あの...星井さんはどこかで知っていますか？')
        find_word(words=['高槻','やよい'], echo="ζ*'ヮ')ζ＜うっうー ")
        find_word(words=['萩原','雪歩'], echo='あ、先のお茶は萩原さんからの')
        find_word(words=['秋月','律子'], echo='律子さんは毎日仕事するで、大変ですよね〜')
        find_word(words=['三浦','あずさ'], echo='え？あずささんは今北海道に！？')
        find_word(words=['水瀬','伊織'], echo='このショコラは今朝水瀬さんからの、みな一緒に食べろう！')
        find_word(words=['菊地','真'], echo='真さんは今、王子役の仕事をしていますよ。',els='真さんは今、ヒーロー役の仕事をしていますよ～～激しい光は黒の衝撃 VERTEX BLACK!!!!',prob=700,allco=True)
        find_word(words=['我那覇','響'], echo='ハム蔵はどこでしょうか？探していますね',els='弾ける光は浅葱の波濤 VERTEX LIGHTBLUE!!',prob=700,allco=True)
        find_word(words=['四条','貴音'], echo='昨日〜貴音さんがわたしに色々な美味しい麺屋を紹介しました！',els='秘めたり光は臙脂の炎 VERTEX CARMINE〜〜',prob=700)
        find_word(words=['亜美'], echo='亜美？あそこよ')
        find_word(words=['真美'], echo='真美？いないよ')
        find_word(words=['双海'], echo='亜美真美？先に外へ行きました')
    ###################################
    #               NAZO              #
    ###################################
    test=update.message.text
    if test.find('tumu@db')!=-1:
        rmsg=update.message.reply_to_message
        col=['name','url']
        if rmsg.text.find('http')!=-1:
            data=['adp',rmsg.text]
            dbDump('randtsumugi',data,col)
            bot.send_message(chat_id=update.message.chat_id,text='ok~~')
            return
    ###################################
    #          quote collector        #
    ###################################
    record=False
    test=update.message.text
    if test.find(' #名言')!=-1 or test.find('#名言 ')!=-1:
        if update.message.reply_to_message==None and update.message.from_user.is_bot==False:
            test=test.replace(' #名言','').replace('#名言 ','')
            qdict={'quote': test, 'said': update.message.from_user.first_name, 'tag': '','said_id':update.message.from_user.id}
            MisaMongo.insert_data('quote_main',qdict)
            record=True
    if test.find('#名言')!=-1 and record==False:
        if update.message.reply_to_message is not None and update.message.reply_to_message.from_user.is_bot==False:
            qdict={'quote': update.message.reply_to_message.text, 'said': update.message.reply_to_message.from_user.first_name, 'tag': '','said_id':update.message.reply_to_message.from_user.id}
            MisaMongo.insert_data('quote_main',qdict)


    ###################################
    #          bot_historian          #
    ###################################
    chat_id=update.message.chat_id
    lmessage_id=update.message.message_id
    list=[str(chat_id),lmessage_id]
    global last_message_list
    fvalue=False
    for i in last_message_list:
        if i[0].find(list[0])!=-1:
            fvalue=True
            i[1]=list[1]
            break
    if fvalue==False:
        last_message_list.append(list)


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

def daily_reset(bot,job):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key)
    user_config=sheet.worksheet('config').get_all_values()
    for i in user_config:
        if i[1].find('q') != -1:
            set_config(i[0],'q')

def refresh_buffer(bot,job):
    #key_word_j_buffer
    global kw_j_buffer
    global kw_j_buffer_Plock
    kw_j_buffer_temp=[]
    k=[]
    key_word_j=get_sheet('key_word_j_m')
    try:
        k=key_word_j.get_all_values()
    except:
        return
    else:
        for i in k:
            try:
                temp=json.loads(i[0])
            except:
                pass
            else:
                kw_j_buffer_temp.append(temp)
    #lock
    kw_j_buffer_Plock=True
    kw_j_buffer=kw_j_buffer_temp
    kw_j_buffer_Plock=False
    #unlock

    #config_buffer
    global config_buffer
    global config_buffer_Plock
    config_sheet=get_sheet('config')
    config_buffer_Plock=True
    config_buffer=config_sheet.get_all_values()
    config_buffer_Plock=False

    #refresh lstmessage
    global last_message_list

    worksheet=get_sheet('last_message_misaki')
    for i in last_message_list:
        try:
            cell=worksheet.find(i[0])
        except:#not found
            worksheet.insert_row(i, 1)
        else:
            worksheet.update_cell(cell.row,cell.col+1,i[1])


################################################
#              menu command                    #
################################################
def menu_actions(bot, update):
    query = update.callback_query
    query_text=query.data
    def fin_text():
        bot.edit_message_text(text="了解しました♪",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
    if query_text == "main":
        bot.edit_message_text(chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text='何がご用事ですか？',
            reply_markup=main_menu_keyboard())
    elif query_text == "cmd_state":
        fin_text()
        temp=Template(GLOBAL_WORDS.word_state)
        un=str(room_member_num(bot,update=query))
        text=temp.substitute(user_number=un)
        bot.send_message(text=text,chat_id=query.message.chat_id)
    elif query_text == "cmd_about":
        fin_text()
        temp=Template(GLOBAL_WORDS.word_about)
        rt=str((init_time+timedelta(hours=8)).strftime("%y/%m/%d %H:%M:%S"))
        text=temp.substitute(boot_time=rt)
        bot.send_message(text=text,chat_id=query.message.chat_id,parse_mode=ParseMode.HTML)
    elif query_text == "cmd_resp_check":
        data_value = MisaMongo.display_data('config',{'id':query.from_user.id},'reply')
        if data_value is None:
            data_value=True#default open
        text='{}P目前狀態：{}'.format(query.from_user.first_name,bool2text(data_value))
        bot.edit_message_text(chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text=text,
                reply_markup=sub_menu_keyboard(data_value))
    elif query_text == "cmd_resp_switch_off":
        MisaMongo.modify_data('config',pipeline={'id':query.from_user.id},key='reply',update_value=False)
        bot.edit_message_text(chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text="停止{}的回話功能。".format(query.from_user.first_name))
    elif query_text == "cmd_resp_switch_on":
        MisaMongo.modify_data('config',pipeline={'id':query.from_user.id},key='reply',update_value=True)
        bot.edit_message_text(chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text="開啟{}的回話功能。".format(query.from_user.first_name))

# Keyboards
def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton(text='回話設定',callback_data='cmd_resp_check'),
               InlineKeyboardButton(text='群組狀態',callback_data="cmd_state")],
              [InlineKeyboardButton(text='關於美咲',callback_data="cmd_about")]]
    return InlineKeyboardMarkup(keyboard)

def sub_menu_keyboard(state):
    keyboard = [[InlineKeyboardButton(text='關閉回話' if state else '開啟回話',callback_data='cmd_resp_switch_off' if state else 'cmd_resp_switch_on')],
                [InlineKeyboardButton(text='取消',callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)
################################################
#                   init                       #
################################################
@do_once
def initialization():
    # ---Record init time---
    global init_time
    init_time = datetime.now()
################################################
#                   main                       #
################################################
def main():
    """Start the bot."""

    # <initialization>
    initialization()

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # <function start>

    # ---repeating jobs---
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
    updater.job_queue.run_repeating(refresh_buffer, interval=60, first=0)


    # ---Command answer---
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("rule", rule))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("tbgame", tbgame))
    dp.add_handler(CommandHandler("config", config))
    dp.add_handler(CommandHandler("nanto", nanto, pass_args=True))
    dp.add_handler(CommandHandler("which", which, pass_args=True))
    dp.add_handler(CommandHandler("quote",quote))
    dp.add_handler(CommandHandler("randChihaya",randchihaya))
    dp.add_handler(CommandHandler("randTsumugi",randtsumugi))
    dp.add_handler(CommandHandler("sticker",sticker_matome))
    dp.add_handler(CallbackQueryHandler(menu_actions))
    # test function
    dp.add_handler(CommandHandler("savepic",savepic))

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
