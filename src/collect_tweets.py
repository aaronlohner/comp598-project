import argparse
import os.path as osp
from pathlib import Path
import requests
import json
import tweepy as tw


parent_dir = Path(__file__).parent.resolve()
consumer_key = None
consumer_secret = None
access_token = None
access_token_secret = None
bearer_token = None
auth = None
client = None


def initialize():
    global consumer_key, consumer_secret, access_token, access_token_secret, auth, bearer_token, client, api
    with open(osp.join(parent_dir, '..', 'keys.txt')) as f:
        consumer_key, consumer_secret, access_token, access_token_secret, bearer_token = f.read().splitlines()

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    #client = tw.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret, return_type=dict, wait_on_rate_limit=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')#, required=True)
    args = parser.parse_args()

if __name__ == '__main__':
    initialize()

    # assert not "retweeted"
    tweets = api.search_tweets('#covid', lang='en', result_type='popular', count=1001)
    for tweet in tweets:
        print(f'text: {tweet.text}, created: {tweet.created_at}')
    #print(api.reverse_geocode(56.448727, -102.745408, max_results = 5))
