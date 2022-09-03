class IboodDeal():
    def __init__(self,product_name,product_advice_price,product_curr_price,product_discount_percentage,product_image_url,
        product_image,product_link,is_soldout):
        self.product_name:str = product_name
        self.product_advice_price = product_advice_price
        self.product_curr_price = product_curr_price
        self.product_discount_percentage = product_discount_percentage
        self.product_image_url = product_image_url
        self.product_image = product_image
        self.product_link = product_link
        self.is_soldout = is_soldout
    

    def get_inches_from_name(self):
        try:
            nums_in_reverse = []
            index = self.product_name.find("\"")
            while self.product_name[index - 1].isnumeric():
                nums_in_reverse.append(self.product_name[index-1])
                index -= 1
            size = []
            for i in range(len(nums_in_reverse),0):
                print(i,nums_in_reverse[i])
            
        except Exception:
            #if find doesn't find the inch symbol in the string that means that there is no size available
            #it will raise an exception, which will be caught and the function will just return None
            return None