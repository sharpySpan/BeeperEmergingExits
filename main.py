import cv2
import time
import winsound
import pygame

pygame.mixer.init()
sound = pygame.mixer.Sound("241227_002040_Tr1.WAV")

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

min_frames_tracked = 3
last_beep_time = 0
frames_with_face = 0

while True:
    sound.play()
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        frames_with_face += 1

        face_area = w * h
        delay = max(0.1, min(1.0, 20000 / face_area))

        if frames_with_face >= min_frames_tracked:
            if time.time() - last_beep_time > delay:
                winsound.Beep(1000, 200)
                last_beep_time = time.time()

        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    else:
        frames_with_face = 0

    cv2.imshow('Head Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
