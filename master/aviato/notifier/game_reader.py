"""
Module that will scan the reddit subreddit r/GameDeals and return all the free games that it could find

--------------------------------------------------------------------------------------------------------------------

# docs: https://praw.readthedocs.io/en/stable/code_overview/models/submission.html?highlight=submission#praw.models.Submission

#gmail acces, gaat ge wrs op een gegeven moment eens moeten doen vrees ik
#https://developers.google.com/gmail/api/quickstart/python
"""

from genericpath import exists
from logging import exception
import pickle
import praw
import time
import os
import sys
import re

from . import credentials
from . import gamedeal_mailer
from .containers import freeGame

UTC_PICKLE_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'gameDealsFiles','utc.pk'))
STDERR_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'gameDealsFiles','stderror.log'))




def changeStdOut():
    sys.stderr = open(STDERR_PATH,'w+')
    return

def storeUTC(curr_time):
    with open(UTC_PICKLE_PATH, 'wb+') as pick:
        pickle.dump(int(curr_time), pick)
        pick.close()
    return

def loadUTC():
    #first check if file exists, if not this is the first time the script is run -> create one with current utc
    #and stop the program

    current_time = time.time()-1

    if not exists(UTC_PICKLE_PATH):
        storeUTC(current_time)
        return -1
    #else, just continue and open the file 

    with open(UTC_PICKLE_PATH, 'rb+') as pick:
        try:
            new_time = pickle.load(pick)
            pick.close()
            storeUTC(current_time)
            return new_time
        except EOFError:
            return -1


def getFromReddit():
    freeGames = []
    lastCheckTime = 0#loadUTC()
    if lastCheckTime == -1:
        #first time checking, we could check every game or we could just stop
        exit(99999)
    wereChanges = False
    reddit = praw.Reddit(client_id=credentials.reddit_client_id(), client_secret=credentials.reddit_client_secret(),
                         user_agent=credentials.reddit_user_agent())
    reddit.read_only = True
    for submissions in reddit.subreddit("GameDeals").new(limit=100):
        if submissions.created_utc > lastCheckTime:
            # game hasn't been checked before
            game = checkSubmission(submissions)
            if game is not None:
                freeGames.append(game)
                wereChanges = True
        else:
            # checked all new ones
            if wereChanges:
                print("Checked all the new ones")
            else:
                print("No new games were found")
            return freeGames
    # stopped checking because passed limit
    print("There were new submissions that haven't been checked yet")
    return freeGames

def checkSubmission(submission):
    # get category
    s = str(submission.title)
    s = s.lower()
    s = s.replace("free demo","")
    if s.__contains__("Free") or s.__contains__("FREE") or s.__contains__("free") or s.__contains__("100%"):
        if containsException(s):
            return None
        category = s[s.find("[") + len("["):s.rfind("]")]
        target = "[" + str(category) + "] "
        title = str.replace(submission.title, target, "")
        return freeGame(category, title, submission.permalink)
    else:
        return None

def containsException(target):
    if re.search("Free Weekend", target, re.IGNORECASE):
        # steam free weekend trigger -> not important
        return True
    control = "free"
    match = target.lower().find(control)
    if (match == -1) or (match-1)<0 or (match+len(control))>(len(target)-1):
        return False
    else:
        if target[match-1].isalpha() or target[match+len(control)].isalpha():
            #the character is a letter thus meaning that free is used in a word like freedom
            return True
        return False

def sendGames(freeGames):
    print("Going to sort the games")
    try:
        mailer = gamedeal_mailer.GameDealMailSender()
        for free_game in freeGames:
            mailer.add_new_deal(free_game)
        mailer.send_mail()
    except Exception as e:
        print(str(e))




def main():
    print("Starting gamedeals checker")
    #changeStdOut()
    freeGames = getFromReddit()
    sendGames(freeGames)
    print("gamedeals checker shutting down")
    return