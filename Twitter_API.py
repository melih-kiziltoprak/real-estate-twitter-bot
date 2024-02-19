import tweepy
from tweepy import API
import requests
import credentials
def get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret) -> tweepy.API:
    """Get twitter conn 1.1"""
    auth = tweepy.OAuth1UserHandler(api_key, api_secret)
    auth.set_access_token(
        access_token,
        access_token_secret,
    )
    return tweepy.API(auth)

def get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret) -> tweepy.Client:
    """Get twitter conn 2.0"""
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    return client

client_v1 = get_twitter_conn_v1(credentials.consumer_key, credentials.consumer_secret, credentials.access_token, credentials.access_token_secret)
client_v2 = get_twitter_conn_v2(credentials.consumer_key, credentials.consumer_secret, credentials.access_token, credentials.access_token_secret)

def send_tweet(tweet_text):
    photos = []
    for photo_index in range(1, 5):
        media = client_v1.media_upload(filename= ("downloaded_image_" + str(photo_index) + ".jpg") )
        photos.append(media.media_id)

    tweet_response = client_v2.create_tweet(text=tweet_text[:250], media_ids=photos)
    print(tweet_response)
    tweet_id = tweet_response.data['id']
    for i in range(1, int(len(tweet_text) / 250) + 1):
        reply_text = tweet_text[i*250 : (i+1)*250]
        if(i != int(len(tweet_text) / 250)):
            reply_text += " +++++"
        tweet_id = client_v2.create_tweet(
            text=reply_text,
            in_reply_to_tweet_id=tweet_id
        ).data['id']
