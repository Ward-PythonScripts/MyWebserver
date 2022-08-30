import sqlite3
import json

from .containers import Recipient
    


def get_all_recipients():
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
        
def remove_recipient(id):
    conn = sqlite3.connect(DB_REF)
    delete_statement = "delete FROM recipient where id=?"
    cursor = conn.cursor()
    cursor.execute(delete_statement,(str(id),))
    conn.commit()
    cursor.close()
    conn.close()

def add_recipient(name,mail):
    conn = sqlite3.connect(DB_REF)
    create_statement = "INSERT INTO " + TABLE_REC + " (Name,mail) VALUES (?,?)"
    cursor = conn.cursor()
    cursor.execute(create_statement,[name,mail])
    conn.commit()
    cursor.close()
    conn.close()

def update_recipient(name,mail,id):
    conn = sqlite3.connect(DB_REF)
    update_statement = "UPDATE " + TABLE_REC + " SET Name = ?, mail = ? Where Id = ?"
    cursor = conn.cursor()
    cursor.execute(update_statement,[name,mail,id])
    conn.commit()
    cursor.close()
    conn.close()




CREATE_STATEMENT = """CREATE TABLE "recipient" (
	"Id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"mail"	TEXT NOT NULL,
	"preference"	TEXT NOT NULL DEFAULT '{"allowed":"all","denied":"none"}',
	PRIMARY KEY("Id" AUTOINCREMENT)
)"""
TABLE_REC = "recipient"
DB_REF = "../notifier.db"