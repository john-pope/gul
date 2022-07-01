from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from gul.types import CIDR, INET, MACADDR, HostName


class ARPEntry(BaseModel):
    id: int
    ip: INET
    mac: MACADDR
    device: HostName
    port: int

    startstamp: datetime
    stopstamp: Optional[datetime]


class ARPResult(BaseModel):
    id: int
    ip: INET
    mac: MACADDR
    device: HostName
    port: int
    description: str

    startstamp: datetime
    stopstamp: Optional[datetime]


class Address(BaseModel):
    addres: INET
    mac: MACADDR
    pool: int
    reserved: bool
    network: CIDR
    changed: datetime
    changed_by: int


class AddressResult(BaseModel):
    address: INET
    mac: MACADDR
    source: str
    type: str
    starts: datetime
    ends: datetime


class LookupResults(BaseModel):
    arp: List[ARPResult]
    dhcp: List[AddressResult]
