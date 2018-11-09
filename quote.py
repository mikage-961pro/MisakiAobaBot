from telegram import *
from module import *
import menu
from datetime import datetime
import random
quotes=[]

def quote_collecter(bot, update, context, room_switch):
    if room_switch!=True:
        """Switch"""
        return False
    ###################################
    #          quote collector        #
    ###################################
    record=False
    if context.find(' #名言')!=-1 or context.find('#名言 ')!=-1:
        if update.message.reply_to_message==None and update.message.from_user.is_bot==False:
            context=context.replace(' #名言','').replace('#名言 ','')
            qdict={
                'quote': context,
                'said': update.message.from_user.first_name,
                'tag': '',
                'said_id':update.message.from_user.id,
                'date':datetime.now()
                }
            insert_data('quote_main',qdict)
            record=True
    if context.find('#名言')!=-1 and record==False:
        if update.message.reply_to_message is not None and update.message.reply_to_message.from_user.is_bot==False:
            qdict={
                'quote': update.message.reply_to_message.text,
                'said': update.message.reply_to_message.from_user.first_name,
                'tag': '',
                'said_id':update.message.reply_to_message.from_user.id,
                'date':datetime.now()
                }
            insert_data('quote_main',qdict)

def quote_finder(context,bot, update):
    quote_search={}
    if context=="":
        """Case 1: No words"""
        bot.send_message(chat_id=update.message.chat_id,text="Please enter word.")
        return False
    # Search initialization
    find_result=db_quote_finder(context)
    result_length=len(find_result)
    search_init_time=datetime.now()

    if result_length==0:
        """Case 2: No search result"""
        bot.send_message(chat_id=update.message.chat_id,text="No search result.")
        return False

    elif result_length<10:
        """Case 3: Result is less than 10"""
        # Hint user that result is in PM
        if if_int_negative(update.message.chat_id):
            bot.send_message(chat_id=update.message.chat_id,text="結果將顯示於私人對話。")

        # context user has start bot
        try:
            bot.send_message(chat_id=update.message.from_user.id,
                text="以下為【{}】的搜尋結果".format(context))
        except:
            bot.send_message(chat_id=update.message.chat_id,
                    text=GLOBAL_WORDS.word_PM_notice,
                    parse_mode='HTML')
            return False

        # Package result
        result=[]
        t=""
        counter=1
        for i in find_result:
            try:
                # Pharse Bug fix
                if i['quote'].find('(*>△<)')!=-1 or i['said'].find('(*>△<)')!=-1:
                    t=t+str(counter)+'. '+'<pre>'+i['quote'].replace('(*>△<)','(*＞△＜)')+'</pre>'+' -- '+i['said'].replace('(*>△<)','(*＞△＜)')+'\n'
                elif not htmlPharseTester(i['quote']) or not htmlPharseTester(i['said']):
                    t=t+str(counter)+'. '+'<pre>'+i['quote'].replace('<','＜')+'</pre>'+' -- '+i['said'].replace('<','＜')+'\n'
                else:
                    t=t+str(counter)+'. '+'<pre>'+i['quote']+'</pre>'+' -- '+i['said']+'\n'
            except TypeError:
                logger.warning("Quote finder has problem on:%s,%s Oid=%s",
                    str(i['quote']),str(i['said']),str(i['_id']))
            counter+=1
        result.append(t)

        # Sending result
        try:
            quote_search[update.message.from_user.id]=result
            # save to globle var
            bot.send_message(chat_id=update.message.from_user.id,
                text=result[0],
                reply_markup=menu.page_keyboard(result,1),
                parse_mode='HTML')
        except:
            bot.send_message(chat_id=update.message.from_user.id,text="ぜ")
            return False
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
                text="以下為【{}】的搜尋結果".format(context))
        except:
            bot.send_message(chat_id=update.message.chat_id,
                    text=GLOBAL_WORDS.word_PM_notice,
                    parse_mode='HTML')
            return False

        # Package result
        result=[]
        result_sub=[]
        counter=1
        for i in find_result:
            try:
                # Pharse Bug fix
                if i['quote'].find('(*>△<)')!=-1 or i['said'].find('(*>△<)')!=-1:
                    t=str(counter)+'. '+'<pre>'+i['quote'].replace('(*>△<)','(*＞△＜)')+'</pre>'+' -- '+i['said'].replace('(*>△<)','(*＞△＜)')+'\n'

                elif not htmlPharseTester(i['quote']) or not htmlPharseTester(i['said']):
                    t=str(counter)+'. '+'<pre>'+i['quote'].replace('<','＜')+'</pre>'+' -- '+i['said'].replace('<','＜')+'\n'
                else:
                    t=str(counter)+'. '+'<pre>'+i['quote']+'</pre>'+' -- '+i['said']+'\n'
                result_sub.append(t)
            except TypeError:
                logger.warning("Quote finder has problem on:%s,%s Oid=%s",
                    str(i['quote']),str(i['said']),str(i['_id']))
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
        quote_search[update.message.from_user.id]=result # save to globle var
        try:
            # Sending result
            bot.send_message(chat_id=update.message.from_user.id,
                text=result[0],
                reply_markup=menu.page_keyboard(result,1),
                parse_mode='HTML')
        except:
            bot.send_message(chat_id=update.message.from_user.id,text="ぜ")
            return False
        finally:
            search_total_time=(datetime.now()-search_init_time).total_seconds()
            t="結束搜尋。共有{}筆資料共{}頁。\n共耗時{}秒。".format(result_length,int((result_length-1)/10)+1,search_total_time)
            bot.send_message(chat_id=update.message.from_user.id,text=t,parse_mode='HTML')
    return quote_search

def quote_get():
    """Return an arranged quote"""
    global quotes
    if len(quotes)==0:
        quote_shuffle()
        return quotes.pop()
    return quotes.pop()
    
def quote_shuffle():
    global quotes
    after=datetime.datetime.now()-datetime.timedelta(5,0,0)
    quotes=randget(Collection='quote_main',size=5)+randget_t(Collection='quote_main',size=5,after=after)
    random.shuffle(quotes)
    