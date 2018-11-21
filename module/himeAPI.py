#coding=utf-8
import requests
import json
import datetime

END_POINT='https://api.matsurihi.me/mltd/v1/'

def event_score():
    q1="events/{}/rankings/logs/eventPoint/{}"
    q2="events/{}".format('62')
    event_name=requests.get(END_POINT+q2).json()['name']
    border_info={'name':event_name}
    def border(rank):
        api=requests.get(END_POINT+q1.format('62',rank)).json()[0]['data']
        now=int(api[len(api)-1]['score'])
        summaryT=str(api[len(api)-1]['summaryTime'])
        summaryT= datetime.datetime.strptime(summaryT[:-7],'%Y-%m-%dT%H:%M:%S')-datetime.timedelta(hours=1)
        past_2='--'
        if len(api)>2:
            past_2=int(api[len(api)-4]['score'])
        return {'rank':rank,'score':now,'past_2':past_2,'summaryTime':summaryT.strftime("%Y-%m %H:%M")}
        
    border_info[3]=border(3)
    border_info[100]=border(100)
    border_info[2500]=border(2500)
    border_info[5000]=border(5000)
    border_info[10000]=border(10000)
    border_info[25000]=border(25000)
    return border_info

    
        
        