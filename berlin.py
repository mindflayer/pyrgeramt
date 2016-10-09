from collections import defaultdict
import webbrowser

from robobrowser import RoboBrowser

SERVICE_NAME = 'anmeldung'

START_URL = 'https://service.berlin.de'
FAKE_UA = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'

browser = RoboBrowser(parser="html.parser", user_agent=FAKE_UA)
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
    print('No dates in "{}", try another Bürgeramt area.'.format(area))
