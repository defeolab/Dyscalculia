# run this notebook (possibly on a google colab instance) to simulate a client trying to access the server remotely through the internet
# this works only when my (Franco) machine is running the server.

#alternatively use the localhost to just simulate client interaction with local client and server

import socket

import time

HOST = "127.0.0.1"  # Ip address
PORT = 65432  # Port that forwards to the right server socket of my machine


running = True

n= 2

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    for i in range(0, n):
      s.sendall(b"TRIALS:")
      data = s.recv(2048)

      print(f"Received {data}")

      time.sleep(1)

      mockResponse = 'COMPLETE:{"results":[{"DecisionTime":719.0502,"Correct":true,"TrialData":{"area1Data":{"circleRadius":0.75,"sizeOfChicken":2.5002152919769289,"averageSpaceBetween":0.6000000238418579,"numberOfChickens":45},"area2Data":{"circleRadius":0.699999988079071,"sizeOfChicken":2.5002152919769289,"averageSpaceBetween":0.6000000238418579,"numberOfChickens":37},"chickenShowTime":4.0,"maxTrialTime":8.0}}]}'
      s.send(str.encode(mockResponse))
      data = s.recv(2048)
      #print(f"Received {data}")
    
    s.send(str.encode("END:"))
    
print(f"Received {data!r}")