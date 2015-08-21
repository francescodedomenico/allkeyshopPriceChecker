import requests
from bs4 import BeautifulSoup
import re
from time import sleep
from os.path import isfile

pricesDatabase = dict()

def fetchPrices(metaTags):
    toReturn = list()
    for tag in metaTags:
        if 'class="voucher-price"' in str(tag) or 'itemprop="price"' in str(tag):
            priceTag = tag.text
            if priceTag is None:
                continue
            price = priceTag.replace(u'\u20ac','')
            toReturn.append(float(price))
    return toReturn

def checkPrices():
    while True:
        in_file = open('games.txt', 'r')
        links = {}
        for line in in_file:
            title = line.split(',')[0]
            link = line.split(',')[1]
            links[title] = link
        in_file.close()

        if isfile('pricesdb.txt'):
            pricesFile = open('pricesdb.txt', 'r')
            for line in pricesFile:
                title = line.split(',')[0]
                price = line.split(',')[1]
                pricesDatabase[title] = float(price)
            pricesFile.close()

        for key, value in links.iteritems():
            r = requests.get(value)
            htmlTree = BeautifulSoup(r.text, "html.parser",from_encoding='utf8')
            prices = fetchPrices(htmlTree.findAll('strong'))
            minPrice = str(min(prices))
            print 'Minimum price for '+key+" is: "+minPrice
            if float(minPrice) < pricesDatabase[key]:
                beforePrice = pricesDatabase[key]
                print 'New minimum price for '+key+', before was '+beforePrice+', now is '+minPrice
            pricesDatabase[key] = float(minPrice)
            sleep(5)
        outPrices = open('pricesdb.txt', 'wb')
        for key in pricesDatabase:
            outPrices.write(key+','+str(pricesDatabase[key])+'\n')
        outPrices.close()
        sleep(600)
checkPrices()
