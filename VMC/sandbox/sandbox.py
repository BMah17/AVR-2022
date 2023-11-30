"""from bell.avr.mqtt.client import MQTTModule
from bell.avr import utils
from bell.avr.utils import timing
from bell.avr.mqtt.payloads import(
    AvrAutonomousEnablePayload,
    AvrPcmSetBaseColorPayload,
    AvrApriltagsVisiblePayload,
    AvrPcmSetTempColorPayload,
    AvrPcmSetServoOpenClosePayload,
    AvrApriltagsSelectedPayload,
)
import random

from loguru import logger
import time
class Sandbox(MQTTModule):
    is_auton = False
    tag_list = []
    id = 9
    horiz_dist = 10000
    can_flash = True
    def __init__(self):
        super().__init__()
        self.topic_map = {"avr/apriltags/visible": self.show_april_tag_detected, "avr/autonomous/enable": self.autonomous_enabled}
    def autonomous_enabled(self, payload: AvrAutonomousEnablePayload):
        self.is_auton = payload["enabled"]
        logger.debug(f'self.is_auton = {self.is_auton}')

    def show_april_tag_detected(self, payload: AvrApriltagsVisiblePayload):
        logger.debug("April tag detected")
        self.tag_list = payload["tags"]
        self.id = self.tag_list[0]["id"]
        self.horiz_dist = self.tag_list[0]["horizontal_dist"]
        self.vertDist = self.tag_list[0]["vertical_dist"]

        if self.horiz_dist < 10 and self.vertDist < 60:
            if self.can_flash:
                self.can_flash = False
                self.flash_lights()
            self.control_servo(1, 'open')
        elif self.horiz_dist > 10 or self.vertDist > 60:
            self.control_servo(1, 'close')
            self.can_flash = True

    def control_servo(self, num, action):
        self.send_message(
            "avr/pcm/set_servo_open_close",
            {"servo": num, "action": action}
        )

    def flash_lights(self):
        for _ in range(3):
            self.send_message(
                "avr/pcm/set_temp_color",
                {"wrgb": (0, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))}
            )
            time.sleep(.5)

    def drop_ball(self):
        self.control_servo(2, 'open')
        time.sleep(1)
        self.control_servo(2, 'close')
        time.sleep(1)
        self.canDrop = True

if __name__ == "__main__":
    box = Sandbox()
    box.run()
"""
from bell.avr.mqtt.client import MQTTModule
from bell.avr.mqtt.payloads import *
from bell.avr.utils import timing
import time
import random
from threading import Thread


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
                            "avr/autonomous/building/drop": self.drop
                         }
        self.home_val = None
        self.building_drop = False
        self.balls = True
        self.doorOne = True
        self.colors = [[0,255,0,0],[0,0,255,0],[0,0,0,255]]
        self.canFlash = True

#open servo 0 (left one with dropper facing u upside down): self.open_servo(), close servo: self.open_servo(0, 0)
#open servo 1 (right one with dropper facing u upside down): self.open_servo(1, 0), close servo: self.open_servo(1, 79)

    def flashLedStrip(self) -> None:
        if self.canFlash:
            self.canFlash = False
            logger.debug("Entry: flashLedStrip")
            self.send_message("avr/pcm/set_temp_color", {"wrgb": (0,0,255,0)})
            time.sleep(1)
            self.send_message("avr/pcm/set_temp_color", {"wrgb": (0,0,255,0)})
            time.sleep(1)
            self.send_message("avr/pcm/set_temp_color", {"wrgb": (0,0,255,0)})
        logger.debug("Exit: flashLedStrip")

    def fligh(self):
        logger.debug("it is running")
        self.arm()
        time.sleep(1)
        self.takeoff()
        time.sleep(1)
        self.land()


    def auton(self, payload):
        """if payload["enabled"]:
            loop_thread = Thread(target=self.fligh)
            loop_thread.setDaemon(
                    True
                )
            loop_thread.start()"""

    def drop(self, payload):
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

    def open_servo_abs(self, percent = 450) -> None:
        # It's super easy, use the `self.send_message` method with the first argument
        # as the topic, and the second argument as the payload.
        logger.debug("set servo")
        self.send_message(  # type: ignore (to appease type checker)
            "avr/pcm/set_servo_abs",
            {"absolute": percent, "servo": 0},
        )

    def open_servo(self, servo = 0, percent = 68) -> None:
        # It's super easy, use the `self.send_message` method with the first argument
        # as the topic, and the second argument as the payload.
        logger.debug("open servo")
        self.send_message(  # type: ignore (to appease type checker)
            "avr/pcm/set_servo_pct",
            {"servo": servo, "percent": percent},
        )

    def close_servo(self, servo = 0, action = "close") -> None:
        # It's super easy, use the `self.send_message` method with the first argument
        # as the topic, and the second argument as the payload.
        logger.debug("close servo")
        self.send_message(  # type: ignore (to appease --type checker)
            "avr/pcm/set_servo_open_close",
            {"servo": servo, "action": action},
        )
    def setServo(self, wowverygood, servo = 0):
        self.send_message(
            "avr/pcm/set_servo_abs",
            {"servo": servo, "absolute": wowverygood}
        )

    def april_tag(self, payload: AvrApriltagsVisiblePayload) -> None:
        logger.debug(payload)
        if payload["tags"][0]["horizontal_dist"] < 30 and payload["tags"][0]["vertical_dist"] < 130:
            if self.balls:
                loop_thread = Thread(target=self.flashLedStrip)
                loop_thread.setDaemon(
                    True
                )
                loop_thread.start()
                if not self.doorOne and payload["tags"][0]["id"] == 3 and payload["tags"][0]["id"] == 2 and payload["tags"][0]["id"] == 1:
                    self.open_servo_abs()
                    logger.debug("door one activate")
                    self.doorOne = True
                elif payload["tags"][0]["id"] == 3 and payload["tags"][0]["id"] == 2 and payload["tags"][0]["id"] == 1:
                    self.open_servo_abs(2300)
                    logger.debug("door two activate")
                    self.doorOne = False
        else:
            self.canFlash = True
            if not self.balls and payload["tags"][0]["id"] == 3 and payload["tags"][0]["id"] == 2 and payload["tags"][0]["id"] == 1:
                self.open_servo(1150)
            self.balls = True

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
    # loop_thread = Thread(target=box.ledChecker)
    # loop_thread.setDaemon(
    #     True
    # )
    # loop_thread.start()
    box.run()
    #box.takeoff()
    #time.sleep(6)
