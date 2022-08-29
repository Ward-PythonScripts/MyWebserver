from . import credentials
#credentials is just a py module that returns the needed strings like mail-address and password
from . import notifier_backend

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
        pass