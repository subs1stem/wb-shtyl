import time
from os import getenv

from dotenv import load_dotenv
from snmp import Manager
from snmp.exceptions import Timeout
from snmp.v1.exceptions import NoSuchName

from modules.mqtt.mqtt import MQTTClient
from modules.snmp.channels import CHANNELS
from modules.snmp.functions import *

load_dotenv()

FAIL_COUNT = 0

mqtt = MQTTClient(getenv('MQTT_BROKER_HOST'), getenv('MQTT_ROOT_TOPIC'))
mqtt.publish_meta(getenv('MQTT_DEVICE_NAME'))

while True:
    manager = Manager(getenv('DEVICE_SNMP_COMMUNITY').encode())
    host = getenv('DEVICE_SNMP_HOST')

    try:
        for key in CHANNELS:
            try:
                oid = CHANNELS[key]['OID']
                mqtt_order = CHANNELS[key]['Order']
                if 'Table' in key:
                    key = key.replace('Table', '')
                    response = manager.walk(host, oid)
                    table = read_snmp_table(response, key, mqtt_order)
                    for name in table:
                        mqtt_data = table[name]['Value']
                        mqtt_type = table[name]['Type']
                        mqtt_units = table[name]['Units']
                        mqtt_order = table[name]['Order']
                        mqtt.publish_control(data=mqtt_data,
                                             name=name,
                                             data_type=mqtt_type,
                                             units=mqtt_units,
                                             error='',
                                             order=mqtt_order)
                else:
                    mqtt_type = CHANNELS[key]['Type']
                    mqtt_units = CHANNELS[key]['Units']
                    response = manager.get(host, oid)
                    value = transform_item(response[0], key)
                    mqtt.publish_control(data=value,
                                         name=key,
                                         data_type=mqtt_type,
                                         units=mqtt_units,
                                         error='',
                                         order=mqtt_order)

            except NoSuchName:
                continue

        FAIL_COUNT = 0

    except Timeout as e:
        FAIL_COUNT += 1
        print(f'Request for {e} timed out')

    finally:
        manager.close()

        if FAIL_COUNT > 2:
            mqtt.publish_error('Work_status')

        time.sleep(int(getenv('POLLING_INTERVAL')))
