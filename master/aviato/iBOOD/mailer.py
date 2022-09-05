from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from subprocess import CREATE_DEFAULT_ERROR_MODE
from .container import Recipient,Search,IboodDeal
from . import ibood_db
from . import credentials
from io import BytesIO
import ssl

class Mailer():
    def __init__(self,recipient,deals) -> None:
        self.recipient:Recipient = recipient
        self.deals:list[IboodDeal] = deals
        if len(self.deals) == 0:
            return
        self.deals_to_mail:list[IboodDeal] = []
        self.filter_for_already_informed_mails()
        if len(self.deals_to_mail) == 0:
            return
        self.send_mail()

    def send_mail(self):
        #build body
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Some new iBOOD products have been found"
        msg['From'] = credentials.gameDeals_mail()
        msg['To'] = self.recipient.mail


        image_index = 1
        for deal in self.deals_to_mail:
            # text = MIMEText('<img src="cid:image"'+str(image_index)+'>','html')
            # msg.attach(text)
            # image = MIMEImage(BytesIO(deal.product_image))
            # image.add_header('Content-ID','<image'+str(image_index)+'>')
            # msg.attach(image)
            text = MIMEText('<html><body><h1>Hello World</h1></body></html>','html','utf-8')
            msg.attach(text)

            image_index += 1

        print("msg as string",msg.as_string(),"there were ",len(self.deals_to_mail),"deals to mail")

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(credentials.gameDeals_mail(),credentials.gameDeals_app_password())
            #smtp.sendmail(credentials.gameDeals_mail(),self.recipient.mail,msg.as_string())
            smtp.close()


    def filter_for_already_informed_mails(self):
        deals = self.deals
        for deal in deals:
            # if ibood_db.create_item_and_add_to_history(name=deal.product_name,curr_price=deal.product_curr_price,
            #     advice_price=deal.product_advice_price,discount_percentage=deal.get_discount_as_numbers(),
            #     image_url=deal.product_image_url,image=deal.product_image,link=deal.product_link,soldout=deal.is_soldout,
            #     recipient_id=self.recipient.id):
                #wasn't yet in the history -> add to the mailing list
            self.deals_to_mail.append(deal)
        

