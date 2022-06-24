import re
from pydantic.json import ENCODERS_BY_TYPE
from ipaddress import IPv4Address
from sqlalchemy.dialects import postgresql

class Net:
    mac: str = "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    hostname: str = "^[0-9a-zA-Z_\-\.]+$"
    ip4: str = "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    ip6: str = "^((([0-9a-fA-F]){1,4})\:){7}([0-9a-fA-F]){1,4}$"

    @classmethod
    @property
    def ip(cls):
        return f"{cls.ip4}|{cls.ip6}"

# add encoders for postgres specific types to pydantic
class CustomValidator:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, str) and cls._pattern:
            pattern = re.compile(cls._pattern)
            if not pattern.match(v):
                raise TypeError(f"Invalid value {v} (pattern: {cls._pattern})")
        return v
        

    @classmethod
    def __modify_schema__(cls, field_schema):
        if cls._example:
            field_schema.update(type="string", example=cls._example)

class INET(postgresql.INET, CustomValidator):
    _example = '192.168.0.1'
    _pattern = Net.ip

class MACADDR(postgresql.MACADDR, CustomValidator):
    _example = 'aa:bb:cc:dd:ee:ff:00'
    _pattern = Net.mac


class HostName(CustomValidator):
    _example = 'example.com'
    _pattern = Net.hostname

ENCODERS_BY_TYPE |= {INET: str} | {MACADDR: str}