import cv2
import time
import winsound
from pyenttec import DMXConnection
import pygame

# variables
min_frames_tracked = 3
last_beep_time = 0
frames_with_face = 0
COM_PORT = 'COM3'
DMX_START_ADDRESS = 1

# setup dmx
def set_light(dmx, intensity=0, red=0, green=0, blue=0):
    dmx.set_channel(DMX_START_ADDRESS, intensity)
    dmx.set_channel(DMX_START_ADDRESS + 1, red)
    dmx.set_channel(DMX_START_ADDRESS + 2, green)
    dmx.set_channel(DMX_START_ADDRESS + 3, blue)
    dmx.render()

# Dmx control
dmx = DMXConnection(COM_PORT)
set_light(dmx, intensity=100, red=100, green=0, blue=0)

# ambient sound
pygame.mixer.init()
sound = pygame.mixer.Sound("ambient video.mp3")
sound.play()

# face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        frames_with_face += 1

        face_area = w * h
        delay = max(0.1, min(1.0, 20000 / face_area))

        if frames_with_face >= min_frames_tracked:
            if time.time() - last_beep_time > delay:
                set_light(dmx, intensity=255, red=255, green=0, blue=0)
                winsound.Beep(1000, 250)
                set_light(dmx, intensity=100, red=100, green=0, blue=0)
                last_beep_time = time.time()

        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    else:
        frames_with_face = 0

    cv2.imshow('Head Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
