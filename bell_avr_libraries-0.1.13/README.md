# AVR-Python-Libraries

## Install

To install the base package, run:

```bash
pip install bell-avr-libraries
```

Additionally, the `mqtt` and `serial` extras are available if you want to use
the MQTT or PCC functionality.

```bash
pip install bell-avr-libraries[mqtt,serial]
```

## Usage

### MQTT

```python
from bell.avr import mqtt
```

These are MQTT utilities that are used to have a consistent messaging protocol
throughout all the AVR software modules.

The first part of this are the payloads for the MQTT messages themselves. As AVR
exclusively uses JSON, these are all
[`TypedDict`](https://docs.python.org/3/library/typing.html#typing.TypedDict)s
that have all of the required fields for a message.

Example:

```python
from bell.avr.mqtt.payloads import AvrPcmSetBaseColorPayload

payload = AvrPcmSetBaseColorPayload((128, 232, 142, 0))
```

The second part of the MQTT libraries, is the `MQTTModule` class.
This is a boilerplate module for AVR that makes it very easy to send
and recieve MQTT messages and do something with them.

Example:

```python
from bell.avr.mqtt.client import MQTTModule
from bell.avr.mqtt.payloads import AvrFcmVelocityPayload, AvrPcmSetServoOpenClosePayload


class Sandbox(MQTTModule):
    def __init__(self) -> None:
        super().__init__()
        self.topic_map = {"avr/fcm/velocity": self.show_velocity}

    def show_velocity(self, payload: AvrFcmVelocityPayload) -> None:
        vx = payload["vX"]
        vy = payload["vY"]
        vz = payload["vZ"]
        v_ms = (vx, vy, vz)
        print(f"Velocity information: {v_ms} m/s")

    def open_servo(self) -> None:
        payload = AvrPcmSetServoOpenClosePayload(servo=0, action="open")
        self.send_message("avr/pcm/set_servo_open_close", payload)


if __name__ == "__main__":
    box = Sandbox()
    box.run()
```

The `topic_map` dictionary is a class attribute that maps topics to subscribe to
and a function that will handle an incoming payload. The `payload` argument
should match the appropriate `Payload` class for that topic.

Additionally, the `message_cache` attribute is a dictionary that holds
a copy of the last payload sent by that module on a given topic. The keys are the
topic strings, and the values are the topic payloads.

### Utils

```python
from bell.avr import utils
```

These are general purpose utilities.

#### Decorators

```python
from bell.avr.utils import decorators
```

There are 3 different function decorators available, which are helpful for MQTT
message callbacks. First is the `try_except` decorator, which wraps the
function in a `try: except:` statement and will log any exceptions to the console:

```python
    @decorators.try_except
    def assemble_hil_gps_message(self) -> None:
        ...
```

Additionally, there is the `reraise` argument, which can be set to `True` to raise
any exceptions that are encountered. This is helpful if you still want exceptions
to propagate up, but log them.

There is an async version of this decorator as well with an `async_` prefix.

```python
    @decorators.async_try_except()
    async def connected_status_telemetry(self) -> None:
        ...
```

The last decorator is `run_forever` which will run the wrapped function forever,
with a given `period` or `frequency`.

```python
    @decorators.run_forever(frequency=5)
    def read_data(self) -> None:
        ...
```

#### Timing

```python
from bell.avr.utils import timing
```

Here is a `rate_limit` function which take a callable and a
period or frequency, and only run the callable at that given rate.

```python
for _ in range(10):
    # add() will only run twice
    timing.rate_limit(add, period=5)
    time.sleep(1)
```

This works tracking calls to the `rate_limit` function from a line number
within a file, so multiple calls to `rate_limit` say within a loop
with the same callable and period will be treated seperately. This allows
for dynamic frequency manipulation.

### Serial

```python
from bell.avr import serial
```

These are serial utilities that help facilitate finding and communicating
with the AVR peripherial control computer.

#### Client

```python
from bell.avr.serial import client
```

The `SerialLoop` class is a small wrapper around the `pyserial` `serial.Serial`
class which adds a `run` method that will try to read data from the serial device
as fast as possible.

```python
ser = client.SerialLoop()
```

#### PCC

```python
from bell.avr.serial import client
```

The `PeripheralControlComputer` class sends serial messages
to the AVR peripherial control computer, via easy-to-use class methods.

```python
import bell.avr.serial.client
import bell.avr.serial.pcc
import threading

client = bell.avr.serial.client.SerialLoop()
client.port = port
client.baudrate = baudrate
client.open()

pcc = bell.avr.serial.pcc.PeripheralControlComputer(client)

client_thread = threading.Thread(target=client.run)
client_thread.start()

pcc.set_servo_max(0, 100)
```

#### Ports

```python
from bell.avr.serial import ports
```

Here is a `list_serial_ports` function which returns a list of detected serial
ports connected to the system.

```python
serial_ports = ports.list_serial_ports()
# ["COM1", "COM5", ...]
```

## Development

Install [`poetry`](https://python-poetry.org/) and run
`poetry install --extras mqtt --extras serial` to install of the dependencies
inside a virtual environment.

Build the auto-generated code with `poetry run python build.py`. From here,
you can now produce a package with `poetry build`.

To add new message definitions, add entries to the `bell/avr/mqtt/messages.jsonc` file.
The 3 parts of a new message are as follows:

1. "topic": This is the full topic path for the message. This must be all lower case and
   start with "avr/".
2. "payload": These are the keys of the payload for the message.
   This is a list of key entries (see below).
3. "docs": This is an optional list of Markdown strings that explains what this
   message does. Each list item is a new line.

The key entries for a message have the following elements:

1. "key": This is the name of the key. Must be a valid Python variable name.
2. "type": This is the data type of the key such as `Tuple[int, int, int, int]`.
   Must be a valid Python type hint. Otherwise, this can be a list of more
   key entries, effectively creating a nested dictionary.
3. "docs": This is an optional list of Markdown strings that explains what the
   key is. Each list item is a new line.

The `bell/avr/mqtt/schema.json` file will help ensure the correct schema is maintained,
assuming you are using VS Code.

## MQTT Documentation

### Data Types

#### AvrApriltagsRawTags

- `"id"` (`int`):
    The ID of the AprilTag
- `"pos"` (`AvrApriltagsRawTagsPos`)
- `"rotation"` (`Tuple[Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float, float]]`):
    The 3x3 rotation matrix

#### AvrApriltagsRawTagsPos

- `"x"` (`float`):
    The position in meters of the camera relative to the AprilTag's X frame
- `"y"` (`float`):
    The position in meters of the camera relative to the AprilTag's Y frame
- `"z"` (`float`):
    The position in meters of the camera relative to the AprilTag's Z frame

#### AvrApriltagsSelectedPos

The position of the vehicle in world frame in centimeters

- `"n"` (`float`):
    The +north position of the vehicle relative to the world origin in world frame
- `"e"` (`float`):
    The +east position of the vehicle relative to the world origin in world frame
- `"d"` (`float`):
    The +down position of the vehicle relative to the world origin in world frame

#### AvrApriltagsVisibleTags

- `"id"` (`int`):
    The ID of the AprilTag
- `"horizontal_dist"` (`float`):
    The horizontal scalar distance from vehicle to AprilTag, in centimeters
- `"vertical_dist"` (`float`):
    The vertical scalar distance from vehicle to AprilTag, in centimeters
- `"angle_to_tag"` (`float`):
    The angle formed by the vector pointing from the vehicles body to the AprilTag in world frame relative to world-north
- `"heading"` (`float`):
    The heading of the vehicle in world frame
- `"pos_rel"` (`AvrApriltagsVisibleTagsPosRel`):
    The relative position of the vehicle to the tag in world frame in centimeters
- `"pos_world"` (`AvrApriltagsVisibleTagsPosWorld`):
    The position of the vehicle in world frame in centimeters (if the tag has no truth data, this will not be present in the output)

#### AvrApriltagsVisibleTagsPosRel

The relative position of the vehicle to the tag in world frame in centimeters

- `"x"` (`float`):
    The x (+north/-south) position of the vehicle relative to the AprilTag in world frame
- `"y"` (`float`):
    The y (+east/-west) position of the vehicle relative to the AprilTag in world frame
- `"z"` (`float`):
    The z (+down/-up) position of the vehicle relative to the AprilTag in world frame

#### AvrApriltagsVisibleTagsPosWorld

The position of the vehicle in world frame in centimeters (if the tag has no truth data, this will not be present in the output)

- `"x"` (`Optional[float]`):
    The x position of the vehicle relative to the world origin (this is the ship) in world frame (for reference the mountain is **north** of the beach)
- `"y"` (`Optional[float]`):
    The y position of the vehicle relative to the world origin in world frame
- `"z"` (`Optional[float]`):
    The z position of the vehicle relative to the world origin in world frame

### Message Payloads

#### AvrApriltagsFpsPayload

Topic: `avr/apriltags/fps`

This reports the framerate of AprilTag processing

- `"fps"` (`int`):
    Number of frames of video data processed in the last second

#### AvrApriltagsRawPayload

Topic: `avr/apriltags/raw`

This topic publishes the raw AprilTag data

- `"tags"` (`List[AvrApriltagsRawTags]`)

#### AvrApriltagsSelectedPayload

Topic: `avr/apriltags/selected`

This topic publishes its best candidate for position feedback

- `"tag_id"` (`int`):
    The id of the tag
- `"pos"` (`AvrApriltagsSelectedPos`):
    The position of the vehicle in world frame in centimeters
- `"heading"` (`float`)

#### AvrApriltagsVisiblePayload

Topic: `avr/apriltags/visible`

This topic publishes the transformed AprilTag data

- `"tags"` (`List[AvrApriltagsVisibleTags]`)

#### AvrAutonomousBuildingDropPayload

Topic: `avr/autonomous/building/drop`

This enables or disables a building payload drop. This is not used by any Bell code, but available to students to listen to.

- `"id"` (`int`):
    0-index ID of the relevant building
- `"enabled"` (`bool`):
    Boolean of whether the building should have drop enabled

#### AvrAutonomousEnablePayload

Topic: `avr/autonomous/enable`

This enables or disables autonomous mode. This is not used by any Bell code, but available to students to.

- `"enabled"` (`bool`)

#### AvrFcmAttitudeEulerPayload

Topic: `avr/fcm/attitude/euler`

This reports the current attitude of the drone from the flight controller.

- `"roll"` (`float`):
    Roll in degrees
- `"pitch"` (`float`):
    Pitch in degrees
- `"yaw"` (`float`):
    Yaw in degrees

#### AvrFcmBatteryPayload

Topic: `avr/fcm/battery`

This reports battery information from the flight controller.

- `"voltage"` (`float`):
    Battery voltage
- `"soc"` (`float`):
    State of charge (0 - 100)

#### AvrFcmEventsPayload

Topic: `avr/fcm/events`

This reports events from the flight controller such as flight mode changes.

- `"name"` (`str`):
    The name of the event.
- `"payload"` (`str`):
    The payload of the event.

#### AvrFcmGpsInfoPayload

Topic: `avr/fcm/gps_info`

This reports the current status of the flight controller's GPS connection.

- `"num_satellites"` (`int`):
    Number of visible satellites in use. HIL GPS will appear as 13.
- `"fix_type"` (`str`):
    GPS fix type

#### AvrFcmHilGpsStatsPayload

Topic: `avr/fcm/hil_gps_stats`

This reports statistics on the HIL GPS data that is fed into the flight controller.

- `"num_frames"` (`int`):
    This is the number of messages that have been sent to the flight controller since the software has started.

#### AvrFcmLocationGlobalPayload

Topic: `avr/fcm/location/global`

This reports the current position of the drone in global coordinates from the flight controller.

- `"lat"` (`float`):
    Latitude in degrees
- `"lon"` (`float`):
    Longitude in degrees
- `"alt"` (`float`):
    Altitude relative to takeoff altitude in meters
- `"hdg"` (`float`):
    Heading in degrees.

#### AvrFcmLocationHomePayload

Topic: `avr/fcm/location/home`

This reports the current position of the drone's home position in global coordinates.

- `"lat"` (`float`):
    Latitude in degrees of the home position
- `"lon"` (`float`):
    Longitude in degrees of the home position
- `"alt"` (`float`):
    Altitude relative to the home position in meters

#### AvrFcmLocationLocalPayload

Topic: `avr/fcm/location/local`

This reports the current position of the drone in local coordinates from the flight controller.

- `"dX"` (`float`):
    X position in a local North/East/Down coordinate system in meters
- `"dY"` (`float`):
    Y position in a local North/East/Down coordinate system in meters
- `"dZ"` (`float`):
    Z position in a local North/East/Down coordinate system in meters

#### AvrFcmStatusPayload

Topic: `avr/fcm/status`

This reports general status of the flight controller.

- `"armed"` (`bool`):
    Boolean of if the drone is currently armed
- `"mode"` (`str`):
    Current flight mode, which is one of the following:
    - 'UNKNOWN'
    - 'READY'
    - 'TAKEOFF'
    - 'HOLD'
    - 'MISSION'
    - 'RETURN_TO_LAUNCH'
    - 'LAND'
    - 'OFFBOARD'
    - 'FOLLOW_ME'
    - 'MANUAL'
    - 'ALTCTL'
    - 'POSCTL'
    - 'ACRO'
    - 'STABILIZED'
    - 'RATTITUDE'

#### AvrFcmVelocityPayload

Topic: `avr/fcm/velocity`

This reports the current velocity vectors of the drone from the flight controller.

- `"vX"` (`float`):
    X velocity in a local North/East/Down coordinate system in meters per second
- `"vY"` (`float`):
    Y velocity in a local North/East/Down coordinate system in meters per second
- `"vZ"` (`float`):
    Z velocity in a local North/East/Down coordinate system in meters per second

#### AvrFusionAttitudeEulerPayload

Topic: `avr/fusion/attitude/euler`

This reports the computed attitude of the drone from our sensor fusion.

- `"psi"` (`float`):
    Roll in radians
- `"theta"` (`float`):
    Pitch in radians
- `"phi"` (`float`):
    Yaw in radians

#### AvrFusionAttitudeHeadingPayload

Topic: `avr/fusion/attitude/heading`

This reports the computed heading of the drone from our sensor fusion.

- `"heading"` (`float`):
    Heading in degrees

#### AvrFusionAttitudeQuatPayload

Topic: `avr/fusion/attitude/quat`

This reports the computed attitude of the drone from our sensor fusion.

- `"w"` (`float`):
    Quaternion w value
- `"x"` (`float`):
    Quaternion x value
- `"y"` (`float`):
    Quaternion y value
- `"z"` (`float`):
    Quaternion z value

#### AvrFusionClimbratePayload

Topic: `avr/fusion/climbrate`

This reports the computed rate of climb of the drone from our sensor fusion.

- `"climb_rate_fps"` (`float`):
    Rate of climb in feet per second

#### AvrFusionCoursePayload

Topic: `avr/fusion/course`

This reports the computed course of the drone from our sensor fusion.

- `"course"` (`float`):
    Course in degrees

#### AvrFusionGeoPayload

Topic: `avr/fusion/geo`

This reports the computed position of the drone in global coordinates from our sensor fusion.

- `"lat"` (`float`):
    Latitude in degrees
- `"lon"` (`float`):
    Longitude in degrees
- `"alt"` (`float`):
    Altitude relative to takeoff altitude in meters

#### AvrFusionGroundspeedPayload

Topic: `avr/fusion/groundspeed`

This reports the computed groundspeed of the drone from our sensor fusion.

- `"groundspeed"` (`float`):
    Groundspeed of the drone in meters per second. This is a normal vector of the N and E velocities.

#### AvrFusionHilGpsPayload

Topic: `avr/fusion/hil_gps`

This is the raw data that will get converted to a MAVLink message and sent to the flight controller for HIL GPS. <https://mavlink.io/en/messages/common.html#HIL_GPS>

- `"time_usec"` (`int`):
    UNIX epoch timestamp in microseconds
- `"fix_type"` (`int`):
    0-1: no fix, 2: 2D fix, 3: 3D fix.
- `"lat"` (`int`):
    WGS84 Latitude * 10000000
- `"lon"` (`int`):
    WGS84 Longitude * 10000000
- `"alt"` (`int`):
    Altitude from sea level in mm. Positive for up.
- `"eph"` (`int`):
    GPS HDOP horizontal dilution of position
- `"epv"` (`int`):
    GPS VDOP vertical dilution of position
- `"vel"` (`int`):
    GPS ground speed in centimeters per second
- `"vn"` (`int`):
    GPS velocity in north direction in centimeters per second
- `"ve"` (`int`):
    GPS velocity in east direction in centimeters per second
- `"vd"` (`int`):
    GPS velocity in down direction in centimeters per second
- `"cog"` (`int`):
    Course over ground in degrees
- `"satellites_visible"` (`int`):
    Number of satellites visible. This is hardcoded to 13 for our HIL GPS.
- `"heading"` (`int`):
    Custom heading field. This is the heading in degrees * 100.

#### AvrFusionPositionNedPayload

Topic: `avr/fusion/position/ned`

This reports the computed position of the drone in local coordinates from our sensor fusion.

- `"n"` (`float`):
    X position in a local North/East/Down coordinate system in meters
- `"e"` (`float`):
    Y position in a local North/East/Down coordinate system in meters
- `"d"` (`float`):
    Z position in a local North/East/Down coordinate system in meters

#### AvrFusionVelocityNedPayload

Topic: `avr/fusion/velocity/ned`

This reports the computed velocity vectors of the drone from our sensor fusion.

- `"Vn"` (`float`):
    X velocity in a local North/East/Down coordinate system in meters per second
- `"Ve"` (`float`):
    Y velocity in a local North/East/Down coordinate system in meters per second
- `"Vd"` (`float`):
    Z velocity in a local North/East/Down coordinate system in meters per second

#### AvrPcmFireLaserPayload

Topic: `avr/pcm/fire_laser`

Fires the laser for a 0.25 sec pulse. Has a cooldown of 0.5 sec.

There is no content for this class

#### AvrPcmSetBaseColorPayload

Topic: `avr/pcm/set_base_color`

This sets the color of the LED strip on the PCC

- `"wrgb"` (`Tuple[int, int, int, int]`):
    A list of 4 `int`s between 0 and 255 to set the base color of the LEDs. This is in order of White, Red, Green, Blue. Example: [0, 0, 255, 0] would be Green.

#### AvrPcmSetLaserOffPayload

Topic: `avr/pcm/set_laser_off`

Turns off laser (laser off from blip mode - but doesn't prevent fire_laser)

There is no content for this class

#### AvrPcmSetLaserOnPayload

Topic: `avr/pcm/set_laser_on`

Turns on laser (in blip mode - 0.1 second on every 0.5. sec)

There is no content for this class

#### AvrPcmSetServoAbsPayload

Topic: `avr/pcm/set_servo_abs`

This sets the absolute position of a specific servo. SERVOMIN 150 is closed, and SERVOMAX 425 is open. We need to send a High and Low byte due to limitations of the API

- `"servo"` (`int`):
    ID of the servo to set the percent as an `int`. This is 0-indexed.
- `"absolute"` (`int`):
    Absolute position between SERVOMIN 150 and SERVOMAX 425

#### AvrPcmSetServoMaxPayload

Topic: `avr/pcm/set_servo_max`

This sets the maximum pulse width of a specific servo.

- `"servo"` (`int`):
    ID of the servo to set the maximum pulse width as an `int`. This is 0-indexed.
- `"max_pulse"` (`int`):
    A `int` between 0 and 1000.

#### AvrPcmSetServoMinPayload

Topic: `avr/pcm/set_servo_min`

This sets the minimum pulse width of a specific servo.

- `"servo"` (`int`):
    ID of the servo to set the minimum pulse width as an `int`. This is 0-indexed.
- `"min_pulse"` (`int`):
    A `int` between 0 and 1000.

#### AvrPcmSetServoOpenClosePayload

Topic: `avr/pcm/set_servo_open_close`

This opens or closes a specific servo.

- `"servo"` (`int`):
    ID of the servo to open or close as an `int`. This is 0-indexed.
- `"action"` (`Literal["open", "close"]`):
    Either the literal string "open" or "close".

#### AvrPcmSetServoPctPayload

Topic: `avr/pcm/set_servo_pct`

This sets the percentage of a specific servo. 0 is closed, and 100 is open.

- `"servo"` (`int`):
    ID of the servo to set the percent as an `int`. This is 0-indexed.
- `"percent"` (`int`):
    A `int` between 0 and 100.

#### AvrPcmSetTempColorPayload

Topic: `avr/pcm/set_temp_color`

This sets the color of the LED strip on the PCC temporarily

- `"wrgb"` (`Tuple[int, int, int, int]`):
    A list of 4 `int`s between 0 and 255 to set the base color of the LEDs. This is in order of White, Red, Green, Blue. Example: [0, 0, 255, 0] would be Green.
- `"time"` (`float`):
    Optional `float` for the number of seconds the color should be set for. Default is 0.5.

#### AvrStatusLightApriltagsPayload

Topic: `avr/status/light/apriltags`

There is no content for this class

#### AvrStatusLightFcmPayload

Topic: `avr/status/light/fcm`

There is no content for this class

#### AvrStatusLightPcmPayload

Topic: `avr/status/light/pcm`

There is no content for this class

#### AvrStatusLightThermalPayload

Topic: `avr/status/light/thermal`

There is no content for this class

#### AvrStatusLightVioPayload

Topic: `avr/status/light/vio`

There is no content for this class

#### AvrThermalReadingPayload

Topic: `avr/thermal/reading`

This publishes data from the thermal camera

- `"data"` (`str`):
    The raw data from the thermal camera are integer values from an 8x8 grid of pixels. This data is then converted into a bytearray and base64 encoded. Any example of how to unpack this data:
    
    ```python
    import base64
    import json
    
    data = json.loads(payload)["data"]
    base64_decoded = data.encode("utf-8")
    as_bytes = base64.b64decode(base64_decoded)
    pixel_ints = list(bytearray(as_bytes))
    ```

#### AvrVioConfidencePayload

Topic: `avr/vio/confidence`

This reports the tracking camera's confidence

- `"tracker"` (`float`):
    Number between 0 and 100 of tracking confidence

#### AvrVioHeadingPayload

Topic: `avr/vio/heading`

This reports the measued heading of the drone from the tracking camera.

- `"degrees"` (`float`):
    Heading in degrees

#### AvrVioOrientationEulPayload

Topic: `avr/vio/orientation/eul`

This reports the measued attitude of the drone from the tracking camera.

- `"psi"` (`float`):
    Roll in radians
- `"theta"` (`float`):
    Pitch in radians
- `"phi"` (`float`):
    Yaw in radians

#### AvrVioOrientationQuatPayload

Topic: `avr/vio/orientation/quat`

This reports the measued attitude of the drone from the tracking camera.

- `"w"` (`float`):
    Quaternion w value
- `"x"` (`float`):
    Quaternion x value
- `"y"` (`float`):
    Quaternion y value
- `"z"` (`float`):
    Quaternion z value

#### AvrVioPositionNedPayload

Topic: `avr/vio/position/ned`

This reports the measured position of the drone in local coordinates from the tracking camera.

- `"n"` (`float`):
    X position in a local North/East/Down coordinate system in meters
- `"e"` (`float`):
    Y position in a local North/East/Down coordinate system in meters
- `"d"` (`float`):
    Z position in a local North/East/Down coordinate system in meters

#### AvrVioResyncPayload

Topic: `avr/vio/resync`

This reports significant position differences from the tracking camera, and detected AprilTags at known positions.

- `"n"` (`float`):
    X position difference in a local North/East/Down coordinate system in meters
- `"e"` (`float`):
    Y position difference in a local North/East/Down coordinate system in meters
- `"d"` (`float`):
    Z position difference in a local North/East/Down coordinate system in meters
- `"heading"` (`float`):
    Heading difference in degrees

#### AvrVioVelocityNedPayload

Topic: `avr/vio/velocity/ned`

This reports the measued velocity vectors of the drone from the tracking camera.

- `"n"` (`float`):
    X velocity in a local North/East/Down coordinate system in meters per second
- `"e"` (`float`):
    Y velocity in a local North/East/Down coordinate system in meters per second
- `"d"` (`float`):
    Z velocity in a local North/East/Down coordinate system in meters per second
