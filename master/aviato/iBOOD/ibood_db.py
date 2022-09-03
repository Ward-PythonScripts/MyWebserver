from imp import SEARCH_ERROR
import sqlite3
import traceback


from .container import Recipient


def get_all_recipients():
    try:
        conn = sqlite3.connect(DB_REF)

        recipients = []
        results = conn.execute("Select * from " + TABLE_REC).fetchall()
        for row in results:
            id = row[0]
            name = row[1]
            mail = row[2]
            preference = row[3]
            recipients.append(Recipient(id,name,mail,preference))
        conn.close()
        return recipients
    except Exception as e:
        print(traceback.print_exc())
        conn.close()
    
def remove_recipient(id):
    try:
        conn = sqlite3.connect(DB_REF)
        delete_statement = "delete FROM "+TABLE_REC+" where id=?"
        cursor = conn.cursor()
        cursor.execute(delete_statement,(str(id),))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(str(e))
        conn.close()

def add_recipient(name,mail):
    try:
        conn = sqlite3.connect(DB_REF)
        create_statement = "INSERT INTO " + TABLE_REC + " (Name,mail) VALUES (?,?)"
        cursor = conn.cursor()
        cursor.execute(create_statement,[name,mail])
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(str(e))
        conn.close()


def update_recipient(name,mail,id):
    try:
        conn = sqlite3.connect(DB_REF)
        update_statement = "UPDATE " + TABLE_REC + " SET Name = ?, mail = ? Where Id = ?"
        cursor = conn.cursor()
        cursor.execute(update_statement,[name,mail,id])
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(str(e))
        conn.close()

def add_search(recipient_Id,search_action):
    try:
        conn = sqlite3.connect(DB_REF)
        create_statement = "INSERT INTO " + TABLE_SEARCH + " (recipient_Id,search_action) VALUES (?,?)"
        cursor = conn.cursor()
        cursor.execute(create_statement,[recipient_Id,search_action])
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(str(e))
        conn.close()

def remove_recipient(id):
    try:
        conn = sqlite3.connect(DB_REF)
        delete_statement = "delete FROM "+TABLE_SEARCH+" where id=?"
        cursor = conn.cursor()
        cursor.execute(delete_statement,(str(id),))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(str(e))
        conn.close()

def update_search(string_json,id):
    try:
        conn = sqlite3.connect(DB_REF)
        update_statement = "UPDATE " + TABLE_SEARCH + " SET search_action = ? Where Id = ?"
        cursor = conn.cursor()
        cursor.execute(update_statement,[string_json,id])
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(str(e))
        conn.close()

def get_int_from_bool(bool):
    if bool:
        boolint = 1
    else:
        boolint = 0
    return boolint



def change_item_soldout_from_name(name,soldout):
    soldout_int = get_int_from_bool(soldout)
    try:
        conn = sqlite3.connect(DB_REF)
        update_statement = "UPDATE " + TABLE_ITEM + " SET Soldout = ? Where Name = ?"
        cursor = conn.cursor()
        cursor.execute(update_statement,[soldout_int,name])
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(str(e))
        conn.close()

def create_item_and_add_to_history(name,curr_price,advice_price,discount_percentage,image_url,image,link,soldout,recipient_id):
    #initialize
    item_id = -1
    #first check if the item was already created, no need to create anymore otherwise
    if not item_already_present(name,link):
        soldout_int = get_int_from_bool(soldout)
        try:
            conn = sqlite3.connect(DB_REF)
            create_statement = "INSERT INTO " + TABLE_ITEM + " (Name,Curr_Price,Advice_Price,Discount_Percentage,Image_URL,Image,Link,Soldout) VALUES (?,?,?,?,?,?,?,?)"
            cursor = conn.cursor()
            cursor.execute(create_statement,[name,curr_price,advice_price,discount_percentage,image_url,image,link,soldout_int])
            conn.commit()
            item_id = cursor.lastrowid
            cursor.close()
            conn.close()
        except Exception as e:
            print(str(e))
            conn.close()
    
    #then add to history, but first check if we still need to go and find the cursor_id
    if item_id == -1:
        item_id = get_id_from_item_name_and_link(name,link)

    #add to history
    add_to_history(item_id,recipient_id)

    
def add_to_history(item_id,recipient_id):
        try:
            conn = sqlite3.connect(DB_REF)
            create_statement = "INSERT INTO " + TABLE_HISTORY + " (recipient_Id,item_Id) VALUES (?,?)"
            cursor = conn.cursor()
            cursor.execute(create_statement,[recipient_id,item_id])
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(traceback.print_exc())
            conn.close()


def get_id_from_item_name_and_link(name,link):
    try:
        conn = sqlite3.connect(DB_REF)
        create_statement = "Select Id from " + TABLE_ITEM + " where name = ? and link = ?"
        cursor = conn.cursor()
        result = cursor.execute(create_statement,[name,link]).fetchone()
        cursor.close()
        conn.close()
        return int(result[0])
    except Exception as e:
        print(traceback.print_exc())
        conn.close()


def item_already_present(name,link):
    try:
        conn = sqlite3.connect(DB_REF)
        select_stmt = "Select * from " + TABLE_REC+ " where Name = ? and Link = ?"
        cursor = conn.cursor()
        results = cursor.execute(select_stmt,[name,link]).fetchall()
        if results is not None:
            conn.close()
            return True
        else:
            conn.close()
            return False
    except Exception as e:
        print(traceback.print_exc())
        conn.close()    

CREATE_RECIPIENT_TABLE = """CREATE TABLE "recipient" (
	"Id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"mail"	TEXT NOT NULL,
	PRIMARY KEY("Id" AUTOINCREMENT)
)"""

CREATE_SEARCH_TABLE = """CREATE TABLE "search" (
	"Id"	INTEGER,
	"recipient_Id"	INTEGER NOT NULL,
	"search_action"	TEXT NOT NULL DEFAULT '{}',
	PRIMARY KEY("Id" AUTOINCREMENT)
)"""

CREATE_ITEM_TABLE = """CREATE TABLE "item" (
	"Id"	INTEGER,
	"Name"	TEXT,
	"Curr_Price"	REAL,
	"Advice_Price"	REAL,
	"Discount_Percentage"	REAL,
	"Image_URL"	TEXT,
	"Image"	BLOB,
	"Link"	TEXT,
	"Soldout"	INTEGER,
	PRIMARY KEY("Id" AUTOINCREMENT)
)"""

CREATE_HISTOREY_TABLE = """CREATE TABLE "history" (
	"Id"	INTEGER,
	"recipient_Id"	INTEGER NOT NULL,
	"item_Id"	INTEGER,
	PRIMARY KEY("Id" AUTOINCREMENT)
)"""

TABLE_REC = "recipient"
TABLE_ITEM = "item"
TABLE_SEARCH = "search"
TABLE_HISTORY = "history"

DB_REF = "../idoob.db"