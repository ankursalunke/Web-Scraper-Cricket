import pandas as pd
import json
import urllib3
from time import sleep

http = urllib3.PoolManager()

col_data = pd.DataFrame()
mat_data = pd.DataFrame()
periods = ["1","2"]
pages = ["1","2","3","4","5","6","7","8","9","10"]
leagueId="8048"
eventId=""

dat_url = pd.read_csv("/spiders/tmp/match_details.csv")
eventId_gp= [str(url).split("/")[6] for url in dat_url["url"]]
len_url= len(eventId_gp)

for count in range(len_url):
    eventId = eventId_gp[count]
    print(count)
    for period in periods:
        for page in pages:
            sleep(15)
            col_data = pd.DataFrame()
            match_dat= http.request('GET', 'https://hsapi.espncricinfo.com/v1/pages/match/comments?lang=en&leagueId='+leagueId+'&eventId='+eventId+'&period=' +period+ '&page='+page+'&filter=full&liveTest=false')
            if(len(match_dat.data)<100):
                break
            data = json.loads(match_dat.data)
            df = pd.json_normalize(data['comments'])
            bowler=[]
            batsman=[]

            for bat,bowl in zip(df["currentBatsmen"],df["currentBowlers"]):
                batsman.append(bat[0]["name"])
                bowler.append(bowl[0]["name"])

            df["bowler"]= bowler
            df["batsman"] = batsman
            col_data = df.copy()    

            if(period=="1"):               
                df["innings"]=1
            else:
                df["innings"]=2

            if("matchWicket.text" in col_data.columns):
                col_data["matchWicket.text"].fillna("NA",inplace=True)
                col_data["run_out"]= ["Yes" if "run out" in wicket_text else "No" for wicket_text in col_data["matchWicket.text"]]
            else:
                col_data["matchWicket.text"]="NA"
                col_data["run_out"]="No"
                   
         
            col_data["match_id"] = eventId        
            mat_data = pd.concat([mat_data,col_data])   

mat_data.drop(["id","shortText","text","preText","postText","currentBatsmen","currentBowlers","currentInning.balls","currentInning.runs","currentInning.wickets","matchOver.maiden","matchOver.runs","matchOver.wickets","matchOver.totalRuns","matchOver.totalWicket","matchOver.runRate","matchOver.requiredRunRate","matchOver.batsmen","matchOver.bowlers","matchOver.teamShortName","matchOver.remainingOvers","matchOver.remainingBalls","matchOver.remainingRuns","matchWicket.id","matchWicket.batsmanRuns","matchWicket.batsmanBalls","matchWicket.text"],axis=1,inplace=True)
mat_data.to_csv("/spiders/tmp/score.csv")
