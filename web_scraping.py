#!/usr/bin/env python

#
# Web scraping
# ASNs (Autonomous System Numbers) are one of the building blocks of the
# Internet. This project is to create a mapping from each ASN in use to the
# company that owns it. For example, ASN 36375 is used by the University of
# Michigan - http://bgp.he.net/AS36375
# 
# The site http://bgp.he.net/ has lots of useful information about ASNs. 
# Starting at http://bgp.he.net/report/world crawl and scrape the linked country
# reports to make a structure mapping each ASN to info about that ASN.
# Sample structure:
#   {3320: {'Country': 'DE',
#     'Name': 'Deutsche Telekom AG',
#     'Routes v4': 13547,
#     'Routes v6': 268},
#    36375: {'Country': 'US',
#     'Name': 'University of Michigan',
#     'Routes v4': 14,
#     'Routes v6': 1}}
#
# When done, output the collected data to a json file.
#
# Use any python libraries. One suggestion, a good one for scraping is
# BeautifulSoup:
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/
# 

import urllib2
import bs4
import re
import json
from urlparse import urlparse, urljoin



# To help get you started, here is a function to fetch and parse a page.
# Given url, return soup.
def url_to_soup(url):
    # bgp.he.net filters based on user-agent.
    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    html = urllib2.urlopen(req).read()
    soup = bs4.BeautifulSoup(html)
    return soup

class ASN:
    """Maps ASN numbers to specified data from passed in URL
       url = base page to scrape countries from
       countries = optional list of countries to retrieve data from
          [default is to retrieve all countries]
    """
    def __init__(self, url, countries=None):
        self.country_urls = {}
        self.head_map = {}
        self.asn_map = {}
        # Scrape the links for all the countries
        try:
            self.get_world(url)
        except urllib2.HTTPError:
            print "HTTP Error: '%s'" % url
            return
        if countries is None:
            countries = self.country_urls.keys()
        # Loop over each country and fetch ASN data into dict
        for key in countries:
            print "Fetching data for %s" % key
            self.get_country_data(self.country_urls[key], key)
        self.write_json('asn_output.json')


    def get_world(self, url):
        """Given url scrape all the country urls and store in dict"""
        parsed_url = urlparse(url)
        base_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)
        world = url_to_soup(url)
        countries = world.find(id='table_countries').tbody.find_all('tr')
        for country in countries:
            country_name = country.find(class_="down2 floatleft").string.strip()
            new_url = urljoin(base_url, country.find(href=re.compile('country')).get('href'))
            self.country_urls[country_name] = new_url

    def get_country_data(self, url, country_name):
        """Get ASN data for each country
           Extract desired headers and map to locations in table"""
        header_list = ['ASN', 'Name', 'Routes v4', 'Routes v6']
        try:
            country = url_to_soup(url)
            country_block = country.find(id='country')
            # map header table to column numbers
            if len(self.head_map.keys()) == 0:
                header = country_block.thead.tr
                next_sibling = header.th
                i = 0
                while next_sibling is not None:
                    if next_sibling.string in header_list:
                        self.head_map[next_sibling.string] = i
                    next_sibling = next_sibling.next_sibling
                    i += 1
            # extract country data from table
            country_table = country_block.tbody
            rows = country_table.find_all('tr')
            for row in rows:
                row_data = []
                for data in row.find_all('td'):
                    if data.string is not None:
                        row_data.append(data.string)
                    else:
                        row_data.append('')
                self.asn_map[int(row_data[self.head_map['ASN']][2:])] = {
                    "Country":  country_name,
                    "Name":  unicode(row_data[self.head_map['Name']]),
                    "Routes v4": int(unicode(row_data[self.head_map['Routes v4']]).replace(',','')),
                    "Routes v6": int(unicode(row_data[self.head_map['Routes v6']]).replace(',',''))
                }
        except AttributeError:
            print "No ASN data for %s!" % country_name
            return

    def write_json(self, filename):
        with open(filename, 'w') as outfile:
            json.dump(self.asn_map, outfile)


if __name__ == '__main__':
    a = ASN('http://bgp.he.net/report/world')