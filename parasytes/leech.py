from multiprocessing import Pool, cpu_count
from typing import final
from ra import getClubs, getClub
from maps import getPlace
import json


def cleanClub(club):
    finalClub = {}
    result = club['result']
    finalClub['id'] = club['url'].split('/')[-1]
    finalClub['address'] = club['address']['streetAddress']
    finalClub['region'] = club['address']['addressRegion']
    finalClub['country'] = club['address']['addressCountry']
    finalClub['name'] = club['name']
    finalClub['description'] = club['description']
    finalClub['eventsSoFar'] = club.get('eventsSoFar', None)
    finalClub['capacity'] = club.get('maximumAttendeeCapacity', None)
    finalClub['artists'] = club['artists']
    finalClub['placeId'] = result['place_id']
    finalClub['lat'] = result['geometry']['location']['lat']
    finalClub['lng'] = result['geometry']['location']['lng']
    finalClub['types'] = result['types']
    finalClub['businessStatus'] = result.get('business_status', None)
    finalClub['openingHours'] = result.get('opening_hours', None)
    finalClub['priceLevel'] = result.get('price_level', None)
    finalClub['rating'] = result.get('rating', None)
    finalClub['ratingCount'] = result.get('user_ratings_total', None)
    finalClub['vicinity'] = result.get('vicinity', None)
    finalClub['website'] = result.get('website', None)
    finalClub['logo'] = club.get('logo', club.get(
        'logoUrl', result.get('icon', None)))
    finalClub['image'] = club.get('image', [None])[0]
    return finalClub


def updateClub(club):
    try:
        print(f'Updating {club["name"]}')
        club.update(getClub(club['id']))
        club.update(getPlace(f"{club['name']} Club Berlin"))
        club = cleanClub(club)
        print(f'Updated {club["name"]}')
    except Exception as e:
        print(f'Failed to update {club["name"]}', e)
    return club


def getMixedClubs():
    clubs = getClubs()
    with Pool(cpu_count()-1) as p:
        parsed_clubs = p.map(updateClub, clubs)
    return parsed_clubs


if __name__ == '__main__':
    json.dump(getMixedClubs(), open('clubs.json', 'w'))
