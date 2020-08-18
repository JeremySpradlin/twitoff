"""Retrieve Tweets, embeddings, and persist in the database."""
from os import getenv
import basilica
import tweepy
from models import DB, Tweet, User


TWITTER_USERS = ['calebhicks', 'elonmusk', 'rrherr', 'SteveMartinToGo',
                 'alyankovic', 'nasa', 'sadserver', 'jkhowland', 'austen',
                 'common_squirrel', 'KenJennings', 'conanobrien',
                 'big_ben_clock', 'IAM_SHAKESPEARE']

TWITTER_API_KEY = getenv('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = getenv('TWITTER_API_KEY_SECRET')
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)
print(TWITTER)
BASILICA = basilica.Connection(getenv('BASILICA_KEY'))


def add_or_update_user(username):
    """Add or update a user and their Tweets, error if not a Twitter user."""
    try:
        print(TWITTER_API_KEY)
        print('entering try block')
        twitter_user = TWITTER.get_user(username)
        print('got twitter user name')
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id, name=username))
        print('created db_user')
        DB.session.add(db_user)
        print('added db_user to session')
        # Lets get the tweets - focusing on primary (not retweet/reply)
        # tweets = twitter_user.timeline(
        #     count=200, exclude_replies=True, include_rts=False,
        #     tweet_mode='extended', since_id=db_user.newest_tweet_id
        # )
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False,
            tweet_mode='extended'
        )
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            embedding = BASILICA.embed_sentence(tweet.full_text,
                                                model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:300],
                             embedding=embedding)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e
    else:
        DB.session.commit()


def insert_example_users():
    """Example data to play with."""
    add_or_update_user('austen')
    add_or_update_user('elonmusk')
