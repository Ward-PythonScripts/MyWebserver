import sqlite3
import traceback
from datetime import datetime
from .container import LapsDriver,Session


def get_driver_name(driver_id,cursor):
    try:
        select_stmt = "Select name from Driver where ID=?"
        result = cursor.execute(select_stmt,[driver_id]).fetchone()
        return result[0]
    except:
        print(traceback.print_exc())
        cursor.close()

def get_driver_id(driver_name):
    try:
        conn = sqlite3.connect(DB_REF)

        result = conn.execute("Select * from " + TABLE_DRIVER + " where name=\"" + str(driver_name) + "\"").fetchone()
        if result is None or len(result) == 0:
            #driver wasn't yet present
            create_stmt = "INSERT INTO " + TABLE_DRIVER + " (name) VALUES (?)"
            cursor = conn.cursor()
            cursor.execute(create_stmt,[driver_name])
            conn.commit()
            id = cursor.lastrowid
            cursor.close()
        else:
            #driver was already present
            id = result[0]
        conn.close()
        return id
    except Exception as e:
        print(traceback.print_exc())
        conn.close()  



def get_track_id_from_session(session_id):
    try:
        conn = sqlite3.connect(DB_REF)

        result = conn.execute("Select * from " + TABLE_SESSION + " where Id=" + str(session_id)).fetchone()
        track_id = result[2]
        conn.close()
        return track_id
    except Exception as e:
        print(traceback.print_exc())
        conn.close()




def store_track_record(record):
    try:
        conn = sqlite3.connect(DB_REF)
        create_stmt = "INSERT INTO " + TABLE_TRACK_RECORD + " (driver_id,laptime,track_id) VALUES (?,?,?)"
        cursor = conn.cursor()
        cursor.execute(create_stmt,[record.get("driver_id"),record.get("laptime"),record.get("track_id")])
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(traceback.print_exc())
        conn.close()


def store_lap_times(kart_nr,driver_name,laptimes,session_id):    
    try:
        conn  = sqlite3.connect(DB_REF)

        driver_id = get_driver_id(driver_name)

        store_kart(kart_nr,session_id,driver_id)

        insert_stmt = "INSERT INTO " + TABLE_LAP + " (session_id,laptime_millis,lap_of_session,driver_id) VALUES (?,?,?,?)"
        cursor = conn.cursor()
        lap_of_session = 1
        for laptime in laptimes:
            laptime_millis = convert_lap_to_millis(laptime)
            if laptime_millis != -1: #else error code
                cursor.execute(insert_stmt,[session_id,laptime_millis,lap_of_session,driver_id])
                conn.commit()

            lap_of_session += 1
        cursor.close()
        conn.close()
    except:
        print(traceback.print_exc())
        conn.close()
        


def convert_lap_to_millis(laptime):
    try:
        temp_string = ""
        time_in_millis = 0
        for char in laptime:
            if char == ':':
                time_in_millis += int(temp_string)*60*1000
                temp_string = ""
            elif char == '.' or char == ',':
                time_in_millis += int(temp_string)*1000
                temp_string = ""
            else:
                temp_string += char
        time_in_millis += int(temp_string)
        return time_in_millis
    except:
        print(traceback.print_exc())
        return -1


def store_kart(kart_nr,session_id,driver_id):
    try:
        conn = sqlite3.connect(DB_REF)
        create_stmt = "INSERT INTO " + TABLE_KART + " (driver_id,session_id,kart_nr) VALUES (?,?,?)"
        cursor = conn.cursor()
        cursor.execute(create_stmt,[driver_id,session_id,kart_nr])
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(traceback.print_exc())
        conn.close()


def store_session_info(session_info_string): #returns session id it just created, or -1 if session already exists
    is_still_session_nr = True
    is_still_hours = True
    is_still_minutes = True
    is_still_day = True
    is_still_month = True
    is_still_year = True
    was_nr = False
    temp_string = ""
    for char in session_info_string:
        #example is: Sessie 55 - 21:30 - 24/08/2022 to 21:31 (Kartbaan)   
        try:
            int(char)
            temp_string += char
            was_nr = True
        except:
            try:
                #wasn't a number
                if was_nr:
                    if is_still_session_nr:
                        #session nr is in the temp string
                        session_nr = int(temp_string)
                        is_still_session_nr = False
                    elif is_still_hours:
                        session_hours = int(temp_string)
                        is_still_hours = False
                    elif is_still_minutes:
                        session_minutes = int(temp_string)
                        is_still_minutes = False
                    elif is_still_day:
                        session_day = int(temp_string)
                        is_still_day = False
                    elif is_still_month:
                        session_month = int(temp_string)
                        is_still_month = False
                    elif is_still_year:
                        session_year = int(temp_string)
                        is_still_year = False
                        break
                was_nr = False
                temp_string = ""
                pass
            except:
                print(traceback.print_exc())
    #convert time to epoch in minutes
    time_session = datetime(year=session_year,month=session_month,day=session_day,hour=session_hours,minute=session_minutes)
    session_time_stamp = round(time_session.timestamp())
    try:
        conn = sqlite3.connect(DB_REF)
        cursor = conn.cursor()
        #first check if the session wasn't yet present in the database
        select_stmt = "Select * from " + TABLE_SESSION + " where timestamp=?"
        result = cursor.execute(select_stmt,[session_time_stamp]).fetchone()
        if result is None or len(result) == 0:
            #session hasn't been stored yet -> start storing it
            print("Storing session of",session_time_stamp,time_session)
            create_statment = "INSERT INTO " + TABLE_SESSION + " (timestamp,track_id) VALUES (?,?)"
            cursor.execute(create_statment,[session_time_stamp,get_current_track()])
            conn.commit()
            session_id = cursor.lastrowid
            cursor.close()
            conn.close()
            return session_id
        else:
            print("Already stored session of",session_time_stamp,time_session)
            return -1

    except:
        print(traceback.print_exc())
        conn.close()
        return -1

def get_current_track():
    try:
        conn = sqlite3.connect(DB_REF)
        result = conn.execute("Select ID,MAX(end_date) from " + TABLE_TRACK).fetchone()
        track_id = result[0]
        conn.close()
        return track_id
    except Exception as e:
        print(traceback.print_exc())
        conn.close()

def get_track_layout(track_id):
    try:
        conn = sqlite3.connect(DB_REF)
        result = conn.execute("Select layout_image from " + TABLE_TRACK + " where ID="+str(track_id)).fetchone()
        image = result[0]
        conn.close()
        return image
    except Exception as e:
        print(traceback.print_exc())
        conn.close() 

def update_track_layout(image_url,image):
    try:
        conn = sqlite3.connect(DB_REF)
        search_statement = "Select * from " + TABLE_TRACK + " where layout_url = ?"
        cursor = conn.cursor()
        result = cursor.execute(search_statement,[image_url]).fetchone()
        if result is None or len(result) == 0:
            timestamp_now = round(datetime.now().timestamp())
            #first update the track where end_time is still not none
            update_stmt = "UPDATE " + TABLE_TRACK + " SET end_date=? where end_date=NULL"
            cursor.execute(update_stmt,[timestamp_now])
            conn.commit()
            #track was not present -> new track was found
            create_stmt = "INSERT INTO " + TABLE_TRACK + " (begin_date,layout_image,layout_url) VALUES (?,?,?)"
            cursor.execute(create_stmt,[timestamp_now,image,image_url])
            conn.commit()
        cursor.close()
        conn.close()
    except:
        print(traceback.print_exc())
        cursor.close()
        conn.close()
            
def get_sessions_as_objects():
    try:
        conn = sqlite3.connect(DB_REF)
        #get all sesions
        search_stmt = "SELECT * from " + TABLE_SESSION
        cursor = conn.cursor()
        results = cursor.execute(search_stmt).fetchall()
        session_list = []
        for result in results:
            session_id = result[0]
            timestamp = result[1]
            track_id = result[2]
            new_session = Session(session_id,timestamp,track_id)
            session_list.append(new_session)
            #get all the drivers that have driven on this session and all the laps that they have driven
            driver_ids = get_drivers_in_session(session_id=session_id,cursor=cursor)
            for driver_id in driver_ids:
                driver_name = get_driver_name(driver_id,cursor)
                kart_used = get_drivers_kart_in_session(driver_id=driver_id,session_id=session_id,cursor=cursor)
                laps = get_drivers_laps_in_session(driver_id,session_id,cursor)
                new_laps_driver = LapsDriver(driver_id=driver_id,driver_name=driver_name,kart_nr=kart_used)
                for lap in laps:
                    new_laps_driver.add_laptime_as_string(lap)
                new_session.add_drivers_laps(new_laps_driver)
        return session_list

    except:
        print(traceback.print_exc())
        cursor.close()
        conn.close()


def get_drivers_laps_in_session(driver_id,session_id,cursor):
    try:
        stmt = "Select laptime_millis from " + TABLE_LAP + " where driver_id=? and session_id=?"
        results = cursor.execute(stmt,[driver_id,session_id])
        laps = []
        for result in results:
            laps.append(result[0])
        return laps
    except:
        print(traceback.print_exc())
        cursor.close()


def get_drivers_in_session(session_id,cursor):
    try:
        get_drivers_stmt = "Select DISTINCT(driver_id) from Lap where session_id=? order by driver_id,lap_of_session"
        drivers = cursor.execute(get_drivers_stmt,[session_id]).fetchall()
        driver_ids = []
        for driver in drivers:
            driver_ids.append(driver[0])
        return driver_ids
    except:
        print(traceback.print_exc())
        cursor.close()




def get_drivers_kart_in_session(driver_id,session_id,cursor):
    try:
        get_kart_stmt = "Select kart_nr from " + TABLE_KART + " where driver_id=? and session_id=?"
        result = cursor.execute(get_kart_stmt,[driver_id,session_id]).fetchone()
        return result[0]
    except:
        print(traceback.print_exc())
        cursor.close()

def get_all_drivers():
    try:
        get_drivers_stmt = "Select * from Driver order by name asc"
        conn = sqlite3.connect(DB_REF)
        results = conn.execute(get_drivers_stmt).fetchall()
        driver_names = []
        for result in results:
            driver_names.append({
                "name":result[1],
                "id":result[0]
                })
        return driver_names
    except:
        print(traceback.print_exc())
        return None


def get_driver_like(target_string):
    try:
        get_driver_like_stmt = 'Select * from Driver where name like("%' + str(target_string) + '%") order by name asc'
        conn = sqlite3.connect(DB_REF)
        results = conn.execute(get_driver_like_stmt).fetchall()
        driver_names = []
        for result in results:
            driver_names.append({
                "name":result[1],
                "id":result[0]
                })
        return driver_names
    except:
        print(traceback.print_exc())
        return None

def get_driver_id_from_name(driver_name):
    try:
        get_driver_like_stmt = 'Select ID from Driver where name="'+str(driver_name)+'"'
        conn = sqlite3.connect(DB_REF)
        results = conn.execute(get_driver_like_stmt).fetchone()
        return results[0]
    except:
        print(traceback.print_exc())
        return None

def get_driver_name_from_id(driver_id):
    try:
        get_driver_like_stmt = 'Select name from Driver where ID='+str(driver_id)
        conn = sqlite3.connect(DB_REF)
        results = conn.execute(get_driver_like_stmt).fetchone()
        return results[0]
    except:
        print(traceback.print_exc())
        return None


CREATE_TABLE_DRIVER = """CREATE TABLE "Driver" (
	"ID"	INTEGER,
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("ID" AUTOINCREMENT)
)"""
CREATE_TABLE_KART = """CREATE TABLE "Kart" (
	"ID"	INTEGER,
	"driver_id"	INTEGER,
	"session_id"	INTEGER,
	"kart_nr"	INTEGER,
	FOREIGN KEY("driver_id") REFERENCES "Driver"("ID"),
	FOREIGN KEY("session_id") REFERENCES "Session"("ID"),
	PRIMARY KEY("ID" AUTOINCREMENT)
)"""
CREATE_TABLE_LAP = """CREATE TABLE "Lap" (
	"ID"	INTEGER,
	"session_id"	INTEGER,
	"laptime_millis"	INTEGER NOT NULL,
	"lap_of_session"	INTEGER NOT NULL,
	"driver_id"	INTEGER,
	PRIMARY KEY("ID" AUTOINCREMENT),
	FOREIGN KEY("driver_id") REFERENCES "Driver"("ID"),
	FOREIGN KEY("session_id") REFERENCES "Session"("ID")
)"""
CREATE_TABLE_SESSION = """CREATE TABLE "Session" (
	"ID"	INTEGER,
	"timestamp"	INTEGER,
	"track_id"	INTEGER,
	FOREIGN KEY("track_id") REFERENCES "Track"("ID"),
	PRIMARY KEY("ID" AUTOINCREMENT)
)"""
CREATE_TABLE_TRACK = """CREATE TABLE "Track" (
	"ID"	INTEGER,
	"begin_date"	INTEGER NOT NULL,
	"end_date"	INTEGER NOT NULL,
	"layout_image"	BLOB,
	"layout_url"	TEXT,
	PRIMARY KEY("ID" AUTOINCREMENT)
)"""
CREATE_TABLE_TRACK_RECORD = """CREATE TABLE "Track_Record" (
	"ID"	INTEGER,
	"driver_id"	INTEGER,
	"laptime"	INTEGER,
	"track_id"	INTEGER,
	FOREIGN KEY("track_id") REFERENCES "Track"("ID"),
	FOREIGN KEY("driver_id") REFERENCES "Driver"("ID"),
	PRIMARY KEY("ID" AUTOINCREMENT)
)"""

TABLE_DRIVER = "Driver"
TABLE_KART = "Kart"
TABLE_LAP = "Lap"
TABLE_SESSION = "Session"
TABLE_TRACK = "Track"
TABLE_TRACK_RECORD = "Track_Record"

DB_REF = "../karting.db"