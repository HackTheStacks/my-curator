import flask
from flask import Flask
from flask.ext.heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy
from model import (
    get_one,
    Configuration,
    production_session,
    DisplayItem
)

class Conf(object):
    def __init__(self):
        Configuration.load()
        self.db = production_session()

Conf = Conf()

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'
heroku = Heroku(app)

app = Flask(__name__)

if __name__ == "__main__":
    app.run()

@app.route('/display_items', methods=['GET'])
def all_display_items():
    return flask.jsonify(**DisplayItem.all(Conf.db))

@app.route('/display_item/<major>/<minor>', methods=['GET'])
def get_collection(major, minor):
    item = get_one(
        Conf.db, DisplayItem,
        beacon_major_id=int(major), beacon_minor_id=int(minor)
    )
    return flask.jsonify(**item.json)
