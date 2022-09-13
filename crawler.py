import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

def get_page(url):
    try:
        page = requests.get(url)
        return page
    except:
        print("Error: Could not get page")

def get_soup(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def data_list():
    url = 'http://www.cim.mcgill.ca/~dudek/206/Logs/AOL-user-ct-collection/user-ct-test-collection-01.txt'
    #From the url, get all links and store them in a list
    page = get_page(url)
    soup = get_soup(page)
    data_list = []
    for line in soup:
        line = line.split()
        if line.startswith('http'):
            data_list.append(line)
    return data_list

if __name__ == '__main__':
    url = 'http://www.cim.mcgill.ca/~dudek/206/Logs/AOL-user-ct-collection/user-ct-test-collection-01.txt'
    print(data_list())