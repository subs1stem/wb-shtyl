import re
from datetime import timedelta

from snmp.types import INTEGER


def decode_byte_value(value):
    value = value.decode('cp1251')
    if not re.match(r'[а-яА-ЯёЁ]', value):
        value = re.sub(r'[^0-9.]', '', value)
    return value


def get_uptime(value):
    seconds = int(value / 100)
    value = str(timedelta(seconds=seconds))
    return value


def transform_item(item, key=''):
    value = eval(str(item.value))
    if isinstance(value, bytes):
        value = decode_byte_value(value)
        if key == 'DC_power':
            value = float(value) * 1000
        return value
    elif key == 'AC_flag':
        return 0 if value == 1 else 1
    elif key == 'Uptime':
        return get_uptime(value)
    return value


def read_snmp_table(table, key, mqtt_order):
    result = {}
    table = list(table)
    for item in table:
        if isinstance(item[0].value, INTEGER):
            continue
        number = str(item[0].name)[-2]
        snmp_value = str(item[0].value)
        value = transform_item(item[0])

        if 'A' in snmp_value:
            mqtt_name = f'i{key}{number}'
            mqtt_type = 'value'
            mqtt_units = 'А'
        elif 'V' in snmp_value:
            mqtt_name = f'v{key}{number}'
            mqtt_type = 'voltage'
            mqtt_units = None
        elif 'C' in snmp_value:
            mqtt_name = f't{key}{number}'
            mqtt_type = 'temperature'
            mqtt_units = None
        elif 'Hz' in snmp_value:
            mqtt_name = f'freq{key}{number}'
            mqtt_type = 'value'
            mqtt_units = 'Гц'
        else:
            mqtt_name = f'alarm{key}{number}'
            mqtt_type = 'text'
            mqtt_units = None

        result[mqtt_name] = {
            'Value': value,
            'Type': mqtt_type,
            'Units': mqtt_units,
            'Order': mqtt_order,
        }

        mqtt_order += 1

    return result
