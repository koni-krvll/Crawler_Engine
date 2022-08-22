from lib.parasytes.spy import getSpy
from lib.parsers.nextApolloParser import parsePageIntoJson, waitForNextData


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
    waitForNextData(spy)
    return list(filter(filterClubs, list(parsePageIntoJson(spy.page_source))))


def getClub(id):
    """
    Gets a club from ra.co by id
    """
    spy = getSpy()
    spy.get(f'https://ra.co/clubs/{id}')
    waitForNextData(spy)
    values = parsePageIntoJson(spy.page_source)
    return list(filter(lambda club: filterClub(club, id), values))[0]


def getEvents():
    spy = getSpy()
    spy.get(f'https://ra.co/events/de/berlin')
    waitForNextData(spy)
    return list(filter(filterEvents, parsePageIntoJson(spy.page_source)))


def getEvent(id):
    spy = getSpy()
    spy.get(f'https://ra.co/events/{id}')
    waitForNextData(spy)
    events = list(filter(filterEvent, parsePageIntoJson(spy.page_source)))
    event = next(e for e in events if e.get('__typename', '') == 'Event')
    event['images'] = []
    for e in events:
        if e.get('__typename', '') == 'EventImage':
            event['images'].append(e.get('filename', 'null'))
    return event
