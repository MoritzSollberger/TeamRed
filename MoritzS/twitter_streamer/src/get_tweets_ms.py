import json
import tweepy
import time

KEYWORDS = ["puppies"]

consumer_key = 'zCFwJQI52I7pqzC3mRClCjY8U'
consumer_secret = 'l2Q07VDeCQfrf7M7InKqyYoXJ623a12yCvTSRUEE10vo6IG3Wd'
access_token = '2304999817-GlqxNQDeN9lPO1jPGliIza4yiLc2wyl7iRYwEQr'
access_token_secret = 'uziyEzKLn8z8fNhmfNFDtr6oJMaOAYb4tOVGG5bU8FTwf'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
user = api.me()


class StreamListener(tweepy.StreamListener):
    def __init__(self, limit, callback):
        super().__init__()
        self.limit = limit
        self.counter = 0
        self.callback = callback

    def on_error(self, status_code):
        '''stops stream when error 420 occurs'''
        if status_code == 420:
            return False

    def get_media(self, t):
        media_url = []
        if 'extended_tweet' in t and 'media' in t['extended_tweet']['entities']:
            for media in t['extended_tweet']['entities']['media']:
                media_url.append(media['media_url_https'])
                media_type = media['type']
        else:
            media_url = None
            media_type = ''
        return media_url, media_type

    def get_hashtags(self, t):
        hashtags = []
        if 'extended_tweet' in t:
            for hashtag in t['extended_tweet']['entities']['hashtags']:
                hashtags.append(hashtag['text'])
        elif 'hashtags' in t['entities'] and len(t['entities']['hashtags']) > 0:
            hashtags = [item['text'] for item in t['entities']['hashtags']]
        else:
            hashtags = []
        return hashtags

    def get_tweet_dict(self, t):
        '''extract information from the tweet'''
        if 'extended_tweet' in t:
            text = t['extended_tweet']['full_text']
        else:
            text = t['text']
        hashtags = self.get_hashtags(t)
        media_url, media_type = self.get_media(t)
        tweet = {'created_at': t['created_at'],
                 'id': t['id_str'],
                 'text': text,
                 'username': t['user']['screen_name'],
                 'followers':t['user']['followers_count'],
                 'user_favorites_count': t['user']['favourites_count'],
                 'retweets': t['retweet_count'],
                 'favorites': t['favorite_count'],
                 'hashtags': hashtags,
                 'media_url': media_url,
                 'media_type': media_type,
                 'interesting': 0}
        return tweet

    def on_data(self, data):
        '''collect, filter and parse the tweets from twitter API'''
        t = json.loads(data)
        if t['retweeted'] == False and 'RT' not in t['text'] and t['in_reply_to_status_id'] == None:
            tweet = self.get_tweet_dict(t)
            self.callback(tweet)
            self.counter += 1
            if self.counter == self.limit:
                return False


def get_tweets(limit, callback):
    stream_listener = StreamListener(limit, callback)
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=KEYWORDS, languages=['en'])

def show_text(tweet):
    print(tweet['text'])


if __name__ == '__main__':
    get_tweets(5, show_text)
