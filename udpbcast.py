import socket

MY_HOST = ''   # '' is a shorthand way to designate localhost
MY_PORT = 0    # port 0 means "find a suitable port" 
MY_PORT = 12000 
MY_ADDR = (MY_HOST, MY_PORT)
TO_HOST = '<broadcast>'  # <broadcast> is a special IPv4 "host" for whole LAN
TO_PORT = 12000
TO_ADDR = (TO_HOST, TO_PORT)
MSG = 'Hello from udpbcast.py!'

print('ATTEMPTING BCAST')
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(MY_ADDR)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    data = bytes(MSG, 'utf-8')
    s.sendto(data, TO_ADDR)
    print('BCAST SENT:')
    print('  PORT: ', TO_ADDR[1])
    print('  MSG : ', MSG)
finally:
    s.close()
    