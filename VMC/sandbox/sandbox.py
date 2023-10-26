from bell.avr.mqtt.client import MQTTModule
from bell.avr.mqtt.payloads import *
import time


# This imports the third-party Loguru library which helps make logging way easier
# and more useful.
# https://loguru.readthedocs.io/en/stable/
from loguru import logger


class Sandbox(MQTTModule):
    def __init__(self) -> None:
        super().__init__()
        # Here, we're creating a dictionary of MQTT topic names to method handles.
        self.topic_map = {
                            "avr/apriltags/visible": self.april_tag,
                            "avr/autonomous/enable": self.auton,
                            "avr/autonomous/building/drop": self.buildingListener
                         }
        self.home_val = None
        self.building_drop = False

    def auton(self, payload):
        logger.debug(payload)
        if payload["enabled"]:
            logger.debug("auton is enabled")
            self.arm()
            logger.debug("worked horray :)")
            self.takeoff()
            time.sleep(5)
            self.land()

    def buildingListener(self, payload):
        #self.building_drop = payload["enabled"]
        if payload["enabled"]:
            logger.debug(payload)
            self.open_servo()

    def arm(self) -> None:
        self.send_message(
            "/avr/fcm/actions",
            {
                "action": "arm",
                "payload": {}
            }
        )

    def open_servo(self) -> None:
        # It's super easy, use the `self.send_message` method with the first argument
        # as the topic, and the second argument as the payload.
        self.send_message(  # type: ignore (to appease type checker)
            "avr/pcm/set_servo_pct",
            {"servo": 0, "percent": 50},
        )

    def april_tag(self, payload: AvrApriltagsVisiblePayload) -> None:
        logger.debug(f'april_tag is running\npayload: {payload}')

    def captureHome(self) -> None:
        self.home_val = self.send_message(
            "avr/fcm/capture_home"
        )

    def takeoff(self) -> None:
        self.send_message(
            "/avr/fcm/actions",
            {
                "action": "takeoff",
                "payload": {
                "alt": 1
                }
            }
        )

    def land(self) -> None:
        self.send_message(
            "/avr/fcm/actions",
            {
                "action": "land",
                "payload": {}
            }
        )

    def move(self, payload, pos: str) -> None:
        if self.home_val is None:
            self.captureHome()
        north, east, down = pos
        self.send_message(
            "/avr/fcm/actions",
            {
                "action": "goto_location_ned",
                "payload": {
                "n": north,
                "e": east,
                "d": down,
                "heading": 0
                }
            }
        )


if __name__ == "__main__":
    # This is what actually initializes the Sandbox class, and executes it.
    box = Sandbox()
    # The `run` method is defined by the inherited `MQTTModule` class and is a
    # convience function to start processing incoming MQTT messages infinitely.
    box.run()
    #box.takeoff()
    #time.sleep(6)
