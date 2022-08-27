import sqlite3

class Recipient():
    def __init__(self,id,name,mail,preference) -> None:
        self.id = id
        self.name = name
        self.mail = mail
        self.preference = preference


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





CREATE_STATEMENT = 'CREATE TABLE "recipient" ("Id"	INTEGER NOT NULL,"Name"	TEXT NOT NULL,"mail"	TEXT NOT NULL,"preference"	TEXT NOT NULL,PRIMARY KEY("Id" AUTOINCREMENT))'
TABLE_REC = "recipient"
DB_REF = "../notifier.db"