from . import game_reader

from schedule import Scheduler,CancelJob
import threading
import time
#method below from stack overflow: https://stackoverflow.com/questions/44896618/django-run-a-function-every-x-seconds



def run_continuously(self, interval=1):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run

Scheduler.run_continuously = run_continuously




def start_scheduler():
    scheduler = Scheduler()
    scheduler.run_continuously()
    scheduler.every(4).hours.do(game_reader.main)
    start_one_time_job(scheduler,game_reader.main)
    


#one time job is basically just so that a task can be start right after boot as well
def start_one_time_job(scheduler:Scheduler,function):
    scheduler.every(10).seconds.do(self_destroying_call,function=function)
    

def self_destroying_call(function):
    function()
    return CancelJob