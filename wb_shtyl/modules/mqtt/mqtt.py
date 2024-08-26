import paho.mqtt.client as mqtt


class MQTTClient:
    def __init__(self, host: str, root_topic: str):
        self.client = mqtt.Client()
        self.host = host
        self.root_topic = root_topic
        self.client.connect(self.host)

    def __del__(self):
        self.disconnect()

    def publish_meta(self, name: str, error: str = '') -> None:
        self.publish_multiple([
            (f'{self.root_topic}/meta/name', name, 1, True),
            (f'{self.root_topic}/meta/error', error, 1, True),
        ])

    def publish_control(
            self,
            data,
            name: str,
            data_type: str,
            units: str,
            error: str = '',
            order: int = None,
            retain: bool = True,
    ) -> None:
        control_topic = f'{self.root_topic}/controls/{name}'
        self.publish_multiple([
            (control_topic, data, 0, retain),
            (f'{control_topic}/meta/type', data_type, 0, retain),
            (f'{control_topic}/meta/units', units, 0, retain),
            (f'{control_topic}/meta/order', order, 0, retain),
            (f'{control_topic}/meta/error', error, 0, retain),
        ])

    def publish_error(self, name: str, retain: bool = True) -> None:
        self.client.publish(f'{self.root_topic}/controls/{name}/meta/error', 'r', retain=retain)

    def publish_multiple(self, msgs) -> None:
        for topic, payload, qos, retain in msgs:
            self.client.publish(topic, payload, qos, retain)

    def disconnect(self) -> None:
        self.client.disconnect()
