import cv2
import datetime
import winsound
import threading
import time
cap = cv2.VideoCapture(0)
bg = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
RX1, RY1 = 200, 150
RX2, RY2 = 440, 350
siren_on = False
def is_inside(hx, hy, hw, hh):
    return hx < RX2 and hx + hw > RX1 and hy < RY2 and hy + hh > RY1
def is_night_time():
    hour = datetime.datetime.now().hour
    return hour >= 23 or hour < 5
def log_event(message):
    with open("log.txt", "a") as f:
        f.write(message + "\n")
def siren():
    global siren_on
    while siren_on:
        winsound.MessageBeep(winsound.MB_ICONHAND)
        time.sleep(0.4)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (640, 480))
    night = is_night_time()
    cv2.rectangle(frame, (RX1, RY1), (RX2, RY2), (0, 0, 255), 2)
    cv2.putText(frame, "Restricted Area", (RX1, RY1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    fgmask = bg.apply(frame)
    _, thresh = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    thresh = cv2.medianBlur(thresh, 5)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    motion = any(cv2.contourArea(c) > 1500 for c in contours)
    intrusion = False
    if motion:
        humans, _ = hog.detectMultiScale(frame, winStride=(8, 8))
        for (x, y, w, h) in humans:
            color = (0, 255, 0)
            label = "Human"
            if is_inside(x, y, w, h):
                intrusion = True
                color = (0, 0, 255)
                label = "ALERT! Night Intrusion" if night else "ALERT! Restricted Area"
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    if intrusion and not siren_on:
        siren_on = True
        threading.Thread(target=siren, daemon=True).start()
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        log_event(f"{timestamp} - Human inside restricted area")
    if not intrusion:
        siren_on = False
    mode_text = "NIGHT MODE" if night else "DAY MODE"
    mode_color = (0, 0, 255) if night else (0, 255, 0)
    cv2.putText(frame, mode_text, (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, mode_color, 2)
    cv2.imshow("Smart Hostel AI Surveillance", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
