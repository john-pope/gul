import re
from typing import Dict

from gul.repositories.lookup import lookup_by_hostname, lookup_by_ip, lookup_by_mac
from gul.types import InvalidRequestException, Net

lookup_map: Dict[str, callable] = {
    Net.mac: lookup_by_mac,
    Net.ip: lookup_by_ip,
    Net.hostname: lookup_by_hostname,
}


async def gul_lookup(search: str):
    for lookup_pattern, lookup in lookup_map.items():
        pattern = re.compile(lookup_pattern)

        if pattern.match(search):
            return await lookup(search)

    raise InvalidRequestException(
        f"Invalid lookup", value=search, patterns=list(lookup_map.keys())
    )
