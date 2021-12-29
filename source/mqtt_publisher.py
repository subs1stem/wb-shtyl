from paho.mqtt.publish import multiple

from settings import *


def publish_meta(name: str, error: str):
    msgs = [
        {'topic': '{}/meta/name'.format(ROOT_MQTT_TOPIC),
         'payload': name,
         'retain': True},

        {'topic': '{}/meta/error'.format(ROOT_MQTT_TOPIC),
         'payload': error,
         'retain': True},
    ]

    multiple(msgs, hostname=MQTT_BROKER_IP)


def publish_control(data,
                    name: str,
                    data_type: str,
                    units: str,
                    error: str,
                    order=None,
                    retain=True):
    msgs = [
        {'topic': '{}/controls/{}'.format(ROOT_MQTT_TOPIC, name),
         'payload': data,
         'retain': retain},

        {'topic': '{}/controls/{}/meta/type'.format(ROOT_MQTT_TOPIC, name),
         'payload': data_type,
         'retain': retain},

        {'topic': '{}/controls/{}/meta/units'.format(ROOT_MQTT_TOPIC, name),
         'payload': units,
         'retain': retain},

        {'topic': '{}/controls/{}/meta/order'.format(ROOT_MQTT_TOPIC, name),
         'payload': order,
         'retain': retain},

        {'topic': '{}/controls/{}/meta/error'.format(ROOT_MQTT_TOPIC, name),
         'payload': error,
         'retain': retain},
    ]

    multiple(msgs, hostname=MQTT_BROKER_IP)
