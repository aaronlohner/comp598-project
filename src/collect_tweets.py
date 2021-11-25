import argparse
import os.path as osp
from pathlib import Path
import json
import csv
import tweepy as tw
from time import sleep


parent_dir = Path(__file__).parent.resolve()
consumer_key = None
consumer_secret = None
access_token = None
access_token_secret = None
bearer_token = None
auth = None
client = None
keywords = ['covid', 'vaccine', 'vaccination', 'vaccinated', 'pfizer', 'moderna', 'astrazeneca']


def initialize():
    global consumer_key, consumer_secret, access_token, access_token_secret, auth, bearer_token, client, api
    with open(osp.join(parent_dir, '..', 'keys.txt')) as f:
        consumer_key, consumer_secret, access_token, access_token_secret, bearer_token = f.read().splitlines()

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    #client = tw.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret, wait_on_rate_limit=True)


def meets_conditions(tweet):
    if tweet.in_reply_to_status_id is None: #tweet.user.location != "" and not hasattr(tweet, 'retweeted_status') and
        return True

def fetch_tweets(output, num_tweets):
    words = ' OR '.join(keywords) + ' OR ' + ' OR #'.join(keywords)
    tweet_list = []
    with open('tweets1.csv', newline='', encoding='utf-8') as f:
        csvr = csv.reader(f, delimiter=';')
        [tweet_list.append(row) for row in csvr]
    tweet_count = 0
    with open(output, 'w', encoding='utf-8', newline='') as c, open(output+'.json', 'w') as j:#, open(output+'.txt', 'w', encoding='utf-8') as t:
        while tweet_count < 2000:
            tweets = api.search_tweets(words, lang='en', result_type='mixed', count=num_tweets, tweet_mode='extended')
            #tweets = client.search_recent_tweets(query='covid lang:en', max_results=10, expansions = ["author_id"])
            csvw = csv.writer(c, delimiter=';', quoting=csv.QUOTE_ALL)
            for tweet in tweets:
                if meets_conditions(tweet):
                    tweet_row = [tweet.created_at, tweet.user.location, tweet.full_text.replace('\n','\t').replace('\r','\t')]
                    if tweet_row not in tweet_list:
                        tweet_list.append(tweet_row)
                        csvw.writerow(tweet_row)
                        #print(f"text: {tweet.full_text}")
                        #t.write(str(tweet))
                        #print(f'time_zone: {tweet.user.time_zone}, utc_offset: {tweet.user.utc_offset}, place: {tweet.place}, loc: {tweet.user.location}')
                        json.dump(tweet._json, j, indent = 4)
                        tweet_count += 1
                        print(tweet_count)
            print('sleeping')
            sleep(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num_tweets', default=1000)
    parser.add_argument('-o', '--output', required=True)
    args = parser.parse_args()

    initialize()
    fetch_tweets(args.output, args.num_tweets)

if __name__ == '__main__':
    main()
