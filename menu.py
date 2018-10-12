from telegram import *
from module import *
from string import Template
global quote_search

################################################
#              menu command                    #
################################################
def menu_actions(bot, update):
    query = update.callback_query
    query_text=query.data
    qcid=query.message.chat_id
    qmid=query.message.message_id
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
        text=temp.substitute(boot_time=init_time)
        bot.send_message(text=text,chat_id=query.message.chat_id,parse_mode=ParseMode.HTML)
    def menu_resp_check():
        data_value = display_data('config',{'id':query.from_user.id},'reply')
        if data_value is None:
            data_value=True#default open
        text='{}P目前狀態：{}'.format(query.from_user.first_name,bool2text(data_value))
        bot.edit_message_text(chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text=text,
                reply_markup=user_echo_switch_keyboard(data_value))
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
        if user_admin_value(query.message) is not True:
            bot.edit_message_text(chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    text="只有管理員擁有此權限。")
            return
        mention_url='tg://user?id={}'.format(query.message.from_user.id)
        first_name=query.message.from_user.first_name
        text='請回覆群規文字。\n本功能支援HTML格式。'.format(mention_url,first_name)
        f=ForceReply(force_reply=True,selective=True)
        bot.delete_message(chat_id=query.message.chat_id,
                message_id=query.message.message_id)
        rpl=bot.send_message(chat_id=query.message.chat_id,
            text=text,reply_to_message=query.message,reply_markup=f,parse_mode='HTML')
        global reply_pair
        """[0]:Function [1]:Data"""
        reply_pair[query.from_user.id]=["RULE_EDIT",rpl]

    def menu_turn_left(page):
        try:
            result=quote_search[query.from_user.id]
        except KeyError:
            bot.edit_message_text(chat_id=query.from_user.id,
                    message_id=query.message.message_id,
                    text="搜尋逾時，請重新搜尋。")
            return
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
            bot.edit_message_text(chat_id=query.from_user.id,
                    message_id=query.message.message_id,
                    text="搜尋逾時，請重新搜尋。")
            return
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
    def get_room_config():
        echo_value=display_data2('room_config',{'room_id':qcid},'echo')
        water_value=display_data2('room_config',{'room_id':qcid},'water')
        pic_value=display_data2('room_config',{'room_id':qcid},'savepic')
        quote_value=display_data2('room_config',{'room_id':qcid},'quote')
        return [echo_value,water_value,pic_value,quote_value]
    def menu_room_switch():
        """
        if user_admin_value(query.message) is not True:
            bot.edit_message_text(chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    text="只有管理員擁有此權限。")
        """
        bot.edit_message_text(chat_id=qcid,
            message_id=qmid,
            text='群組的各項設定開關：（僅限管理員使用）',
            reply_markup=room_setting_switch_keyboard(get_room_config()))
    def menu_room_switch_echo():
        echo_value=display_data2('room_config',{'room_id':qcid},'echo')
        if echo_value:
            VALUE=False
        else:
            VALUE=True
        updata_data("room_config",{'room_id':qcid},{"$set":{'echo':VALUE}})
        bot.edit_message_text(chat_id=qcid,
            message_id=qmid,
            text='群組的各項設定開關：（僅限管理員使用）',
            reply_markup=room_setting_switch_keyboard(get_room_config()))
    def menu_room_switch_water():
        water_value=display_data2('room_config',{'room_id':qcid},'water')
        if water_value:
            VALUE=False
        else:
            VALUE=True
        updata_data("room_config",{'room_id':qcid},{"$set":{'water':VALUE}})
        bot.edit_message_text(chat_id=qcid,
            message_id=qmid,
            text='群組的各項設定開關：（僅限管理員使用）',
            reply_markup=room_setting_switch_keyboard(get_room_config()))
    def menu_room_switch_quote():
        quote_value=display_data2('room_config',{'room_id':qcid},'quote')
        if quote_value:
            VALUE=False
        else:
            VALUE=True
        updata_data("room_config",{'room_id':qcid},{"$set":{'quote':VALUE}})
        bot.edit_message_text(chat_id=qcid,
            message_id=qmid,
            text='群組的各項設定開關：（僅限管理員使用）',
            reply_markup=room_setting_switch_keyboard(get_room_config()))
    def menu_room_switch_savepic():
        savepic_value=display_data2('room_config',{'room_id':qcid},'savepic')
        if savepic_value:
            VALUE=False
        else:
            VALUE=True
        updata_data("room_config",{'room_id':qcid},{"$set":{'savepic':VALUE}})
        bot.edit_message_text(chat_id=qcid,
            message_id=qmid,
            text='群組的各項設定開關：（僅限管理員使用）',
            reply_markup=room_setting_switch_keyboard(get_room_config()))

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
    elif query_text == "cmd_room_switch":
        """room setting for some switch"""
        menu_room_switch()
    elif query_text == "cmd_room_switch_echo":
        """room echo setting"""
        menu_room_switch_echo()
    elif query_text == "cmd_room_switch_quote":
        """room switch setting"""
        menu_room_switch_quote()
    elif query_text == "cmd_room_switch_water":
        """room water setting"""
        menu_room_switch_water()
    elif query_text == "cmd_room_switch_savepic":
        """room savepic setting"""
        menu_room_switch_savepic()
    elif query_text == "None":
        """No cmd, decoration"""
        pass


# Keyboards
def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton(text='回話設定',callback_data='cmd_resp_check'),
               InlineKeyboardButton(text='群規設定',callback_data="cmd_ruleSetting")],
              [InlineKeyboardButton(text='群組狀態',callback_data="cmd_state")
              ,InlineKeyboardButton(text='關於美咲',callback_data="cmd_about")],
              [InlineKeyboardButton(text='群組開關',callback_data="cmd_room_switch")],
              [InlineKeyboardButton(text='取消',callback_data="cmd_canceled")]]
    return InlineKeyboardMarkup(keyboard)

def user_echo_switch_keyboard(state):
    keyboard = [[InlineKeyboardButton(text='關閉回話' if state else '開啟回話',
        callback_data='cmd_resp_switch_off' if state else 'cmd_resp_switch_on')],
                [InlineKeyboardButton(text='取消',callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)

def room_setting_switch_keyboard(state):
    """input is a list to call the state in each function"""
    keyboard = [[InlineKeyboardButton(text='群組回話[{}]'.format(bool2text(state[0])),callback_data='cmd_room_switch_echo')],
                [InlineKeyboardButton(text='水量計數[{}]'.format(bool2text(state[1])),callback_data='cmd_room_switch_water')],
                [InlineKeyboardButton(text='圖片記錄[{}]'.format(bool2text(state[2])),callback_data='cmd_room_switch_savepic')],
                [InlineKeyboardButton(text='名言紀錄[{}]'.format(bool2text(state[3])),callback_data='cmd_room_switch_quote')],
                [InlineKeyboardButton(text='回主頁',callback_data="main"),
                InlineKeyboardButton(text='結束',callback_data="cmd_canceled")]]
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
