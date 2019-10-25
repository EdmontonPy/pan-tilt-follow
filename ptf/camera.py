import cv2
# import pigpio


class Camera():
    FLIP_HORIZONTAL = 0
    FLIP_VERTICAL = 1
    FLIP_HORIZONTAL_VERTICAL = -1

    X_PIN = 2
    Y_PIN = 3

    X_MIN = 500
    X_MAX = 2500

    Y_MIN = 500
    Y_MAX = 2500

    WINDOW_NAME = 'Camera'

    def __init__(self):
        self.pi = pigpio.pi()
        self.camera = cv2.VideoCapture(0)

        self.x = 128;
        self.y = 128;

    def getFrame(self):
        ret, frame = self.camera.read()
        frame = cv2.flip(frame, Camera.FLIP_HORIZONTAL_VERTICAL)
        return frame

    def render(self, frame):
        cv2.imshow(Camera.WINDOW_NAME, frame)
        cv2.waitKey(1)
        if cv2.getWindowProperty(Camera.WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            return False
        return True

    def shutdown(self):
        self.camera.release()
        cv2.destroyAllWindows()

    def scaleX(self, minValue, value, maxValue):
        return (value - minValue)*(Camera.X_MAX - Camera.X_MIN)/(maxValue - minValue) + Camera.X_MIN

    def scaleY(self, minValue, value, maxValue):
        return (value - minValue)*(Camera.Y_MAX - Camera.Y_MIN)/(maxValue - minValue) + Camera.Y_MIN

    def moveX(self, x):
        if (not Camera.X_MIN <= x <= Camera.X_MAX):
            print(f'Value x is out of range {x}')
            return;

        if (self.x != x):
            self.pi.set_servo_pulsewidth(Camera.X_PIN, x)
            self.x = x

    def moveY(self, y):
        if (not Camera.Y_MIN <= y <= Camera.Y_MAX):
            print(f'Value y is out of range {y}')
            return;

        if (self.y != y):
            self.pi.set_servo_pulsewidth(Camera.Y_PIN, y)
            self.y = y
