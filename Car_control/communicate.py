# Socket communication
import socket
import time
#from CV import output

HOST = '10.49.31.212' #wlan
PORT = 6666

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST,PORT))
sock.listen(2)

while True:
    connect, addr = sock.accept()
    #try:
#         connect.settimeout(10)
#         buf = connect.recv(1024)
#         if buf:
#             connect.send(b'Welcome!')
#             print('Connect!')
#         else:
#             connect.send(b'Go!')
#     except socket.timeout:
#         print('time out')     
    connect.settimeout(10)
    buf = connect.recv(1024)
    if buf:
        #connect.send(output.encode())
        connect.send(b'hi')
        print('Connect!')
    
    connect.close()
    
    