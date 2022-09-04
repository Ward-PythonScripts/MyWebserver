import traceback
import json


class IboodDeal():
    def __init__(self,product_name,product_advice_price,product_curr_price,product_discount_percentage,product_image_url,
        product_image,product_link,is_soldout):
        self.product_name:str = product_name
        self.product_advice_price = self.price_to_int(product_advice_price)
        self.product_curr_price = self.price_to_int(product_curr_price)
        self.product_discount_percentage:str = product_discount_percentage
        self.product_image_url = product_image_url
        self.product_image = product_image
        self.product_link = product_link
        self.is_soldout = is_soldout
    

    def get_inches_from_name(self) -> int:
        try:
            nums_in_reverse = []
            self.product_name = self.product_name.replace("”","\"") #sometimes the site uses these ”  instead of the normal "
            index = self.product_name.find("\"") 
            while self.product_name[index - 1].isnumeric():
                nums_in_reverse.append(self.product_name[index-1])
                index -= 1
            size = ""
            nums_in_reverse.reverse()
            for num in nums_in_reverse:
                size += num
            return int(size)
            
        except Exception:
            #if find doesn't find the inch symbol in the string that means that there is no size available
            #it will raise an exception, which will be caught and the function will just return None
            return -1
    def get_discount_as_numbers(self) -> float:
        try:
            numerics = ""
            for charac in self.product_discount_percentage:
                if charac.isnumeric():
                    numerics += charac
            return numerics
        except Exception as e:
            #not supposed to happen
            print(traceback.print_exc())

    def price_to_int(self,price_string:str) -> float:
        try:
            price_string = price_string.replace("€ ","")
            price_string = price_string.replace("-","0") #ibood writes numbers: € 369,- . the - will mess with things -> replace it with just a normal 0
            price_string = price_string.replace(",",".") #site uses , instead of . in numbers (9,0 should be 9.0)
            return float(price_string)

        except Exception as e:
            #not supposed to happen
            print(traceback.print_exc(),"got this far",price_string)

class Recipient():
    def __init__(self,id,name,mail,searches) -> None:
        self.id = id
        self.name = name
        self.mail = mail
        self.searches = searches
    
    def get_searches_as_json(self):
        serialized_list = []
        for search in self.searches:
            serialized_list.append(search.to_dict())
        json_string = json.dumps(serialized_list)
        return {
            'list':json_string
        }



class Search():
    def __init__(self,action,name,recipient_Id,search_id) -> None:
        self.action = action
        self.name = name
        self.search_Id = search_id
        if recipient_Id is None:
            self.recipient_Id = -1
        else:
            self.recipient_Id = recipient_Id
    def to_dict(self):
        return {
            'action':self.action,
            'name':self.name,
            'recipient_Id':self.recipient_Id,
            'search_Id':self.search_id,
        }


class Filter():
    def __init__(self,key,value) -> None:
        self.key = key
        self.value = value
    
