import asyncio
from datetime import datetime

from database import database
from database.tables import addresses, arpentries, deviceport, leases_history
from sqlalchemy import literal_column, nullsfirst
from sqlalchemy.sql import select, text
from sqlalchemy.sql.functions import coalesce, max, now

from gul.models import LookupResults


async def lookup_by_hostname(hostname: str):
    return {"hostname": hostname}


async def lookup_by_mac(mac: str):
    return {"mac": mac}


async def lookup_by_ip(ip: str, limit=10, offset=0):
    arp_query = (
        select(
            arpentries.c.id,
            arpentries.c.ip,
            arpentries.c.mac,
            arpentries.c.port,
            arpentries.c.startstamp,
            coalesce(arpentries.c.stopstamp, now()),
            deviceport.c.device,
            deviceport.c.description,
        )
        .join(deviceport, arpentries.c.port == deviceport.c.port)
        .where(
            arpentries.c.ip == ip,
        )
        .order_by(
            nullsfirst(arpentries.c.stopstamp.desc()), arpentries.c.startstamp.desc()
        )
        .limit(limit)
        .offset(offset)
    )

    arp, dhcp = await asyncio.gather(database.fetch_all(arp_query), getleasesbyip(ip))

    return LookupResults(arp=arp, dhcp=dhcp)


async def getleasesbyip(ip):
    # check to see if its a static ip. if so, leases don't matter
    ipam_static_query = select(
        addresses.c.mac,
        addresses.c.address,
        literal_column(f"'{datetime.fromtimestamp(0)}'").label("starts"),
        literal_column(f"'{datetime.now()}'").label("ends"),
        literal_column("'Ipam'").label("source"),
        literal_column("'Static'").label("type"),
    ).where(addresses.c.address == ip)

    ipam_static_address = await database.fetch_one(ipam_static_query)

    if (
        ipam_static_address and ipam_static_address["mac"]
    ):  # does the result exist and have a mac address?
        return [ipam_static_address]

    # do the slow dhcp log search. this could use some optimization
    ipam_dhcp_query = (
        select(
            leases_history.c.mac,
            leases_history.c.address,
            leases_history.c.starts,
            max(leases_history.c.ends).label("ends"),
            literal_column("'Ipam'").label("source"),
            literal_column("'Dynamic'").label("type"),
        )
        .where(
            leases_history.c.ends > text("NOW() - interval '2 days'"),
            leases_history.c.address == ip,
        )
        .group_by(
            leases_history.c.mac, leases_history.c.address, leases_history.c.starts
        )
    )

    return await database.fetch_all(ipam_dhcp_query)
