#! /usr/bin/env python
"""Goes to met.ie and finds the weather forecasts"""
import sys
a = sys.argv
a.append('')
argsList = ['today', 'tonight', 'tomorrow']
if len(a) < 1 or a[1] not in argsList:
        print ('Usage: %s %s' % (a[0].split('/')[-1], '|'.join(argsList)))
else:
        import bs4, urllib
        soup = bs4.BeautifulSoup(urllib.urlopen('http://www.met.ie/forecasts').read())
        forecasts = soup.find_all('span', class_='daybox')
        if a[1] == 'today':
                today = forecasts[0].find_next().string
                   print (today)
        elif a[1] == 'tonight':
                tonight = forecasts[1].next_sibling.next_sibling.next_sibling.string.rstrip()
                print (tonight)
        elif a[1] == 'tomorrow':
                tomorrow = forecasts[2].next_sibling.next_sibling.next_sibling.string.strip()
                print (tomorrow)