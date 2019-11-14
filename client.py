import socket
import sys

lista_arg=[]
for arg in sys.argv:
    lista_arg.append(arg)
   
dir_socket="/tmp/db.tuples.sock"
if lista_arg[0] == "-s":
    dir_socket = lista_arg[1]
    
HOST =socket.gethostname()   # The server's hostname or IP address
PORT = 55001      # The port used by the server

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

conectado=False
cmd=""
while cmd!= "quit":
    cmd=input()
    
    if(cmd == "connect"):
			#Se conecta el socket
        server_address = (HOST, PORT)
        print ('connecting to {} port {}'.format(sys.stderr, server_address))
        sock.connect(server_address)
        conectado = True;
        print("Conectado con exito al servidor")
    
    elif(cmd == "disconnect"):
        sock.close()