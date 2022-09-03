import traceback

class IboodDeal():
    def __init__(self,product_name):
        self.product_name:str = product_name
    

    def get_inches_from_name(self):
        print("getting inches",self.product_name)
        try:
            nums_in_reverse = []
            index = self.product_name.find("\"")
            while self.product_name[index - 1].isnumeric():
                nums_in_reverse.append(self.product_name[index-1])
                index -= 1
            size = ""
            nums_in_reverse.reverse()
            for num in nums_in_reverse:
                size += num
            return size
            
        except Exception:
            #if find doesn't find the inch symbol in the string that means that there is no size available
            #it will raise an exception, which will be caught and the function will just return None
            return None

try:

    name = "Philips 4K UHD LED 35\" Smart TV 55PUS7556/12"
    ib = IboodDeal(product_name=name)
    ib.get_inches_from_name()
except Exception as e:
    print(traceback.print_exc())