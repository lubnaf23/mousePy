# Virtual Mouse using OpenCV and MediaPipe

This project implements a virtual mouse that uses hand tracking through a webcam. It enables mouse movement, scrolling, and gesture-based interaction such as left and right clicks, all controlled by specific finger positions and motions.

## Features

- Cursor movement controlled by the index finger tip
- Vertical scrolling by moving the index finger up and down
- Gesture recognition for:
  - Left click
  - Right click

## How It Works

- Uses MediaPipe to detect and track 21 hand landmarks in real time
- The index finger tip coordinates are mapped to the screen resolution for smooth mouse movement
- Scrolling is based on changes in the Y-coordinate of the index finger
- Gesture logic determines left and right clicks using angle and distance calculations between key landmarks

## Requirements

Install the necessary packages:

```bash
pip install opencv-python mediapipe pyautogui
```
Make sure you have webcam connected.
Once you do you're ready click run and use your virtual mouse!
