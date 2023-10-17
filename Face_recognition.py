import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime
import time

video_capture = cv2.VideoCapture(0)

bubu_image = face_recognition.load_image_file("photos/bubu.jpg")
bubu_encoding = face_recognition.face_encodings(bubu_image)[0]

dida_image = face_recognition.load_image_file("photos/bubu.jpg")
dida_encoding = face_recognition.face_encodings(dida_image)[0]

known_face_encoding = [
    bubu_encoding,
    dida_encoding
]

known_face_names = [
    "bubu",
    "dida"
]

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
end_time = start_time + 60  # 1 hour later

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
                matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
                name = ""
                face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
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
        cv2.imshow("attendance system", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        # After end time, mark remaining students as absent
        for student in students:
            lnwriter.writerow([student, 'Absent'])
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()
