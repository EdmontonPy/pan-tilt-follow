import evdev

from evdev import InputDevice, ecodes

from .camera import Camera
from .faceTracker import FaceTracker


class PTF():
    BUTTON2 = 289

    BUTTON_UP = 1
    BUTTON_DOWN = 0

    JOYSTICK_MIN = 0
    JOYSTICK_MAX = 255

    CONTROLLER_ID = 'Logitech Dual Action'

    def __init__(self):
        self.gamepad = None
        self.faceTracking = False
        self.faceTracker = FaceTracker()
        self.camera = Camera()

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

            if (self.faceTracking):
                x, y, xMax, yMax, frame = self.faceTracker.getCoordinates(frame)
                if (x is not None and y is not None):
                    xDirection = -1
                    if ((x / xMax) - 0.5 < 0):
                        xDirection = 1
                    yDirection = 1
                    if ((y / yMax) - 0.5 < 0):
                        yDirection = -1

                    xMagnitude = int((((x / xMax) - 0.5) * 10)**3)
                    yMagnitude = int((((y / yMax) - 0.5) * 10)**3)

                    xDelta = xDirection * xMagnitude
                    yDelta = yDirection * yMagnitude

                    self.camera.moveX(self.camera.x + xDelta)
                    self.camera.moveY(self.camera.y + yDelta)

            if (not self.camera.render(frame)):
                return

            try:
                for event in self.gamepad.read():
                    if (event.code == PTF.BUTTON2 and event.value == PTF.BUTTON_UP):
                        self.faceTracking = not self.faceTracking
                        print(f'FaceTracking: {self.faceTracking}')

                    if (not self.faceTracking and event.type == ecodes.EV_ABS):
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
