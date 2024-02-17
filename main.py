import cv2
import pickle
import pyrebase
import numpy as np
import threading
from datetime import datetime
import RPi.GPIO as GPIO

# Set up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Firebase configuration
firebaseConfig = {
    "apiKey": "AIzaSyDbAwVRyQZwseyc2Npvr5MMaWjDxnpEzHM",
    "authDomain": "smartparking-a6015.firebaseapp.com",
    "databaseURL": "https://smartparking-a6015-default-rtdb.firebaseio.com",
    "projectId": "smartparking-a6015",
    "storageBucket": "smartparking-a6015.appspot.com",
    "messagingSenderId": "246089811699",
    "appId": "1:246089811699:web:d815bccc3aefb843961986",
    "measurementId": "G-N1T7KM9GYK"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

# Initial data setup
initial_data = {
    "slot0": {"availability": True, "occupancy_status": False, "entry_time": "00:00:00", "exit_time": "00:00:00", "total_duration": "00:00:00"},
    "slot1": {"availability": True, "occupancy_status": False, "entry_time": "00:00:00", "exit_time": "00:00:00", "total_duration": "00:00:00"},
    "slot2": {"availability": True, "occupancy_status": False, "entry_time": "00:00:00", "exit_time": "00:00:00", "total_duration": "00:00:00"},
    # Add more slots as needed
}

# Set initial data in Firebase
db.child("parking_slots").set(initial_data)

# Camera initialization
cap = cv2.VideoCapture(0)

# Function for entry and exit checks
def entry_check(slot):
    entry_time = datetime.now().strftime('%H:%M:%S')
    db.child("parking_slots").child(slot).update({"availability": False, "occupancy_status": True, "entry_time": entry_time})

def exit_check(slot):
    exit_time = datetime.now().strftime('%H:%M:%S')
    entry_time = db.child("parking_slots").child(slot).child("entry_time").get().val()
    total_duration = calculate_duration(entry_time, exit_time)
    db.child("parking_slots").child(slot).update({"availability": True, "occupancy_status": False, "exit_time": exit_time, "total_duration": total_duration})

def calculate_duration(entry_time, exit_time):
    entry_time_obj = datetime.strptime(entry_time, '%H:%M:%S')
    exit_time_obj = datetime.strptime(exit_time, '%H:%M:%S')
    duration = exit_time_obj - entry_time_obj
    return str(duration)

# Function for parking space checking
def check_parking_space():
    # Implementation of computer vision techniques to detect occupancy status of each parking slot
    # This function analyzes video frames from the camera and updates the Firebase database accordingly
    pass

# Function for input handling
def get_input():
    while True:
        code = input("Enter slot code (e.g., slot0, slot1, etc.): ")
        if code in initial_data.keys():
            if initial_data[code]["availability"]:
                entry_check(code)
                print("Vehicle entered slot:", code)
            else:
                exit_check(code)
                print("Vehicle exited slot:", code)
        else:
            print("Invalid slot code.")

# Main execution loop
try:
    threading.Thread(target=get_input).start()
    while True:
        success, img = cap.read()
        # Call function to check parking space occupancy status
        check_parking_space()
        # Perform other processing tasks as needed
except KeyboardInterrupt:
    GPIO.cleanup()
