from telegram import *
from module import *
from datetime import datetime

def picSave_main(bot, update, context, room_switch):
    if room_switch!=True:
        """Switch"""
        return False
    ###################################
    #              picsave            #
    ###################################
    if context.find("@db")!=-1:
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
                else:
                    logger.info("Not valid url while saving:%s",rmsg.text)
                    bot.send_message(chat_id=update.message.chat_id,text="不正確的連結。")
            except AttributeError:
                bot.send_message(chat_id=update.message.chat_id,text="画像がない。保存失敗しました。")
        elif cmd_word_save=='':
            bot.send_message(chat_id=update.message.chat_id,text="もう！こんな遊ばなってください！")
        else:
            pass
            #bot.send_message(chat_id=update.message.chat_id,text="知らない人ですよ。")
        # Exit region
    Enti=update.message.parse_entities()
    Enti_list=list(Enti.keys())
    for i in Enti_list:
        if i.type=='hashtag':
            cmd_word_save=Enti[i][1:].lower()
            if cmd_word_save in GLOBAL_WORDS.idol_list:
                rmsg=update.message.reply_to_message
                if rmsg is not None:
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
                        else:
                            logger.info("Not valid url while saving:%s",rmsg.text)
                            bot.send_message(chat_id=update.message.chat_id,text="不正確的連結。")
                    except AttributeError:
                        bot.send_message(chat_id=update.message.chat_id,text="画像がない。保存失敗しました。")
