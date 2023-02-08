#!/usr/bin/python3
# ECHO SERVER
# Binds to UDP socket.
# Receives a message, converts received text to uppercase, then sends it back to
# who sent it.
# Runs as an infinite loop; you need to press ctrl-c to exit.
#-------------------------------------------------------------------------------
import socket  
# The import loads a module, i.e. additional python code
# In this case, the socket module contains functions and classes for
# accessing the OS's network interface.


# In python (and many other programming languages), it is customary to make 
# constants (i.e. variables that you don't intend to change over the life of the
# program) in all caps. Note that python lets you
SERVER_HOST_STR = 'localhost'
SERVER_PORT_INT = 12000
SERVER_ADDRESS_TUPLE = (SERVER_HOST_STR, SERVER_PORT_INT)
MAX_BYTES_RX_INT = 2048

# The following line of code can be interpreted as follows:
#  from the socket module, create an instance of the socket class, which is
#  configured for Internet Protocol (IP) version 4 (which is specified by 
#  AF_INET in the "socket module language"), and which is also configured for 
#  the User Datagram Protocol (UDP) (which is specified as SOCK_DGRAM in the 
#  socket module language). The variable name active_socket holds the socket
#  instance. Using the "with" statement (aka "context"), ensures that the socket
#  gets closed automatically if there is an error.
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as active_socket:

  # The bind statement configures the socket to be attached to the hostname and 
  # port designated in the address (if the port is free). 
  active_socket.bind(SERVER_ADDRESS_TUPLE)
  
  print('The echo server is ready to receive and SEND BACK')
  
  # The while statement below is a never-ending loop. The program "blocks", or 
  # pauses, while it is waiting for new data to be received by the socket, 
  # thus keeping the CPU from racing needlessly.
  while True:
    print('...socket listening...press ctrl-c to quit')
    # The program will "block" at the following recvfrom function until data
    # is delivered to this socket (i.e. to this computer on the listening port).
    rxd_message_bytes, client_address = active_socket.recvfrom(MAX_BYTES_RX_INT)

    # If we get here, a message must have been received.
    print('MESSAGE RXD:')
    print('  FROM:', client_address)
    # Data is sent over the sockets as a number of bytes (i.e. 8 bits), whereas
    # python stores a str in a variable format. The following decode function 
    # converts the the byte-format data into a str.
    rxd_message_str = rxd_message_bytes.decode()
    print('  MSG :', rxd_message_str)
    
    # We next echo the message back out after converting to uppercase.
    tx_message_str = rxd_message_str.upper()
    print('MESSAGE TX:')
    print('  TO:', client_address)
    print('  MSG :', tx_message_str)
    # Convert the str into the byte format needed by the socket (called "utf-8")
    tx_message_bytes = tx_message_str.encode()
    
    # Send out the message.
    active_socket.sendto(tx_message_bytes, client_address)
    print('...sent data to the socket...')
