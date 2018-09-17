# coding=utf-8
#ミサキ・ファミリア

import MisaMongo

def set_to_track(chat_id=None):
    if chat_id is not None:
        MisaMongo.insert_data('group_config',{'group_id':chat_id})
    else:
        return

def track(chat_id,message_id):
    if MisaMongo.display_data('group_config',{'group_id':chat_id},'group_id')==chat_id:
        MisaMongo.modify_data('group_config',
        {'group_id':chat_id},key='last_message',
        update_value=message_id)

def history()        