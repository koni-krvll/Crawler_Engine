from lib.parasytes.leech import getMixedClub, getMixedClubs, getEvent, getEvents
from lib.parasytes.maps import getPopularTimes
from flask import Flask, request, abort
from dotenv import load_dotenv
from os import getenv, path
import sys
sys.path.insert(1, path.abspath('./lib'))



load_dotenv()
KEY = getenv('KEY')
if not KEY:
    raise Exception('No KEY set')


application = Flask(__name__)


@application.before_request
def hook():
    key = request.headers.get('Authorization').split(' ')[1]
    if key != KEY:
        abort(401)


@application.route('/all', methods=['GET'])
def index():
    return getMixedClubs()


@application.route('/<id>', methods=['GET'])
def get(id):
    return getMixedClub({'id': id})


@application.route('/popular/<id>', methods=['GET'])
def get_popular(id):
    try:
        return getPopularTimes(id)
    except:
        return {}


@application.route('/events', methods=['GET'])
def events():
    return getEvents()


@application.route('/events/<id>', methods=['GET'])
def get_event(id):
    return getEvent(id)


if __name__ == '__main__':
    application.run()
