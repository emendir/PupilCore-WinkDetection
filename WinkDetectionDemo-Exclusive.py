"""Demonstrates the interaction with the WinkDetection plugin
over PupilCapture's Network API.
Filters the multiple notifications produced by the plugin so that
the wink-eventhandler functions are called only once per wink,
and so that simultaneous winks by both eyes are ignored."""
import zmq
from datetime import datetime
import msgpack

# IP Address and Port of Pupil Capture
ip = 'localhost'  # If you talk to a different machine use its IP.
port = 50020  # The port defaults to 50020. Set in Pupil Capture GUI.

ctx = zmq.Context()
pupil_remote = ctx.socket(zmq.REQ)

pupil_remote.connect(f'tcp://{ip}:{port}')
pupil_remote.send_string('SUB_PORT')
sub_port = pupil_remote.recv_string()

subscriber = ctx.socket(zmq.SUB)
subscriber.connect(f'tcp://{ip}:{sub_port}')
subscriber.subscribe('wink')


def OnRightWink():
    """Gets called when the right eye completes a wink
    during which the left eye was always open"""
    print("Right wink!")


def OnLeftWink():
    """Gets called when the left eye completes a wink
    during which the right eye was always open"""
    print("Left wink!")


def Start():
    status_right = ""
    status_left = ""
    while True:
        topic, payload = subscriber.recv_multipart()
        message = msgpack.loads(payload)
        if message["eye"] == "right":
            if message["type"] == "onset":
                if status_right == "":
                    status_right = "onset"
            if message["type"] == "offset":
                if status_right == "onset":
                    status_right = ""
                    if status_left == "onset":  # if left is closed
                        status_left = ""        # cancel left wink and this
                    else:
                        OnRightWink()
        if message["eye"] == "left":
            if message["type"] == "onset":
                if status_left == "":
                    status_left = "onset"
            if message["type"] == "offset":
                if status_left == "onset":
                    status_left = ""
                    if status_right == "onset":  # if right is closed
                        status_right = ""       # cancel right wink and this
                    else:
                        OnLeftWink()


if __name__ == "__main__":
    Start()
