# This file is automatically generated. DO NOT EDIT!
# fmt: off

from __future__ import annotations

import copy
import json
from typing import Any, Literal, overload

import paho.mqtt.client as mqtt
from loguru import logger

from .constants import _MQTTTopicCallableTypedDict, _MQTTTopicPayloadTypedDict
from .payloads import (
    AvrApriltagsFpsPayload,
    AvrApriltagsRawPayload,
    AvrApriltagsSelectedPayload,
    AvrApriltagsVisiblePayload,
    AvrAutonomousBuildingDropPayload,
    AvrAutonomousEnablePayload,
    AvrFcmAttitudeEulerPayload,
    AvrFcmBatteryPayload,
    AvrFcmEventsPayload,
    AvrFcmGpsInfoPayload,
    AvrFcmHilGpsStatsPayload,
    AvrFcmLocationGlobalPayload,
    AvrFcmLocationHomePayload,
    AvrFcmLocationLocalPayload,
    AvrFcmStatusPayload,
    AvrFcmVelocityPayload,
    AvrFusionAttitudeEulerPayload,
    AvrFusionAttitudeHeadingPayload,
    AvrFusionAttitudeQuatPayload,
    AvrFusionClimbratePayload,
    AvrFusionCoursePayload,
    AvrFusionGeoPayload,
    AvrFusionGroundspeedPayload,
    AvrFusionHilGpsPayload,
    AvrFusionPositionNedPayload,
    AvrFusionVelocityNedPayload,
    AvrPcmFireLaserPayload,
    AvrPcmSetBaseColorPayload,
    AvrPcmSetLaserOffPayload,
    AvrPcmSetLaserOnPayload,
    AvrPcmSetServoAbsPayload,
    AvrPcmSetServoMaxPayload,
    AvrPcmSetServoMinPayload,
    AvrPcmSetServoOpenClosePayload,
    AvrPcmSetServoPctPayload,
    AvrPcmSetTempColorPayload,
    AvrStatusLightApriltagsPayload,
    AvrStatusLightFcmPayload,
    AvrStatusLightPcmPayload,
    AvrStatusLightThermalPayload,
    AvrStatusLightVioPayload,
    AvrThermalReadingPayload,
    AvrVioConfidencePayload,
    AvrVioHeadingPayload,
    AvrVioOrientationEulPayload,
    AvrVioOrientationQuatPayload,
    AvrVioPositionNedPayload,
    AvrVioResyncPayload,
    AvrVioVelocityNedPayload,
)
from ..utils.decorators import try_except


class MQTTModule:
    """
    Generic MQTT Module class that should be inherited by other modules.
    The `topic_map` attribute should be a dictionary of topics to functions
    that will be called with a payload.
    """

    def __init__(self):
        # these should be not be changed
        self.mqtt_host = "mqtt"
        self.mqtt_port = 18830

        # create the MQTT client
        self._mqtt_client = mqtt.Client(protocol=mqtt.MQTTv311)

        # set up the on connect and on message handlers
        self._mqtt_client.on_connect = self.on_connect
        self._mqtt_client.on_message = self.on_message

        # dictionary of MQTT topics to callback functions
        # this is intended to be overwritten by the child class
        self.topic_map: _MQTTTopicCallableTypedDict = {}

        # maintain a cache of the last message sent on a topic by this module
        self.message_cache: _MQTTTopicPayloadTypedDict = {}

        # record if we were started with loop forever
        self._looped_forever = False

    def run(self) -> None:
        """
        Class entrypoint. Connects to the MQTT broker and starts the MQTT loop
        in a blocking manner.
        """
        # connect the MQTT client
        self._mqtt_client.connect(host=self.mqtt_host, port=self.mqtt_port, keepalive=60)
        # run forever
        self._looped_forever = True
        self._mqtt_client.loop_forever()

    def run_non_blocking(self) -> None:
        """
        Class entrypoint. Connects to the MQTT broker and starts the MQTT loop
        in a non-blocking manner.
        """
        # connect the MQTT client
        self._mqtt_client.connect(host=self.mqtt_host, port=self.mqtt_port, keepalive=60)
        # run in background
        self._mqtt_client.loop_start()

    @try_except()
    def on_message(self, client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage) -> None:
        """
        On message callback, dispatches the message to the appropriate function.
        """
        # logger.debug(f"Recieved {msg.topic}: {msg.payload}")
        if msg.topic in self.topic_map:
            # we talk JSON, no exceptions
            payload = json.loads(msg.payload)
            self.topic_map[msg.topic](payload)

    def on_connect(self, client: mqtt.Client, userdata: Any, flags: dict, rc: int) -> None:
        """
        On connection callback. Subscribes to MQTT topics in the topic map.
        """
        logger.debug(f"Connected with result {rc}")

        for topic in self.topic_map.keys():
            client.subscribe(topic)
            logger.success(f"Subscribed to: {topic}")

    @overload
    def send_message(self, topic: Literal["avr/apriltags/fps"], payload: AvrApriltagsFpsPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/apriltags/raw"], payload: AvrApriltagsRawPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/apriltags/selected"], payload: AvrApriltagsSelectedPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/apriltags/visible"], payload: AvrApriltagsVisiblePayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/autonomous/building/drop"], payload: AvrAutonomousBuildingDropPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/autonomous/enable"], payload: AvrAutonomousEnablePayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/fcm/attitude/euler"], payload: AvrFcmAttitudeEulerPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/fcm/battery"], payload: AvrFcmBatteryPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/fcm/events"], payload: AvrFcmEventsPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/fcm/gps_info"], payload: AvrFcmGpsInfoPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/fcm/hil_gps_stats"], payload: AvrFcmHilGpsStatsPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/fcm/location/global"], payload: AvrFcmLocationGlobalPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/fcm/location/home"], payload: AvrFcmLocationHomePayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/fcm/location/local"], payload: AvrFcmLocationLocalPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/fcm/status"], payload: AvrFcmStatusPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/fcm/velocity"], payload: AvrFcmVelocityPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/fusion/attitude/euler"], payload: AvrFusionAttitudeEulerPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/fusion/attitude/heading"], payload: AvrFusionAttitudeHeadingPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/fusion/attitude/quat"], payload: AvrFusionAttitudeQuatPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/fusion/climbrate"], payload: AvrFusionClimbratePayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/fusion/course"], payload: AvrFusionCoursePayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/fusion/geo"], payload: AvrFusionGeoPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/fusion/groundspeed"], payload: AvrFusionGroundspeedPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/fusion/hil_gps"], payload: AvrFusionHilGpsPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/fusion/position/ned"], payload: AvrFusionPositionNedPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/fusion/velocity/ned"], payload: AvrFusionVelocityNedPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/pcm/fire_laser"], payload: AvrPcmFireLaserPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/pcm/set_base_color"], payload: AvrPcmSetBaseColorPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/pcm/set_laser_off"], payload: AvrPcmSetLaserOffPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/pcm/set_laser_on"], payload: AvrPcmSetLaserOnPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/pcm/set_servo_abs"], payload: AvrPcmSetServoAbsPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/pcm/set_servo_max"], payload: AvrPcmSetServoMaxPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/pcm/set_servo_min"], payload: AvrPcmSetServoMinPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/pcm/set_servo_open_close"], payload: AvrPcmSetServoOpenClosePayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/pcm/set_servo_pct"], payload: AvrPcmSetServoPctPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/pcm/set_temp_color"], payload: AvrPcmSetTempColorPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/status/light/apriltags"], payload: AvrStatusLightApriltagsPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/status/light/fcm"], payload: AvrStatusLightFcmPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/status/light/pcm"], payload: AvrStatusLightPcmPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/status/light/thermal"], payload: AvrStatusLightThermalPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/status/light/vio"], payload: AvrStatusLightVioPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/thermal/reading"], payload: AvrThermalReadingPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/vio/confidence"], payload: AvrVioConfidencePayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/vio/heading"], payload: AvrVioHeadingPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/vio/orientation/eul"], payload: AvrVioOrientationEulPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/vio/orientation/quat"], payload: AvrVioOrientationQuatPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/vio/position/ned"], payload: AvrVioPositionNedPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/vio/resync"], payload: AvrVioResyncPayload, force_write: bool) -> None: ...

    @overload
    def send_message(self, topic: Literal["avr/vio/velocity/ned"], payload: AvrVioVelocityNedPayload, force_write: bool) -> None: ...

    def send_message(self, topic, payload, force_write = False) -> None:
        """
        Sends a message to the MQTT broker. Enabling `force_write` will
        forcefully send the message, bypassing threading mutex. Only use this
        if you know what you're doing.
        """
        # logger.debug(f"Sending message to {topic}: {payload}")
        self._mqtt_client.publish(topic, json.dumps(payload))

        # https://github.com/eclipse/paho.mqtt.python/blob/9782ab81fe7ee3a05e74c7f3e1d03d5611ea4be4/src/paho/mqtt/client.py#L1563
        # pre-emptively write network data while still in a callback, bypassing
        # the thread mutex.
        # can only be used if run with .loop_forever()
        # https://www.bellavrforum.org/t/sending-messages-to-pcc-from-sandbox/311/8
        if self._looped_forever or force_write:
            self._mqtt_client.loop_write()

        self.message_cache[topic] = copy.deepcopy(payload)