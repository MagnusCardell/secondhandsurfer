"""
File: main.py
Author: Robert Siwerz

Extracts all the titles from a chosen category with its corresponding 
content from blocket.se.

TODO: Traverse all pages

"""

import requests, json
from elasticsearch import Elasticsearch
es = Elasticsearch()



from bs4 import BeautifulSoup
import bs4

def get_item_attributes(all_prices, all_items):
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
    for prices, items in zip(all_prices, all_items):
        for price, item in zip(prices, items):
            item_request = requests.get(item['href'])
            item_soup = BeautifulSoup(item_request.text, features="html.parser")

            location = item_soup.find("span", attrs={"class": "area_label"})
            description = item_soup.find("div", attrs={"class": "col-xs-12 body"}).text
            if location:
                location = location.text.replace("(", "").replace(")", "")
            else:
                location = "Sweden"
            item = {
                "title": item.text,
                "description": description,
                "size": "placeholder",
                "gender": "M",
                "color": "black",
                "price": price.text,
                "location": location
            }
            items.append(item)
            print(item)
    return items


FEMALE_JEANS_LINK = "?q=&cg=4080&w=3&st=s&cs=1&ck=2&csz=&ca=11&is=1&l=0&md=th"
MALE_JEANS_LINK =   "?q=&cg=4080&w=3&st=s&cs=2&ck=2&csz=&ca=11&is=1&l=0&md=th"


categories = [FEMALE_JEANS_LINK, MALE_JEANS_LINK]
BASE_PART = "https://www.blocket.se/hela_sverige"

for category in categories:
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
        items = test_soup.findAll("a", attrs={"class": "item_link"})

        all_prices.append(prices)
        all_items.append(items)

        items = get_item_attributes(all_prices, all_items)

        counter += 1

    i = 1
    for id, item in enumerate(items):
        blocket_url = "http://localhost:9200/blocket/items"
        payload ={
            "title": item.title,
            "description": item.description,
            "size": item.size,
            "gender": item.gender,
            "color": item.color,
            "price": item.price,
            "location": item.location
        }
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
        payload = json.dumps(payload)

        response = requests.request("POST", blocket_url, data=payload, headers=headers)
        if(response.status_code==201):
            print("Values saved in blocket index")

        print("----------------", i, "----------------------")
        i = i + 1
        #res = es.index(index="jeans", doc_type='item', id=id, body=item)

    








