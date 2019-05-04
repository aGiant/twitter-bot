
| ![TwitterBot](https://s3.amazonaws.com/com.twilio.prod.twilio-docs/images/twitter-python-logos.width-808.jpg) | 
|:--:| 
| *Pic credit https://www.twilio.com* |

Social media is full of bots today and twitter is one of the most bot friendly enviorment these days. In this article, we are building a bot to automate twitter tasks. This program can integrate with the Twitter platform, automatically posting, retweeting, liking, or following other users.


### How to make a Twitter bot

To create a Twitter bot we'll be using tweetpy. It manages the Twitter API calls and provides a simple interface to work with. We can post tweet, like tweets and do much more with just a few lines of code. We can follow the bellow checklist to create our own bot

#### Bot Checklist
    
 1. Make a task list for the bot
 2. Apply for a developer account & Create a Twitter app
 3. Authenticate
 4. Program the bot
 5. Deploy

### 1 Tasks for the bot

This is going to be a very simple bot, we are adding the bellow functionality for now. later we can add more depending on the need

* Tweet chuck norris joke once a week
* Retweet posts if it contains a specific # tag
* Like tweets if it contains a specific # tag

### 2. Apply for a developer account

First step is to get the credential from twitter.com, we can use this link https://developer.twitter.com/apps to fill-in some basic details and create an app. Once done we can access Consumer Key (API Key) and the Consumer Secret (API Secret), both available from the Keys and Access Tokens which will be used to authenticate tweetpy session.


### 3. Authenticate

This step involves little bit of coding. Once we have applied for a developer account and create a twitter app. we can obtain the Consumer key, Consumer secret, Access token and Access token secret from the **Keys and tokens** tab.

The code bellow will authenticate the API so that we can use the functionality. I am reading creadictials from a json file and using the credintials to authenticate the session but we can also save the credential in a form or string directly as mentioned on code comment


```
import json 
import tweepy # !pip install tweepy
import requests # !pip install requests
from datetime import datetime as dt

## Reading creadictials from a json file
with open("localconfig.json", 'r') as config_file:
    config = json.load(config_file)
creds = config[0]['twitter']

## Saving credentials to a variable
consumer_key = creds['consumer_key']                    # or "your key xxxxxxxxxxxxx"
consumer_secret = creds['consumer_secret']              # or "your key xxxxxxxxxxxxx"
access_token = creds['access_token']                    # or "your key xxxxxxxxxxxxx"
access_token_secret = creds['access_token_secret']      # or " your key xxxxxxxxxxxxx"

## Authenticating
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

user = api.me()
print("Connected user {}".format(user.name)) ## Printing authentication status
```

    Connected user Naveen singh


### 4. Program the bot

Now that we have all the credentials needed and our api is authenticated, we can write small functions to do a pirticular task. We can consolidate these functions to make our final bot

##### A function that takes text as input and tweets it 


```
## Updating status update 
def update_status(text):
    try:
        api.update_status(text)
        print("Status updated sucessfully")
    except Exception as e:
        print("Error in update_status", str(e))
        
update_status("Hi, this is just a msg to test twitter bot")
```

##### A Function that takes search query string as input searches for tweets with given query string and retweets it


```
## Like a post and retweet
def retweet_post(self, query):
    try:
        for tweet in tweepy.Cursor(self.api.search, q=query, rpp=100).items(10):
            tweet.retweet()
        print("Liked and favorated {}".tweet.text)
    except Exception as e:
        print("Error in like_and_retweet")

retweet_post("#100daysofcode")
```

##### A Function that takes search query string as input searches for tweets with given query string and likes it


```
## Like a post and retweet
def like_tweet(self, query):
    try:
        for tweet in tweepy.Cursor(self.api.search, q=query, rpp=100).items(10):
            tweet.favorite()
        print("Liked and favorated {}".tweet.text)
    except Exception as e:
        print("Error in like_and_retweet")

like_tweet("#100daysofcode")
```

Three basic functions are enough for now we can add more if required. I personally use only these 3 features most frequently but there is a lot we can do. A detailed documentation is available [here](http://docs.tweepy.org/en/v3.5.0/)

### 5. Full code Deployement

Now we have understanding of the basing freatures, we can use this to create a program that can perform some scheduled tasks at a given time. This bot is going to perform the bellow tasks

* Post one chuck norris joke every saturday
* Retweet and like 10 posts every sunday
* Save the log of all activity in a json file

We are going to use python schedule library for scheduling its a fairly simple library and makes it really easier to schedule tasks, for deployement I'll be using https://pythonanywhere.com because it has a free plan and can be accessed from anywhere.


```
import tweepy
import requests

class TwitterAPI:
    
    def __init__(self):
        
        with open("localconfig.json", 'r') as config_file:
            config = json.load(config_file)
        creds = config[0]['twitter']
        
        consumer_key = creds['consumer_key']
        consumer_secret = creds['consumer_secret']
        access_token = creds['access_token']
        access_token_secret = creds['access_token_secret']
        
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        
        user = self.api.me()
        print("Connected user {}".format(user.name))
        
    def get_chuck_joke(self):
        """ This function fetches a chuck norris joke from the internet """
        url = "http://api.icndb.com/jokes/random"
        jres = requests.get(url).json()
        return jres['value']['joke']

    def write_log(self, payload):
        """Creates a log of all the actions performed by the bot """
        try:
            with open("log.json", 'r') as log_file:
                data = json.load(log_file)
                data.append(payload[0])

            print("Saving logs")
            with open("log.json", 'w') as log_file:
                json.dump(data, log_file)

        except FileNotFoundError:
            print("Log file not found, writing new log")
            with open("log.json", 'w') as log_file:
                json.dump(payload, log_file)

    def like_and_retweet(self, query):
        try:
            with open("log.json", 'r') as log_file:
                data = json.load(log_file)
            last_id = max([i['id'] for i in data])
            for tweet in tweepy.Cursor(self.api.search, q=query, since_id=last_id).items():
                try:
                    tweet.retweet()
                    tweet.favorite()
                    print("Retweeted {} ".format(tweet.text))

                    ## Saving logs
                    tweet_id = tweet.id
                    text = tweet.text
                    payload = {
                        "id": tweet_id,
                        "type":"retweet",
                        "text":text,
                        "addedon": int(dt.strftime(dt.now(),"%s"))
                    }
                    write_log([payload])
                except Exception as e:
                    print(e)
                    continue
        except FileNotFoundError:
            for tweet in tweepy.Cursor(self.api.search, q=query, rpp=100).items(10):
                try:
                    tweet.retweet()
                    tweet.favorite()
                    print("Retweeted {} ".format(tweet.text))

                    ## Saving logs
                    tweet_id = tweet.id
                    text = tweet.text
                    payload = {
                        "id": tweet_id,
                        "type":"retweet",
                        "text":text,
                        "addedon": int(dt.strftime(dt.now(),"%s"))
                    }
                    write_log([payload])
                except TweepError as e:
                    print(e)
                    continue

    def update_status(self):
        """ This function tweets using the tweetpy API """
        try:
            joke = self.get_chuck_joke()
            joke = joke + " #TweetByBot"
            self.api.update_status(joke)
            with open("log.json", 'r') as log_file:
                data = json.load(log_file)
            tweet_id = [i for i in data if i['type'] == 'status_update']
            print(tweet_id)
            payload = {
                "id": len(tweet_id)+1,
                "type":"status_update",
                "text":text,
                "addedon": int(dt.strftime(dt.now(),"%s"))
            }
            write_log([payload])
        except Exception as e:
            print("Error in update_status", str(e))


import schedule # !pip install schedule
import time

twitter_api = TwitterAPI()    
schedule.every().saturday.do(twitter_api.update_status)
schedule.every().sunday.do(twitter_api.like_and_retweet, "#100DaysOfMLCode")

while True:
    schedule.run_pending()
    time.sleep(1)
```

    Connected user Naveen singh
    Updating status
    Tornados occur when Chuck Norris sneezes.#TweetByBot
    Retwitting called


### Final Notes: 
We now have a working Twitter bot. We only have some basic features for now but we can add more features based on the requirements. We can also built some use cases to solve a specific need or do some basic ML tasks like sentiment analysis and other kind of text analysis. Full code repo is available on github. Feel free to check other sections and blog posts and leave a comment for any question or suggestion 


```

```
