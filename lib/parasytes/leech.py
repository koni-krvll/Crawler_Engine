from multiprocessing import Pool, cpu_count
from parasytes.ra import getClubs, getClub
from parasytes.maps import getPlace
import json

def cleanArtist(artist):
    artist.pop('__typename')
    return artist

def cleanClub(club):
    finalClub = {}
    result = club['result']
    finalClub['id'] = int(club.get('id', '0'))
    finalClub['name'] = club.get('name', 'null')
    finalClub['description'] = club.get('blurb', 'null')
    finalClub['address'] = club.get('address', 'null')
    finalClub['region'] = 'BE' # shouldn't hardcode this
    finalClub['country'] = 'DE' # same
    finalClub['eventsSoFar'] = int(club.get('eventCountThisYear', '0'))
    finalClub['capacity'] = int(club.get('capacity', '0'))
    finalClub['recommended'] = bool(club.get('raSays', 'false'))
    finalClub['closed'] = bool(club.get('isClosed', 'true'))
    finalClub['live'] = bool(club.get('live', 'false'))
    finalClub['artists'] = list(map(cleanArtist, club.get('artists', [])))
    finalClub['placeId'] = result.get('place_id', 'null')
    finalClub['lat'] = float(result['geometry']['location']['lat'])
    finalClub['lng'] = float(result['geometry']['location']['lng'])
    finalClub['status'] = result.get('business_status', 'null')
    finalClub['hours'] = result.get('opening_hours', {})
    finalClub['price'] = int(result.get('price_level', 0))
    finalClub['rating'] = float(result.get('rating', 0.0))
    finalClub['ratings'] = int(result.get('user_ratings_total', 0))
    finalClub['vicinity'] = result.get('vicinity', 'null')
    finalClub['website'] = club.get('website', result.get('website', 'null'))
    finalClub['logo'] = club.get('logoUrl', None)
    if finalClub['logo'] == None:
        finalClub['logo'] = result.get('icon', None)
    finalClub['image'] = club.get('photo', None)
    if finalClub['image'] == None:
        finalClub['image'] = 'https://maps.googleapis.com/maps/api/place/photo?photo_reference=' + result.get('photos', [{}])[0].get('photo_reference', 'NULL')
    finalClub['types'] = result.get('types', [])
    return finalClub

def getMixedClub(club):
    club = getClub(club['id'])
    try:
        club.update(getPlace(f"{club['name']} Club Berlin"))
    except:
        try:
            club.update(getPlace(f"{club['name']}"))
        except:
            return {}
    return cleanClub(club)


def getMixedClubs():
    clubs = getClubs()
    with Pool(cpu_count()-1) as pool:
        clubs = pool.map(getMixedClub, clubs)
    return clubs

if __name__ == '__main__':
    json.dump(getMixedClubs(), open('clubs.json', 'w'))
