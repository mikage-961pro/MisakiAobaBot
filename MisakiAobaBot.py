# coding=utf-8
################################################
# This is MisakiAobaBot
# CopyRight by Dephilia,TAKE
################################################


################################################
# Remember
# 1. Edit version at __init__
# 2. Edit readme.md
# 3. Edit about in GLOBAL_WORDS
################################################

bot_name='@MisakiAobaBot'
DEBUG=False
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
import word_echo
import menu
import quote as quote_toolkit
import picsave

################################################
#                 Global var                   #
################################################
global quote_search
global reply_pair
################################################
#                   command                    #
################################################
@do_after_root
@wait_for_timeOut
def start(bot, update):
    """Send a message when the command /start is issued."""
    bot.send_message(chat_id=update.message.chat_id,
                    text=GLOBAL_WORDS.word_start,
                    parse_mode=ParseMode.HTML)

@do_after_root
@del_cmd
@wait_for_timeOut
def help(bot, update):
    """Send a message when the command /help is issued."""
    if randrange(1000)<30:
        bot.send_message(chat_id=update.message.chat_id, text="ぜ")
    else:
        bot.send_message(chat_id=update.message.chat_id,
                    text=GLOBAL_WORDS.word_help,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True)

@do_after_root
@del_cmd
@wait_for_timeOut
def tbgame(bot, update):
    """Send a message when the command /tbgame is issued."""
    bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_tbgame,
                    parse_mode=ParseMode.HTML)

@run_async
@do_after_root
@del_cmd
@wait_for_timeOut
def rule(bot, update):
    """Send a message when the command /rule is issued."""
    pipeline={'room_id':update.message.chat_id}
    key='room_rule'
    room_data=display_data('room_config',pipeline,key)
    room_rule=""
    if room_data is True:
        room_rule="本群組尚未建立規則。"
    else:
        room_rule=room_data
    if randrange(1000)<30:
        bot.send_message(chat_id=update.message.chat_id, text="ぜ")
    else:
        if not htmlPharseTester(room_rule):
            room_rule=room_rule.replace('<','＜')
        msg=bot.send_message(chat_id=update.message.chat_id, text=room_rule,
                        parse_mode=ParseMode.HTML)
        time.sleep(60)
        bot.delete_message(chat_id=update.message.chat_id, message_id=msg.message_id)

@do_after_root
@wait_for_timeOut
def config(bot, update):
    """Send a message when the command /config is issued."""
    """Config is use to let user to turn on/off some function"""
    try:
        bot.send_message(chat_id=update.message.chat_id,
            text='何がご用事ですか？',
            reply_markup=menu.main_menu_keyboard())
    except TelegramError as e:
        if e=="Timed out":
            bot.send_message(chat_id=update.message.chat_id,
                text='請稍候')


@run_async
@do_after_root
@del_cmd
@wait_for_timeOut
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
@wait_for_timeOut
def which(bot, update, args):
    """Send a message when the command /which is issued."""
    split_symbol="#"
    if update.message.date > init_time:
        if not args:
            text="請輸入要給我決定的事情♪\n記得用〔$symbol〕分開喔！".replace('$symbol',split_symbol)
            bot.send_message(chat_id=update.message.chat_id, text=text)
        else:
            things=' '.join(args).split(split_symbol)
            if len(things)==1:
                result=things[0]
                text="そんな$resたいなら、私と諮問することは必要じゃないでしょ？".replace('$res',result)
                bot.send_message(chat_id=update.message.chat_id, text=text)
            else:
                result=things[randrange(len(things))]
                text="わたしは〜♬［$res］が良いと思うよ〜えへへ。".replace('$res',result)
                bot.send_message(chat_id=update.message.chat_id, text=text)

@do_after_root
@run_async
def quote(bot,update,args):
    # search parameter
    global quote_search
    search_para=formula('f',' '.join(args))
    if search_para!=False:
        search_data=quote_toolkit.quote_finder(search_para,bot,update)
        if not isinstance(search_data, bool):
            quote_search.update(search_data)

    #daily quote
    if display_data('config',{'id':update.message.from_user.id},'day_quote')==False:
        del_cmd_func(bot,update)
        return
    else:

        modify_data('config',pipeline={'id':update.message.from_user.id},key='day_quote',update_value=False)

        del_cmd_func(bot,update)
    quote=quote_toolkit.quote_get()
    text='<pre>'+quote['quote']+'</pre>\n'+'-----<b>'+quote['said']+'</b> より'
    msg=bot.send_message(chat_id=update.message.chat_id,text=text,parse_mode='HTML')

@do_after_root
@wait_for_timeOut
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

    if not url_valid(url):
        logger.info("Not valid url when send picture:%s",url)
        return
    try:
        url_text="""<a href="$URL">〔原圖網址〕</a>""".replace('$URL',url)
        bot.send_photo(chat_id=update.message.chat_id,
            photo=picLinker(url),
            caption=url_text,
            parse_mode=ParseMode.HTML,
            disable_notification=True)
    except TimedOut:
        pass
        #bot.send_message(chat_id=update.message.chat_id,text='讀取中...')
    except:
        #bot.send_message(chat_id=update.message.chat_id,text='這位偶像還沒有圖喔！')
        logger.warning("Unexpect error while sending picture.")



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

def forcesave(bot, update):
    chat_id=update.message.chat_id

    last_data=room_state_getter(room_id=chat_id)


    try:
        msg=bot.send_message(chat_id=chat_id,text='聊天室資訊更新中...')
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
        bot.send_message(chat_id=update.message.chat_id,
            text='請輸入資料！\n輸入<pre>/addecho -h</pre> 以尋求幫助。',
            parse_mode='HTML')
        return

    if formula('h',context):
        """help"""
        word_echo.addEcho_help(update,bot)
        return

    try:
        data=word_echo.addEcho_main(context,update=update,bot=bot)
        if data:
            mongo_data=insert_data('words_echo',data)
            logger.info("Insert echo data sucessful:%s ID=%s",str(data['words']),mongo_data.inserted_id)
            bot.send_message(chat_id=update.message.chat_id,text='資料寫入成功！')
        else:
            logger.info("Insert echo data failed.")
            bot.send_message(chat_id=update.message.chat_id,text='資料寫入失敗！')

    except TimedOut:
        bot.send_message(chat_id=update.message.chat_id,text='Saving...')

def exrate(bot, update, args):
    context=' '.join(args)
    split_symbol=">"
    country=context.split(split_symbol)
    if len(country)!=2:
        bot.send_message(chat_id=update.message.chat_id,text="格式錯誤喔～")
        return
    if country[0]==country[1]:
        bot.send_message(chat_id=update.message.chat_id,text="我就知道你想這樣玩(●･▽･●)")
        return
    try:
        output_data=exRate(country[0],country[1])
    except IndexError:
        error_msg="未知的貨幣代碼："+country[0]+" > "+country[1]
        bot.send_message(chat_id=update.message.chat_id,text=error_msg)
        return
    text="以下顯示1"+country[1]+"等於多少"+country[0]+"\n"+\
        "匯率: "+str(output_data['Exrate'])+"\n"+\
        "牌價時間: "+output_data['UTC']+" (UTC Time)"+\
        """
此服務由<a href="https://tw.rter.info/howto_currencyapi.php">即匯站</a>所提供
        """
    bot.send_message(chat_id=update.message.chat_id,
        text=text,
        parse_mode='HTML',
        disable_web_page_preview=True)

def twd2jpy(bot, update):
    output_data=exrate_twbank("JPY")
    text="以下顯示日圓匯率\n"+\
        "匯率: "+str(output_data)+"\n"+\
        """
此服務為台灣銀行公告牌價
        """
    bot.send_message(chat_id=update.message.chat_id,
        text=text,
        parse_mode='HTML',
        disable_web_page_preview=True)

def mltdrank(bot, update):
    k=bot.send_message(chat_id=update.message.chat_id,text='我看一下喔')
    border=event_score()
    bInfo="""
<pre>
[{0:>8}]
[{1:>8}]
   3:[{2:>8}] +[{6:>6} pts/hr
 100:[{3:>8}] +[{7:>6} pts/hr
2500:[{4:>8}] +[{8:>6} pts/hr</pre>
    """.format(border['name'],border[3]['summaryTime'],border[3]['score'],border[100]['score'],border[2500]['score'],border[3]['past_1'],border[100]['past_1'],border[2500]['past_1'])
    bot.edit_message_text(text=bInfo,message_id=k.message_id,chat_id=update.message.chat_id,parse_mode=ParseMode.HTML)
    bot.send_message(chat_id=update.message.chat_id,text='要不要買ジュリア8400個R??')
        
def finduser(bot, update, args):
    """used to find user data from user_id"""
    context=' '.join(args)
    data=context.split('#')
    try:
        room_id=int(data[0])
        user_id=int(data[1])
    except ValueError:
        logger.warning("Lack of information while find user")
        bot.send_message(chat_id=update.message.chat_id,text="請輸入正確的格式。")
        return

    try:
        user_data=bot.get_chat_member(chat_id=room_id,user_id=user_id)
        first_name=user_data.user.first_name
        last_name=user_data.user.last_name
        username=user_data.user.username
        text="User {} in chat {} is {} {} with username:{}.".format(user_id,room_id,first_name,last_name,username)
        bot.send_message(chat_id=update.message.chat_id,text=text)
    except UnboundLocalError:
        logger.warning("Wrong information while find user")
        bot.send_message(chat_id=update.message.chat_id,text="請輸入正確的代號。")
        return

def testfunc(bot, update):
    """print something"""
    pass
################################################
#               not command                    #
################################################
def key_word_reaction(bot,update):
    """Observe all msg from user."""
    key_words=update.message.text #record
    ###################################
    #          reply_pair             #
    ###################################
    try:
        m=reply_pair[update.message.from_user.id]
    except KeyError:
        pass
    else:
        """Main function"""
        function_type=m[0]
        if function_type=="RULE_EDIT":
            """RULE_EDIT"""
            if update.message.reply_to_message==m[1]:
                room_data={
                'room_id':update.message.chat_id,
                'room_name':update.message['chat']['title'],
                'update_time':update.message.date,
                'room_rule':update.message.text
                }

                updata_data("room_config",{'room_id':update.message.chat_id},{"$set":room_data})
                bot.send_message(chat_id=update.message.chat_id,text="更新成功！")
            del reply_pair[update.message.from_user.id]


    """RUN"""
    # switch
    user_echo_switch=display_data('config',{'id':update.message.from_user.id},'reply')
    room_echo_switch=display_data2('room_config',{'room_id':update.message.chat_id},'echo')
    room_savepic_switch=display_data2('room_config',{'room_id':update.message.chat_id},'savepic')
    room_quote_switch=display_data2('room_config',{'room_id':update.message.chat_id},'quote')

    word_echo.wordEcho(bot,update,user_switch=user_echo_switch,room_switch=room_echo_switch,key_words=key_words)
    picsave.picSave_main(bot, update, context=key_words, room_switch=room_savepic_switch)
    quote_toolkit.quote_collecter(bot, update, context=key_words, room_switch=room_quote_switch)

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
    def save_room_state_main(chat_id):

        try:
            msg=bot.send_message(chat_id=chat_id,text='聊天室資訊更新中...')
        except TimedOut:
            logger.error('(%s):Update time out.','save_room_state')
            return
        except Unauthorized:
            logger.error('(%s):Bot is not in room.','save_room_state')
            updata_data("room_config",{'room_id':msg.chat_id},{"$set":{'echo':False}})
            return
        except BadRequest:
            return

        room_data={
            'room_id':msg.chat_id,
            'room_name':msg['chat']['title'],
            'update_time':datetime.now(),
            'total_message':msg.message_id,
            'members_count':msg.chat.get_members_count()
            }
        last_data=room_state_getter(room_id=chat_id)
        insert_data('room_state',room_data)
        if last_data==None:
            text="初次儲存。儲存成功。"
            try:
                bot.send_message(chat_id=chat_id,text=text)
            except BadRequest:
                return
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
                return
    water_room_id=[]
    if DEBUG:
        water_room_id.append(-1001289458175)
    else:
        for data in display_alldata('room_config'):
            try:
                if data['water']==True:
                    water_room_id.append(data['room_id'])
            except KeyError:
                pass
    for id in water_room_id:
        save_room_state_main(id)

def daily_reset(bot,job):
    modify_many_data('config',pipeline={"day_quote":False},key='day_quote',update_value=True)



################################################
#                   inline                     #
################################################
@wait_for_modify
def inline_handler(bot,update):
    query=update.inline_query.query

    #rand pic
    def pic_url(name):
        result=randget_idol(name)
        if result:
            return result[0]['url']
        return randget_idol('all')[0]['url']

    name=query.lower()
    url=pic_url(name)
    url_text="""<a href="$URL">〔原圖網址〕</a>""".replace('$URL',url)
    try:
        rand_idol_pic=InlineQueryResultPhoto(
            id=str(datetime.now()),
            title='RANDPIC',
            photo_url=url,
            thumb_url="https://i.imgur.com/kdAihxk.jpg",
            caption=url_text,
            parse_mode=ParseMode.HTML
        )

        bot.answer_inline_query(inline_query_id=update.inline_query.id,
        results=[rand_idol_pic],
        cache_time=2,
        is_personal=True)
    except TelegramError as e:
        if e=="Message is not modified":
            pass

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
    dj.run_daily(misaki_changeday_alarm,stime(22,30))
    # mission_show record every 8 hours
    m_history=[stime(7,0,0),stime(15,0,0),stime(23,0,0)]
    for t in m_history:
        #plug in mission time with loop
        dj.run_daily(save_room_state,t)
    # mission refresh daily gasya
    dj.run_daily(daily_reset,stime(23,59,59))

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
    dp.add_handler(CommandHandler("addecho", addecho, pass_args=True))
    dp.add_handler(CommandHandler("exrate", exrate, pass_args=True))
    dp.add_handler(CommandHandler("twd2jpy", twd2jpy))
    dp.add_handler(CommandHandler("mltdrank", mltdrank))


    # hidden function
    dp.add_handler(CommandHandler("forcesave",forcesave))
    dp.add_handler(CommandHandler("finduser", finduser, pass_args=True))

    # test function
    if DEBUG:

        # dp.add_handler(CommandHandler("savepic",savepic))
        dp.add_handler(CommandHandler("testfunc",testfunc))

    # ---Menu function---
    dp.add_handler(CallbackQueryHandler(menu.menu_actions))

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
