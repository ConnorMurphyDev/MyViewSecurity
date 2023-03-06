#Inactive, kept for reference for future updates.
#Example of pushing notifications to phones

from pushbullet import Pushbullet
import datetime
from datetime import timedelta

API_KEY = "UNKOWN"

def pushToPhone(name):
        
    pb = Pushbullet(API_KEY)
    pb.push_note('Security Camera', name + " was seen by camera 1")


# Returns true if a notification has not been pushed in the last 5 minutes
def recentPushCheck(currentTime):

    if currentTime == None or datetime.datetime.now() > currentTime + timedelta(minutes = 5):
        return True