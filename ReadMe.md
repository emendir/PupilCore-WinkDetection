# PupilCore WinkDetection Plugin
A plugin for [Pupil Capture](https://docs.pupil-labs.com/core/#_1-put-on-pupil-core) by [PupilLabs](https://pupil-labs.com/) for their [PupilCore](https://pupil-labs.com/products/core/) headset that detects the headset wearer's winks.  
This plugin is based entirely on the built-in [blink detection plugin](https://github.com/pupil-labs/pupil/blob/master/pupil_src/shared_modules/blink_detection.py), modified to detect the winks of individual eyes instead of only the blinks of both eyes.

# Installation:
Place this project's [WinkDetection.py](WinkDetection.py) script in PupilCapture's 'plugins' directory.

# Usage:
The notification data provided by this plugin is identical to that provided by the blink detector, except that it has an added property 'eye' which specifies whether the left or right eye winked.
```
{   # blink datum
    'topic': 'blink',
    'eye': 'left' or 'right',
    'confidence': <float>,  # blink confidence
    'timestamp': <timestamp float>,
    'base_data': [<pupil positions>, ...]
    'type': 'onset' or 'offset'
}
```
Because this plugin works exactly like PupilCapture's BlinkDetection plugin, this plugin produces multiple notifications per wink. In order to filter out these multiple notifications to get only one notification per wink, take a look at [WinkDetectionDemo.py](WinkDetectionDemo.py).
[WinkDetectionDemo-Exclusive.py](WinkDetectionDemo-Exclusive.py) demonstrates how to filter out simultaneous winks of both eyes.


## For Other PupilCapture Plugins
As long as your plugin's execution order is greater than 0.8, you will be able to acces this plugin's data in your plugin's recent_events class.  
If you are new to PupilCapture plugin development, save the code below in a file with the .py extension in PupilCapture's 'plugins' folder, run PupilCapture from a terminal, and activate this new plugin ("MyPlugin") in the PupilCaptures plugins menu.
Read [PupilLabs' documentation](https://docs.pupil-labs.com/developer/core/plugin-api/) to understand how to build plugins for PupilCapture.
```python
from plugin import Plugin

class MyPlugin(Plugin):
    order = 0.81  # order must be greater than 0.8, which is the execution order of the WinkDetection plugin

    def __init__(self, g_pool):
        super().__init__(g_pool)


    def recent_events(self, events):
        """Gets the latest values eye-gaze and plugin data."""
        data = events["winks"]
        if data:
            data = data[0]
            print(f"{data['eye']} is winking!")
            print(f"    eye: {data['eye']}")
            print(f"    type: {data['type']}")
            print(f"    timestamp: {data['timestamp']}")
            print(f"    confidence: {data['confidence']}")
```
## Externally (From Outside PupilCore)
Connect to [PupilCapture's network API](https://docs.pupil-labs.com/developer/core/network-api/) and subscribe to this plugin's wink notifications using [ZMQ](https://zeromq.org/).
```python
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

def Start():
    status_right = ""
    status_left = ""
    while True:
        topic, payload = subscriber.recv_multipart()
        data = msgpack.loads(payload)
        
        print(f"{data['eye']} is winking!")
        print(f"    eye: {data['eye']}")
        print(f"    type: {data['type']}")
        print(f"    timestamp: {data['timestamp']}")
        print(f"    confidence: {data['confidence']}")


if __name__ == "__main__":
    Start()
```

## Links
This project's IPFS URL:  
[ipns://k2k4r8nismm5mmgrox2fci816xvj4l4cudnuc55gkfoealjuiaexbsup#PupilCore-WinkDetection](https://ipfs.io/ipns/k2k4r8nismm5mmgrox2fci816xvj4l4cudnuc55gkfoealjuiaexbsup#PupilCore-WinkDetection)