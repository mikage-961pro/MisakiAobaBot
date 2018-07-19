# coding=utf-8

bot_name='@MisakiAobaBot'
if debug_mode is True:
    token='690274765:AAFxDyslvSkuVbPJXUAjWm2u6iy92bBB-JU'
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
