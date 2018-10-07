from telegram import *
from module import *

def addEcho_help(update,bot):
    """HELP"""
    text="""
<pre>/addecho -w=abc,123 -e=test,test1 -els=300 -al -eli<pre>
-w:可以是多個文字，像是-w=もちょ,ナンス,天ちゃん。空格請用/_/（左右斜線中間底線）替代
［以下三個請擇一輸入］
-e:會回應的文字。像是-e=(●･▽･●)
-p:回應的圖片。可以是imgur圖床網址。
-v:回應的影像。像是gif等，注意格式均為mp4。

-pr:機率。若是落在此機率外則觸發els（可填入0~1000）
-els:若是在機率外就會觸發文字。只能填入一行。-els=(o・∇・o)
-al:要-w中的文字全對才會觸發
-eli:若此為true，則echo可以為多行（會隨機觸發）
    """
    bot.send_message(chat_id=update.message.chat_id,text=text,parse_mode='HTML')

def addEcho_main(context,update,bot,space_word="/_/"):
    # deal space
    unspaced_word=formula('w',context,if_list=True)
    spaced_word=[]
    for word in unspaced_word:
        spaced_word.append(word.replace(space_word,' '))
    unspaced_echo=formula('e',context,if_list=True)
    spaced_echo=[]
    if isinstance(unspaced_echo, list):
        for echo in unspaced_echo:
            spaced_echo.append(echo.replace(space_word,' '))

    # --input data
    data={
        'words':spaced_word,
        'echo':spaced_echo,
        'photo':formula('p',context),
        'video':formula('v',context),
        'prob':int(formula('pr',context)),
        'els':formula('els',context),
        'allco':formula('al',context),
        'echo_list':formula('eli',context),
        'add_by':update.message.chat_id
        }

    if formula('pr',context)==False:
        data['prob']=1000

    # --check
    if data['echo']==False:data['echo']=None
    if data['photo']==False:data['photo']=None
    if data['video']==False:data['video']=None
    if data['els']==False:data['els']=None
    if data['echo_list']==False and data['echo']!=None:
        try:
            data['echo']=data['echo'][0]
        except IndexError:
            pass

    if not isinstance(data['allco'], bool):
        data['allco']=False
    if not isinstance(data['echo_list'], bool):
        data['echo_list']=False
    if data['words']=='':
        data['words']=None
    if data['echo']=='':
        data['echo']=None
    if data['photo']=='':
        data['photo']=None
    if data['video']=='':
        data['video']=None
    def sdmsg(t):
        bot.send_message(chat_id=update.message.chat_id,text=t)
    for i in data['words']:
        if i=="":
            sdmsg('什麼都沒輸入欸ˊˋ')
            return
        if len(i)<2:
            sdmsg('請至少為需要回應的文字輸入至少兩個字。')
            return
    if data['words']==None:
        sdmsg('什麼都沒輸入欸ˊˋ')
        return
    if (data['echo']==[] and data['photo']==None and data['video']==None):
        sdmsg('請輸入至少一個反饋文字。')
        return
    if (data['echo']!=[] and data['photo']!=None):
        sdmsg('請不要輸入兩種反饋。')
        return
    if (data['video']!=None and data['photo']!=None):
        sdmsg('請不要輸入兩種反饋。')
        return
    if (data['echo']!=[] and data['video']!=None):
        sdmsg('請不要輸入兩種反饋。')
        return
    if data['prob']>1000 or data['prob']<0:
        sdmsg('你這樣操作機率會抽不到SSR的！')
        return
    if data['prob']==0:
        sdmsg('這樣到了宇宙都不會發生欸...')
        return
    if isinstance(data['video'], str):
        if not url_valid(data['video']):
            sdmsg('請為影片輸入一個有效的網址！\n或許你應該用 -e 指令？')
            return
    if isinstance(data['photo'], str):
        if not url_valid(data['photo']):
            sdmsg('請為圖片輸入一個有效的網址！\n或許你應該用 -e 指令？')
            return
    return data
