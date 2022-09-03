import traceback


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