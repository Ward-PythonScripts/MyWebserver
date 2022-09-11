import requests
from bs4 import BeautifulSoup
import traceback
import json
import time

from . import ibood_db
from .mailer import Mailer

from .container import IboodDeal

POSSIBLE_FILTERS = ['name-contains','not-name-contains','inches-smaller',
    'inches-bigger','discount-bigger','price-smaller','not-soldout']


def get_all_dealslink(page_nr):
    return "https://www.ibood.com/be/nl/all-deals/?page="+str(page_nr)


def collect_deals():
    #electronics_url = "https://https://www.ibood.com/be/nl/all-deals/?page=1&vertical=electronics"

    products_list = []

    #for each page in all_deals
    current_page = 1
    still_pages_left = True
    while(still_pages_left):
        url = get_all_dealslink(current_page)
        response = requests.get(url)
        if response.ok:
            try:
                #get all elements from the page
                soup = BeautifulSoup(response.text,'html.parser')
                items = soup.find_all("div",{"class": "MuiGrid-item"})
                for item in items:
                    try:
                        #object class names are generated dynamically -> can't parse it with those
                        card_offer_container = item.findChild("div")
                        product_link_container = card_offer_container.findChild("a")
                        product_link = "https://www.ibood.com"+product_link_container.get("href")  
                        item_info_container = product_link_container.findChild("div")
                        other_info = item_info_container.findChildren("div")
                        for x in range(0,len(other_info)):
                            if x == 0:
                                #gettting the discount
                                product_discount_percentage = other_info[x].get_text()
                            elif x == 1:
                                #getting the image
                                image_tag_cont = other_info[x].findChild("img")
                                product_image_url = image_tag_cont.get("src")
                            elif x == 2:
                                #prices and name
                                product_name = other_info[x].findChild("h2").get_text()
                                prices_conts = other_info[x].findChildren("div")
                                product_advice_price = prices_conts[0].findChild("span").get_text()
                                product_curr_price = prices_conts[1].findChild("div").get_text()
                            elif x == 3:
                                #there was an element that specifies that the item is soldout
                                is_soldout = True

                        products_list.append(IboodDeal(product_name,product_advice_price,product_curr_price,
                            product_discount_percentage,product_image_url,product_link,is_soldout))
                    except AttributeError as ae:
                        #probably means it was a Nonetype -> found some item that doesn't have a link and is probably just some ui element somewhere
                        pass
                    except Exception as e:
                        print("exception in parsing the webpage but continuing anyways\n",traceback.format_exc())
                
                #check if there is still another page left
                page_references = soup.findAll("span",{"data-testid":"offers-pagination-page-number"})
                last_reference = page_references[len(page_references)-1]
                last_pagenr = last_reference.get_text()
                if int(last_pagenr) <= current_page:
                    #at the last page -> stop looking for the next pages
                    still_pages_left = False       
                current_page += 1      
                print("IBOOD: Scanned a page, this is slowed down with a sleep of 5 seconds as to not overload the ibood site")       
                    
            except Exception as e:
                print(traceback.format_exc())
        #wait as to not overspam their server and get banned
        time.sleep(5)
    
    return products_list


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

def remove_empty_from_filter(filter):
    new_dict = {}
    for key in filter.keys():
        if not filter[key] == "":
            new_dict[key] = filter[key]
    return new_dict


def start_scraping():
    print("Starting the iBOOD scraper")
    all_hardware_deals = collect_deals()
    #for each person filter the deals and add in db if they are relevant
    recipients = ibood_db.get_all_recipients()
    for recipient in recipients:
        for rec_filter in recipient.searches:
            filter = rec_filter.action
            filter = json.loads(filter)
            filter = remove_empty_from_filter(filter)
            found_deals = filter_deals(all_hardware_deals,filter)
            if found_deals is not None:
                Mailer(recipient=recipient,deals=found_deals)
    print("iBOOD scraper shutting down")


