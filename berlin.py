from collections import defaultdict
import webbrowser
import time
import random
import sys

from robobrowser import RoboBrowser
from fake_useragent import UserAgent


class BurgyBrowser(RoboBrowser):
    ua = UserAgent(cache=False)
    requests = 0

    def open(self, *args, **kwargs):
        time.sleep(random.uniform(0.5, 1.5))
        self.session.headers['User-Agent'] = self.ua.random
        if self.requests:
            sys.stdout.write("#")
            sys.stdout.flush()
        super(BurgyBrowser, self).open(*args, **kwargs)
        self.requests += 1

SERVICE_NAME = 'anmeldung'

START_URL = 'https://service.berlin.de'

browser = BurgyBrowser(parser="html.parser")

browser.open('{}{}'.format(START_URL, '/standorte/buergeraemter/'))

print('Select a Bürgeramt area corresponding number:\n')

area_list = []
burgers = defaultdict(list)
for i, z in enumerate(browser.find_all('div', 'ort-group')):
    zone = z.find('h2')
    zone.find('a').clear()
    area_list.append(zone.text.strip())
    print("{}: {}".format(str(i).zfill(2), zone.text))
    for b in z.find_all("li", "topic-dls", "row-fluid"):
        burgers[i].append(b.find('a'))

n = int(input('--> '))

area = area_list[n]
print('Inspecting "{}"...'.format(area))

services_pages = []
for burgy in burgers[n]:
    url = '{}{}'.format(START_URL, burgy.get('href'))
    browser.open(url)
    services = browser.find_all('div', 'block termin')[0].find_all('a')
    services_pages += [s.get('href') for s in services if SERVICE_NAME in s.text.lower()]

reservation_pages = []
for p in services_pages:
    url = '{}{}'.format(START_URL, p)
    browser.open(url)
    reservation = [a.get('href') for a in browser.find_all('a', 'btn') if a.text == 'Termin hier buchen']
    reservation_pages += reservation

slots = []
for url in reservation_pages:
    browser.open(url)
    base_url = url.rsplit('/', 1)[0]
    for n in browser.find_all('th', 'next'):
        for a in n.find_all('a'):
            u = base_url + '/' + a.get('href')
            browser.open(u)
            slot = [base_url + '/' + a.get('href') for a in browser.find_all('a', 'tagesauswahl')]
            slots += slot

l_slots = len(slots)
if l_slots > 1:
    webbrowser.open_new(slots[0])
    for s in slots[1:]:
        webbrowser.open_new_tab(s)
elif l_slots == 1:
    webbrowser.open_new(slots[0])
else:
    print('\nNo dates in "{}", try another Bürgeramt area.'.format(area))
