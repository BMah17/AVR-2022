from bell.avr.mqtt.client import MQTTModule
from bell.avr.mqtt.payloads import AvrFcmVelocityPayload
from bell.avr.mqtt.payloads import AvrApriltagsVisiblePayload

# This imports the third-party Loguru library which helps make logging way easier
# and more useful.
# https://loguru.readthedocs.io/en/stable/
from loguru import logger


class Sandbox(MQTTModule):
    def __init__(self) -> None:
        super().__init__()
        # Here, we're creating a dictionary of MQTT topic names to method handles.
        self.topic_map = {"avr/fcm/velocity": self.show_velocity, "avr/apriltags/visible": self.april_tag}

    # This is what executes whenever a message is received on the "avr/fcm/velocity"
    # topic. The content of the message is passed to the `payload` argument.
    # The `AvrFcmVelocityMessage` class here is beyond the scope of AVR.
    def show_velocity(self, payload: AvrFcmVelocityPayload) -> None:
        vx = payload["vX"]
        vy = payload["vY"]
        vz = payload["vZ"]
        v_ms = (vx, vy, vz)

        # Use methods like `debug`, `info`, `success`, `warning`, `error`, and
        # `critical` to log data that you can see while your code runs.

        logger.debug(f"Velocity information: {v_ms} m/s")

    def open_servo(self) -> None:
        # It's super easy, use the `self.send_message` method with the first argument
        # as the topic, and the second argument as the payload.
        self.send_message(  # type: ignore (to appease type checker)
            "avr/pcm/set_servo_open_close",
            {"servo": 0, "action": "open"},
        )

    def april_tag(self, payload: AvrApriltagsVisiblePayload) -> None:
        logger.debug(f'april_tag is running\npayload: {payload}')


if __name__ == "__main__":
    # This is what actually initializes the Sandbox class, and executes it.
    box = Sandbox()
    # The `run` method is defined by the inherited `MQTTModule` class and is a
    # convience function to start processing incoming MQTT messages infinitely.
    box.run()
