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
