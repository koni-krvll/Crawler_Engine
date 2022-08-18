import json
import bs4

def parsePageIntoJson(rawPage):
    soup = bs4.BeautifulSoup(rawPage)
    next = soup.find('script', {'id': '__NEXT_DATA__'}).decode_contents()
    data = json.loads(next)['props']['apolloState']
    data = dict.values(data)
    return data