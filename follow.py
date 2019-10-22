import os.path
import pkg_resources

import cv2

print('OpenCV loaded.')

camera = cv2.VideoCapture(0)
ret, frame = camera.read()
frame = cv2.flip(frame, 0)
camera.release()
print(frame)

for f in [
    # when python-opencv(-contrib?) is installed via pip
    pkg_resources.resource_filename(
        'cv2', 'data/haarcascade_frontalface_default.xml'),
    # in the opencv-data deb
    '/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml',
]:
    if os.path.isfile(f):
        haar_xml = f
        break

classifier = cv2.CascadeClassifier(haar_xml)
faces = classifier.detectMultiScale(frame)
annotated = frame.copy()
for (x, y, w, h) in faces:
    cv2.rectangle(annotated, (x, y), (x+w, y+h), (255, 0, 0), 3)

cv2.imshow('frame', annotated)
cv2.waitKey()
