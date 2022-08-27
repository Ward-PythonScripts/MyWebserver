from email import message
from email.message import EmailMessage
from email.parser import BytesParser, Parser 
import smtplib
from imapclient import IMAPClient
import imaplib
import ssl
import traceback
import email

from urllib import response
import credentials
#credentials is just the client ID and the client secret which for obvious reasons will not be pushed to git

#maybe this works https://www.youtube.com/watch?v=g_j6ILT-X0k


class MailReader():
    def __init__(self) -> None:
        email_addr = credentials.get_email()
        pwd = credentials.get_app_password()
        smtp_server = "imap.gmail.com"
        SMTP_PORT = 993

        server = IMAPClient(smtp_server,use_uid=True)
        server.login(email_addr,pwd)
        server.select_folder('INBOX',readonly=True)
        self.server = server
        
    def get_unread_emails(self,cb):
        server = self.server
        messages = server.search(['FROM',str(credentials.owner_mail())])
        #we search for owner mail's so that we aren't trying to parse the gmail default spam emails
        for uid, message_data in server.fetch(messages, "RFC822").items():
            to_file(message_data,"kd")
            email_message = email.message_from_bytes(message_data[b"RFC822"])
            print(email_message)
            print(uid, email_message.get("From"), email_message.get("Subject"))
            

        


        # data = mail.search(None,'ALL')
        # mail_ids = data[1]
        # id_list = mail_ids[0].split()
        # print(id_list)
        # first_email_id = int(id_list[0])
        # latest_email_id = int(id_list[-1])

        # for i in range(first_email_id,latest_email_id+1):
        #     data = mail.fetch(str(i), '(RFC822)' )
        #     to_file(data,str(i))
        #     for response_part in data:
        #         arr = response_part[0]
        #         #to_file(arr)
        #         if isinstance(arr, tuple):
        #             msg = email.message_from_string(str(arr[1],'utf-8'))
        #             if cb(msg):
        #                 mark_email_read(msg)

        server.logout()

def to_file(data,secondPartName):
    file = open("dump"+secondPartName+".txt","w+")
    file.write(str(data))
    file.close()

def mark_email_read(msg):
    pass

def parse_mail(email) -> bool:
    email_from = str(email['from'])
    print("Received an email from",email_from)
    index_in_addr = email_from.find(credentials.owner_mail())
    if index_in_addr != -1:
        #the owners email addres was found inside of the mail_address -> is not some random ass email
        pass


    return True


def main():
    mailReader = MailReader()
    mailReader.get_unread_emails(parse_mail)




###Tutorial class on how to send an email with python
def send_mail():
    email = credentials.get_email()
    email_password = credentials.get_app_password()
    email_receiver = credentials.get_email_to_send_to()

    subject = "Test"
    body = """
    Let's see if this works
    would be nice
    """
    em = EmailMessage()
    em['From'] = email
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(email,email_password)
        smtp.sendmail(email,email_receiver,em.as_string())
###Tutorial Class on how to go through all the received emails
def receive_mail():
    try:
        email_addr = credentials.get_email()
        pwd = credentials.get_app_password()
        smtp_server = "imap.gmail.com"
        SMTP_PORT = 993

        mail = imaplib.IMAP4_SSL(smtp_server)
        mail.login(email_addr,pwd)
        mail.select('inbox')

        data = mail.search(None,'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id,first_email_id, -1):
            data = mail.fetch(str(i), '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print('From : ' + email_from + '\n')
                    print('Subject : ' + email_subject + '\n')

    except Exception as e:
        traceback.print_exc() 
        print(str(e))

    
main()
