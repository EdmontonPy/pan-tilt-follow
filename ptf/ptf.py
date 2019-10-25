import evdev

from evdev import InputDevice, ecodes

from .camera import Camera
from .faceTracker import FaceTracker
from .hatCatch import HatCatch


class PTF():
    BUTTON1 = 288
    BUTTON2 = 289
    BUTTON3 = 290

    BUTTON_UP = 1
    BUTTON_DOWN = 0

    JOYSTICK_MIN = 0
    JOYSTICK_MAX = 255

    CONTROLLER_ID = 'Logitech Dual Action'

    CONTROLLED = 1
    FACE = 2
    HAT = 3

    def __init__(self):
        self.gamepad = None
        self.faceTracking = False
        self.faceTracker = FaceTracker()
        self.camera = Camera()
        self.hatCatch = HatCatch()
        self.state = PTF.CONTROLLED

    def initialize(self):
        controllerInfo = None
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if (PTF.CONTROLLER_ID in device.name):
                controllerInfo = device

        if (controllerInfo is None):
            raise RuntimeError('No gamepad found.')

        self.gamepad = InputDevice(controllerInfo.path)

    def shutdown(self):
        self.camera.shutdown()

    def run(self):
        self.initialize()

        while True:
            frame = self.camera.getFrame()

            if (self.state == PTF.FACE):
                x, y, xMax, yMax, frame = self.faceTracker.getCoordinates(frame)
                if (x is not None and y is not None):
                    xDirection = -1
                    if ((x / xMax) - 0.5 < 0):
                        xDirection = 1
                    yDirection = 1
                    if ((y / yMax) - 0.5 < 0):
                        yDirection = -1

                    xMagnitude = int(abs(((x / xMax) - 0.5) * 10)**3)
                    yMagnitude = int(abs(((y / yMax) - 0.5) * 10)**3)

                    xDelta = xDirection * xMagnitude
                    yDelta = yDirection * yMagnitude

                    self.camera.moveX(self.camera.x + xDelta)
                    self.camera.moveY(self.camera.y + yDelta)

            if (self.state == PTF.HAT):
                frame = self.hatCatch.render(frame)

            if (not self.camera.render(frame)):
                return

            try:
                for event in self.gamepad.read():
                    if (event.code == PTF.BUTTON1 and event.value == PTF.BUTTON_UP):
                        self.state = PTF.CONTROLLED
                        print('State CONTROLLED')

                    if (event.code == PTF.BUTTON2 and event.value == PTF.BUTTON_UP):
                        self.state = PTF.FACE
                        print('State FACE')

                    if (event.code == PTF.BUTTON3 and event.value == PTF.BUTTON_UP):
                        self.state = PTF.HAT
                        self.hatCatch.startGame()
                        print('State HAT')

                    if (self.state == PTF.CONTROLLED and event.type == ecodes.EV_ABS):
                        if event.code == ecodes.ABS_X:
                            self.camera.moveX(
                                self.camera.scaleX(
                                    PTF.JOYSTICK_MIN,
                                    event.value,
                                    PTF.JOYSTICK_MAX
                                )
                            )
                        elif event.code == ecodes.ABS_Y:
                            self.camera.moveY(
                                self.camera.scaleY(
                                    PTF.JOYSTICK_MIN,
                                    event.value,
                                    PTF.JOYSTICK_MAX
                                )
                            )
            except BlockingIOError as error:
                # No input from controller do nothing
                pass
