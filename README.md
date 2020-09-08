# Web-Scraper-Cricket
A introductory tutorial for web scraping in Python

Web scraping is an useful tool to gather data on the internet. Data can be available across multiple sites in different formats and it is extremely handy to have tools that one can customize to gather the necessary data.

Python has useful libraries like scrapy and beatiful soup 4 for web scraping. Depending on the source from which we are to get the data we can choose our tools/libraries.

Pre Requisities:-
1. Python 2.7 and above
2. scrapy
3. json
4. urllib3

I have prepared scripts to gather data for Indian Premier League 2019 (Cricket) from espncricinfo.com . They are kind enough to allow crawling with a delay if 15 seconds which we would follow.

I have scraped the match data and ball by ball data. The match data had to be scraped using scrapy in the cric_match.py while the ball by ball data has been scraped using json since json data was available. The script for ball by ball data is in ball_by_ball.py .

Please note that the cric_match.py contains a scrapy spider and thus is run from the terminal using "scrap crawl cric_match". 
The ball_by_ball.py can be run using your python IDE or from the terminal.

The scraped data is also uploaded in the scraped-data folder.

The data that has been scraped might not seem complete as I decided to work on these scripts to get an understanding of web scraping. Please feel free to add and format the fields present.
