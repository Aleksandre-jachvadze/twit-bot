"""
Twitter Bot Python Script
Author: Aleksandre Jachvadze
Date: 2025-09-24
Description: Fully functional Twitter bot using Tweepy 4.x
"""

__author__ = "Aleksandre Jachvadze"

import tweepy
import pandas as pd

# ================== Twitter API Keys ==================
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"
bearer_token = "YOUR_BEARER_TOKEN"  # Required for StreamingClient

# ================== Authenticate ==================
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)
api = tweepy.API(auth, wait_on_rate_limit=True)

# ================== Profile Functions ==================
def update_profile(name=None, url=None, location=None, description=None, profile_image_path=None):
    if name or url or location or description:
        api.update_profile(name=name, url=url, location=location, description=description)
    if profile_image_path:
        api.update_profile_image(profile_image_path)

# ================== Tweet Functions ==================
def post_tweet(text):
    api.update_status(text)

def post_tweet_with_media(text, filename):
    media = api.media_upload(filename)
    api.update_status(text, media_ids=[media.media_id_string])

def reply_tweet(tweet_id, text):
    tweet = api.get_status(tweet_id)
    username = tweet.user.screen_name
    api.update_status(f"@{username} {text}", in_reply_to_status_id=tweet_id)

def retweet(tweet_id):
    api.retweet(tweet_id)

def unretweet(tweet_id):
    api.unretweet(tweet_id)

def favorite(tweet_id):
    api.create_favorite(tweet_id)

def unfavorite(tweet_id):
    api.destroy_favorite(tweet_id)

# ================== User Data ==================
def user_timeline_keywords(username, keyword="tesla", limit=150):
    tweets = []
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode="extended").items(limit):
        if keyword.lower() in tweet.full_text.lower():
            tweets.append(tweet.full_text)
    return tweets

def get_followers_ids(username):
    return [fid for fid in tweepy.Cursor(api.get_follower_ids, screen_name=username).items()]

def get_friends_ids(username):
    return [fid for fid in tweepy.Cursor(api.get_friend_ids, screen_name=username).items()]

# ================== Trends ==================
def extract_trends(woeid=1, threshold=10000):
    all_trends = api.get_place_trends(woeid)
    trends_list = []
    for t in all_trends[0]['trends']:
        if t['tweet_volume'] and t['tweet_volume'] > threshold:
            trends_list.append((t['name'], t['tweet_volume']))
    df = pd.DataFrame(trends_list, columns=["Trend", "Volume"]).sort_values(by="Volume", ascending=False)
    return df

# ================== Streaming ==================
class MyStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(f"New tweet: {tweet.text}")

def start_stream(keywords_list):
    stream = MyStream(bearer_token)
    for kw in keywords_list:
        stream.add_rules(tweepy.StreamRule(kw))
    stream.filter()

# ================== Example Usage ==================
if __name__ == "__main__":
    print(f"Script written by {__author__}")
    
    # Tweet something
    # post_tweet("Hello from my Python bot 🚀")
    
    # Get tweets containing keyword
    tweets = user_timeline_keywords("elonmusk", keyword="tesla")
    print("Latest Tesla Tweets:", tweets[:5])
    
    # Extract trends with volume > 10000
    print("Top Trends:\n", extract_trends(woeid=1, threshold=10000))
    
    # Start streaming tweets with keywords
    # start_stream(["tesla", "spacex"])
