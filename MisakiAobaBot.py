# coding=utf-8

#BotFather-commend setting
"""
start-我是765事務所的事務員，青羽美咲
help-由青羽小姐提供您幫助
rule-本群規則瀏覽
state-群狀態
config-設定
nanto-なんとぉ！
"""

#dev
"""
〖開發目標〗
伺服器
入群通知
提醒功能
自由設定文字
"""

#debug mode
debug_mode=True

################################################
#                   Global                     #
################################################
# import
from telegram import (Bot, Chat, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import time
import os

bot_name='@MisakiAobaBot'
if debug_mode is True:
    token='690274765:AAFxDyslvSkuVbPJXUAjWm2u6iy92bBB-JU'
    # this is a test bot token
else:
    token = os.environ['TELEGRAM_TOKEN']

#global words

word_start = """青羽美咲です！宜しくお願い致します！
尋求幫助 - /help

みんなのアカウント
<a href="https://twitter.com/imasml_theater">〔ML〕</a>
<a href="https://twitter.com/imassc_official">〔SC〕</a>
<a href="https://twitter.com/imascg_stage">〔CG〕</a>
"""

word_help = """
/help - 由青羽小姐提供您幫助
/rule - 本群規則瀏覽
/state - 群狀態
/config - 設定
/nanto - なんとぉ！
"""
word_rule = """
　　　　<b>【台湾アイマスTelegram鯖ルール】</b>

<b>〖宗旨〗</b>
　　本群組為提供アイマス愛好者交流之群組，主要討論包含偶像大師本家、ML、CG、SC等等系列之討論，但<b>不限於此</b>。
　　也就是說任何討論皆可，但請注意不要太專注在自我小世界。

<b>〖討論限制〗</b>
　　A. 不得含有任意<b>辱罵、侮辱、挑撥、等侵害他人言論</b>
　　B. 禁止惡意的<b>廣告文</b>投放
　　C. 禁止任何違反<b>中華民國法律</b>之言論
　　D. 圖片限制：目前設定為<b>高度</b>限制

　　☞高度限制：任何圖片包括性暗示、擬獸，以及妨害風俗及18禁等圖片的最高限度禁止
　　中度限制：露點、高度露出、激凸之圖片的中度禁止
　　低度限制：僅限制露點圖片，包括三次元二次元

　　E. 為求言論自由性，A、B二條款為告訴乃論。
　　F. 若有以上違規事由者，管理者有權利停止其發言，停止時間一率為一週，視情況嚴重可以加重至一個月。
　　G. 群內不能打棒球
　　H. 也不能踢足球

<b>〖最後〗</b>
　　輕鬆地討論吧～！

<b>〖遊戲分群〗</b>
　　<a href="https://t.me/joinchat/IFtWTxKG_KG-500YZBBnDA">〔點此進入〕</a>
"""
word_nanto_1="""
今日のログインボーナスはこちらです♪
明日はこちらがもらえますからね！
"""
word_nanto_2="""
☆★☆★☆★☆★☆★☆★☆★☆★
"""
word_nanto_3="""
なんとっー！
"""
word_nanto_4="""
ただいま、スペシャルログインボーナスを开催中です♪
明日もログインすると、きっといいことがあると思いますよぉ～。えへへぇ♪
"""

word_test="""
<b>bold</b>, <strong>bold</strong>
<i>italic</i>, <em>italic</em>
<a href="http://www.example.com/">inline URL</a>
<code>inline fixed-width code</code>
<pre>pre-formatted fixed-width code block</pre>
"""

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

################################################
#                   command                    #
################################################
def start(bot, update):
    """Send a message when the command /start is issued."""
    bot.send_message(chat_id=update.message.chat_id, text=word_start,
                  parse_mode=ParseMode.HTML)
    #update.message.reply_text(word_start)

def help(bot, update):
    """Send a message when the command /help is issued."""
    bot.send_message(chat_id=update.message.chat_id, text=word_help)

def rule(bot, update):
    """Send a message when the command /rule is issued."""
    bot.send_message(chat_id=update.message.chat_id, text=word_rule, 
                  parse_mode=ParseMode.HTML)

def state(bot, update):
    """Send a message when the command /state is issued."""
    bot.send_message(chat_id=update.message.chat_id,
    text='目前室內人數：{}'.format(str(bot.get_chat_members_count(update.message.chat.id)))+'\n'+
    "版本：Alpha.0.1")

def config(bot, update):
    """Send a message when the command /config is issued."""
    bot.send_message(chat_id=update.message.chat_id, text="本功能目前沒有毛用")

def nanto(bot, update):
    """Send a message when the command /nanto is issued."""
    bot.send_message(chat_id=update.message.chat_id, text=word_nanto_1)
    time.sleep(1)
    bot.send_message(chat_id=update.message.chat_id, text=word_nanto_2)
    time.sleep(0.5)
    bot.send_message(chat_id=update.message.chat_id, text=word_nanto_3)
    time.sleep(2)
    bot.send_message(chat_id=update.message.chat_id, text=word_nanto_4)

def welcome(bot, update):
    if update.message.new_chat_members!=None:
        new_chat_members=update.message.new_chat_members
    for u in new_chat_members:
        text='野生的'+u.first_name+'出現了'
        bot.send_message(chat_id=update.message.chat_id,text=text)
    if update.message.left_chat_member!=None:
        text=update.message.left_chat_member.first_name+'，別再回來了！'
        bot.send_message(chat_id=update.message.chat_id,text=text)

def test(bot, update):
    """Send a message when the command /test is issued."""
    bot.send_message(chat_id=update.message.chat_id, text=word_test, 
                  parse_mode=ParseMode.HTML)

def echo(bot, update):
    """Echo the user message."""
    global lastnum
    lastnum += int(update.message.text)
    update.message.reply_text(lastnum)



def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


################################################
#                   main                       #
################################################
def main():
    """Start the bot."""
    #TOKEN
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("rule", rule))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("state", state))
    dp.add_handler(CommandHandler("config", config))
    dp.add_handler(CommandHandler("nanto", nanto))
    dp.add_handler(CommandHandler("test", test))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))

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
