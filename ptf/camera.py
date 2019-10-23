# import pigpio


class Camera():
    X_PIN = 2
    Y_PIN = 3

    X_MIN = 500
    X_MAX = 2500

    Y_MIN = 500
    Y_MAX = 2500

    def __init__(self):
        # self.pi = pigpio.pi()
        self.x = 128;
        self.y = 128;

    def scaleX(self, minValue, value, maxValue):
        return (value - minValue)*(Camera.X_MAX - Camera.X_MIN)/(maxValue - minValue) + Camera.X_MIN

    def scaleY(self, minValue, value, maxValue):
        return (value - minValue)*(Camera.Y_MAX - Camera.Y_MIN)/(maxValue - minValue) + Camera.Y_MIN

    def moveX(self, x):
        if (not Camera.X_MIN <= x <= Camera.X_MAX):
            print(f'Value x is out of range {x}')

        if (self.x != x):
            print(f'Moving X to {x}')
            # self.pi.set_servo_pulsewidth(Camera.X_PIN, x)
            self.x = x

    def moveY(self, y):
        if (not Camera.Y_MIN <= y <= Camera.Y_MAX):
            print(f'Value y is out of range {y}')

        if (self.y != y):
            print(f'Moving Y to {y}')
            # self.pi.set_servo_pulsewidth(Camera.Y_PIN, y)
            self.y = y
