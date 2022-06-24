import asyncio
from datetime import datetime
from database import database
from database.tables import arpentries

ORDER_BY = 'stopstamp DESC NULLS FIRST, startstamp DESC'


def lookup_by_hostname(hostname: str):
    return {"hostname": hostname}

def lookup_by_mac(mac: str):
    return {"mac": mac}

async def lookup_by_ip(ip: str):
    arp_query = f"""
        select
            arpentries.mac,arpentries.ip,startstamp,coalesce(stopstamp, now()) as stopstamp,
            deviceport.device, description
        from
            arpentries
            left join deviceport on (
                arpentries.device = deviceport.device
                and arpentries.port = deviceport.port
            ) where ip=:ip order by {ORDER_BY} limit 10;
    """

    arp, dhcp = await asyncio.gather(
        database.fetch_all(arp_query, {'ip': ip}),
        getleasesbyip(ip)
    )
    return {"arp": arp,  "dhcp": dhcp }
    # getleasesbyip



async def getleasesbyip(ip):
    #check to see if its a static ip. if so, leases don't matter
    ipam_static_query = "select mac, address from addresses where address=:ip"
    ipam_static_address = await database.fetch_all(ipam_static_query, {'ip': ip})
    print(ipam_static_address[0])
    if (ipam_static_address and ipam_static_address[0]['mac']): #does the result exist and have a mac address?
        return [{ "mac": ipam_static_address['mac'], "address": ipam_static_address['address'], "starts": datetime.fromtimestamp(0), "ends": datetime.now(), "source": 'Ipam', "type": 'Static'}]
    #do the slow dhcp log search. this could use some optimization
    #cur.execute("select mac, starts, max(ends), 'Ipam', 'Dynamic' from leases_log_all_v where ends > NOW() - interval '2 days' and address=%s group by mac, address, starts;", (ip,))
    ipam_dhcp_query = """
        select
            mac, address, starts, max(ends), 'Ipam' as source, 'Dynamic' as type
        from
            leases_history
        where
            ends > NOW() - interval '2 days'
            and address=:ip
        group by
            mac, address, starts;"""
    return database.fetch_all(ipam_dhcp_query, {'ip': ip})