# chatserver.py
#
# This server program maintains a public ledger and list of 
# clients that are interacting with the server. Clients send 
# incoming UDP packets on port 15000, the packet payload text
# should comprise a valid VINCENTS protocol command. The server
# will sequentially parse incomming packets. The incoming 
# packets should have a message that contains a VINCENTS protocol 
# command with correct syntax. Invalid packet messages are 
# ignored.
#
# VINCENTS PROTOCOL COMMANDS:
#  name - used to "register" a user, server ties name to (IP,PORT)
#  tx   - used to add a transaction/message to ledger
#  GETLEDGER - used to request full ledger be sent
# EXAMPLES
#  packet_msg = "name|John"
#  packet_msg = "tx|Hello world!"
#  packet_msg = "tx|John sends 10 coin to Aesha."
#
#
import socket
s = socket.socket(type=socket.SOCK_DGRAM)
s.bind(('',15000))

clientdict = {} # userdict[addr] = str name
ledger = ['\n------------------\nVinCents Ledger\n']

print('VinCents server waiting')

while True:
  # handle next incoming packet
  msg, addr = s.recvfrom(2000) # blocking wait
  print('PACKET RECEIVED!')
  print('  from:', addr)
  print('  msg:', msg.decode())
  
  tokens = msg.decode().split('|')
  if len(tokens) > 2:
    # invalid transaction
    reply = 'INVALID TRANSACTION:' + msg.decode()
    print(reply)
    s.sendto(reply.encode(),addr)
  else:
    cmd = tokens[0]
    if cmd == 'name':
      # add name to client dict
      name = tokens[1]
      clientdict[addr] = name
      reply = 'Welcome new user: ' + name
      print(reply)
      # notify everyone of new user
      for addr_i in clientdict:
        s.sendto(reply.encode(), addr_i)
      # send new user the ledger
      ledger_str = ''.join(ledger) + '\n------------------'
      s.sendto(ledger_str.encode(), addr)
    elif cmd == 'tx':
      # add transaction to ledger
      tx = tokens[1]
      if addr in clientdict:
        name = clientdict[addr]
        newtx = name + ':' + tx + '\n'
        print(newtx)
        ledger.append(newtx)
        for addr_i in clientdict:
          s.sendto(newtx.encode(), addr_i)
      else:
        reply = 'UNREGISTERED addr, send NAME packet first'
        s.sendto(reply.encode(),addr)
    elif cmd == 'getledger':
      ledger_str = ''.join(ledger) + '\n------------------'
      s.sendto(ledger_str.encode(), addr)
      print('sent ledger to:', addr)
    else:
      reply = 'UNRECOGNIZED CMD:' + cmd
      print(reply)
      s.sendto(reply.encode(),addr)

s.close()
