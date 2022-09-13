import traceback

  
class LapsDriver():
    def __init__(self,driver_id,driver_name,kart_nr) -> None:
        self.driver_id = driver_id
        self.driver_name = driver_name
        self.kart_nr = kart_nr
        self.laptimes = []

    #important that give them in chronological order
    def add_laptime_as_string(self,laptime):
        try:
            lap_int = int(laptime)
            self.laptimes.append(lap_int)
        except:
            print(traceback.print_exc())

    def get_as_json(self):
        return {
            "driver_id":self.driver_id,
            "driver_name":self.driver_name,
            "kart_nr":self.kart_nr,
            "laptimes":self.laptimes
        }


class Session():
    def __init__(self,sesion_id,timestamp,track_id):
        self.session_id = sesion_id
        self.timestamp = timestamp
        self.track_id = track_id
        self.laps:list[LapsDriver] = []

    def add_drivers_laps(self,laps:LapsDriver):
        self.laps.append(laps)

    def get_as_json(self):
        lap_list = []
        for lap in self.laps:
            lap_list.append(lap.get_as_json())

        json_dict = {
            "session":{
                "session_id":self.session_id,
                "timestamp":self.timestamp,
                "track_id":self.track_id,
                "drivers_laps":lap_list
            }
        }
        return json_dict