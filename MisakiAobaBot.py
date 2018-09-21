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
from string import Template
from random import randrange

# ---Telegram
from telegram import Bot, Chat, Sticker, ReplyKeyboardMarkup,MessageEntity
from telegram import ReplyKeyboardRemove, ParseMode,ForceReply
from telegram import InlineQueryResultArticle, InputTextMessageContent,InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,JobQueue,CallbackQueryHandler
from telegram.ext.dispatcher import run_async
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)

token = os.environ['TELEGRAM_TOKEN']
updater = Updater(token,workers=16)

# ---error log setting
logging.basicConfig(format='[%(asctime)s](%(levelname)s) %(name)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# ---postgresql
from postgre import dbDump,dbrandGet,dbGet

# ---User Module
from global_words import GLOBAL_WORDS
from tk import do_once, del_cmd, do_after_root, admin_cmd
from tk import init_time
from tk import url_valid
import MisaMongo,tk

################################################
#                 Gloval var                   #
################################################
quote_search={} # Use on /quote
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
@run_async
def quote(bot,update,args):
    # search parameter
    search_para=tk.formula('f',' '.join(args))
    if search_para != False:
        if search_para=="":
            """Case 1: No words"""
            bot.send_message(chat_id=update.message.chat_id,text="Please enter word.")
            return
        # Search initialization
        find_result=MisaMongo.quote_finder(search_para)
        result_length=len(find_result)
        search_init_time=datetime.now()
        global quote_search

        if result_length==0:
            """Case 2: No search result"""
            bot.send_message(chat_id=update.message.chat_id,text="No search result.")

        elif result_length<10:
            """Case 3: Result is less than 10"""
            # Hint user that result is in PM
            if tk.if_int_negative(update.message.chat_id):
                bot.send_message(chat_id=update.message.chat_id,text="結果將顯示於私人對話。")

            # Test user has start bot
            try:
                bot.send_message(chat_id=update.message.from_user.id,
                    text="以下為【{}】的搜尋結果".format(search_para))
            except:
                bot.send_message(chat_id=update.message.chat_id,
                        text='<a href="https://telegram.me/MisakiAobaBot?start=sticker">請先在私訊START</a>',
                        parse_mode='HTML')
                return

            # Package result
            result=[]
            t=""
            counter=1
            for i in find_result:
                t=t+str(counter)+'. '+'<pre>'+i['quote']+'</pre>'+' -- '+i['said']+'\n'
                counter+=1
            result.append(t)

            # Sending result
            try:
                quote_search[update.message.from_user.id]=result
                # save to globle var
                bot.send_message(chat_id=update.message.from_user.id,
                    text=result[0],
                    reply_markup=page_keyboard(result,1),
                    parse_mode='HTML')
            except:
                bot.send_message(chat_id=update.message.from_user.id,text="ぜ")
                return
            finally:
                search_total_time=(datetime.now()-search_init_time).total_seconds()
                t="結束搜尋。共有{}筆資料。\n共耗時{}秒。".format(result_length,search_total_time)
                bot.send_message(chat_id=update.message.from_user.id,text=t,parse_mode='HTML')

        else:
            """Case 4: Result is more than 10"""
            # Hint user that result is in PM
            if tk.if_int_negative(update.message.chat_id):
                bot.send_message(chat_id=update.message.chat_id,text="結果將顯示於私人對話。")

            # Test user has start bot
            try:
                bot.send_message(chat_id=update.message.from_user.id,
                    text="以下為【{}】的搜尋結果".format(search_para))
            except:
                bot.send_message(chat_id=update.message.chat_id,
                        text='<a href="https://telegram.me/MisakiAobaBot?start=sticker">請先在私訊START</a>',
                        parse_mode='HTML')
                return

            # Package result
            result=[]
            result_sub=[]
            counter=1
            for i in find_result:
                result_sub.append(str(counter)+'. '+'<pre>'+i['quote']+'</pre>'+' -- '+i['said']+'\n')
                counter+=1
                if len(result_sub) == 10:
                    t=""
                    for j in result_sub:
                        t+=j
                    result.append(t)
                    result_sub=[]
            # last message
            if result_sub!=[]:
                # Issue: for length is times of 10, will have more 1 page
                t=""
                for j in result_sub:
                    t+=j
                result.append(t)
                result_sub=[]

            try:
                # Sending result
                quote_search[update.message.from_user.id]=result # save to globle var
                bot.send_message(chat_id=update.message.from_user.id,
                    text=result[0],
                    reply_markup=page_keyboard(result,1),
                    parse_mode='HTML')
            except:
                bot.send_message(chat_id=update.message.from_user.id,text="ぜ")
                return
            finally:
                search_total_time=(datetime.now()-search_init_time).total_seconds()
                t="結束搜尋。共有{}筆資料共{}頁。\n共耗時{}秒。".format(result_length,int((result_length-1)/10)+1,search_total_time)
                bot.send_message(chat_id=update.message.from_user.id,text=t,parse_mode='HTML')
        return

    #daily quote
    if MisaMongo.display_data('config',{'id':update.message.from_user.id},'day_quote')==False:
        tk.del_cmd_func(bot,update)
        return
    else:

        MisaMongo.modify_data('config',pipeline={'id':update.message.from_user.id},key='day_quote',update_value=False)

        tk.del_cmd_func(bot,update)
    quote=MisaMongo.randget()[0]
    text='<pre>'+quote['quote']+'</pre>\n'+'-----<b>'+quote['said']+'</b> より'
    msg=bot.send_message(chat_id=update.message.chat_id,text=text,parse_mode='HTML')

@do_after_root
def randPic(bot,update,args):
    idol_name=' '.join(args)
    if idol_name=='':
        url=MisaMongo.randget_idol('all')[0]['url']
    elif idol_name in GLOBAL_WORDS.idol_list:
        url=MisaMongo.randget_idol(idol_name)[0]['url']
    elif idol_name not in GLOBAL_WORDS.idol_list:
        bot.send_message(chat_id=update.message.chat_id,text='だれ？')
        return
    else:
        return

    try:
        bot.send_photo(chat_id=update.message.chat_id,photo=url)
    except TimedOut:
        bot.send_message(chat_id=update.message.chat_id,text='讀取中...')
    except:
        bot.send_message(chat_id=update.message.chat_id,text='這位偶像還沒有圖喔！')



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
reply_pair={}
@do_after_root
def savepic(bot, update):
    """Send a message when the command /savepic is issued."""
    """Send msg to ask user and save pic"""
    mention_url='tg://user?id={}'.format(update.message.from_user.id)
    first_name=update.message.from_user.first_name
    m_ent=[MessageEntity('mention',offset=0, length=len(first_name),user=update.message.from_user)]
    text='<a href="{}">{}</a>さん、何がご用事ですか？'.format(mention_url,first_name)
    f=ForceReply(force_reply=True,selective=True)
    rpl=bot.send_message(chat_id=update.message.chat_id,
        text=text,reply_to_message=update.message,reply_markup=f,parse_mode='HTML')
    global reply_pair
    reply_pair[update.message.from_user.id]=rpl

def forcesave(bot, update):
    chat_id=update.message.chat_id

    last_data=MisaMongo.room_state_getter(room_id=chat_id)

    try:
        msg=bot.send_message(chat_id=chat_id,text='聊天室資訊更新中！')
    except TimedOut:
        logger.error('ERROR(save_room_state):Update time out.')
    except Unauthorized:
        logger.error('ERROR(save_room_state):Bot is not in room.')
    except BadRequest:
        pass
    room_data={
        'room_id':update.message.chat_id,
        'room_name':update.message['chat']['title'],
        'update_time':tk.utc8now_datetime(),
        'total_message':update.message.message_id,
        'members_count':update.message.chat.get_members_count()
        }
    MisaMongo.insert_data('room_state',room_data)

    wt=room_data['total_message']-last_data['total_message']
    mb=room_data['members_count']-last_data['members_count']
    tm_temp=(room_data['update_time']-last_data['update_time'])
    tm=tk.strfdelta(tm_temp, "{hours}小時{minutes}分鐘")
    temp=Template("更新成功！\n在$time內，水量上漲了$water的高度，出現了$member個野生的P。")
    text=temp.substitute(time=tm,water=wt,member=mb)
    try:
        bot.send_message(chat_id=chat_id,text=text)
    except BadRequest:
        pass

def addecho(bot, update, args):
    context=' '.join(args)
    """
    words, echo=None, photo=None, video=None,prob=1000, els=None,allco=False, echo_list=False
    words=['夏川','椎菜','ナンス'], echo='(*>△<)<ナーンナーンっ',els='https://imgur.com/AOfQWWS.mp4',prob=300
    """
    data={
        'words':tk.formula('w',context,if_list=True),
        'echo':tk.formula('e',context),
        'photo':tk.formula('p',context),
        'video':tk.formula('v',context),
        'prob':tk.formula('p',context),
        'els':tk.formula('els',context),
        'allco':tk.formula('al',context),
        'echo_list':tk.formula('eli',context)
        }
    print(data)


def testfunc(bot, update):
    """print something"""
    print(MisaMongo.room_state_getter())
    pass
################################################
#               not command                    #
################################################
def key_word_reaction(bot,update):
    ###################################
    #        key word reaction        #
    ###################################
    def find_word(words, echo=None, photo=None, video=None,
        prob=1000, els=None,allco=False, echo_list=False):
        """
        words: words need to reaction, need to be a list.
        echo, photo, video: msg send after reaction
            If echo is multiple, will show random averagely
        prob: probability, if not, send els msg (1 for 0.1%)
        els: if not in prob, show it
        allco: words are all correct will go
        passArg: if true, the function will never go; default is false
        """
        key_words=update.message.text
        cid=update.message.chat_id
        def msgSend(words):
            bot.send_message(chat_id=cid,text=words)
        def videoSend(vid):
            bot.send_video(chat_id=cid, video=vid)
        def picSend(pic):
            bot.send_photo(chat_id=cid, photo=pic)
        # a random number from 0 to 999
        num = randrange(1000)

        key_words_value=False

        """check if all word correct will go"""
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

        if key_words_value==True:
            if echo != None:
                if num<prob:
                    if echo_list:
                        msgSend(tk.randList(echo))
                    else:
                        msgSend(echo)
                if num>=prob and els!=None:
                    if els.find('https://')!=-1:
                        videoSend(els)
                    else:
                        msgSend(els)
            elif video != None and num<prob:
                if echo_list:
                    videoSend(tk.randList(video))
                else:
                    videoSend(video)
            elif photo != None and num<prob:
                if echo_list:
                    picSend(tk.randList(photo))
                else:
                    picSend(photo)


        return key_words_value

    # switch
    switch=MisaMongo.display_data('config',{'id':update.message.from_user.id},'reply')

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
        find_word(words=['天','ナンス','もちょ'],video=pic_trys,allco=True,echo_list=True)
        find_word(words=['麻倉','もも','もちょ'], echo='(●･▽･●)',els='(o・∇・o)もちー！もちもちもちもちもちーーーもちぃ！',prob=900)
        find_word(words=['夏川','椎菜','ナンス'], echo='(*>△<)<ナーンナーンっ',els='https://imgur.com/AOfQWWS.mp4',prob=300)
        find_word(words=['雨宮','てん','天ちゃん'], video=pic_ten,echo_list=True)
        find_word(words=['天'], prob=15, video=pic_ten,echo_list=True)
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
        find_word(words=['菊地','真'], echo='真さんは今、王子役の仕事をしていますよ。',
            els='真さんは今、ヒーロー役の仕事をしていますよ～～激しい光は黒の衝撃 VERTEX BLACK!!!!',prob=700,allco=True)
        find_word(words=['我那覇','響'], echo='ハム蔵はどこでしょうか？探していますね',els='弾ける光は浅葱の波濤 VERTEX LIGHTBLUE!!',prob=700,allco=True)
        find_word(words=['四条','貴音'], echo='昨日〜貴音さんがわたしに色々な美味しい麺屋を紹介しました！',els='秘めたり光は臙脂の炎 VERTEX CARMINE〜〜',prob=700)
        find_word(words=['亜美'], echo='亜美？あそこよ')
        find_word(words=['真美'], echo='真美？いないよ')
        find_word(words=['双海'], echo='亜美真美？先に外へ行きました')

    ###################################
    #          reply_pair             #
    ###################################
    global reply_pair
    try:
        m=reply_pair[update.message.from_user.id]
    except KeyError:
        pass
    else:
        if update.message.reply_to_message==m:
            bot.send_message(chat_id=update.message.chat_id,text=update.message.text)
        del reply_pair[update.message.from_user.id]
    ###################################
    #              picsave            #
    ###################################
    if update.message.text.find("@db")!=-1:
        cmd_word_save=update.message.text.replace("@db","")
        if cmd_word_save in GLOBAL_WORDS.idol_list:
            rmsg=update.message.reply_to_message
            try:
                if url_valid(rmsg.text):
                    idol_db={
                        'name':cmd_word_save,
                        'url':rmsg.text,
                        'date':tk.utc8now(),
                        'saved_by':update.message.from_user.id
                    }
                    MisaMongo.insert_data('ml_idol_pic_colle',idol_db)
                    echo_word='画像が保存しました！'
                    bot.send_message(chat_id=update.message.chat_id,text=echo_word)
            except AttributeError:
                bot.send_message(chat_id=update.message.chat_id,text="画像がない。保存失敗した。")
        elif cmd_word_save=='':
            bot.send_message(chat_id=update.message.chat_id,text="もう！こんな遊ばなってください！")
        else:
            bot.send_message(chat_id=update.message.chat_id,text="知らない人ですよ。")
        # Exit region
        return
    ###################################
    #          quote collector        #
    ###################################
    record=False
    test=update.message.text
    if test.find(' #名言')!=-1 or test.find('#名言 ')!=-1:
        if update.message.reply_to_message==None and update.message.from_user.is_bot==False:
            test=test.replace(' #名言','').replace('#名言 ','')
            qdict={
                'quote': test,
                'said': update.message.from_user.first_name,
                'tag': '',
                'said_id':update.message.from_user.id,
                'date':tk.utc8now()
                }
            MisaMongo.insert_data('quote_main',qdict)
            record=True
    if test.find('#名言')!=-1 and record==False:
        if update.message.reply_to_message is not None and update.message.reply_to_message.from_user.is_bot==False:
            qdict={
                'quote': update.message.reply_to_message.text,
                'said': update.message.reply_to_message.from_user.first_name,
                'tag': '',
                'said_id':update.message.reply_to_message.from_user.id,
                'date':tk.utc8now()
                }
            MisaMongo.insert_data('quote_main',qdict)

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

################################################
#              repeating command               #
################################################

def misaki_changeday_alarm(bot,job):
    # 玩人狼玩到忘記每日
    bot.send_message(chat_id='-1001290696540',text=GLOBAL_WORDS.word_do_mission)

def save_room_state(bot, job):
    ######################
    #put in your group id#
    ######################
    chat_id=-1001290696540

    last_data=MisaMongo.room_state_getter()

    try:
        msg=bot.send_message(chat_id=chat_id,text='聊天室資訊更新中！')
    except TimedOut:
        logger.error('ERROR(save_room_state):Update time out.')
    except Unauthorized:
        logger.error('ERROR(save_room_state):Bot is not in room.')
    except BadRequest:
        pass
    room_data={
        'room_id':msg.chat_id,
        'room_name':msg['chat']['title'],
        'update_time':tk.utc8now_datetime(),
        'total_message':msg.message_id,
        'members_count':msg.chat.get_members_count()
        }
    MisaMongo.insert_data('room_state',room_data)

    wt=room_data['total_message']-last_data['total_message']
    mb=room_data['members_count']-last_data['members_count']
    tm_temp=(room_data['update_time']-last_data['update_time'])
    tm=tk.strfdelta(tm_temp, "{hours}小時{minutes}分鐘")
    temp=Template("更新成功！\n在$time內，水量上漲了$water的高度，出現了$member個野生的P。")
    text=temp.substitute(time=tm,water=wt,member=mb)
    try:
        bot.send_message(chat_id=chat_id,text=text)
    except BadRequest:
        pass

def daily_reset(bot,job):
    MisaMongo.modify_many_data('config',pipeline={"day_quote":False},key='day_quote',update_value=True)


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
    def menu_main():
        bot.edit_message_text(chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text='何がご用事ですか？',
            reply_markup=main_menu_keyboard())
    def menu_state():
        fin_text()
        temp=Template(GLOBAL_WORDS.word_state)
        rn=query.message['chat']['title']
        rid=query.message.chat_id
        tm=query.message.message_id
        dt=tk.utc8now()
        un=str(tk.room_member_num(bot,update=query))
        text=temp.substitute(room_name=rn,room_id=rid,msg_num=tm,user_number=un,time=dt)
        bot.send_message(text=text,chat_id=query.message.chat_id)
    def menu_about():
        fin_text()
        temp=Template(GLOBAL_WORDS.word_about)
        rt=tk.utc8now()
        text=temp.substitute(boot_time=rt)
        bot.send_message(text=text,chat_id=query.message.chat_id,parse_mode=ParseMode.HTML)
    def menu_resp_check():
        data_value = MisaMongo.display_data('config',{'id':query.from_user.id},'reply')
        if data_value is None:
            data_value=True#default open
        text='{}P目前狀態：{}'.format(query.from_user.first_name,tk.bool2text(data_value))
        bot.edit_message_text(chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text=text,
                reply_markup=sub_menu_keyboard(data_value))
    def menu_crsoff():
        MisaMongo.modify_data('config',pipeline={'id':query.from_user.id},key='reply',update_value=False)
        bot.edit_message_text(chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text="停止{}的回話功能。".format(query.from_user.first_name))
    def menu_crson():
        MisaMongo.modify_data('config',pipeline={'id':query.from_user.id},key='reply',update_value=True)
        bot.edit_message_text(chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text="開啟{}的回話功能。".format(query.from_user.first_name))
    def menu_canceled():
        bot.edit_message_text(chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text="まだね〜")
    def menu_ruleSetting():
        admin_access=tk.is_admin(bot,update)
        if admin_access == False:
            bot.edit_message_text(chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    text="只有管理員擁有此權限。")
            return
        room_config={}
        room_config['room_id']=query.message.chat_id
        room_config['room_name']=query.message['chat']['title']
        room_config['update_time']=query.message.date

        print(room_config)
        bot.edit_message_text(chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text="更新完成。")
        """
        mention_url='tg://user?id={}'.format(update.message.from_user.id)
        first_name=update.message.from_user.first_name
        m_ent=[MessageEntity('mention',offset=0, length=len(first_name),user=update.message.from_user)]
        text='<a href="{}">{}</a>さん、何がご用事ですか？'.format(mention_url,first_name)
        f=ForceReply(force_reply=True,selective=True)
        rpl=bot.send_message(chat_id=update.message.chat_id,
            text=text,reply_to_message=update.message,reply_markup=f,parse_mode='HTML')
        global reply_pair
        reply_pair[update.message.from_user.id]=rpl
        """
    def menu_turn_left(page):
        try:
            result=quote_search[query.from_user.id]
        except KeyError:
            # Some error flag
            pass
        new_page=page-1
        bot.edit_message_text(chat_id=query.from_user.id,
                message_id=query.message.message_id,
                text=result[new_page-1],
                reply_markup=page_keyboard(result,new_page),
                parse_mode='HTML')
    def menu_turn_right(page):
        try:
            result=quote_search[query.from_user.id]
        except KeyError:
            # Some error flag
            pass
        new_page=page+1
        bot.edit_message_text(chat_id=query.from_user.id,
                message_id=query.message.message_id,
                text=result[new_page-1],
                reply_markup=page_keyboard(result,new_page),
                parse_mode='HTML')
    def menu_quote_search_exit():
        try:
            global quote_search
            del quote_search[query.from_user.id]
        except:
            pass
        finally:
            bot.delete_message(chat_id=query.message.chat_id,
                    message_id=query.message.message_id)

    # Switch
    if query_text == "main":
        """Main menu"""
        menu_main()
    elif query_text == "cmd_state":
        """Show room state"""
        menu_state()
    elif query_text == "cmd_about":
        """Show bot info"""
        menu_about()
    elif query_text == "cmd_resp_check":
        """User resp setting"""
        menu_resp_check()
    elif query_text == "cmd_resp_switch_off":
        menu_crsoff()
    elif query_text == "cmd_resp_switch_on":
        menu_crson()
    elif query_text == "cmd_ruleSetting":
        """set/edit room rule"""
        """admin only"""
        menu_ruleSetting()
    elif query_text == "cmd_canceled":
        """Cancel menu"""
        menu_canceled()
    elif query_text.find("cmd_turn_left")!=-1:
        """Last page"""
        page=query_text.replace('cmd_turn_left','')
        if page!='':
            menu_turn_left(int(page))
    elif query_text.find("cmd_turn_right")!=-1:
        """Right page"""
        page=query_text.replace('cmd_turn_right','')
        if page!='':
         menu_turn_right(int(page))
    elif query_text == "cmd_quote_search_exit":
        """Clear template data"""
        menu_quote_search_exit()
    elif query_text == "None":
        """No cmd, decoration"""
        pass

# Keyboards
def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton(text='回話設定',callback_data='cmd_resp_check'),
               InlineKeyboardButton(text='群龜設定',callback_data="cmd_ruleSetting")],
              [InlineKeyboardButton(text='群組狀態',callback_data="cmd_state")
              ,InlineKeyboardButton(text='關於美咲',callback_data="cmd_about")],
              [InlineKeyboardButton(text='取消',callback_data="cmd_canceled")]]
    return InlineKeyboardMarkup(keyboard)

def sub_menu_keyboard(state):
    keyboard = [[InlineKeyboardButton(text='關閉回話' if state else '開啟回話',callback_data='cmd_resp_switch_off' if state else 'cmd_resp_switch_on')],
                [InlineKeyboardButton(text='取消',callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)

def page_keyboard(list,page):
    total_page=len(list)
    if total_page==1:
        keyboard = [[InlineKeyboardButton(text='||',callback_data='None'),
                     InlineKeyboardButton(text='P{}'.format(page),callback_data='None'),
                     InlineKeyboardButton(text='||',callback_data='None')],
                    [InlineKeyboardButton(text='結束',callback_data='cmd_quote_search_exit')]]
    elif page==1:
        keyboard = [[InlineKeyboardButton(text='||',callback_data='None'),
                     InlineKeyboardButton(text='P{}'.format(page),callback_data='None'),
                     InlineKeyboardButton(text='>>',callback_data='cmd_turn_right'+str(page))],
                    [InlineKeyboardButton(text='結束',callback_data='cmd_quote_search_exit')]]
    elif page==total_page:
        keyboard = [[InlineKeyboardButton(text='<<',callback_data='cmd_turn_left'+str(page)),
                     InlineKeyboardButton(text='P{}'.format(page),callback_data='None'),
                     InlineKeyboardButton(text='||',callback_data='None')],
                    [InlineKeyboardButton(text='結束',callback_data='cmd_quote_search_exit')]]
    else:
        keyboard = [[InlineKeyboardButton(text='<<',callback_data='cmd_turn_left'+str(page)),
                     InlineKeyboardButton(text='P{}'.format(page),callback_data='None'),
                     InlineKeyboardButton(text='>>',callback_data='cmd_turn_right'+str(page))],
                    [InlineKeyboardButton(text='結束',callback_data='cmd_quote_search_exit')]]
    return InlineKeyboardMarkup(keyboard)

# error logs
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
    logger.info("Bot start.")
################################################
#                   main                       #
################################################
def main():
    """Start the bot."""

    # <initialization>
    initialization()

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dj = updater.job_queue

    # <function start>

    # ---repeating jobs---
    # mission_callback every 22:30 daily
    dj.run_daily(misaki_changeday_alarm,stime(14,30))
    # mission_show record every 8 hours
    m_history=[stime(7,0,0),stime(15,0,0),stime(23,0,0)]
    for t in m_history:
        #plug in mission time with loop
        dj.run_daily(save_room_state,t)
    # mission refresh daily gasya
    dj.run_daily(daily_reset,stime(14,59,59))

    # ---Command answer---
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("rule", rule))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("tbgame", tbgame))
    dp.add_handler(CommandHandler("config", config))
    dp.add_handler(CommandHandler("nanto", nanto, pass_args=True))
    dp.add_handler(CommandHandler("which", which, pass_args=True))
    dp.add_handler(CommandHandler("quote",quote, pass_args=True))
    dp.add_handler(CommandHandler("randpic",randPic, pass_args=True))
    dp.add_handler(CommandHandler("sticker",sticker_matome))

    # beta version function
    dp.add_handler(CommandHandler("forcesave",forcesave))
    dp.add_handler(CommandHandler("addecho", addecho, pass_args=True))

    # test function
    dp.add_handler(CommandHandler("savepic",savepic, pass_job_queue=True))
    dp.add_handler(CommandHandler("testfunc",testfunc))

    # ---Menu function---
    dp.add_handler(CallbackQueryHandler(menu_actions))

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
