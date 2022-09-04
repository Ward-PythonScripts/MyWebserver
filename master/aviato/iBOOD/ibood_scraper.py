from itertools import product
import requests
from bs4 import BeautifulSoup
import traceback

from .container import IboodDeal


def collect_deals():
    url = "https://www.ibood.com/be/nl/flash-sales/00000/23185/de-hardware/"
    IBOOD_ITEM_CLASS = "MuiGrid-root MuiGrid-item MuiGrid-grid-xs-6 MuiGrid-grid-sm-4 MuiGrid-grid-md-3 MuiGrid-grid-lg-3 MuiGrid-grid-xl-3"
    IBOOD_ITEM_NAME_CLASS = "jss98"
    IBOOD_ADVICE_PRICE = "jss101"
    IBOOD_CURR_PRICE = "jss100"
    IBOOD_PROD_LINK = "jss104"
    IBOOD_DISCOUNT_PERCENTAGE = "jss94"
    IBOOD_PROD_IMAGE = "jss97"


    response = requests.get(url)
    
    if response.ok:
        try:
            products_list = []

            soup = BeautifulSoup(response.text,'html.parser')
            items = soup.find_all("div",{"class": IBOOD_ITEM_CLASS})
            for item in items:
                product_name = item.find("h2",{"class":IBOOD_ITEM_NAME_CLASS}).get_text()
                product_advice_price = item.find("span",{"class":IBOOD_ADVICE_PRICE}).get_text()
                product_curr_price = item.find("div",{"class":IBOOD_CURR_PRICE}).get_text()
                product_discount_percentage = item.find("div",{"class":IBOOD_DISCOUNT_PERCENTAGE}).get_text()
                product_image_url = item.find("img",{"class":IBOOD_PROD_IMAGE}).get("src")
                product_image = requests.get("https:"+product_image_url).content
                product_link = "https://www.ibood.com"+item.find("a",{"class":IBOOD_PROD_LINK}).get("href")
                is_soldout = (item.find("div",{"class":"jss105"}) is not None)

                products_list.append(IboodDeal(product_name,product_advice_price,product_curr_price,
                    product_discount_percentage,product_image_url,product_image,product_link,is_soldout))

                
            return products_list
                
        except Exception as e:
            print(traceback.format_exc())

def filter_deals(deals:list[IboodDeal],filter):
    #product name filters, english bad so instead of higher/lower -> bigger/smaller my bad ;)
    if 'name-contains' in filter:
        name_contains = filter.get('name-contains')
        new_deals = []
        for deal in deals:
            if deal.product_name.lower().__contains__(name_contains):
                new_deals.append(deal)
        deals = new_deals
    if 'not-name-contains' in filter:
        name_not_contains = filter.get('not-name-contains')
        new_deals = []
        for deal in deals:
            if not deal.product_name.lower().__contains__(name_not_contains):
                new_deals.append(deal)
        deals = new_deals
    if 'inches-smaller' in filter:
        inches_smaller = filter.get('inches-smaller')
        new_deals = []
        for deal in deals:
            inches = deal.get_inches_from_name()
            if not inches == -1:
                #no inches found in the name
                if inches <= int(inches_smaller):
                    new_deals.append(deal)
        deals = new_deals
    if 'inches-bigger' in filter:
        inches_bigger = filter.get('inches-bigger')
        new_deals = []
        for deal in deals:
            inches = deal.get_inches_from_name()
            if not inches == -1:
                if inches >= int(inches_bigger):
                    new_deals.append(deal)
        deals = new_deals
    if 'discount-bigger' in filter:
        discount_bigger = filter.get('discount-bigger')
        new_deals = []
        for deal in deals:
            if deal.get_discount_as_numbers() >= discount_bigger:
                new_deals.append(deal)
        deals = new_deals
    if 'price-smaller' in filter:
        try:
            price_smaller = filter.get('price-smaller')
            new_deals = []
            for deal in deals:
                if deal.product_curr_price <= float(price_smaller):
                    new_deals.append(deal)
            deals = new_deals
        except Exception as e:
            print(traceback.print_exc(),"user probably didn't give a proper float value")
    if 'not-soldout' in filter:
        new_deals = []
        for deal in deals:
            if not deal.is_soldout:
                new_deals.append(deal)
        deals = new_deals



    return deals


def start_scraping():
    print("Starting the iBOOD scraper")
    filter = {
        'name-contains':'tv',
        'not-name-contains':'tv muurbeugel',
        'inches-smaller':'60',
        'discount-bigger':'41',
        'price-smaller':'400',
    }
    deals = filter_deals(collect_deals(),filter)
    print("End result")
    for deal in deals:
        print(deal.product_name,deal.product_discount_percentage,deal.product_curr_price)


