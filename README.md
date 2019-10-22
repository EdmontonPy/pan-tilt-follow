## Setup instructions

From a new install of raspbian:

  - At a terminal, run

        sudo systemctl enable pigpiod
        sudo systemctl start pigpiod

In `raspi-config`:

  - Enable camera

Recommended but not necessary:

  - Enable SSH

### Python

    pip3 install --user inputs
    sudo apt install -y python3-opencv opencv-data

## Using it

To steer the camera with a gamepad, start

    python3 track.py

To get a preview window for the camera:

    raspivid -t 0 -p 100,100 -vf

Note that this can mess up the OpenCV python code later, possibly requiring
a reboot.

Then, to run the current face-track demo:

    python3 follow.py
