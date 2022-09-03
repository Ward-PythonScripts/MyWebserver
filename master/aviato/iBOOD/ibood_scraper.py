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

                
                
                
        except Exception as e:
            print(traceback.format_exc())

def filter_deals(deals:list[IboodDeal],filter):
    #product name filters
    if 'name-contains' in filter:
        name_contains = filter.get('name-contains')
        for deal in deals:
            if deal.product_name.__contains__(name_contains):
                deals.remove(deal)
    if 'inches-smaller' in filter:
        inches_smaller = filter.get('inches-smaller')
        for deal in deals:
            deal.get_inches_from_name()


        


def start_scraping():
    print("Starting the iBOOD scraper")
    filter = {
        'name-contains':'tv',
        'inches-smaller':'60',
    }
    deals = filter_deals(collect_deals(),filter)



