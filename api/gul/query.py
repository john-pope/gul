import re
from typing import Dict
from gul.types import Net
from gul.repositories.arpentries import lookup_by_hostname, lookup_by_ip, lookup_by_mac


lookup_map: Dict[str, callable] = {
    Net.mac: lookup_by_mac,
    Net.ip: lookup_by_ip,
    Net.hostname: lookup_by_hostname,
}


def gul_lookup(search: str):
    for lookup_pattern, lookup in lookup_map.items():
        pattern = re.compile(lookup_pattern)

        if pattern.match(search):
            return lookup(search)

    raise InvalidLookupPattern()


class InvalidLookupPattern(Exception):
    pass