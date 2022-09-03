from io import BytesIO
import requests
from bs4 import BeautifulSoup
from PIL import Image
import traceback


def start_sraper():
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
                print("it is soldout",is_soldout)
                # img = Image.open(BytesIO(product_image))
                # img.show()
                print(product_name,product_discount_percentage)
                
                
                
        except Exception as e:
            print(traceback.format_exc())

start_sraper()