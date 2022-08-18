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



if __name__ == '__main__':
    clubs = getClubs()
    club = getClub(clubs[0]['id'])
    print(club)
