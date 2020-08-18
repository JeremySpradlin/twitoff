
"""SQLAlchemy models and utility functions for TwitOff."""
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    """Twitter users corresponding to Tweets."""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)
    # Tweet IDs are ordinal ints, so can be used to fetch only more recent
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return '-User {}-'.format(self.name)


class Tweet(DB.Model):
    """Tweet text and data."""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))  # Allows for text + links
    embedding = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '-Tweet {}-'.format(self.text)


# Commented out old methods for new api usage
# Equivlanet methods are now located in twitter.py
# def insert_example_users():
#     """Example data to play with."""
#     austen = User(id=1, name='austen')
#     elon = User(id=2, name='elonmusk')
#     jeremy = User(id=3, name='JeremySpradlin')
#
#     DB.session.add(austen)
#     DB.session.add(elon)
#     DB.session.add(jeremy)
#     DB.session.commit()
#
#
# def insert_example_tweets():
#     """ Example tweets to play with"""
#     t1 = Tweet(id=1, text='This is a tweet', user_id=3)
#     t2 = Tweet(id=2, text='This is another tweet!', user_id=2)
#     t3 = Tweet(id=3, text='THESE ARE ALL TWEETS!!!', user_id=1)
#     t4 = Tweet(id=4, text='MOAR TWEETS!!!!', user_id=3)
#     t5 = Tweet(id=5, text='Dr Rollergator For Prez!', user_id=3)
#     t6 = Tweet(id=6, text='Im just Elon Musk with Tusks', user_id=2)
#     DB.session.add(t1)
#     DB.session.add(t2)
#     DB.session.add(t3)
#     DB.session.add(t4)
#     DB.session.add(t5)
#     DB.session.add(t6)
#     DB.session.commit()
