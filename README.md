# Face Recognition Based Attendance System

This project uses face recognition to identify students and mark their attendance. It also sends a WhatsApp message to students who are marked absent.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have the following Python libraries installed:

- face_recognition
- cv2
- numpy
- csv
- os
- datetime
- time
- pyttsx3
- pywhatkit
- json

You can install them using pip:

```bash
pip install face_recognition opencv-python numpy pyttsx3 pywhatkit
```

### Usage

1. Add photos of the students in the `photos` directory. The photos should be clear and have only the student's face. The filename should be the student's name with a `.jpg` or `.png` extension.

2. Add the student names and their phone numbers in the `students_phone_numbers.json` file in the following format:

```json
{
    "student1": "+911111111111",
    "student2": "+912222222222"
    // Add more students here
}
```

Replace `"student1"` and `"student2"` with the actual student names and `"+911111111111"` and `"+912222222222"` with their actual phone numbers.

3. Run the script:

```bash
python script.py
```

The script will start the webcam, recognize students' faces, mark their attendance, and send a WhatsApp message to absent students.

## Important Note

Sensitive files containing personal data have been removed from this project for privacy reasons. Users need to add their own data (photos and phone numbers) to use this system.


