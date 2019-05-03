import time
import schedule # !pip install schedule
from twi_bot import TwitterAPI

twitter_api = TwitterAPI()    
schedule.every().saturday.do(twitter_api.update_status)
schedule.every().sunday.do(twitter_api.like_and_retweet, "#100DaysOfMLCode")

while True:
    schedule.run_pending()
    time.sleep(1)