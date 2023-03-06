# MyViewSecurity
Welcome to My View Security, a home surveillance system designed to capture live video and recognize faces using Pyqt5, Face_recognition, and cv2. This prototype system is designed to enhance home security while also preserving privacy.

The system is designed to capture live video and recognize faces in real-time, saving data to a local SQLite database for easy access. When the system recognizes a person, it captures their name, photo, and timestamp and stores it in the database. The system also allows the user to sort the database by date and view photos of recognized individuals.

Here are some of the technical details of this project:

➊ Uses Pyqt5 for the graphical user interface (GUI)

➋ Uses the Face_recognition library for face recognition

➌ Uses cv2 for capturing live video

➍ Saves data to a local SQLite database

➎ Works with both wired and wireless IP cameras

➏ Passes video frames between the recorder and GUI using threads

Future updates for My View Security I have in the pipeline:

- Migrating from threading to multi-processing for video processing, resulting in improved performance.
- Implementing enhanced facial detection capabilities to prevent the system from being tricked with static images.
- Adding additional camera settings to provide more control over the system.
- Completing AWS integration, allowing for seamless access to updates from anywhere.
- Improving the style of the GUI for a more user-friendly experience.

Stay tuned for these exciting updates, as I continue to develop My View Security to be the ultimate home surveillance solution.




![Gui Screenshot](https://i.imgur.com/D08Onup.png)
