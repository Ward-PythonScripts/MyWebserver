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
from PIL import Image

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

        body_text = ""

        image_index = 1
        for deal in self.deals_to_mail:
            image_id = "image"+str(image_index)
            soldout_string = "not yet soldout"
            if deal.is_soldout:
                soldout_string = "SOLDOUT"
            body_text += '<h1>'+deal.product_name+'</h1><img src="cid:'+image_id+'"><h2>advice price was: '+str(deal.product_advice_price)+' EUR, now available for: '+str(deal.product_curr_price)+' EUR ('+str(deal.product_discount_percentage)+')</h2><a href="'+str(deal.product_link)+'" >Click to go to iDOOB.com <a><br>'+soldout_string+'<br><br><br><br>'

            image_index +=1

        mail_text = MIMEText(body_text,'html')
        msg.attach(mail_text)

        #add images that have to fill in the mail
        
        image_index = 1
        for deal in self.deals_to_mail:
            img = Image.open(BytesIO(deal.product_image))
            #need to do the following so that we can open the image in MIME
            byte_buffer = BytesIO()
            img.save(byte_buffer,"PNG")
            image = MIMEImage(byte_buffer.getvalue())
            image_id = "image"+str(image_index)
            image.add_header('Content-ID','<'+image_id+'>')
            msg.attach(image)

            image_index += 1

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(credentials.gameDeals_mail(),credentials.gameDeals_app_password())
            smtp.sendmail(credentials.gameDeals_mail(),self.recipient.mail,msg.as_string())
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
        

