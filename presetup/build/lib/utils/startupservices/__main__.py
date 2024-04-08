import sys

from .ipfetchstartuprentdrive import ip_fetch
from .portlistenstartuprentdrive import listen_ports

if len(sys.argv) != 2:
    print("USAGE: python -m utils.startupservices [ip_fetch|port_listen]")
else:
    cmd = sys.argv[1]
    
    if cmd == 'ip_fetch':
        ip_fetch()
    elif cmd == 'port_listen':
        listen_ports()
    else:
        print("USAGE: python -m utils.startupservices [ip_fetch|port_listen]")