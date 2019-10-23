from inputs import devices

from .camera import Camera
from .faceTracker import FaceTracker


class PTF():
    BUTTON_UP = 1
    BUTTON_DOWN = 0

    JOYSTICK_MIN = 0
    JOYSTICK_MAX = 255

    def __init__(self):
        self.gamepad = None
        self.faceTracking = True
        self.faceTracker = FaceTracker()
        self.camera = Camera()

    def initialize(self):
        if len(devices.gamepads) == 0:
            raise RuntimeError('No gamepad found.')
        if len(devices.gamepads) > 1:
            raise RuntimeError('Multiple gamepads founds. Only one is supported.')

        self.gamepad = devices.gamepads[0]

    def shutdown(self):
        self.faceTracker.shutdown()

    def run(self):
        self.initialize()
        while True:
            if (self.faceTracking):
                x, y, xMax, yMax = self.faceTracker.getCoordinates()
                self.camera.moveX(self.camera.scaleX(0, x, xMax))
                self.camera.moveY(self.camera.scaleY(0, y, yMax))

            # for buttonPress in self.gamepad.read():
            #     if buttonPress.ev_type not in ['Key', 'Absolute']:
            #         continue

            #     if (buttonPress.code == 'BTN_THUMB' and buttonPress.state == PTF.BUTTON_UP):
            #         self.faceTracking = not self.faceTracking
            #         print(f'FaceTracking: {self.faceTracking}')

            #     if (not self.faceTracking):
            #         if buttonPress.code == 'ABS_X':
            #             self.camera.moveX(
            #                 self.camera.scaleX(
            #                     PTF.JOYSTICK_MIN,
            #                     buttonPress.state,
            #                     PTF.JOYSTICK_MAX
            #                 )
            #             )
            #         elif buttonPress.code == 'ABS_Y':
            #             self.camera.moveY(
            #                 self.camera.scaleY(
            #                     PTF.JOYSTICK_MIN,
            #                     buttonPress.state,
            #                     PTF.JOYSTICK_MAX
            #                 )
            #             )
            #     # print(f'code={buttonPress.code}, ev_type={buttonPress.ev_type}, state={buttonPress.state}')
