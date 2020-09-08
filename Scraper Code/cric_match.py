import scrapy
import requests
import numpy as np
import re

class cric_match(scrapy.Spider):
   #name of spider
    name = 'cric_match'
   
   #list of allowed domains
    allowed_domains = ['https://www.espncricinfo.com/']
   #starting url
    start_urls = ['https://www.espncricinfo.com/scores/series/8048/season/2019/indian-premier-league?view=results']
   #location of csv file
    custom_settings = {'FEED_URI' : 'tmp/match_details.csv','DOWNLOAD_DELAY':15}
    
    def parse(self, response):

        url_main = "https://www.espncricinfo.com/scores/series/8048/season/2019/indian-premier-league?view=results"
        scrapy.Request(url_main, callback=self.parse,dont_filter=True)
        match_url = response.xpath('//a[@data-hover="Scorecard"]/@href').extract()

        for count in range(len(match_url)):
            url = match_url[count]
            url = "https://www.espncricinfo.com"+url
            eventId= str(url).split("/")[6]
            yield scrapy.Request(url, callback=self.parse_match,dont_filter=True,meta = {"item":{"url":url,"match_id":eventId}})


    def parse_match(self, response):
        item = response.meta["item"]
        teams = response.xpath('//a[@target="_self"]/span[@title]/@title').extract()
        item["team_1"]=teams[0]
        item["team_2"]=teams[1]

        item["win_runs"]="NA"
        item["win_wickets"]="NA"
        item["winner"]="NA"
        item["match_drawn"]="NA"
        item["match_abandoned"]="NA"
        item["no_result"] ="NA"
        win = response.xpath('//div[@class="summary"]/span/text()').extract()

        if("won" in str(win)):
            win_map = {"Mumbai Indians":"Mum Indians","Delhi Capitals" :"Capitals","Chennai Super Kings":"Super Kings","Sunrisers Hyderabad":"Sunrisers","Rajasthan Royals":"Royals","Royal Challengers Bangalore":"RCB","Kolkata Knight Riders":"KKR","Kings XI Punjab":"Kings XI"}
            if( item["team_1"] in str(win) or win_map[item["team_1"]] in str(win)):
                item["winner"] = item["team_1"]
            elif (item["team_2"] in str(win) or win_map[item["team_2"]] in str(win)):
                item["winner"]  = item["team_2"]

            if("runs" in str(win) or "run" in str(win)):
                item["win_runs"] = win[0].split("by")[1].split(" ")[1]
            else:
                item["win_wickets"] = win[0].split("by")[1].split(" ")[1]
        elif ("Match drawn" in str(win)):
            item["match_drawn"] = "Yes"
        elif ("abandoned" in str(win) or "cancelled" in str(win)):
            item["match_abandoned"]="Yes"
        elif ("No result" in str(win)):
            item["no_result"] ="Yes"

        toss = response.xpath('//table[@class="w-100 table match-details-table"]/tbody/tr[2]/td[2]/text()').extract()
        item["toss_winner"] = str(toss).split("'")[1].split(",")[0].strip()
        item["winner_choice"]=  ["Field" if "field" in str(toss) else "Bat"]
        item["series"] = response.xpath('//table[@class="w-100 table match-details-table"]/tbody/tr[3]/td[2]/a/text()').extract()
        item["pom"] = response.xpath('//div[@class="best-player-name"]/a/text()').extract()
        match_desc = response.xpath('//div[@class="desc text-truncate"]/text()').extract()
        item["match_number"] = re.findall(r'\d+', str(match_desc).split(" ")[0])

        if (len(item["match_number"])==0):
            item["match_number"]= str(match_desc).split("'")[1].split(" ")[0]

        item["city"] = str(match_desc).split(",")[1].strip()
        item["date"] = str(match_desc).split(",")[2].lstrip()
        item["day_night"] = re.search(r'\((.*?)\)',str(match_desc)).group(1)
        return item




