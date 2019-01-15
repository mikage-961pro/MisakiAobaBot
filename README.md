# MisakiAobaBot
<img src="https://i.imgur.com/oHK4EKk.jpg" alt="Misaki" height="80" width="80"> ノノ青羽美咲です！  
![version](https://img.shields.io/badge/Version-v1.0.0-brightgreen.svg?longCache=true&style=popout)
[![package](https://img.shields.io/badge/Telegram.Bot-10.1.0-blue.svg?longCache=true&style=popout)](https://python-telegram-bot.org)
[![telegram chat](https://img.shields.io/badge/Support_Chat-Telegram-blue.svg?style=popout)](https://t.me/MisakiAobaBot)
[![Contribution](https://img.shields.io/badge/Contribution-welcome-yellow.svg?style=popout)](https://t.me/imas_techno)
[![license](https://img.shields.io/github/license/TelegramBots/telegram.bot.svg?style=popout&maxAge=2592000&label=License)](LICENSE)  
Misaki Aoba chat bot.  
This chat bot is originally used to manage our im@s [chat room](https://t.me/imas_zh), but now it can use to manage other chat room.

## Command

- **start** - 我是765事務所的事務員，青羽美咲
- **help** - 由青羽小姐提供您幫助
- **rule** - 本群規則瀏覽
- **config** - 設定，情報
設定個人情報。房間設定必須由房間管理員才有權限使用。
- **tbgame** - 765プロゲーム部入口，進去跟大家玩桌遊吧
- **nanto** - なんとぉ！  
`/nanto who#thing` or `/nanto thing`
- **which** - 把事情丟給美咲決定（用#井字號分隔事情）  
`/which abc#123`
- **quote** - 每日一句  
`/quote -f=[word]`可以查詢名言
- **randpic** - 召喚隨機圖片  
`/randpic idol_name`可以指定召喚
- **sticker** - STICKERまとめ
- **exrate** - 匯率轉換  
`\exrate TWD>JPY`
- **twd2jpy** - 台幣日幣匯率  
本資料由台灣銀行提供
- **mltdrank** - MLTD簡易即時排名資訊  
本資料由[matsurihi.me](https://api.matsurihi.me)提供

## Inline command
- **Inline picture**  
使用指令
`@MisakiAobaBot`或是`@MisakiAobaBot [idol_name]`就可以在任意房間召喚偶像。

## Function

- **quote:** Record words that you interest, which will show when `/quote` command entered.  
回覆他人並且鍵入`#名言`即可儲存。  
本功能每個房間皆為獨立。  
房間預設關閉，必須去`/config`設定開啟。
- **words reaction:** Bot will say something when user enter some specific words.  
房間預設關閉，必須去`/config`設定開啟。
- **group state record:** Record the member and message number every time. Admin can turn on record daily function.  
房間預設關閉，必須去`/config`設定開啟。
- **picture save and call:** 使用`#idol`功能儲存你喜歡的偶像圖。  
房間預設關閉，必須去`/config`設定開啟。
- **rule setting:** 可以自訂不同的群規則。

## Update Log
New Version: v1.0.1  
Last Update:2018/12/23

### v1.0.1
1. Seperate quote by room.

### Stable v1.0.0
**Everything is on the right way.**  

1. Add MLTD rank showbox.


## Contributing

Contributions are [Welcome!!](https://www.project-imas.com/wiki/Welcome!!)  
Please join the [Telegram Group](https://t.me/imas_techno) for more information.
