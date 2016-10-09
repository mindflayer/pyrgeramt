from collections import defaultdict
import webbrowser
import time
import random
import sys
import argparse


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

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--service", help="Which service are you going to book (e.g.: anmeldung)?", default=None)
args = parser.parse_args()

if not args.service:
    parser.print_help()
    sys.exit()

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
    services_pages += [s.get('href') for s in services if args.service in s.text.lower()]

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
if l_slots:
    input("\n--- Press ENTER and watch the first page I'm opening to solve the CAPTCHA (if it's there). ---")
    webbrowser.open_new(slots[0])
    input("--- Press ENTER when solved, or CTRL-C to finish, if you've already booked a reservation. ---")
    for s in slots:
        webbrowser.open_new_tab(s)
else:
    print('\nNo dates in "{}", try another Bürgeramt area.'.format(area))
