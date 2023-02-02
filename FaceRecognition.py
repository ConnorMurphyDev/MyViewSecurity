# NEEDED UPDATES
# Improve identification with more samples for each person
# Change 5 minute delay between notifications to be name specific
# Change notifications to say who was identified


from datetime import timedelta, datetime

import face_recognition
import cv2
import numpy as np

from PushNotification import *

import os

import sqlite3

import localDataFuntions



"""
#UPDATE: base for sending info to servers later on
def sendNameToServer(name):
    print(name)
"""


"""
# UPDATE: to pull multiple faces in future update

def retrieveFaces():
    for x in os.listdir("Faces/"):
        if x.endswith(".jpg"):
            print(x)
 """







# Sets up / connects to local DB
cursor, connection = localDataFuntions.localDatabaseConnect()


# For current version, this pulls the video from the webcam. "To open default camera using default backend just pass 0"
video_capture = cv2.VideoCapture(0)



#Only gets the jpeg files
files = [file for file in os.listdir("Faces/") if file.endswith(('.jpeg', '.jpg'))]
faceImages = [None] * len(files)
known_face_encodings = [None] * len(files)
known_face_names = [os.path.splitext(file)[0] for file in files]


# Create arrays of known face encodings and their names.
i = 0
while i < len(files):
    faceImages[i] = face_recognition.load_image_file("Faces/" + files[i])
    known_face_encodings[i] = face_recognition.face_encodings(faceImages[i])[0]
    i = i + 1



"""
OLD NOT YET REMOVED FOR REFERENCE
# Import a facial image and learn to identify it.
connor_image = face_recognition.load_image_file("Faces/Connor1.jpg")
connor_face_encoding = face_recognition.face_encodings(connor_image)[0]

# Create arrays of known face encodings and their names. Add more later by simply adding a comma between names.
known_face_encodings = [
    connor_face_encoding
]
known_face_names = [
    "Connor M"
]
"""




face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

currentTime = None

while True:
    # Returns one frame at a time. "video_capture.read: Grabs, decodes and returns the next video frame"
    ret, frame = video_capture.read()

    # Only process every other frame
    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"




            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    #Switchinges between True and False to only process every other frame
    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        #Saves names and timestamps to the local SQLite Database
        localDataFuntions.updateLocalDatabase(cursor,connection,name, frame)
        #i added frame

        """
        #UPDATE: TO SEND PUSH NOTIFICATIONS IN FUTURE UPDATE
        #Pushes Notification to phone if one has not been sent in the last 5 minutes
        #if currentTime == None or datetime.datetime.now() > currentTime + timedelta(minutes = 5):
        #if recentPushCheck(currentTime):    
        #    pushToPhone(name)
        #currentTime = datetime.datetime.now()
        """

    # Display the resulting image
    cv2.imshow('Video', frame)

    
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

