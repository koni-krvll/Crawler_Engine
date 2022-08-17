from os import getenv
from os import getenv
from unittest import result
from dotenv import load_dotenv
from googlemaps import Client

load_dotenv()

gmaps = Client(key=getenv("MAPS_API"), queries_per_second=32)


def getPlace(query):
    result = gmaps.find_place(
        input=query,
        input_type="textquery",
        location_bias='circle:20000@52.5200,13.4050'
    )
    print(f'Maps found {result} results for {query}')
    results = result['candidates']
    place = results[0]
    return getPlaceId(place['place_id'])


def getPlaceId(id):
    return gmaps.place(place_id=id)


if __name__ == "__main__":
    print(getPlace(query="Berghain Club Berlin"))
