# coding=utf-8
# hacked from https://github.com/markbarks/FundaScraper
from datetime import date
import httplib
import re
import sys
import logging
from urllib2 import URLError
import urlparse
from datetime import datetime
import time

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from django.contrib.gis.geos import GEOSGeometry

from .models import House


BEWRD_URL = 'http://www.funda.nl/mijn/bewaard/'
LOGIN_URL = 'https://www.funda.nl/mijn/login/'
USER = ''
PASSWD = ''
#USER =
#PASSWD =
GEOCODE_URL = 'https://geodata.nationaalgeoregister.nl/geocoder/Geocoder?zoekterm='


# To make sure you're seeing all debug output:
logger = logging.getLogger("mechanize")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)


def get_html(link):
    while True:
        time.sleep(1)
        response = requests.get(link.rstrip())

        if "fout/500" in response.url:
            print str(datetime.now()) + " ... retrying " + response.url
            continue
        break

    if "fout/404" not in response.url and "fout/500" not in response.url:
        html = response.text
        if "Object niet (meer) beschikbaar" not in html:
            return html
    else:
        print str(datetime.now()) + " ... failed " + response.url
    return None


def parse_html(html):
    try:
        soup = BeautifulSoup(html)
        specs = {}
        header = soup.find_all("div", class_="prop-hdr")[0]
        specs["Address"] = header.h1.get_text()
        specs["Postcode"] = header.p.get_text().replace("    Tophuis", "")
        specs["Areacode"] = specs["Postcode"].split(" ")[0]
        nav = soup.find_all("p", class_="path-nav")[0]
        specs["Area"] = nav.get_text(strip=True).split(">")[-1]

        for table in soup.find_all("table", class_="specs-cats"):
            for tr in table.find_all('tr'):
                if tr.th is not None and tr.td is not None and tr.td.get_text(strip=True):
                    key = tr.th.get_text(strip=True)

                    text = tr.td.get_text("|", strip=True)

                    text = text.replace(u"\u00B2", u'')  # replace squares
                    text = text.replace(u"\u00B3", u'')  # replace cubes
                    text = re.sub("\W+m$", "", text)  # replace metres
                    text = text.replace(u"\u20AC", u'').strip()  # replace euros

                    if key in ['Vraagprijs', 'Laatste vraagprijs', 'Oorspronkelijke vraagprijs']:
                        if "v.o.n." in text:
                            text = text.replace(" v.o.n.", "")
                            specs["Cost"] = "v.o.n."
                        elif "k.k." in text:
                            text = text.replace(" k.k.", "")
                            specs["Cost"] = "k.k."
                        text = text.replace(".", "")

                    specs[key] = text
        return specs
    except BaseException as e:
        print str(datetime.now()) + " ... failed: " + e.message
        return None


def get_all_keys(all_specs):
    keys = set()
    for specs in all_specs:
        keys.update(specs.keys())
    return sorted(list(keys))


def write_links(datestr):
    while True:
        try:
            s = requests.session()
            s.keep_alive = False
            login_data = {'Email': USER, 'Password': PASSWD}
            s.post('https://www.funda.nl/mijn/login/', login_data)
            break
        except URLError as e:
            print str(datetime.now()) + " [Errno 54] Connection reset by peer .. sleeping"
            time.sleep(1)
    links = list()
    i = 0
    resp = s.get(BEWRD_URL + 'p1')
    soup = BeautifulSoup(resp.text)
    while soup.findAll("a", class_="paging next"):
        try:
            i += 1
            resp = s.get(BEWRD_URL + 'p' + str(i))
            soup = BeautifulSoup(resp.text)
            mydivs = soup.findAll("a", class_="object-street")
            for div in mydivs:
                links.append(urlparse.urljoin('http://www.funda.nl/koop', div['href'] + "kenmerken"))
        except URLError as e:
            print str(datetime.now()) + " [Errno 54] Connection reset by peer .. sleeping"
            time.sleep(1)
        except httplib.BadStatusLine as e:
            print str(datetime.now()) + " BadStatusLine .. sleeping"
            time.sleep(1)
    return links


def process_koop():
    datestr = date.today().isoformat()

    links = write_links(datestr)

    all_specs = list()
    for link in links:
        print str(datetime.now()) + " " + link
        html = get_html(link)
        if html is not None:
            specs = parse_html(html)
            specs["Id"] = parse_id(link)
            specs["Link"] = link
            all_specs.append(specs)
    for specs in all_specs:
        try:
            address = specs["Postcode"].split()
            try:
                postcode = address[0] + " " + address[1]
            except IndexError:
                postcode = "onbekend"
            pcode = specs["Address"] + " " + postcode
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
                #import pdb;pdb.set_trace()
                pnt = GEOSGeometry('POINT({0} {1})'.format(0, 0), srid=4326)

            House.objects.get_or_create(fuid=specs["Id"],
                                        vraagprijs=specs["Vraagprijs"],
                                        postcode=specs["Postcode"],
                                        link=specs["Link"],
                                        rdx=rdxy[0],
                                        rdy=rdxy[1],
                                        geom=pnt)
        except KeyError:
            pass

def parse_id(link):
    regex = re.compile("-(\d+)-")
    r = regex.search(link)
    return r.groups()[0]

