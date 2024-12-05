Virtual Mouse

Overview

This project implements a hand gesture recognition system to control mouse actions like moving the cursor, left-clicking, right-clicking, and double-clicking using a webcam. The system uses Mediapipe for hand tracking and gesture recognition, OpenCV for video processing, and PyAutoGUI for mouse simulation.

Features

Mouse Movement: Move the cursor by tracking the tip of the index finger.

Left Click: Perform a left mouse click by making a specific hand gesture.

Right Click: Perform a right mouse click by making another gesture.

Double Click: Perform a double click using a predefined hand gesture.

Real-Time Detection: Utilizes Mediapipe’s efficient hand-tracking for real-time gesture detection.

Requirements

The following Python libraries are required:

opencv-python

mediapipe

pyautogui

pynput

numpy

To install all dependencies, run:

pip install opencv-python mediapipe pyautogui pynput numpy

How It Works

Hand Tracking: Mediapipe tracks hand landmarks in real-time from the webcam feed.

Gesture Detection: Specific gestures are identified based on angles between finger joints and distances between key points on the hand.

Mouse Actions:

Move Mouse: The index finger tip coordinates are mapped to the screen resolution to control cursor movement.

Left Click: Detected when specific angles and distances between fingers meet the criteria.

Right Click: Triggered by a distinct combination of angles and distances.

Double Click: Identified by another unique gesture.

Action Execution: PyAutoGUI and Pynput execute the corresponding mouse actions.

File Structure

main.py: The main script containing all the code for gesture detection and mouse control.

Usage

Run the Script:

python main.py

Ensure your webcam is functional.

Perform the gestures in front of the camera:

Move Mouse: Point with the index finger.

Left Click: Specific angle and distance conditions.

Right Click: Different angle and distance conditions.

Double Click: Another predefined gesture.

Press Esc to exit the application.

Limitations

Only one hand is supported at a time.

The gestures need to be precise for accurate detection.

Performance may vary depending on lighting and webcam quality.

Acknowledgments

Mediapipe: For real-time hand tracking.

OpenCV: For video processing.

PyAutoGUI & Pynput: For simulating mouse actions.





