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
auth = None
api = None

def initialize():
    global consumer_key, consumer_secret, access_token, access_token_secret, auth, api
    with open(osp.join(parent_dir, '..', 'keys.txt')) as f:
        consumer_key, consumer_secret, access_token, access_token_secret, _ = f.read().splitlines()

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')#, required=True)
    args = parser.parse_args()

    headers = {'User-Agent':'windows:university.project.app:v1.0'}
    payload = {}

    fetch_and_dump(payload, headers, args.subreddit, args.output)

if __name__ == '__main__':
    initialize()
    # date_since = '2021-11-18'
    # for tweet in api.search_tweets(q='#covid',
    #           lang="en").items(5):
    #     print(tweet.text)
