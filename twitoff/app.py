"""
Main app/routing file for TwitOff
"""


# IMPORTS
from flask import Flask, render_template
from .models import DB, User, insert_example_users


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
                               users=User.query.all())

    @app.route('/update')
    def update():
        # Reset the database
        DB.drop_all()
        DB.create_all()
        insert_example_users()
        return render_template('base.html', title='Users Updated',
                               users=User.query.all())

    return app
