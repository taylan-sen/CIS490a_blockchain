#!/usr/bin/python3
#-------------------------------------------------------------------------------
# Prompts the user for a message which is sent to the designated server and 
# and port using the UDP/IP protocols.
#-------------------------------------------------------------------------------
import socket

SERVER_NAME_STR = 'localhost'
SERVER_NAME_STR = ''
CLIENT_HOST_STR = ''
#SERVER_NAME_STR = '192.168.1.4' 
#SERVER_NAME_STR = 'lizard'
SERVER_PORT_INT = 12000 
CLIENT_PORT_INT = 12001
# 
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    client_socket.bind((CLIENT_HOST_STR, CLIENT_PORT_INT))
    tx_message_str = 'This is the client'
    server_host = input('Input server IP to transmit to (eg: 10.128.0.6): ')
    print('TX:', tx_message_str)
    print('TO:', (server_host, SERVER_PORT_INT))
    client_socket.sendto(tx_message_str.encode(),(server_host, SERVER_PORT_INT))
    print('...sent...')
    print('...waiting for response...')
    rx_message_bytes, server_address = client_socket.recvfrom(2048)
    print('RX:', rx_message_bytes.decode())
    print('FROM:', server_address)

