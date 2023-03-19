# vincentclient.py
#
# This client program prints messages from the vincents
# server and allows users to type commands to be sent 
# to the server. The program binds to local UDP port 
# 15001. The receive loop runs as a separate thread so 
# that it does not block user input.
#
# VINCENTS PROTOCOL COMMANDS:
#  name - used to "register" a user, server ties name to (IP,PORT)
#  tx   - used to add a transaction/message to ledger
#  getledger - used to request full ledger be sent
# EXAMPLES
#  packet_msg = "name|John"
#  packet_msg = "tx|Hello world!"
#  packet_msg = "tx|John sends 10 coin to Aesha."
#
#---------------------------------------------------------------

import socket     # for network comm functionality
import threading  # for two "threads" of execution
import time

SERVER_ADDR = ('35.188.79.120',15000) # (IP,PORT)

def receiver():
  """ This function is an infinite loop for receiving
  and printing packets on udp socket s which must have
  been established. """
  while True:
    msg, addr = s.recvfrom(2048)
    print('SERVER: ' + msg.decode())

# MAIN
with socket.socket(type=socket.SOCK_DGRAM) as s:
  s.bind(('',15001))
  
  rx_thread = threading.Thread(target=receiver, daemon=True)
  rx_thread.start()

  while True:
    time.sleep(1) # wait 1 sec before allowing another cmd
    print('   VinCents client, enter cmd: [name/tx/getledger/exit]')
    user_input = input(': ')
    if user_input == 'exit':
      break
    if user_input == '':
      continue
    tokens = user_input.split('|')
    cmd = tokens[0]
    if cmd not in ['name','tx','getledger','']:
      print('   unrecognized command:', user_input)
      continue
    elif cmd == 'getledger':
      s.sendto(b'getledger', SERVER_ADDR)
      print('-->CMD SENT: getledger')
    elif len(tokens) != 2:
      print('   invalid syntax')
    elif cmd == 'name' or cmd == 'tx':
      s.sendto(user_input.encode(), SERVER_ADDR)
      print('-->CMD SENT: ', user_input)

print('VINCENTS CLIENT COMPLETE') 
