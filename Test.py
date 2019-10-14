#! python3
# _*_ coding: utf-8 _*_

import binascii
import ipaddress

ADDRESSES = [
    '192.168.0.105',
    'fe80::d5e7:c867:dab0:9b95'
]

for ip in ADDRESSES:
    addr = ipaddress.ip_address(ip)
    print('{!r}'.format(addr))
    print('  IP version:', addr.version)
    print('  is private:', addr.is_private)
    print(' packed form:', binascii.hexlify(addr.packed))
    print('     integer:', int(addr))
