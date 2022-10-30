#From github, prints the email and all its contents


import imaplib, email, email.parser, email.policy
import html2text
from . import credentials
from bs4 import BeautifulSoup
import requests

from . import karting_db

import traceback

class KartingManager():
    def __init__(self) -> None:
        self.writing = ""
    def add_string(self,to_add):
        self.writing += "\n"+to_add

    def start_parser(self):
        #remove all the /r encodings
        self.writing = self.writing.replace("\r","")
        all_lines = self.writing.split("\n")
        #already reset it so that we can use it for the next one if something were to fail in this parsing
        self.__init__()
        #remove all lines that are empty
        all_lines_no_spaces = filter(lambda val: val != '',all_lines)
        all_lines = list(all_lines_no_spaces)

        #first thing is the sesion number and timestamp of the session
        session_id = parse_session_info(all_lines)
        if session_id == -1:
            return#the session was already present in the database
        
        #get the laptimes of the drivers
        parse_lap_times(all_lines,session_id)

        parse_records(all_lines,session_id)


    def write(self):
        file = open("email_dump.txt","w+")
        file.write(str(self.writing))
        file.close()

def parse_records(all_lines,session_id):
    print(all_lines)
    record_start_index = get_start_records(all_lines)
    if record_start_index == -1:
        print("Couldn't find the start of the records")
        return
    """structure is:
            order_in_ranking
            driver_name
            snelste ronde"""
    identifier_index = 0
    index = record_start_index
    while True:
        if identifier_index == 0:
            #order in ranking, isn't interesting
            #only need to check if there is still a record left to be parsed
            try:
                int(all_lines[index])
            except:
                #if it was the ranking order space we would be able to convert it to an int, if this fails than there is no record to be parsed left
                return
        if identifier_index == 1:
            driver_name = all_lines[index]
        elif identifier_index == 2:
            lap_time = all_lines[index]
            identifier_index = -1
            driver_id = karting_db.get_driver_id(driver_name=driver_name)
            track_id = karting_db.get_track_id_from_session(session_id)
            karting_db.store_track_record({
                "driver_id":driver_id,
                "laptime":lap_time,
                "track_id":track_id
            })
        identifier_index += 1
        index += 1

    
def get_start_records(all_lines):
    index = 0
    for line in all_lines:
        if line.__contains__("records"):
            return index + 4
        index += 1
    return -1

def parse_lap_times(all_lines,session_id):
    starting_index = get_start_lap_times(all_lines)
    if starting_index == -1:
        print("failed to find the start of the laptimes")
    else:
        """layout is as follows:
                kartnr
                driver_name
                time1
                time2
                time3
                ...
        """
        index = starting_index
        identifier_index = 0
        laptimes = []
        while True:
            if identifier_index >= 2:
                #laptimes, if it is longer than 4 characters long -> it is a laptime (unless they suddenly have a kart with number over 999, but strongly doubt that)
                
                #first check if this wasn't the last one to parse
                if all_lines[index].__contains__("270cc") or len(all_lines[index]) < 4:
                    #end of lap times or new kart -> save and check which one of the two it was
                    karting_db.store_lap_times(kartnr,driver_name,laptimes,session_id)
                    laptimes = []
                    identifier_index = 0
                    if all_lines[index].__contains__("270cc"):
                        return 0#OK
                else:
                    #laptime
                    laptimes.append(all_lines[index])
                    index += 1
                    
            else:
                if identifier_index == 0:
                    kartnr = int(all_lines[index])
                elif identifier_index == 1:
                    driver_name = all_lines[index]
            


                identifier_index += 1
                index += 1


def get_start_lap_times(all_lines):
    index = 0
    check_nr = 1
    for line in all_lines:
        if line == str(check_nr):
            if str(check_nr) == str(10):
                #all numbers between 1 and 10 were present -> found the karting times header
                return index + 1
            check_nr += 1
        else:
            check_nr = 1

        index += 1
    return -1



#returns the session id of the session
def parse_session_info(all_lines):
    session_info_line = get_session_info_line(all_lines) + 1
    if session_info_line == -1:
        #couldn't find session info -> somethings wrong
        print("Failed to parse the mail")
        return -1
    else:
        return karting_db.store_session_info(all_lines[session_info_line])


def get_session_info_line(all_lines):
    line_index = 0
    for line in all_lines:
        if line.__contains__("hier zijn jouw"):
            return line_index
        line_index += 1
    else:
        return -1




def myprint(str,karting_manager):
    to_print = str.encode('cp932','replace').decode('cp932')
    karting_manager.add_string(to_print)



#
# search mails in IMAP
#
def search_imap(karting_manager):
    #mail = imaplib.IMAP4_SSL("imap.mail.com", 993)
    mail = imaplib.IMAP4_SSL("imap.gmail.com")

    mail.login(credentials.get_email(),credentials.get_app_password())
    mail.list()
    mail.select('Inbox') # specify inbox

    typ, [data] = mail.search(None, "UNSEEN")

    # for each mail searched
    for num in data.split():

        # fetch whole message as RFC822 format
        result, d = mail.fetch(num, "(RFC822)")
        msg = email2Text(d[0][1])
        myprint(msg["subject"],karting_manager)
        myprint(msg["date"],karting_manager)
        myprint(msg["from"],karting_manager)
        myprint(msg["body"],karting_manager)
        karting_manager.start_parser()

    # closing
    mail.close()
    mail.logout()

#
# Get subject, date, from and body as text from email RFC822 style string
#
def email2Text(rfc822mail):
        # parse the message
        msg_data = email.message_from_bytes(rfc822mail, policy=email.policy.default)
        
        mail_value = {}

        # Get From, Date, Subject
        mail_value["from"] = header_decode(msg_data.get('From'))
        mail_value["date"] = header_decode(msg_data.get('Date'))
        mail_value["subject"] = header_decode(msg_data.get('Subject'))
        

        # Get Body
        #print("--- body ---")
        mail_value["body"] = ""
        if msg_data.is_multipart():
            for part in msg_data.walk():
                #print("--- part ---")
                ddd = msg2bodyText(part)
                if ddd is not None:
                    mail_value["body"] = mail_value["body"] + ddd
        else:
            #print("--- single ---")
            ddd = msg2bodyText(msg_data)
            mail_value["body"] = ddd

        return mail_value

#
# get body text from a message (EmailMessage instance)
#
def msg2bodyText(msg):
    ct = msg.get_content_type()
    cc = msg.get_content_charset() # charset in Content-Type header
    cte = msg.get("Content-Transfer-Encoding")

    # skip non-text part/msg
    if msg.get_content_maintype() != "text":
        return None

    # get text
    ddd = msg.get_content()

    # html to text
    if msg.get_content_subtype() == "html":
        try:
            #print("had html as subtype")
            ddd = html2text.html2text(ddd)
        except:
            print("error in html2text")

    return ddd


def header_decode(header):
    hdr = ""
    for text, encoding in email.header.decode_header(header):
        if isinstance(text, bytes):
            text = text.decode(encoding or "us-ascii")
        hdr += text
    return hdr


def check_for_new_track_layout():
    track_url = "https://extremekart.be/karting/circuit-karts/"
    response = requests.get(track_url)
    if response.ok:
        try:
            soup = BeautifulSoup(response.text,'html.parser')
            image_url = soup.find("div",{"class":"vc_single_image-wrapper"}).find("img").get("src")
            image = requests.get(image_url).content
            karting_db.update_track_layout(image_url,image)
            #store image in db if it is a new one, and set the one that has the latest start time's end time to today as well
            #best to check if new layout based on link name and not on the image itself
        except:
            print("failed to get the new tracklayout")
            print(traceback.print_exc())
            return





def main():
    print("Starting karting_tracker")
    karting_db.create_tables_if_dont_exist()
    check_for_new_track_layout()
    kartingManager = KartingManager()
    search_imap(kartingManager)
    print("Closing karting_tracker")
    