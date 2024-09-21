import requests
from bs4 import BeautifulSoup
import re

page_url = "https://en.wikipedia.org/wiki/Kevin_McCarthy"

response = requests.get(page_url)


soup = BeautifulSoup(response.content, 'html.parser')



def get_politician_data(page_url):
    response = requests.get(page_url)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    infobox = soup.find('table', {'class': 'infobox'})
    if not infobox:
        return None
    for row in infobox.find_all('tr'):
        header = row.find('th')
        if header and 'Born' in header.text:
            bday = row.find('span', {'class': 'bday'}).text.strip()
            print(bday)
            # return party

        if header and 'Political party' in header.text:
            party = row.find('td').text.strip()
            return party
    return None



a = get_politician_data(page_url)
print(a)