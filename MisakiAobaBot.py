# coding=utf-8

bot_name='@MisakiAobaBot'
DEBUG=True
################################################
#              Global Setting                  #
################################################

### ---Module---

# ---Python function
import os
import time
from datetime import datetime,tzinfo,timedelta
from datetime import time as stime#specific time
from string import Template
from random import randrange

# ---Telegram
from telegram import *
from telegram.ext import *
from telegram.ext.dispatcher import run_async
from telegram.error import *

token = os.environ['TELEGRAM_TOKEN']
updater = Updater(token,workers=16)

# ---My Module
from module import *

################################################
#                 Global var                   #
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
    search_para=formula('f',' '.join(args))
    if search_para != False:
        if search_para=="":
            """Case 1: No words"""
            bot.send_message(chat_id=update.message.chat_id,text="Please enter word.")
            return
        # Search initialization
        find_result=quote_finder(search_para)
        result_length=len(find_result)
        search_init_time=datetime.now()
        global quote_search

        if result_length==0:
            """Case 2: No search result"""
            bot.send_message(chat_id=update.message.chat_id,text="No search result.")

        elif result_length<10:
            """Case 3: Result is less than 10"""
            # Hint user that result is in PM
            if if_int_negative(update.message.chat_id):
                bot.send_message(chat_id=update.message.chat_id,text="結果將顯示於私人對話。")

            # Test user has start bot
            try:
                bot.send_message(chat_id=update.message.from_user.id,
                    text="以下為【{}】的搜尋結果".format(search_para))
            except:
                bot.send_message(chat_id=update.message.chat_id,
                        text=GLOBAL_WORDS.word_PM_notice,
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
            if if_int_negative(update.message.chat_id):
                bot.send_message(chat_id=update.message.chat_id,text="結果將顯示於私人對話。")

            # Test user has start bot
            try:
                bot.send_message(chat_id=update.message.from_user.id,
                    text="以下為【{}】的搜尋結果".format(search_para))
            except:
                bot.send_message(chat_id=update.message.chat_id,
                        text=GLOBAL_WORDS.word_PM_notice,
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
    if display_data('config',{'id':update.message.from_user.id},'day_quote')==False:
        del_cmd_func(bot,update)
        return
    else:

        modify_data('config',pipeline={'id':update.message.from_user.id},key='day_quote',update_value=False)

        del_cmd_func(bot,update)
    quote=randget()[0]
    text='<pre>'+quote['quote']+'</pre>\n'+'-----<b>'+quote['said']+'</b> より'
    msg=bot.send_message(chat_id=update.message.chat_id,text=text,parse_mode='HTML')

@do_after_root
def randPic(bot,update,args):
    idol_name=' '.join(args)
    idol_name=idol_name.lower()
    if idol_name=='':
        url=randget_idol('all')[0]['url']
    elif idol_name in GLOBAL_WORDS.idol_list:
        try:
            url=randget_idol(idol_name)[0]['url']
        except IndexError:
            bot.send_message(chat_id=update.message.chat_id,text='這位偶像還沒有圖喔！')
            return
        except:
            bot.send_message(chat_id=update.message.chat_id,text='發生不明錯誤。')
            return

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
    link=display_alldata('sticker')
    slink=''
    for i in link:
        slink=slink+'<a href="https://telegram.me/addstickers/'+i['setname']+'">'+i['about']+'</a>\n'
    try:
        bot.send_message(chat_id=update.message.from_user.id,text=slink,parse_mode='HTML')
    except:
        startme=GLOBAL_WORDS.word_PM_notice
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

    last_data=room_state_getter(room_id=chat_id)


    try:
        msg=bot.send_message(chat_id=chat_id,text='聊天室資訊更新中！')
    except TimedOut:
        logger.error('(%s):Update time out.','forcesave')
    except Unauthorized:
        logger.error('(%s):Bot is not in room.','forcesave')
    except BadRequest:
        pass
    room_data={
        'room_id':update.message.chat_id,
        'room_name':update.message['chat']['title'],
        'update_time':datetime.now(),
        'total_message':update.message.message_id,
        'members_count':update.message.chat.get_members_count()
        }
    insert_data('room_state',room_data)

    if last_data==None:
        text="初次儲存。儲存成功。"
        try:
            bot.send_message(chat_id=chat_id,text=text)
        except BadRequest:
            pass
    else:
        wt=room_data['total_message']-last_data['total_message']
        mb=room_data['members_count']-last_data['members_count']
        tm_temp=(room_data['update_time']-last_data['update_time'])
        tm=strfdelta(tm_temp, "{hours}小時{minutes}分鐘")
        temp=Template("更新成功！\n在$time內，水量上漲了$water的高度，出現了$member個野生的P。")
        text=temp.substitute(time=tm,water=wt,member=mb)
        try:
            bot.send_message(chat_id=chat_id,text=text)
        except BadRequest:
            pass

def addecho(bot, update, args):
    context=' '.join(args)
    if context=="":
        bot.send_message(chat_id=update.message.chat_id,text='請輸入資料！')
        return
    if formula('h',context):
        text="""
        /addecho -w=文字 -e=響應 -p=照片 -v=影像 -pr=機率 -els=機率外響應 -al=文字全對才發生 -eli=響應是否為多數
        -w:可以是多個文字，像是-w=もちょ,ナンス,天ちゃん
        ［以下三個請擇一輸入］
        -e:會回應的文字。像是-e=(●･▽･●)
        -p:回應的圖片。可以是imgur圖床網址。
        -v:回應的影像。像是gif等，注意格式均為mp4。

        -pr:機率。若是落在此機率外則觸發els（可填入0~1000）
        -els:若是在機率外就會觸發文字。只能填入一行。-els=(o・∇・o)
        -al:要-w中的文字全對才會觸發(true/false)。
        -eli:若此為true，則echo可以為多行（會隨機觸發）(true/false)。
        """
        bot.send_message(chat_id=update.message.chat_id,text=text)
        return

    data={
        'words':formula('w',context,if_list=True),
        'echo':formula('e',context,if_list=True),
        'photo':formula('p',context),
        'video':formula('v',context),
        'prob':int(formula('pr',context)),
        'els':formula('els',context),
        'allco':formula('al',context),
        'echo_list':formula('eli',context)
        }
    if data['echo']==False:data['echo']=None
    if data['photo']==False:data['photo']=None
    if data['video']==False:data['video']=None
    if data['prob']==False:data['prob']=1000
    if data['els']==False:data['els']=None

    insert_data('words_echo',data)
    logger.info("Insert echo data sucessful:%s",str(data))
    bot.send_message(chat_id=update.message.chat_id,text='資料寫入成功！')


def testfunc(bot, update):
    """print something"""
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
                        msgSend(randList(echo))
                    else:
                        msgSend(echo[0])
                if num>=prob and els!=None:
                    if els.find('https://')!=-1:
                        videoSend(els)
                    else:
                        msgSend(els)
            elif video != None and num<prob:
                if echo_list:
                    videoSend(randList(video))
                else:
                    videoSend(video)
            elif photo != None and num<prob:
                if echo_list:
                    picSend(randList(photo))
                else:
                    picSend(photo)
        return key_words_value

    # switch
    switch=display_data('config',{'id':update.message.from_user.id},'reply')
    echo_data=display_alldata('words_echo')

    # word_echo
    if switch == True:
        for d in echo_data:
            find_word(words=d['words'], echo=d['echo'], photo=d['photo'], video=d['video'],
                prob=d['prob'], els=d['els'],allco=d['allco'], echo_list=d['echo_list'])
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
        cmd_word_save=update.message.text.replace("@db","").lower()
        if cmd_word_save in GLOBAL_WORDS.idol_list:
            rmsg=update.message.reply_to_message
            try:
                if url_valid(rmsg.text):
                    idol_db={
                        'name':cmd_word_save,
                        'url':rmsg.text,
                        'date':datetime.now(),
                        'saved_by':update.message.from_user.id
                    }
                    insert_data('ml_idol_pic_colle',idol_db)
                    echo_word='画像が保存されました！'
                    bot.send_message(chat_id=update.message.chat_id,text=echo_word)
            except AttributeError:
                bot.send_message(chat_id=update.message.chat_id,text="画像がない。保存失敗しました。")
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
                'date':datetime.now()
                }
            insert_data('quote_main',qdict)
            record=True
    if test.find('#名言')!=-1 and record==False:
        if update.message.reply_to_message is not None and update.message.reply_to_message.from_user.is_bot==False:
            qdict={
                'quote': update.message.reply_to_message.text,
                'said': update.message.reply_to_message.from_user.first_name,
                'tag': '',
                'said_id':update.message.reply_to_message.from_user.id,
                'date':datetime.now()
                }
            insert_data('quote_main',qdict)

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

    last_data=room_state_getter()

    try:
        msg=bot.send_message(chat_id=chat_id,text='聊天室資訊更新中！')
    except TimedOut:
        logger.error('(%s):Update time out.','save_room_state')
    except Unauthorized:
        logger.error('(%s):Bot is not in room.','save_room_state')
    except BadRequest:
        pass
    room_data={
        'room_id':msg.chat_id,
        'room_name':msg['chat']['title'],
        'update_time':datetime.now(),
        'total_message':msg.message_id,
        'members_count':msg.chat.get_members_count()
        }
    insert_data('room_state',room_data)

    wt=room_data['total_message']-last_data['total_message']
    mb=room_data['members_count']-last_data['members_count']
    tm_temp=(room_data['update_time']-last_data['update_time'])
    tm=strfdelta(tm_temp, "{hours}小時{minutes}分鐘")
    temp=Template("更新成功！\n在$time內，水量上漲了$water的高度，出現了$member個野生的P。")
    text=temp.substitute(time=tm,water=wt,member=mb)
    try:
        bot.send_message(chat_id=chat_id,text=text)
    except BadRequest:
        pass

def daily_reset(bot,job):
    modify_many_data('config',pipeline={"day_quote":False},key='day_quote',update_value=True)


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
        dt=utc8now()
        un=str(room_member_num(bot,update=query))
        text=temp.substitute(room_name=rn,room_id=rid,msg_num=tm,user_number=un,time=dt)
        bot.send_message(text=text,chat_id=query.message.chat_id)
    def menu_about():
        fin_text()
        temp=Template(GLOBAL_WORDS.word_about)
        rt=utc8now()
        text=temp.substitute(boot_time=rt)
        bot.send_message(text=text,chat_id=query.message.chat_id,parse_mode=ParseMode.HTML)
    def menu_resp_check():
        data_value = display_data('config',{'id':query.from_user.id},'reply')
        if data_value is None:
            data_value=True#default open
        text='{}P目前狀態：{}'.format(query.from_user.first_name,bool2text(data_value))
        bot.edit_message_text(chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text=text,
                reply_markup=sub_menu_keyboard(data_value))
    def menu_crsoff():
        modify_data('config',pipeline={'id':query.from_user.id},key='reply',update_value=False)
        bot.edit_message_text(chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text="停止{}的回話功能。".format(query.from_user.first_name))
    def menu_crson():
        modify_data('config',pipeline={'id':query.from_user.id},key='reply',update_value=True)
        bot.edit_message_text(chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text="開啟{}的回話功能。".format(query.from_user.first_name))
    def menu_canceled():
        bot.edit_message_text(chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text="まだね〜")
    def menu_ruleSetting():
        admin_access=is_admin(bot,update)
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

################################################
#                   inline                     #
################################################
def inline_handler(bot,update):
    query=update.inline_query.query

    #rand pic
    def pic_url(name):
        result=randget_idol(name)
        if result:
            return result[0]['url']
        return randget_idol('all')[0]['url']

    name=query.lower()
    rand_idol_pic=InlineQueryResultPhoto(
        id=str(datetime.now()),
        title='RANDPIC',
        photo_url=pic_url(name),
        thumb_url="https://i.imgur.com/kdAihxk.jpg"
    )

    bot.answer_inline_query(inline_query_id=update.inline_query.id,
    results=[rand_idol_pic],
    cache_time=2,
    is_personal=True)


# error logs
def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('(Update %s):"%s"', update, error)
################################################
#                   init                       #
################################################
@do_once
def initialization():
    # ---Record init time---
    global init_time
    init_time = datetime.now()
    logger.info("(%s):Bot start.","initialization")
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
    dp.add_handler(CommandHandler("forcesave",forcesave))
    dp.add_handler(CommandHandler("addecho", addecho, pass_args=True))

    # test function
    if DEBUG:
        dp.add_handler(CommandHandler("savepic",savepic, pass_job_queue=True))
        dp.add_handler(CommandHandler("testfunc",testfunc))

    # ---Menu function---
    dp.add_handler(CallbackQueryHandler(menu_actions))

    # ---Inline function---
    dp.add_handler(InlineQueryHandler(inline_handler))

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
