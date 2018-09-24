# coding=utf-8

bot_name='@MisakiAobaBot'
# ---My Module
from module import *

def RESET(words, echo=None, photo=None, video=None,
    prob=1000, els=None,allco=False, echo_list=False):
    data={
        'words':words,
        'echo':echo,
        'photo':photo,
        'video':video,
        'prob':prob,
        'els':els,
        'allco':allco,
        'echo_list':echo_list
        }
    insert_data('words_echo',data)
    logger.info("Reset finished:%s",words)
pic_ten=['https://i.imgur.com/XmWYqS1.mp4',
'https://imgur.com/LYBnOzo.mp4',
'https://i.imgur.com/denCUYX.mp4']
pic_trys=['https://img.gifmagazine.net/gifmagazine/images/2289135/original.mp4',
'https://i.imgur.com/b9s69iK.mp4',
'https://img.gifmagazine.net/gifmagazine/images/1333179/original.mp4']
RESET(words=['大老','dalao','ㄉㄚˋㄌㄠˇ','巨巨','Dalao','大 佬'],echo='你才大佬！你全家都大佬！', prob=200)
RESET(words=['依田','芳乃'], echo='ぶおおー')
RESET(words=['青羽','美咲'], echo='お疲れ様でした！')
RESET(words=['ころあず'], echo='ありがサンキュー！')
RESET(words=['この歌声が'], echo='MILLLLLIIIONNNNNN',els='UNIIIIIOOONNNNN',prob=500)
RESET(words=['天','ナンス','もちょ'],video=pic_trys,allco=True,echo_list=True)
RESET(words=['麻倉','もも','もちょ'], echo='(●･▽･●)',els='(o・∇・o)もちー！もちもちもちもちもちーーーもちぃ！',prob=900)
RESET(words=['夏川','椎菜','ナンス'], echo='(*>△<)<ナーンナーンっ',els='https://imgur.com/AOfQWWS.mp4',prob=300)
RESET(words=['雨宮','てん','天ちゃん'], video=pic_ten,echo_list=True)
RESET(words=['天'], prob=15, video=pic_ten,echo_list=True)
RESET(words=['終わり','結束','沒了','完結'], echo='終わりだよ(●･▽･●)')
RESET(words=['小鳥'], echo='もしかして〜♪ 音無先輩についてのお話ですか')
RESET(words=['誰一百'], echo='咖嘎雅哭')
RESET(words=['咖嘎雅哭'], echo='吼西米～那咧')
RESET(words=['vertex'], echo='IDOL!')
RESET(words=['高木','社長','順二朗'], echo='あぁ！社長のことを知りたい！')
RESET(words=['天海','春香'], echo='天海さんのクッキーはとっても美味しいですね〜')
RESET(words=['閣下'], echo='え！？もしかして春香ちゃん！？',els='恐れ、平れ伏し、崇め奉りなさいのヮの！',prob=900)
RESET(words=['如月','千早'], echo='如月さんの歌は素晴らしい！',els='静かな光は蒼の波紋 VERTEX BLUE!!!!',prob=720)
RESET(words=['72'],prob=10, echo='こんな言えば如月さんは怒ってしまうよ！')
RESET(words=['星井','美希'], echo='あの...星井さんはどこかで知っていますか？')
RESET(words=['高槻','やよい'], echo="ζ*'ヮ')ζ＜うっうー ")
RESET(words=['萩原','雪歩'], echo='あ、先のお茶は萩原さんからの')
RESET(words=['秋月','律子'], echo='律子さんは毎日仕事するで、大変ですよね〜')
RESET(words=['三浦','あずさ'], echo='え？あずささんは今北海道に！？')
RESET(words=['水瀬','伊織'], echo='このショコラは今朝水瀬さんからの、みな一緒に食べろう！')
RESET(words=['菊地','真'], echo='真さんは今、王子役の仕事をしていますよ。',
els='真さんは今、ヒーロー役の仕事をしていますよ～～激しい光は黒の衝撃 VERTEX BLACK!!!!',prob=700,allco=True)
RESET(words=['我那覇','響'], echo='ハム蔵はどこでしょうか？探していますね',els='弾ける光は浅葱の波濤 VERTEX LIGHTBLUE!!',prob=700,allco=True)
RESET(words=['四条','貴音'], echo='昨日〜貴音さんがわたしに色々な美味しい麺屋を紹介しました！',els='秘めたり光は臙脂の炎 VERTEX CARMINE〜〜',prob=700)
RESET(words=['亜美'], echo='亜美？あそこよ')
RESET(words=['真美'], echo='真美？いないよ')
RESET(words=['双海'], echo='亜美真美？先に外へ行きました')
