https://tutorcs.com
WeChat: cstutorcs
QQ: 749389476
Email: tutorcs@163.com
#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2029 Zhiming Huang
#


import select
import socket
import sys
import queue
import time
import re


# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
serverPort = int(sys.argv[2])
# Bind the socket to the port
server_address = ('', serverPort)
#print('starting up on {} port {}'.format(*server_address),
#      file=sys.stderr)
server.bind(server_address)

# Listen for incoming connections
server.listen(5)

# Sockets from which we expect to read
inputs = [server]

# Sockets to which we expect to write
outputs = []

# Outgoing message queues (socket:Queue)
message_queues = {}

# request message
request_message = {}

timeout = 30

while inputs:

    # Wait for at least one of the sockets to be
    # ready for processing
#    print('waiting for the next event', file=sys.stderr)
    readable, writable, exceptional = select.select(inputs,
                                                    outputs,
                                                    inputs,
                                                    timeout)

    # Handle inputs
    for s in readable:

        if s is server:
            # A "readable" socket is ready to accept a connection
            connection, client_address = s.accept()
            connection.setblocking(0)
            inputs.append(connection)
            request_message[connection] = ""
            #new_request[s] = True
            #persistent_socket[connection] = True
            # Give the connection a queue for data
            # we want to send
            message_queues[connection] = queue.Queue()

        else:
            message1 =  s.recv(1024).decode()
            if message1:
                # First check if bad requests
                

                # if not add the message to the request message for s
                request_message[s] =  request_message[s] + message1
                message = request_message[s]
                # check if the end of the requests:
                if  message[-2:] != '\n\n':
                    continue
                # if it is the end of request, process the request
                
                # add the socket s to the output list for watching writability
                if s not in outputs:
                    outputs.append(s)


            else:
                
                # handle the situation where no messages received

    # Handle outputs
    for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except queue.Empty:
            # No messages need to be sent so stop watching
                outputs.remove(s)
                if s not in inputs:
                    s.close()
                    del message_queues[s]
                    del request_message[s]
            else:
                #print logs and send messages
                print_log(s,message_request,printresponse)
                s.send(message2send.encode())
                
                

    # Handle "exceptional conditions"
    for s in exceptional:
        #print('exception condition on', s.getpeername(),
         #     file=sys.stderr)
        # Stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

        # Remove message queue
        del message_queues[s]
    
    if not readable and writable and exceptional:
        #handle timeout events
