from pushbullet import Pushbullet
import datetime
from datetime import timedelta

API_KEY = "o.PJ7dJ6coH87Bdo9ronFTuFnu7D9go0Yj"

def pushToPhone(name):
        
    pb = Pushbullet(API_KEY)
    pb.push_note('Security Camera', name + " was seen by camera 1")


# Returns true if a notification has not been pushed in the last 5 minutes
def recentPushCheck(currentTime):

    if currentTime == None or datetime.datetime.now() > currentTime + timedelta(minutes = 5):
        return True