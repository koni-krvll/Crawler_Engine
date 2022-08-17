from flask import Flask, request, abort
from dotenv import load_dotenv
from os import getenv
from parasytes.filter import getClubs

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
    return getClubs()


@application.route('/<id>', methods=['GET'])
def get(id):
    return list(filter((lambda club: club['id'] == id), getClubs()))


@application.route('/events', methods=['GET'])
def events():
    return 'Get events!'


@application.route('/events/<id>', methods=['GET'])
def get_event(id):
    return f'Get event!{id}'


if __name__ == '__main__':
    application.run()
