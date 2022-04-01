import re

pat_ips = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}")
#TODO: get the routing instance and search against BGP Peers / IPs
#pat_routing_instance = re.compile("")
cidr_dict = {"31": 2, "30": 4, "29": 8, "28": 16}

sometext = """
set routing-instances THIS-INST-01 interface ge-0/0/0.231
This is just some text to parse through
set interfaces ge-0/0/0 unit 231 family inet address 192.168.32.24/31
set interfaces ge-0/0/0 unit 232 family inet address 192.168.32.9/30
set interfaces ge-0/0/0 unit 234 family inet address 192.168.32.17/29
Hey this is some more text down below to test with :)
"""

ips = re.findall(pat_ips, sometext)

search_commands = []

for ip in ips:
    address, mask = ip.split("/")
    octets = address.split(".")
    subnet = int(octets[3]) - int(octets[3]) % cidr_dict[mask]
    broadcast = subnet + cidr_dict[mask] - 1
    last_octets = "|".join([str(fin_oct) for fin_oct in range(subnet, broadcast)])
    last_octets = f".({last_octets})"
    search_command = "show configuration | display set | match \"" + (".").join(octets[:-1]) + last_octets
    search_commands.append(search_command)

print(search_commands)