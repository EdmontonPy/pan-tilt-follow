import math
import os.path
import pkg_resources

import cv2


class FaceTracker():
    COLOR_BLUE = (255, 0, 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_RED = (0, 0, 255)

    BORDER = 2

    RESIZE_FACTOR = 0.25

    def __init__(self):
        xmlClassifierPaths = [
            # when python-opencv(-contrib?) is installed via pip
            pkg_resources.resource_filename(
                'cv2', 'data/haarcascade_frontalface_default.xml'
            ),
            # in the opencv-data deb
            '/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml',
        ]

        xmlClassifierPath = ''
        for xml in xmlClassifierPaths:
            if os.path.isfile(xml):
                 xmlClassifierPath = xml

        self.classifier = cv2.CascadeClassifier(xmlClassifierPath)
        self.x = 0
        self.y = 0
        self.xMax = 0
        self.yMax = 0

    def getCoordinates(self, frame):
        originalFrame = frame.copy()

        # Make the image smaller to speed up processing
        frame = cv2.resize(frame, None, fx=FaceTracker.RESIZE_FACTOR, fy=FaceTracker.RESIZE_FACTOR)
        # Convert to Gray scale
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.classifier.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        closest = None
        closestDistnce = None;

        self.yMax, self.xMax = frame.shape
        frameCentre = ((self.xMax/2), (self.yMax/2),)
        for (x, y, width, height) in faces:
            faceCentre = self._calculateMiddleOfSquare(x, y, width, height)

            distance = self._calculateDistance(
                faceCentre[0],
                faceCentre[1],
                frameCentre[0],
                frameCentre[1]
            )
            if (closest is None or distance < closestDistnce):
                closest = (x, y, width, height)
                closestDistnce = distance


            cv2.rectangle(
                originalFrame,
                (int(x*(1/FaceTracker.RESIZE_FACTOR)), int(y*(1/FaceTracker.RESIZE_FACTOR))),
                (int(x*(1/FaceTracker.RESIZE_FACTOR) + (width*(1/FaceTracker.RESIZE_FACTOR))), int(y*(1/FaceTracker.RESIZE_FACTOR) + (height*(1/FaceTracker.RESIZE_FACTOR)))),
                FaceTracker.COLOR_GREEN,
                FaceTracker.BORDER
            )

        if (closest is not None):
            middle = self._calculateMiddleOfSquare(
                closest[0],
                closest[1],
                closest[2],
                closest[3]
            )
            self.x = middle[0]
            self.y = middle[1]

        return (self.x, self.y, self.xMax, self.yMax, originalFrame)

    def _calculateMiddleOfSquare(self, x, y, width, height):
        return ((x + width/2), (y + height/2),)

    def _calculateDistance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2);
