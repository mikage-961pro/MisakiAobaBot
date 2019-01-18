#coding=utf-8
import requests
import json
import datetime

END_POINT='https://api.matsurihi.me/mltd/v1/'

    
def event_score():
    q="events/"
    q1="events/{}/rankings/logs/eventPoint/{}"

    event=requests.get(END_POINT+q).json()[-1]
    if (event['type']==1 or event['type']==2 or event['type']==6):
        return {'name':event['name'],'rank_able':False}
    border_info={'name':event['name'],'rank_able':True}
    def border(rank):
        api=requests.get(END_POINT+q1.format(event['id'],rank)).json()[0]['data']
        now=int(api[-1]['score'])
        summaryT=str(api[len(api)-1]['summaryTime'])
        summaryT= datetime.datetime.strptime(summaryT[:-7],'%Y-%m-%dT%H:%M:%S')-datetime.timedelta(hours=1)
        past_1='--'
        if len(api)>3:
            past_1=int(api[-3]['score'])
        return {'rank':rank,'score':now,'past_1':past_1,'speed':now-past_1,'summaryTime':summaryT.strftime("%m-%d %H:%M")}
        
    border_info[3]=border(3)
    border_info[100]=border(100)
    border_info[2500]=border(2500)
    border_info[5000]=border(5000)
    border_info[10000]=border(10000)
    border_info[25000]=border(25000)
    return border_info

    
        
        