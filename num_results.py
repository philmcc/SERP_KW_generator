import requests
from bs4 import BeautifulSoup
import argparse
from selenium import webdriver
import pandas as pd


parser = argparse.ArgumentParser(description='Get Google Count.')
parser.add_argument('word', help='word to count')
args = parser.parse_args()

r = requests.get('http://www.google.com/search',
                 params={'q':'"'+args.word+'"',
                         "tbs":"li:1"}
                )
#print(r.text)
soup = BeautifulSoup(r.content,"lxml")
#print(soup)

print(soup.find('div',{'id':'result-stats'}))
print(soup.find("head").find("title"))
print(soup.find('div', id ='result-stats'))
#soup.find('div', id='articlebody')
print(soup.select('result-stats'))
print(soup.find("result-stats"))
print(soup.find(id='resultStats'))
print(soup.find(id="result-stats"))
id="link1"

