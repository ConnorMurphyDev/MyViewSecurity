import os.path
from datetime import datetime

"""
for x in os.listdir("Faces/"):
    if x.endswith(".jpg"):
        print(x)
"""

"""
if os.path.isfile("securityLog.db"):
    print("It exist")
else:
    print("It does not exist")
"""


now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %I:%M:%S %p")
print("date and time =", dt_string)