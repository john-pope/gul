from datetime import datetime
from pydantic import BaseModel

from gul.types import INET, MACADDR, HostName


class ARPEntry(BaseModel):
    id: int
    ip: INET
    mac: MACADDR
    device: HostName
    port: int

    startstamp: datetime
    stopstamp: datetime
