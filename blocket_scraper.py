"""
File: main.py
Author: Robert Siwerz

Extracts all the titles from a chosen category with its corresponding 
content from blocket.se.

TODO: Traverse all pages

"""

import requests, json
import shutil
from elasticsearch import Elasticsearch
from datetime import datetime
from routes.algorithms import ad
import ast

from bs4 import BeautifulSoup
import bs4

es=Elasticsearch([{'host':'localhost','port':9200}])

def get_file(url):
    with open("test.jpg", "wb") as out_file:
        r = requests.get("https://cdn.blocket.com/static/0/images_full/32/3283216851.jpg", stream=True)
        if not r.ok:
            print(r)
        else:
            for block in r.iter_content(1024):
                if not block:
                    break
                out_file.write(block)


def get_item_attributes(all_prices, all_items, gender):
    """
    Function to create an item with all its corresponding
    attributes. The attributes are contained within the link
    as well as the content inside the link. 

    item = {
            "title": the title of the item
            "description": description about item,
            "size": size of item,
            "gender": gender,
            "color": color of the item,
            "price": the price of the item,
            "location": the location of the seller
            }
    """
    items = []
    for prices, items2 in zip(all_prices, all_items):
        for price, item in zip(prices, items2):
            item_request = requests.get(item['href'])
            item_soup = BeautifulSoup(item_request.text, features="html.parser")

            location = item_soup.find("span", attrs={"class": "area_label"})
            picture_link = item_soup.find("img")
            date_added = item_soup.find("time")['datetime']
            datetime_obj = datetime.strptime(date_added, "%Y-%m-%dT%H:%M")
            # print(datetime_obj.hour)
            converted_date = str(datetime_obj.month) + "/" + str(datetime_obj.day) + "/" + str(datetime_obj.year)
            description = item_soup.find("div", attrs={"class": "col-xs-12 body"}).text
            if location:
                location = location.text.replace("(", "").replace(")", "")
            else:
                location = "Sweden"
            item = {
                "title": item.text,
                "date": converted_date,
                "description": description,
                "size": "placeholder",
                "gender": "M" if gender == 1 else "F",
                "color": "black",
                "price": price.text.split(" ")[0],
                "location": location,
                "link": item['href'],
            }
            items.append(item)
            #print(item)
    return items


#FEMALE_JEANS_LINK = "?q=&cg=4080&w=3&st=s&cs=1&ck=2&csz=&ca=11&is=1&l=0&md=th"
#MALE_JEANS_LINK =   "?q=&cg=4080&w=3&st=s&cs=2&ck=2&csz=&ca=11&is=1&l=0&md=th"

FEMALE_CLOTHES = "?q=&cg=4080&w=3&st=s&cs=1&ck=&csz=&ca=11&is=1&l=0&md=th"
MALE_CLOTHES = "?q=&cg=4080&w=3&st=s&cs=2&ck=&csz=&ca=11&is=1&l=0&md=th"


#categories = [FEMALE_JEANS_LINK, MALE_JEANS_LINK]
categories = [FEMALE_CLOTHES, MALE_CLOTHES]
BASE_PART = "https://www.blocket.se/hela_sverige"

iterator = 1
for gender, category in enumerate(categories):
#for category in categories:
    r = requests.get(BASE_PART + category)

    soup = BeautifulSoup(r.text, features="html.parser")

    # Fetch all the pages
    last_page = soup.find("a", attrs={"rel": "Sista sidan"})['href']

    # Create a new request and soup object
    r = requests.get(BASE_PART + last_page)
    page_soup = BeautifulSoup(r.text, features="html.parser")
    # Fetch all the page links in the bottom
    last_pages = page_soup.findAll("a", attrs={"class": "page_nav"})

    # The last numerical link is one before "Första sidan"
    last_link = int(last_pages[-2].text)

    """
    Collect all the links and prices for the items by saving them in an array.
    Possibly this has to be done every X minutes as the links are 
    constantly changing.
    
    """
    all_items = []
    all_prices = []
    counter = 1
    print("Fetching all the items...")
    # TODO: Abstract this?
    while counter <= last_link:
        print(counter)
        print("{}%".format(round(counter / last_link * 100))) 
        if counter == 1:
            r = requests.get(BASE_PART + category)
            # r = requests.get(BASE_PART + "?cg=4080&w=3&st=s&ca=11&l=0&md=th&ck=1")
        else:
            # r = requests.get(BASE_PART + "?cg=4080&w=3&st=s&ca=11&l=0&md=th&ck=1&o=" + str(counter))
            r = requests.get(BASE_PART + category + "&ck=1&o=" + str(counter))

        test_soup = BeautifulSoup(r.text, features="html.parser")
        prices = test_soup.findAll("p", attrs={"class": "list_price font-large"})
        items_raw = test_soup.findAll("a", attrs={"class": "item_link"})

        all_prices.append(prices)
        all_items.append(items_raw)

        items = get_item_attributes(all_prices, all_items, 1)

        counter += 1

    for article in items:
        blocket_url = "http://localhost:9200/blocket/items"
        content ={
            "title": article['title'],
            "description": article['description'],
            "date": article['date'],
            "size": article['size'],
            "gender": article['gender'],
            "color": article['color'],
            "price": article['price'],
            "location": article['location']
        }
        content['description'] = content['description'].replace('\t','')
        content['description'] = content['description'].replace('\n','')
        #add code to initiate the id class
        item = ad.ad(content['price'], content['size'], content['title'], content['description'], content['location'], content['date'])
        #add the condition, number of days and color to json file
        content['condition'] = item.condition 
        content['color'] = item.colors
        content['num_days'] = item.days
        content['info'] = ' '.join(item.tokens)
        content['id'] = iterator
        content['score'] = 0
        iterator += 1
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
        payload = json.dumps(content)

        print(payload)
        es.index(index="blocket", doc_type="items", id=iterator, body=payload)
        #response = requests.request("POST", blocket_url, data=payload, headers=headers)
    
