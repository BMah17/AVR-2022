# This file is automatically generated. DO NOT EDIT!
# fmt: off

from __future__ import annotations

from typing import Any, List, Literal, Optional, Protocol, Tuple, TypedDict

# ======== helper classes ========



class AvrApriltagsRawTags(TypedDict):
    id: int
    """
    The ID of the AprilTag
    """
    pos: AvrApriltagsRawTagsPos
    rotation: Tuple[Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float, float]]
    """
    The 3x3 rotation matrix
    """



class AvrApriltagsRawTagsPos(TypedDict):
    x: float
    """
    The position in meters of the camera relative to the AprilTag's X frame
    """
    y: float
    """
    The position in meters of the camera relative to the AprilTag's Y frame
    """
    z: float
    """
    The position in meters of the camera relative to the AprilTag's Z frame
    """



class AvrApriltagsSelectedPos(TypedDict):
    """
    The position of the vehicle in world frame in centimeters
    """

    n: float
    """
    The +north position of the vehicle relative to the world origin in world frame
    """
    e: float
    """
    The +east position of the vehicle relative to the world origin in world frame
    """
    d: float
    """
    The +down position of the vehicle relative to the world origin in world frame
    """



class AvrApriltagsVisibleTags(TypedDict):
    id: int
    """
    The ID of the AprilTag
    """
    horizontal_dist: float
    """
    The horizontal scalar distance from vehicle to AprilTag, in centimeters
    """
    vertical_dist: float
    """
    The vertical scalar distance from vehicle to AprilTag, in centimeters
    """
    angle_to_tag: float
    """
    The angle formed by the vector pointing from the vehicles body to the AprilTag in world frame relative to world-north
    """
    heading: float
    """
    The heading of the vehicle in world frame
    """
    pos_rel: AvrApriltagsVisibleTagsPosRel
    """
    The relative position of the vehicle to the tag in world frame in centimeters
    """
    pos_world: AvrApriltagsVisibleTagsPosWorld
    """
    The position of the vehicle in world frame in centimeters (if the tag has no truth data, this will not be present in the output)
    """



class AvrApriltagsVisibleTagsPosRel(TypedDict):
    """
    The relative position of the vehicle to the tag in world frame in centimeters
    """

    x: float
    """
    The x (+north/-south) position of the vehicle relative to the AprilTag in world frame
    """
    y: float
    """
    The y (+east/-west) position of the vehicle relative to the AprilTag in world frame
    """
    z: float
    """
    The z (+down/-up) position of the vehicle relative to the AprilTag in world frame
    """



class AvrApriltagsVisibleTagsPosWorld(TypedDict):
    """
    The position of the vehicle in world frame in centimeters (if the tag has no truth data, this will not be present in the output)
    """

    x: Optional[float]
    """
    The x position of the vehicle relative to the world origin (this is the ship) in world frame (for reference the mountain is **north** of the beach)
    """
    y: Optional[float]
    """
    The y position of the vehicle relative to the world origin in world frame
    """
    z: Optional[float]
    """
    The z position of the vehicle relative to the world origin in world frame
    """


# =========== payloads ===========



class AvrApriltagsFpsPayload(TypedDict):
    """
    Topic: `avr/apriltags/fps`
    
    This reports the framerate of AprilTag processing
    """

    fps: int
    """
    Number of frames of video data processed in the last second
    """


class _AvrApriltagsFpsCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/apriltags/fps` topic
    """
    def __call__(self, payload: AvrApriltagsFpsPayload) -> Any:
        ...


class AvrApriltagsRawPayload(TypedDict):
    """
    Topic: `avr/apriltags/raw`
    
    This topic publishes the raw AprilTag data
    """

    tags: List[AvrApriltagsRawTags]


class _AvrApriltagsRawCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/apriltags/raw` topic
    """
    def __call__(self, payload: AvrApriltagsRawPayload) -> Any:
        ...


class AvrApriltagsSelectedPayload(TypedDict):
    """
    Topic: `avr/apriltags/selected`
    
    This topic publishes its best candidate for position feedback
    """

    tag_id: int
    """
    The id of the tag
    """
    pos: AvrApriltagsSelectedPos
    """
    The position of the vehicle in world frame in centimeters
    """
    heading: float


class _AvrApriltagsSelectedCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/apriltags/selected` topic
    """
    def __call__(self, payload: AvrApriltagsSelectedPayload) -> Any:
        ...


class AvrApriltagsVisiblePayload(TypedDict):
    """
    Topic: `avr/apriltags/visible`
    
    This topic publishes the transformed AprilTag data
    """

    tags: List[AvrApriltagsVisibleTags]


class _AvrApriltagsVisibleCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/apriltags/visible` topic
    """
    def __call__(self, payload: AvrApriltagsVisiblePayload) -> Any:
        ...


class AvrAutonomousBuildingDropPayload(TypedDict):
    """
    Topic: `avr/autonomous/building/drop`
    
    This enables or disables a building payload drop. This is not used by any Bell code, but available to students to listen to.
    """

    id: int
    """
    0-index ID of the relevant building
    """
    enabled: bool
    """
    Boolean of whether the building should have drop enabled
    """


class _AvrAutonomousBuildingDropCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/autonomous/building/drop` topic
    """
    def __call__(self, payload: AvrAutonomousBuildingDropPayload) -> Any:
        ...


class AvrAutonomousEnablePayload(TypedDict):
    """
    Topic: `avr/autonomous/enable`
    
    This enables or disables autonomous mode. This is not used by any Bell code, but available to students to.
    """

    enabled: bool


class _AvrAutonomousEnableCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/autonomous/enable` topic
    """
    def __call__(self, payload: AvrAutonomousEnablePayload) -> Any:
        ...


class AvrFcmAttitudeEulerPayload(TypedDict):
    """
    Topic: `avr/fcm/attitude/euler`
    
    This reports the current attitude of the drone from the flight controller.
    """

    roll: float
    """
    Roll in degrees
    """
    pitch: float
    """
    Pitch in degrees
    """
    yaw: float
    """
    Yaw in degrees
    """


class _AvrFcmAttitudeEulerCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/fcm/attitude/euler` topic
    """
    def __call__(self, payload: AvrFcmAttitudeEulerPayload) -> Any:
        ...


class AvrFcmBatteryPayload(TypedDict):
    """
    Topic: `avr/fcm/battery`
    
    This reports battery information from the flight controller.
    """

    voltage: float
    """
    Battery voltage
    """
    soc: float
    """
    State of charge (0 - 100)
    """


class _AvrFcmBatteryCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/fcm/battery` topic
    """
    def __call__(self, payload: AvrFcmBatteryPayload) -> Any:
        ...


class AvrFcmEventsPayload(TypedDict):
    """
    Topic: `avr/fcm/events`
    
    This reports events from the flight controller such as flight mode changes.
    """

    name: str
    """
    The name of the event.
    """
    payload: str
    """
    The payload of the event.
    """


class _AvrFcmEventsCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/fcm/events` topic
    """
    def __call__(self, payload: AvrFcmEventsPayload) -> Any:
        ...


class AvrFcmGpsInfoPayload(TypedDict):
    """
    Topic: `avr/fcm/gps_info`
    
    This reports the current status of the flight controller's GPS connection.
    """

    num_satellites: int
    """
    Number of visible satellites in use. HIL GPS will appear as 13.
    """
    fix_type: str
    """
    GPS fix type
    """


class _AvrFcmGpsInfoCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/fcm/gps_info` topic
    """
    def __call__(self, payload: AvrFcmGpsInfoPayload) -> Any:
        ...


class AvrFcmHilGpsStatsPayload(TypedDict):
    """
    Topic: `avr/fcm/hil_gps_stats`
    
    This reports statistics on the HIL GPS data that is fed into the flight controller.
    """

    num_frames: int
    """
    This is the number of messages that have been sent to the flight controller since the software has started.
    """


class _AvrFcmHilGpsStatsCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/fcm/hil_gps_stats` topic
    """
    def __call__(self, payload: AvrFcmHilGpsStatsPayload) -> Any:
        ...


class AvrFcmLocationGlobalPayload(TypedDict):
    """
    Topic: `avr/fcm/location/global`
    
    This reports the current position of the drone in global coordinates from the flight controller.
    """

    lat: float
    """
    Latitude in degrees
    """
    lon: float
    """
    Longitude in degrees
    """
    alt: float
    """
    Altitude relative to takeoff altitude in meters
    """
    hdg: float
    """
    Heading in degrees.
    """


class _AvrFcmLocationGlobalCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/fcm/location/global` topic
    """
    def __call__(self, payload: AvrFcmLocationGlobalPayload) -> Any:
        ...


class AvrFcmLocationHomePayload(TypedDict):
    """
    Topic: `avr/fcm/location/home`
    
    This reports the current position of the drone's home position in global coordinates.
    """

    lat: float
    """
    Latitude in degrees of the home position
    """
    lon: float
    """
    Longitude in degrees of the home position
    """
    alt: float
    """
    Altitude relative to the home position in meters
    """


class _AvrFcmLocationHomeCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/fcm/location/home` topic
    """
    def __call__(self, payload: AvrFcmLocationHomePayload) -> Any:
        ...


class AvrFcmLocationLocalPayload(TypedDict):
    """
    Topic: `avr/fcm/location/local`
    
    This reports the current position of the drone in local coordinates from the flight controller.
    """

    dX: float
    """
    X position in a local North/East/Down coordinate system in meters
    """
    dY: float
    """
    Y position in a local North/East/Down coordinate system in meters
    """
    dZ: float
    """
    Z position in a local North/East/Down coordinate system in meters
    """


class _AvrFcmLocationLocalCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/fcm/location/local` topic
    """
    def __call__(self, payload: AvrFcmLocationLocalPayload) -> Any:
        ...


class AvrFcmStatusPayload(TypedDict):
    """
    Topic: `avr/fcm/status`
    
    This reports general status of the flight controller.
    """

    armed: bool
    """
    Boolean of if the drone is currently armed
    """
    mode: str
    """
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
    """


class _AvrFcmStatusCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/fcm/status` topic
    """
    def __call__(self, payload: AvrFcmStatusPayload) -> Any:
        ...


class AvrFcmVelocityPayload(TypedDict):
    """
    Topic: `avr/fcm/velocity`
    
    This reports the current velocity vectors of the drone from the flight controller.
    """

    vX: float
    """
    X velocity in a local North/East/Down coordinate system in meters per second
    """
    vY: float
    """
    Y velocity in a local North/East/Down coordinate system in meters per second
    """
    vZ: float
    """
    Z velocity in a local North/East/Down coordinate system in meters per second
    """


class _AvrFcmVelocityCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/fcm/velocity` topic
    """
    def __call__(self, payload: AvrFcmVelocityPayload) -> Any:
        ...


class AvrFusionAttitudeEulerPayload(TypedDict):
    """
    Topic: `avr/fusion/attitude/euler`
    
    This reports the computed attitude of the drone from our sensor fusion.
    """

    psi: float
    """
    Roll in radians
    """
    theta: float
    """
    Pitch in radians
    """
    phi: float
    """
    Yaw in radians
    """


class _AvrFusionAttitudeEulerCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/fusion/attitude/euler` topic
    """
    def __call__(self, payload: AvrFusionAttitudeEulerPayload) -> Any:
        ...


class AvrFusionAttitudeHeadingPayload(TypedDict):
    """
    Topic: `avr/fusion/attitude/heading`
    
    This reports the computed heading of the drone from our sensor fusion.
    """

    heading: float
    """
    Heading in degrees
    """


class _AvrFusionAttitudeHeadingCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/fusion/attitude/heading` topic
    """
    def __call__(self, payload: AvrFusionAttitudeHeadingPayload) -> Any:
        ...


class AvrFusionAttitudeQuatPayload(TypedDict):
    """
    Topic: `avr/fusion/attitude/quat`
    
    This reports the computed attitude of the drone from our sensor fusion.
    """

    w: float
    """
    Quaternion w value
    """
    x: float
    """
    Quaternion x value
    """
    y: float
    """
    Quaternion y value
    """
    z: float
    """
    Quaternion z value
    """


class _AvrFusionAttitudeQuatCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/fusion/attitude/quat` topic
    """
    def __call__(self, payload: AvrFusionAttitudeQuatPayload) -> Any:
        ...


class AvrFusionClimbratePayload(TypedDict):
    """
    Topic: `avr/fusion/climbrate`
    
    This reports the computed rate of climb of the drone from our sensor fusion.
    """

    climb_rate_fps: float
    """
    Rate of climb in feet per second
    """


class _AvrFusionClimbrateCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/fusion/climbrate` topic
    """
    def __call__(self, payload: AvrFusionClimbratePayload) -> Any:
        ...


class AvrFusionCoursePayload(TypedDict):
    """
    Topic: `avr/fusion/course`
    
    This reports the computed course of the drone from our sensor fusion.
    """

    course: float
    """
    Course in degrees
    """


class _AvrFusionCourseCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/fusion/course` topic
    """
    def __call__(self, payload: AvrFusionCoursePayload) -> Any:
        ...


class AvrFusionGeoPayload(TypedDict):
    """
    Topic: `avr/fusion/geo`
    
    This reports the computed position of the drone in global coordinates from our sensor fusion.
    """

    lat: float
    """
    Latitude in degrees
    """
    lon: float
    """
    Longitude in degrees
    """
    alt: float
    """
    Altitude relative to takeoff altitude in meters
    """


class _AvrFusionGeoCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/fusion/geo` topic
    """
    def __call__(self, payload: AvrFusionGeoPayload) -> Any:
        ...


class AvrFusionGroundspeedPayload(TypedDict):
    """
    Topic: `avr/fusion/groundspeed`
    
    This reports the computed groundspeed of the drone from our sensor fusion.
    """

    groundspeed: float
    """
    Groundspeed of the drone in meters per second. This is a normal vector of the N and E velocities.
    """


class _AvrFusionGroundspeedCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/fusion/groundspeed` topic
    """
    def __call__(self, payload: AvrFusionGroundspeedPayload) -> Any:
        ...


class AvrFusionHilGpsPayload(TypedDict):
    """
    Topic: `avr/fusion/hil_gps`
    
    This is the raw data that will get converted to a MAVLink message and sent to the flight controller for HIL GPS. <https://mavlink.io/en/messages/common.html#HIL_GPS>
    """

    time_usec: int
    """
    UNIX epoch timestamp in microseconds
    """
    fix_type: int
    """
    0-1: no fix, 2: 2D fix, 3: 3D fix.
    """
    lat: int
    """
    WGS84 Latitude * 10000000
    """
    lon: int
    """
    WGS84 Longitude * 10000000
    """
    alt: int
    """
    Altitude from sea level in mm. Positive for up.
    """
    eph: int
    """
    GPS HDOP horizontal dilution of position
    """
    epv: int
    """
    GPS VDOP vertical dilution of position
    """
    vel: int
    """
    GPS ground speed in centimeters per second
    """
    vn: int
    """
    GPS velocity in north direction in centimeters per second
    """
    ve: int
    """
    GPS velocity in east direction in centimeters per second
    """
    vd: int
    """
    GPS velocity in down direction in centimeters per second
    """
    cog: int
    """
    Course over ground in degrees
    """
    satellites_visible: int
    """
    Number of satellites visible. This is hardcoded to 13 for our HIL GPS.
    """
    heading: int
    """
    Custom heading field. This is the heading in degrees * 100.
    """


class _AvrFusionHilGpsCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/fusion/hil_gps` topic
    """
    def __call__(self, payload: AvrFusionHilGpsPayload) -> Any:
        ...


class AvrFusionPositionNedPayload(TypedDict):
    """
    Topic: `avr/fusion/position/ned`
    
    This reports the computed position of the drone in local coordinates from our sensor fusion.
    """

    n: float
    """
    X position in a local North/East/Down coordinate system in meters
    """
    e: float
    """
    Y position in a local North/East/Down coordinate system in meters
    """
    d: float
    """
    Z position in a local North/East/Down coordinate system in meters
    """


class _AvrFusionPositionNedCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/fusion/position/ned` topic
    """
    def __call__(self, payload: AvrFusionPositionNedPayload) -> Any:
        ...


class AvrFusionVelocityNedPayload(TypedDict):
    """
    Topic: `avr/fusion/velocity/ned`
    
    This reports the computed velocity vectors of the drone from our sensor fusion.
    """

    Vn: float
    """
    X velocity in a local North/East/Down coordinate system in meters per second
    """
    Ve: float
    """
    Y velocity in a local North/East/Down coordinate system in meters per second
    """
    Vd: float
    """
    Z velocity in a local North/East/Down coordinate system in meters per second
    """


class _AvrFusionVelocityNedCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/fusion/velocity/ned` topic
    """
    def __call__(self, payload: AvrFusionVelocityNedPayload) -> Any:
        ...


class AvrPcmFireLaserPayload(TypedDict):
    """
    Topic: `avr/pcm/fire_laser`
    
    Fires the laser for a 0.25 sec pulse. Has a cooldown of 0.5 sec.
    """



class _AvrPcmFireLaserCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/pcm/fire_laser` topic
    """
    def __call__(self, payload: AvrPcmFireLaserPayload) -> Any:
        ...


class AvrPcmSetBaseColorPayload(TypedDict):
    """
    Topic: `avr/pcm/set_base_color`
    
    This sets the color of the LED strip on the PCC
    """

    wrgb: Tuple[int, int, int, int]
    """
    A list of 4 `int`s between 0 and 255 to set the base color of the LEDs. This is in order of White, Red, Green, Blue. Example: [0, 0, 255, 0] would be Green.
    """


class _AvrPcmSetBaseColorCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/pcm/set_base_color` topic
    """
    def __call__(self, payload: AvrPcmSetBaseColorPayload) -> Any:
        ...


class AvrPcmSetLaserOffPayload(TypedDict):
    """
    Topic: `avr/pcm/set_laser_off`
    
    Turns off laser (laser off from blip mode - but doesn't prevent fire_laser)
    """



class _AvrPcmSetLaserOffCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/pcm/set_laser_off` topic
    """
    def __call__(self, payload: AvrPcmSetLaserOffPayload) -> Any:
        ...


class AvrPcmSetLaserOnPayload(TypedDict):
    """
    Topic: `avr/pcm/set_laser_on`
    
    Turns on laser (in blip mode - 0.1 second on every 0.5. sec)
    """



class _AvrPcmSetLaserOnCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/pcm/set_laser_on` topic
    """
    def __call__(self, payload: AvrPcmSetLaserOnPayload) -> Any:
        ...


class AvrPcmSetServoAbsPayload(TypedDict):
    """
    Topic: `avr/pcm/set_servo_abs`
    
    This sets the absolute position of a specific servo. SERVOMIN 150 is closed, and SERVOMAX 425 is open. We need to send a High and Low byte due to limitations of the API
    """

    servo: int
    """
    ID of the servo to set the percent as an `int`. This is 0-indexed.
    """
    absolute: int
    """
    Absolute position between SERVOMIN 150 and SERVOMAX 425
    """


class _AvrPcmSetServoAbsCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/pcm/set_servo_abs` topic
    """
    def __call__(self, payload: AvrPcmSetServoAbsPayload) -> Any:
        ...


class AvrPcmSetServoMaxPayload(TypedDict):
    """
    Topic: `avr/pcm/set_servo_max`
    
    This sets the maximum pulse width of a specific servo.
    """

    servo: int
    """
    ID of the servo to set the maximum pulse width as an `int`. This is 0-indexed.
    """
    max_pulse: int
    """
    A `int` between 0 and 1000.
    """


class _AvrPcmSetServoMaxCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/pcm/set_servo_max` topic
    """
    def __call__(self, payload: AvrPcmSetServoMaxPayload) -> Any:
        ...


class AvrPcmSetServoMinPayload(TypedDict):
    """
    Topic: `avr/pcm/set_servo_min`
    
    This sets the minimum pulse width of a specific servo.
    """

    servo: int
    """
    ID of the servo to set the minimum pulse width as an `int`. This is 0-indexed.
    """
    min_pulse: int
    """
    A `int` between 0 and 1000.
    """


class _AvrPcmSetServoMinCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/pcm/set_servo_min` topic
    """
    def __call__(self, payload: AvrPcmSetServoMinPayload) -> Any:
        ...


class AvrPcmSetServoOpenClosePayload(TypedDict):
    """
    Topic: `avr/pcm/set_servo_open_close`
    
    This opens or closes a specific servo.
    """

    servo: int
    """
    ID of the servo to open or close as an `int`. This is 0-indexed.
    """
    action: Literal["open", "close"]
    """
    Either the literal string "open" or "close".
    """


class _AvrPcmSetServoOpenCloseCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/pcm/set_servo_open_close` topic
    """
    def __call__(self, payload: AvrPcmSetServoOpenClosePayload) -> Any:
        ...


class AvrPcmSetServoPctPayload(TypedDict):
    """
    Topic: `avr/pcm/set_servo_pct`
    
    This sets the percentage of a specific servo. 0 is closed, and 100 is open.
    """

    servo: int
    """
    ID of the servo to set the percent as an `int`. This is 0-indexed.
    """
    percent: int
    """
    A `int` between 0 and 100.
    """


class _AvrPcmSetServoPctCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/pcm/set_servo_pct` topic
    """
    def __call__(self, payload: AvrPcmSetServoPctPayload) -> Any:
        ...


class AvrPcmSetTempColorPayload(TypedDict):
    """
    Topic: `avr/pcm/set_temp_color`
    
    This sets the color of the LED strip on the PCC temporarily
    """

    wrgb: Tuple[int, int, int, int]
    """
    A list of 4 `int`s between 0 and 255 to set the base color of the LEDs. This is in order of White, Red, Green, Blue. Example: [0, 0, 255, 0] would be Green.
    """
    time: float
    """
    Optional `float` for the number of seconds the color should be set for. Default is 0.5.
    """


class _AvrPcmSetTempColorCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/pcm/set_temp_color` topic
    """
    def __call__(self, payload: AvrPcmSetTempColorPayload) -> Any:
        ...


class AvrStatusLightApriltagsPayload(TypedDict):
    """
    Topic: `avr/status/light/apriltags`
    """



class _AvrStatusLightApriltagsCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/status/light/apriltags` topic
    """
    def __call__(self, payload: AvrStatusLightApriltagsPayload) -> Any:
        ...


class AvrStatusLightFcmPayload(TypedDict):
    """
    Topic: `avr/status/light/fcm`
    """



class _AvrStatusLightFcmCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/status/light/fcm` topic
    """
    def __call__(self, payload: AvrStatusLightFcmPayload) -> Any:
        ...


class AvrStatusLightPcmPayload(TypedDict):
    """
    Topic: `avr/status/light/pcm`
    """



class _AvrStatusLightPcmCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/status/light/pcm` topic
    """
    def __call__(self, payload: AvrStatusLightPcmPayload) -> Any:
        ...


class AvrStatusLightThermalPayload(TypedDict):
    """
    Topic: `avr/status/light/thermal`
    """



class _AvrStatusLightThermalCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/status/light/thermal` topic
    """
    def __call__(self, payload: AvrStatusLightThermalPayload) -> Any:
        ...


class AvrStatusLightVioPayload(TypedDict):
    """
    Topic: `avr/status/light/vio`
    """



class _AvrStatusLightVioCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/status/light/vio` topic
    """
    def __call__(self, payload: AvrStatusLightVioPayload) -> Any:
        ...


class AvrThermalReadingPayload(TypedDict):
    """
    Topic: `avr/thermal/reading`
    
    This publishes data from the thermal camera
    """

    data: str
    """
    The raw data from the thermal camera are integer values from an 8x8 grid of pixels. This data is then converted into a bytearray and base64 encoded. Any example of how to unpack this data:
    
    ```python
    import base64
    import json
    
    data = json.loads(payload)["data"]
    base64_decoded = data.encode("utf-8")
    as_bytes = base64.b64decode(base64_decoded)
    pixel_ints = list(bytearray(as_bytes))
    ```
    """


class _AvrThermalReadingCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/thermal/reading` topic
    """
    def __call__(self, payload: AvrThermalReadingPayload) -> Any:
        ...


class AvrVioConfidencePayload(TypedDict):
    """
    Topic: `avr/vio/confidence`
    
    This reports the tracking camera's confidence
    """

    tracker: float
    """
    Number between 0 and 100 of tracking confidence
    """


class _AvrVioConfidenceCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/vio/confidence` topic
    """
    def __call__(self, payload: AvrVioConfidencePayload) -> Any:
        ...


class AvrVioHeadingPayload(TypedDict):
    """
    Topic: `avr/vio/heading`
    
    This reports the measued heading of the drone from the tracking camera.
    """

    degrees: float
    """
    Heading in degrees
    """


class _AvrVioHeadingCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/vio/heading` topic
    """
    def __call__(self, payload: AvrVioHeadingPayload) -> Any:
        ...


class AvrVioOrientationEulPayload(TypedDict):
    """
    Topic: `avr/vio/orientation/eul`
    
    This reports the measued attitude of the drone from the tracking camera.
    """

    psi: float
    """
    Roll in radians
    """
    theta: float
    """
    Pitch in radians
    """
    phi: float
    """
    Yaw in radians
    """


class _AvrVioOrientationEulCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/vio/orientation/eul` topic
    """
    def __call__(self, payload: AvrVioOrientationEulPayload) -> Any:
        ...


class AvrVioOrientationQuatPayload(TypedDict):
    """
    Topic: `avr/vio/orientation/quat`
    
    This reports the measued attitude of the drone from the tracking camera.
    """

    w: float
    """
    Quaternion w value
    """
    x: float
    """
    Quaternion x value
    """
    y: float
    """
    Quaternion y value
    """
    z: float
    """
    Quaternion z value
    """


class _AvrVioOrientationQuatCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/vio/orientation/quat` topic
    """
    def __call__(self, payload: AvrVioOrientationQuatPayload) -> Any:
        ...


class AvrVioPositionNedPayload(TypedDict):
    """
    Topic: `avr/vio/position/ned`
    
    This reports the measured position of the drone in local coordinates from the tracking camera.
    """

    n: float
    """
    X position in a local North/East/Down coordinate system in meters
    """
    e: float
    """
    Y position in a local North/East/Down coordinate system in meters
    """
    d: float
    """
    Z position in a local North/East/Down coordinate system in meters
    """


class _AvrVioPositionNedCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/vio/position/ned` topic
    """
    def __call__(self, payload: AvrVioPositionNedPayload) -> Any:
        ...


class AvrVioResyncPayload(TypedDict):
    """
    Topic: `avr/vio/resync`
    
    This reports significant position differences from the tracking camera, and detected AprilTags at known positions.
    """

    n: float
    """
    X position difference in a local North/East/Down coordinate system in meters
    """
    e: float
    """
    Y position difference in a local North/East/Down coordinate system in meters
    """
    d: float
    """
    Z position difference in a local North/East/Down coordinate system in meters
    """
    heading: float
    """
    Heading difference in degrees
    """


class _AvrVioResyncCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/vio/resync` topic
    """
    def __call__(self, payload: AvrVioResyncPayload) -> Any:
        ...


class AvrVioVelocityNedPayload(TypedDict):
    """
    Topic: `avr/vio/velocity/ned`
    
    This reports the measued velocity vectors of the drone from the tracking camera.
    """

    n: float
    """
    X velocity in a local North/East/Down coordinate system in meters per second
    """
    e: float
    """
    Y velocity in a local North/East/Down coordinate system in meters per second
    """
    d: float
    """
    Z velocity in a local North/East/Down coordinate system in meters per second
    """


class _AvrVioVelocityNedCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks from the `avr/vio/velocity/ned` topic
    """
    def __call__(self, payload: AvrVioVelocityNedPayload) -> Any:
        ...
