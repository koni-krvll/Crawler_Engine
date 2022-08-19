import sys
from os import path
if __name__ == '__main__':
    sys.path.insert(1, path.abspath('./lib'))

from parasytes.spy import getSpy
from time import sleep
from parsers.nextApolloParser import parsePageIntoJson

SLEEP_SECONDS = 5

def filterClubs(club):
    """
    Filter objects that are not clubs
    """
    return club.get('contentUrl', '').startswith('/clubs/')

def filterClub(club, id):
    """
    Filter objects that are not the club passed by id
    """
    return club.get('id', '') == id

def filterEvents(event):
    return event.get('__typename', '') == 'Event'

def filterEvent(event):
    return event.get('__typename', '') == 'Event' or event.get('__typename', '') == 'EventImage'

def getClubs():
    """
    Gets all clubs from ra.co in berlin
    """
    spy = getSpy()
    spy.get('https://ra.co/clubs/de/berlin?status=open')
    sleep(SLEEP_SECONDS)
    return list(filter(filterClubs, list(parsePageIntoJson(spy.page_source))))


def getClub(id):
    """
    Gets a club from ra.co by id
    """
    spy = getSpy()
    spy.get(f'https://ra.co/clubs/{id}')
    sleep(SLEEP_SECONDS)
    values = parsePageIntoJson(spy.page_source)
    return list(filter(lambda club: filterClub(club, id), values))[0]

def getEvents():
    spy = getSpy()
    spy.get(f'https://ra.co/events/de/berlin')
    sleep(SLEEP_SECONDS)
    return list(filter(filterEvents, parsePageIntoJson(spy.page_source)))

def getEvent(id):
    spy = getSpy()
    spy.get(f'https://ra.co/events/{id}')
    sleep(SLEEP_SECONDS)
    events = list(filter(filterEvent, parsePageIntoJson(spy.page_source)))
    event = next(e for e in events if e.get('__typename', '') == 'Event')
    event['images'] = []
    for e in events:
        if e.get('__typename', '') == 'EventImage':
            event['images'].append(e.get('filename', 'null'))
    return event

if __name__ == '__main__':
    import json
    json.dump(getEvent(getEvents()[1]['id']), open('events.json', 'w'), indent=2)