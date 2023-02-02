import os.path
from datetime import datetime
import os



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

"""
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %I:%M:%S %p")
print("date and time =", dt_string)
"""
"""
files = os.listdir("Faces/")
print(files)
print(type(files))
print(files[0])
print(str(files[0]))
"""

"""
#Only gets the jpeg files
files = [file for file in os.listdir("Faces/") if file.endswith(('.jpeg', '.jpg'))]
print(files)
print(files[0])
print(type(files))
print(len(files))


for i in files:
    print(i)

print(type(files[0]))

no_extension_list = [os.path.splitext(file)[0] for file in files]


i = 0
while i < len(files):
    print("Faces/" + files[i])
    i = i + 1

print("Also hello")
"""


print(hash("02/02/2023 04:03:36 PM"))
print(hash("02/02/2023 04:03:36 PM"))