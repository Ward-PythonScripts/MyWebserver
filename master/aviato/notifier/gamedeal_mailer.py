from . import credentials
#credentials is just a py module that returns the needed strings like mail-address and password
from . import notifier_backend

SORT_ORDER = {"STEAM":0,"EPIC GAMES":1,"EPIC":2}



class GameDealMailSender:
    def __init__(self) -> None:
        self.email = credentials.gameDeals_mail()
        self.email_password = credentials.gameDeals_app_password()
        mail_recipients = notifier_backend.get_all_recipients()
        self.mails = []
        for recipient in mail_recipients:
            self.mails.append(recipient.mail)
        self.mail_subject = "GameDeals - Hello there, some new deals"
        self.gamedeals = []
        
    def add_new_deal(self,gamedeal):
        self.gamedeals.append(gamedeal)
    
    def send_mail(self):
        #sort first
        try:
            sorted_games = sorted(self.gamedeals,key=lambda x: (SORT_ORDER.get(str(x.cat).upper(),len(SORT_ORDER)),x.cat),reverse=False)
            
            #build mail body
            prevCat = ""
            body = ""
            for sorted_game in sorted_games:
                if prevCat != sorted_game.cat:
                    #new category
                    body += "\n" + sorted_game.cat + "\n\n"
                    prevCat = sorted_game.cat
                body += sorted_game.title + "\n"
                body += "https://www.reddit.com"+ sorted_game.reddit + "\n"
            print(body)




        except Exception as e:
            print(str(e))

"""
SORT_ORDER = {"Steam":0,"Epic Games":1}
sorted_games = freeGames.sort(key=lambda x: SORT_ORDER.get(x.cat,len(SORT_ORDER)))
"""