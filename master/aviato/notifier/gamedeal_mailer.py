import email
from email.message import EmailMessage
import json
import smtplib
import ssl

from . import credentials
#credentials is just a py module that returns the needed strings like mail-address and password
from . import notifier_backend
from .containers import Recipient,freeGame

SORT_ORDER = {"STEAM":0,"EPIC GAMES":1,"EPIC":2}



class GameDealMailSender:
    def __init__(self) -> None:
        self.email = credentials.gameDeals_mail()
        self.email_password = credentials.gameDeals_app_password()
        self.mail_recipients:list[Recipient] = notifier_backend.get_all_recipients()
        self.gamedeals:list[freeGame] = []
        
    def add_new_deal(self,gamedeal):
        self.gamedeals.append(gamedeal)
    
    def send_mail(self):
        #sort first.
        try:
            sorted_games = sorted(self.gamedeals,key=lambda x: (SORT_ORDER.get(str(x.cat).upper(),len(SORT_ORDER)),x.cat),reverse=False)
            
            for recipient in self.mail_recipients:
                mail_rec = recipient.mail
                #build mail body
                prevCat = ""
                body = ""
                for sorted_game in sorted_games:
                    if check_if_cat_is_wanted(recipient=recipient,game=sorted_game):
                        if prevCat != sorted_game.cat:
                            #new category
                            body += "\n" + sorted_game.cat + "\n\n"
                            prevCat = sorted_game.cat
                        body += sorted_game.title + "\n"
                        body += "https://www.reddit.com"+ sorted_game.reddit + "\n"
                
                #build the email
                em = EmailMessage()
                em['From'] = self.email
                em['To'] = mail_rec
                em['Subject'] = "Gamedeals - New Games"
                em.set_content(body)

                context = ssl.create_default_context()

                with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                    smtp.login(self.email,self.email_password)
                    #smtp.sendmail(self.email,mail_rec,em.as_string())
                    smtp.close()






        except Exception as e:
            print(str(e))

def check_if_cat_is_wanted(recipient:Recipient,game:freeGame):
    try:
        cat_json = json.loads(recipient.preference)
        allowed = cat_json['allowed']
        denied = cat_json['denied']
        if allowed == 'none':
            return False
        if allowed == 'all':
            #check if there is some stuff denied
            if isinstance(denied,str):
                #will either be all or none
                if denied == 'all':
                    return False
                else:
                    return True
            else:
                #is list with all the denied mail_adresses
                for denied_cat in denied:
                    if game.cat == denied_cat:
                        return False
                #cat wasn't in the list of denied addresses
                return True
        else:
            #client has given specific list of allowed websites
            for allowed_cat in allowed:
                if game.cat == allowed_cat:
                    return True
            #category wasn't one that was allowed
            return False
    except Exception as e:
        print(str(e))
