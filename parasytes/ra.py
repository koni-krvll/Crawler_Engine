from spy import getSpy
import json
import re
from time import sleep

SLEEP_SECONDS = 5


def getClubs():
    spy = getSpy()
    spy.get('https://ra.co/clubs/de/berlin?status=open')
    sleep(SLEEP_SECONDS)
    source = spy.page_source
    parsed = re.findall(r'"Venue:[0-9]*":.*}', source)[0]
    parsed = parsed.split(',"apolloClient":null}')[0]
    parsed = '{"' + parsed[1:-1] + '}'
    spy.close()
    return list(dict.values(json.loads(parsed)))


def getClub(id):
    spy = getSpy()
    spy.get(f'https://ra.co/clubs/{id}')
    sleep(SLEEP_SECONDS)
    source = spy.page_source
    narrow = source.split('<script type="application/ld+json">')[2]
    narrow = narrow.split('</script>')[0]
    object = json.loads(narrow)

    try:
        events_sofar = source.split('Events so far this year')[1]
        events_sofar = events_sofar.split('</span>')[1]
        events_sofar = events_sofar.split('>')[2]
        events_sofar = int(events_sofar)
        object['eventsSoFar'] = events_sofar
    except:
        print('No events found', id)

    artists = []

    try:
        artist_narrow = source.split('Most listed artists')[1]
        artist_narrow = artist_narrow.split('≯</span>')[0]
        for line in artist_narrow.split('href='):
            if (line.find('font-weight') > 0):
                id = line.split(' ')[0].replace('"', '')
                id = id.split('/')[-1]
                name = line.split('>')[-3]
                name = name.split('<')[0]
                artists.append({'name': name, 'id': id})
        object['artists'] = artists
    except:
        print('No artists found', id)

    print('RA found', object['name'])

    spy.close()
    return object


if __name__ == '__main__':
    clubs = getClubs()
    print(getClub(clubs[0]['id']))
