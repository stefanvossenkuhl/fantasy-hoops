#!/usr/bin/env python3
"""Fetch ESPN's unofficial NBA scoreboard into a static cache for GitHub Pages."""
import datetime as dt, json, os, pathlib, time, urllib.request
ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/'data'/'nba.json'
now=dt.datetime.now(dt.timezone.utc)
today=now.date()
start=today-dt.timedelta(days=today.weekday())
headers={'User-Agent':'Mozilla/5.0 (compatible; FantasyHoops/1.0)','Accept':'application/json'}
def get(url):
    req=urllib.request.Request(url,headers=headers)
    with urllib.request.urlopen(req,timeout=18) as r:return json.load(r)
weeks={}; errors=[]
for offset in (0,7):
    monday=start+dt.timedelta(days=offset)
    events=[]
    for i in range(7):
        day=monday+dt.timedelta(days=i)
        try:
            payload=get('https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates='+day.strftime('%Y%m%d')+'&limit=100')
            if not isinstance(payload.get('events'),list):raise ValueError('No events array')
            for e in payload['events']:
                teams=[x.get('team',{}).get('abbreviation','') for x in e.get('competitions',[{}])[0].get('competitors',[])]
                events.append({'id':e.get('id'),'date':e.get('date'),'teams':teams,'completed':bool(e.get('status',{}).get('type',{}).get('completed')),'status':e.get('status',{}).get('type',{}).get('description','')})
        except Exception as exc:errors.append(f'{day}: {exc}')
        time.sleep(.12)
    weeks[monday.isoformat()]=events
if errors:
    raise SystemExit('Incomplete ESPN fetch; preserving previous cache. '+ '; '.join(errors))
OUT.parent.mkdir(exist_ok=True)
new={'updated_at':now.isoformat(),'source':'ESPN unofficial scoreboard','weeks':weeks,'limitations':'Schedules only. No verified injury or projection feed.'}
tmp=OUT.with_suffix('.tmp');tmp.write_text(json.dumps(new,separators=(',',':')));os.replace(tmp,OUT)
print('Wrote',OUT,'with',sum(map(len,weeks.values())),'games')
