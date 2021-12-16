import argparse
import os.path as osp
from pathlib import Path
import json
import csv
import tweepy as tw
from time import sleep

parent_dir = Path(__file__).parent.resolve()

keywords = ['covid', 'covid19', 'coronavirus', 'vaccine', 'vaccination', 'vaccinated',
            'antivax', 'vaxer', 'vaxxer', 'antivaxer', 'antivaxxer', 'antivaxxers', 'antivaxers', 'vaxxed',
            'vaxed', 'pfizer', 'moderna', 'astrazeneca']

def initialize():
    with open(osp.join(parent_dir, '..', 'config.json')) as f:
        tokens = json.load(f)
    auth = tw.OAuthHandler(tokens['consumer_key'], tokens['consumer_secret'])
    auth.set_access_token(tokens['access_token'], tokens['access_token_secret'])
    return tw.API(auth, wait_on_rate_limit=True)

def meets_conditions(tweet):
    if tweet.in_reply_to_status_id is None and not hasattr(tweet, 'retweeted_status'): #tweet.user.location != ""
        return True

def fetch_tweets(api, output, num_tweets):
    words = ' OR '.join(keywords) + ' OR ' + ' OR #'.join(keywords)
    tweet_list = []
    tweet_count = 0
    with open(osp.join(parent_dir, '..', 'data', output+'.csv'), 'w', encoding='utf-8', newline='') as c:#, open(osp.join(parent_dir, '..', 'json', output+'.json'), 'w') as j:
        while tweet_count < num_tweets:
            tweets = api.search_tweets(words, lang='en', result_type='recent', count=num_tweets, tweet_mode='extended')
            csvw = csv.writer(c, delimiter=';', quoting=csv.QUOTE_ALL)
            for tweet in tweets:
                if meets_conditions(tweet):
                    tweet_row = [tweet.created_at, tweet.user.location, tweet.full_text.replace('\n','\t').replace('\r','\t')]
                    if tweet_row not in tweet_list:
                        tweet_list.append(tweet_row)
                        csvw.writerow(tweet_row)
                        #json.dump(tweet._json, j, indent = 4)
                        tweet_count += 1
                        print(tweet_count)
            print('sleeping')
            sleep(1.5)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output', help='name of CSV output file (do not include file extension)')
    parser.add_argument('-n', '--num_tweets', default=1000, help='number of tweets to fetch (default: 1000)')
    args = parser.parse_args()

    api = initialize()
    fetch_tweets(api, args.output, args.num_tweets)

if __name__ == '__main__':
    main()
