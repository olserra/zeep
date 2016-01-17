# coding=utf-8
import re
import sys
import logging
import requests
import urllib
import unidecode
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from django.contrib.gis.geos import GEOSGeometry

from models import House

# TODO: move to settings?
BEWRD_URL = 'http://www.funda.nl/mijn/bewaard/'
LOGIN_URL = 'https://www.funda.nl/mijn/login'
USER = ''
PASSWD = ''
GEOCODE_URL = 'https://geodata.nationaalgeoregister.nl/geocoder/Geocoder?zoekterm='


# To make sure you're seeing all debug output:
logger = logging.getLogger("mechanize")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)


def pagination():
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'})
    tokenRequest = session.get('https://www.funda.nl/mijn/login/')

    request_validation_re = re.compile(r'<input name="__RequestVerificationToken" type="hidden" value="(.*?)" />')
    tokens = request_validation_re.findall(tokenRequest.text)

    sessionCookies = tokenRequest.cookies

    payload = {
        '__RequestVerificationToken': tokens[0],
        'Username': PASSWD,
        'Password': USER,
        'RememberMe': 'false'
    }

    raw = urllib.urlencode(payload)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    session.post('https://www.funda.nl/mijn/login/', data=raw, cookies=sessionCookies, headers=headers)

    links = list()
    resp = session.get(BEWRD_URL + 'p1')
    soup = BeautifulSoup(resp.text)

    pagelinks = soup.find_all("a", attrs={"data-pagination-pagelink":True})
    pages = []
    for page in pagelinks:
        pages.append(int(page["data-pagination-pagelink"]))
    einde = max(pages) + 1

    for i in range(1, einde):
        links.append(BEWRD_URL + 'p' + str(i))

    for page in links:
        html = session.get(page)
        soup = BeautifulSoup(html.text)
        houses = soup.find('ul', class_='search-results saved-objects').find_all('div', class_="search-result-content-inner")
        for house in houses:
            raw_address = house.find('h3', class_='search-result-title').text
            raw_address_list = [s.strip() for s in raw_address.splitlines()]
            street_nr = raw_address_list[1]
            postalcode_city = raw_address_list[3]
            price = int(unidecode.unidecode(house.find('span', class_='search-result-price').text).replace("EUR ", "").replace(".", "").replace("kk",""))

            pcode = street_nr + " " + postalcode_city
            url = GEOCODE_URL + pcode
            response = requests.get(url)
            try:
                # see http://gis.stackexchange.com/questions/58271/using-python-to-parse-an-xml-containing-gml-tags
                root = ET.fromstring(response.content)
                for point in root.findall('.//{http://www.opengis.net/gml}Point'):
                    rdxy = point.findtext("{http://www.opengis.net/gml}pos").split()
                pnt = GEOSGeometry('POINT({0} {1})'.format(rdxy[0], rdxy[1]), srid=28992)
                # see http://gis.stackexchange.com/questions/94640/geodjango-transform-not-working
                pnt.transform(4326)
            except:
                rdxy = [0, 0]
                pnt = GEOSGeometry('POINT({0} {1})'.format(0, 0), srid=4326)

            House.objects.get_or_create(fuid=0,
                                        vraagprijs=price,
                                        postcode=postalcode_city,
                                        link='http://test',
                                        rdx=rdxy[0],
                                        rdy=rdxy[1],
                                        geom=pnt)
