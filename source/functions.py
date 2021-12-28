import re
from datetime import timedelta


def decode_byte_value(key, value):
    value = value.decode('cp1251')
    if not re.match(r'[а-яА-ЯёЁ]', value):
        value = re.sub(r'[^0-9.]', '', value)
        if key == 'DC power':
            value = float(value) * 1000
    return value


def get_uptime(value):
    seconds = int(value / 100)
    value = str(timedelta(seconds=seconds))
    return value
