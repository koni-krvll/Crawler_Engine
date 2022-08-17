import json

MIN_EVENTS = 0
MIN_CAPACITY = 0
BUSINESS_STATUS = 'OPERATIONAL'


def filterClub(club):
    """
    if club.get('eventsSoFar', 0) < MIN_EVENTS:
        return
    if club.get('capacity', 0) < MIN_CAPACITY:
        return
    """
    if club.get('businessStatus', '') != BUSINESS_STATUS:
        return True


def getClubs():
    with open(__package__+'/clubs.json') as f:
        clubs = json.load(f)
    clubs = list(filter(filterClub, clubs))
    return clubs


if __name__ == '__main__':
    print(len(getClubs()))
