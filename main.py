import threading
import time
import winsound
import cv2

ping_speed = 1.0
stop_flag = False


def beeper():
    global ping_speed, stop_flag
    while not stop_flag:
        if ping_speed > 0:
            winsound.Beep(1000, 200)
            time.sleep(ping_speed)
        else:
            time.sleep(0.05)


threading.Thread(target=beeper, daemon=True).start()


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

prev_gray = None

if __name__ == "__main__":
    try:
        while True:
            success, frame = cap.read()
            if not success:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if prev_gray is None:
                prev_gray = gray
                continue

            diff = cv2.absdiff(prev_gray, gray)
            thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
            motion_level = cv2.countNonZero(thresh)

            min_motion, max_motion = 5000, 50000
            min_speed, max_speed = 5.0, 0.05

            if motion_level < 2000:
                ping_speed = 0.0
            elif motion_level <= min_motion:
                    ping_speed = min_speed
            elif motion_level >= max_motion:
                    ping_speed = max_speed
            else:
                scale = (motion_level - min_motion) / (max_motion - min_motion)
                ping_speed = min_speed - scale * (min_speed - max_speed)

            print(f"Motion level - {motion_level} Ping speed - {ping_speed}")

            prev_gray = gray

            cv2.imshow("Motion Detector", thresh)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nStopped.")

    stop_flag = True
    cap.release()
    cv2.destroyAllWindows()
