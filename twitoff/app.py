"""
Main app/routing file for TwitOff
"""


# IMPORTS
from flask import Flask, render_template
from models import DB, User, Tweet
from twitter import insert_example_users


def create_app():
    """
    Create and configure an instance of the flask application
    :return:
    Returns the app
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    # ... TODO Make the app!
    @app.route('/')
    def root():
        return render_template('base.html', title='Home',
                               users=User.query.all(), tweets=Tweet.query.all())

    @app.route('/update')
    def update():
        # Insert example users
        print('before method')
        insert_example_users()
        print('after method')
        # insert_example_tweets() #Commented out old functionality
        return render_template('base.html', title='Users Updated',
                               users=User.query.all(), tweets=Tweet.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset Database!',
                               users=User.query.all())

    @app.route('/user/<int:user_id>')
    def displayUser(user_id):
        user = User.query.filter_by(id=user_id)
        return render_template('user.html', title='User', user=user)

    @app.route('/user/<user_name>')
    def displayUserName(user_name):
        user = User.query.filter_by(name=user_name)
        #tweets = Tweet.query.filter_by(user=user)
        #return render_template('user.html', title='User', user=user, tweets=tweets)
        return render_template('user.html', title='User', user=user)

    return app
