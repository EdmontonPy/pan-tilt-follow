# import pigpio
from inputs import devices

if len(devices.gamepads) == 0:
    raise RuntimeError("No gamepad found.")
if len(devices.gamepads) > 1:
    raise RuntimeError("Multiple gamepads founds. Only one is supported.")

gamepad = devices.gamepads[0]

# pi = pigpio.pi()

print('Ready.')

coords = [128, 128]

def scale(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max-in_min) + out_min

def coord_to_servo(n):
    if n < 0 or n > 255:
        raise RuntimeError(f'{n} out of range')

    return scale(n, 0, 255, 500, 2500)

while True:
    for r in gamepad.read():
        if r.ev_type not in ['Key', 'Absolute']:
            continue

        # Debugging to show button names
        if False:
            print(f'code={r.code}, ev_type={r.ev_type}, state={r.state}')

        prev_coords = coords[:]

        if r.code == 'ABS_X':
            coords[0] = r.state
        elif r.code == 'ABS_Y':
            coords[1] = r.state

        if coords != prev_coords:
            print(coords)

            # pi.set_servo_pulsewidth(2, coord_to_servo(coords[0]))
            # pi.set_servo_pulsewidth(3, coord_to_servo(coords[1]))
