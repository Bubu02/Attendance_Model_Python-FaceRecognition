import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime
import time
import pyttsx3
import pywhatkit as kit
import json

def say_name(name):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # Use the second voice (usually female on Windows)
    engine.setProperty('voice', voices[1].id)
    engine.say("Identification confirmed as " + name)
    engine.runAndWait()



video_capture = cv2.VideoCapture(0)

# Load images and create encodings
photo_dir = "photos"
known_face_encodings = []
known_face_names = []
# Load student names and phone numbers from a JSON file
with open('students_phone_numbers.json', 'r') as f:
    students_phone_numbers = json.load(f)
for filename in os.listdir(photo_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        name = os.path.splitext(filename)[0]
        image = face_recognition.load_image_file(os.path.join(photo_dir, filename))
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(name)

students = known_face_names.copy()

face_location = []
face_encodings = []
face_names = []
s = True

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(current_date+'.csv','w+', newline='')
lnwriter = csv.writer(f)

# Set start and end times for detection period (in seconds)
start_time = time.time()
end_time = start_time + 15  # 1 hour later

while True:
    current_time = time.time()
    if current_time < end_time:
        _,frame = video_capture.read()
        small_frame = cv2.resize(frame,(0,0),fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:,:,::-1]
        if s:
            face_location = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame)
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = ""
                face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distance)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)
                if name in known_face_names:
                    if name in students:
                        students.remove(name)
                        print(students)
                        current_time_str = now.strftime("%H-%M-%S")
                        lnwriter.writerow([name,current_time_str])
                        say_name(name)  # Say the name
        cv2.imshow("attendance system", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        # After end time, mark remaining students as absent and send them a message on WhatsApp
        for student in students:
            lnwriter.writerow([student, 'Absent'])
            # Get the phone number of the student from the dictionary
            phone_number = students_phone_numbers.get(student, None)
            if phone_number is not None:
                # Send a WhatsApp message to the student
                kit.sendwhatmsg_instantly(phone_no=phone_number, message='You were marked absent today.')
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()
