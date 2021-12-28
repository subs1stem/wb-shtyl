import time

import snmp.v1.exceptions
from snmp import Manager
from snmp.exceptions import Timeout

from functions import *
from mqtt_publisher import *
from settings import *
from snmp_channels import CHANNELS

publish_meta(DEVICE_NAME, '')

while True:
    manager = Manager(SNMP_COMMUNITY)
    host = SNMP_DEVICE_ADDRESS
    try:
        for key in CHANNELS:
            oid = CHANNELS[key]['OID']
            data_type = CHANNELS[key]['Type']
            units = CHANNELS[key]['Units']
            order = CHANNELS[key]['Order']
            response = manager.get(host, oid)
            for item in response:
                value = eval(str(item.value))
                if isinstance(value, bytes):
                    value = decode_byte_value(key, value)
                elif key == 'AC flag':
                    value = not value
                elif key == 'Uptime':
                    value = get_uptime(value)
                publish_control(data=value,
                                name=key,
                                data_type=data_type,
                                units=units,
                                error='',
                                order=order,)

    except Timeout as e:
        print("Request for {} from host {} timed out".format(e, host))

    except snmp.v1.exceptions.NoSuchName as e:
        print("Request for {} from host {} timed out".format(e, host))

    finally:
        manager.close()
        time.sleep(POLLING_INTERVAL)
