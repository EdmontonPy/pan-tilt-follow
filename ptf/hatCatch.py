import math
import os.path
import pkg_resources
import random

import cv2
import imutils

import numpy
from datetime import datetime, timedelta


class HatCatch():
    COLOR_BLUE = (255, 0, 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_RED = (0, 0, 255)

    BORDER = 2

    RESIZE_FACTOR = 0.5

    HAT_POINTS = 5

    GAME_RUN_TIME = timedelta(seconds=30)
    HAT_DROP_CHANCE = 0.05
    HAT_DROP_TIME = timedelta(seconds=3)
    HAT = cv2.imread('./hat.png', -1)

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

        self.hats = []
        self.gameStart = None
        self.score = 0

    @property
    def running(self):
        return self._running

    def startGame(self):
        self.hats = []
        self.gameStart = datetime.now()
        self.score = 0

    def render(self, frame):
        renderFrame = frame.copy()
        self._moveHats(frame)
        self._generateHats(frame)
        self._renderHats(renderFrame)
        frame, renderFrame, faces = self._getFaces(frame, renderFrame)
        self._detectCollisions(faces)
        self._renderScore(renderFrame)
        return renderFrame

    def _renderScore(self, frame):
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(
            frame,
            f'Score: {self.score}',
            (10,450),
            font,
            1,
            HatCatch.COLOR_GREEN,
            HatCatch.BORDER,
            cv2.LINE_AA
        )

    def _detectCollisions(self, faces):
        updatedHats = []
        for hat in self.hats:
            doesCollide = False
            for face in faces:
                collides = self._collides(
                    face,
                    (hat[0], hat[1], HatCatch.HAT.shape[1], HatCatch.HAT.shape[0])
                )
                if collides:
                    doesCollide = True
                    self.score += HatCatch.HAT_POINTS
                    break
            if not doesCollide:
                updatedHats.append(hat)

        self.hats = updatedHats

    def _collides(self, face, hat):
        if (face[0] < hat[0] + hat[2] and
           face[0] + face[2] > hat[0] and
           face[1] < hat[1] + hat[3] and
           face[1] + face[3] > hat[1]):
            return True
        return False

    def _moveHats(self, frame):
        updatedHats = []
        yMax = frame.shape[0] + (HatCatch.HAT.shape[0]*2)
        for hat in self.hats:
            elapsedTime = datetime.now() - hat[2]
            dropPercent = elapsedTime / HatCatch.HAT_DROP_TIME
            newlocation = int(yMax * dropPercent)
            if newlocation < yMax:
                updatedHats.append((hat[0], newlocation, hat[2]))
        self.hats = updatedHats

    def _generateHats(self, frame):
        xMax = frame.shape[1]
        x = random.randint(0, (xMax-HatCatch.HAT.shape[1]))
        if (random.random() < HatCatch.HAT_DROP_CHANCE):
            self.hats.append((x, frame.shape[0] + HatCatch.HAT.shape[0], datetime.now()))

    def _renderHats(self, frame):
        for hat in self.hats:
            cv2.rectangle(
                frame,
                (hat[0], hat[1],),
                (hat[0] + HatCatch.HAT.shape[1], hat[1] + HatCatch.HAT.shape[0],),
                HatCatch.COLOR_GREEN,
                HatCatch.BORDER
            )
            self.overlay_transparent(frame, HatCatch.HAT, hat[0], hat[1])
        return frame

    def overlay_transparent(self, background, overlay, x, y):
        # https://stackoverflow.com/questions/40895785/using-opencv-to-overlay-transparent-image-onto-another-image
        background_width = background.shape[1]
        background_height = background.shape[0]

        if x >= background_width or y >= background_height:
            return background

        h, w = overlay.shape[0], overlay.shape[1]

        if x + w > background_width:
            w = background_width - x
            overlay = overlay[:, :w]

        if y + h > background_height:
            h = background_height - y
            overlay = overlay[:h]

        if overlay.shape[2] < 4:
            overlay = numpy.concatenate(
                [
                    overlay,
                    numpy.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
                ],
                axis = 2,
            )

        overlay_image = overlay[..., :3]
        mask = overlay[..., 3:] / 255.0

        background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image
        return background

    def _getFaces(self, frame, renderFrame):
        originalFrame = frame.copy()

        # Make the image smaller to speed up processing
        frame = imutils.resize(frame, width=int(frame.shape[1]*HatCatch.RESIZE_FACTOR))
        # Convert to Gray scale
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.classifier.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        returnedFaces = []
        for (x, y, width, height) in faces:
            cv2.rectangle(
                renderFrame,
                (int(x*(1/HatCatch.RESIZE_FACTOR)), int(y*(1/HatCatch.RESIZE_FACTOR))),
                (int(x*(1/HatCatch.RESIZE_FACTOR) + (width*(1/HatCatch.RESIZE_FACTOR))), int(y*(1/HatCatch.RESIZE_FACTOR) + (height*(1/HatCatch.RESIZE_FACTOR)))),
                HatCatch.COLOR_GREEN,
                HatCatch.BORDER
            )
            returnedFaces.append((
                int(x*(1/HatCatch.RESIZE_FACTOR)),
                int(y*(1/HatCatch.RESIZE_FACTOR)),
                (width*(1/HatCatch.RESIZE_FACTOR)),
                (height*(1/HatCatch.RESIZE_FACTOR))
            ))
        return (originalFrame, renderFrame, returnedFaces)

    def _calculateMiddleOfSquare(self, x, y, width, height):
        return ((x + width/2), (y + height/2),)
