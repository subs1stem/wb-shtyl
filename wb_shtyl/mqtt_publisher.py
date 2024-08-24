import paho.mqtt.client as mqtt


class MQTTPublisher:
    def __init__(self, broker_ip: str, root_topic: str):
        self.client = mqtt.Client()
        self.broker_ip = broker_ip
        self.root_topic = root_topic
        self.client.connect(self.broker_ip)

    def __del__(self):
        self.disconnect()

    def publish_meta(self, name: str, error: str = '') -> None:
        msgs = [
            ('{}/meta/name'.format(self.root_topic), name, 1, True),
            ('{}/meta/error'.format(self.root_topic), error, 1, True),
        ]
        self.publish_multiple(msgs)

    def publish_control(
            self,
            data,
            name: str,
            data_type: str,
            units: str,
            error: str,
            order=None,
            retain=True,
    ) -> None:
        msgs = [
            ('{}/controls/{}'.format(self.root_topic, name), data, 0, retain),
            ('{}/controls/{}/meta/type'.format(self.root_topic, name), data_type, 0, retain),
            ('{}/controls/{}/meta/units'.format(self.root_topic, name), units, 0, retain),
            ('{}/controls/{}/meta/order'.format(self.root_topic, name), order, 0, retain),
            ('{}/controls/{}/meta/error'.format(self.root_topic, name), error, 0, retain),
        ]
        self.publish_multiple(msgs)

    def publish_error(self, name: str, retain: bool = True) -> None:
        self.client.publish(
            '{}/controls/{}/meta/error'.format(self.root_topic, name),
            'r',
            retain=retain
        )

    def publish_multiple(self, msgs) -> None:
        for msg in msgs:
            topic, payload, qos, retain = msg
            self.client.publish(topic, payload, qos, retain)

    def disconnect(self) -> None:
        self.client.disconnect()
