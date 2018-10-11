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


###################################
#        key word reaction        #
###################################
def wordEcho(bot,update,user_switch,room_switch,key_words):
    """Detect what user say and misaki will response."""
    # --Step.1 Switch--
    if user_switch==False or room_switch==False:
        """Switch"""
        return False

    word_pool=[] #create a pool to save those have chance to send
    def comparator(word,data):
        """Input text, compare to data in database, return value and save in pool."""
        # word is str, where data is a dict
        if not isinstance(word, str):
            raise TypeError
        if not isinstance(data, dict):
            raise TypeError

        """check if all word correct will go"""
        try:
            for check in data['words']:
                if data['allco'] == False:
                    "one word correct will go"
                    if word.find(check)!=-1:
                        return data
                else:
                    "all word correct will go"
                    if word.find(check)!=-1:
                        continue
                    else:
                        return False
                    return data
        except TypeError:
            logger.error("Words type wrong:%s",str(words))
        return False
        # If nothing return false

    # --Step.2 Compare data--
    echo_data=display_alldata('words_echo') # Catch all data in db
    for d in echo_data:
        # Search data in db
        data_value=comparator(key_words,d)
        if data_value:
            word_pool.append(data_value)
            # If search engine has result, save it to pool

    if not word_pool:
        # If pool has nothing, return
        return False

    # --Step.3 Pick data from pool--
    pool_rand=weighted_random()
    type="" # Video / Photo / String
    for i in word_pool:
        """
        Determine its type. Msg or Video or Photo? Pack it and send.
        Note that echo may be video.
        """
        echo=i['echo']
        photo=i['photo']
        video=i['video']
        prob=i['prob']
        els=i['els']

        if echo:
            """ECHO case"""
            if i['echo_list']:
                """If echo is a list"""
                each_prob=int(prob/len(echo))
                for each_echo in echo:
                    rand_data={"Type":"STRING","Data":each_echo}
                    pool_rand.add(rand_data,each_prob)
            else:
                rand_data={"Type":"STRING","Data":echo}
                pool_rand.add(rand_data,prob)
            if url_valid(els):
                rand_data={"Type":"VIDEO","Data":els}
                pool_rand.add(rand_data,1000-prob)
            elif els==None:
                pool_rand.add_none(1000-prob)
            else:
                rand_data={"Type":"STRING","Data":els}
                pool_rand.add(rand_data,1000-prob)
        elif photo:
            """PHOTO case"""
            if i['echo_list']:
                """If echo is a list"""
                each_prob=int(prob/len(photo))
                for each_photo in photo:
                    rand_data={"Type":"PHOTO","Data":each_photo}
                    pool_rand.add(rand_data,each_prob)
            else:
                rand_data={"Type":"PHOTO","Data":photo}
                pool_rand.add(rand_data,prob)

            if els==None:
                pool_rand.add_none(1000-prob)
            else:
                rand_data={"Type":"PHOTO","Data":els}
                pool_rand.add(rand_data,1000-prob)
        elif video:
            """VIDEO case"""
            if i['echo_list']:
                """If echo is a list"""
                each_prob=int(prob/len(video))
                for each_video in video:
                    rand_data={"Type":"VIDEO","Data":each_video}
                    pool_rand.add(rand_data,each_prob)
            else:
                rand_data={"Type":"VIDEO","Data":video}
                pool_rand.add(rand_data,prob)
            if els==None:
                pool_rand.add_none(1000-prob)
            else:
                rand_data={"Type":"VIDEO","Data":els}
                pool_rand.add(rand_data,1000-prob)




    # --Step.4 Send--
    cid=update.message.chat_id
    def msgSend(words):
        try:
            bot.send_message(chat_id=cid,text=words)
        except:
            logger.error("Word echo failed while sending word %s.",words)
    def videoSend(vid):
        try:
            bot.send_video(chat_id=cid, video=vid)
        except:
            logger.error("Word echo failed while sending video %s.",vid)
    def picSend(pic):
        try:
            bot.send_photo(chat_id=cid, photo=pic)
        except:
            logger.error("Word echo failed while sending photo %s.",pic)

    jump_from_pool=pool_rand.output_one()
    if jump_from_pool==None:
        return
    pool_type=jump_from_pool['Type']
    if pool_type=="STRING":
        msgSend(jump_from_pool['Data'])
    elif pool_type=="PHOTO":
        photoSend(jump_from_pool['Data'])
    elif pool_type=="VIDEO":
        videoSend(jump_from_pool['Data'])
