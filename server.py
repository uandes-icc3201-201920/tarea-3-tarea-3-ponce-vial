import socket
import random
import _thread

clave_autogenerada = random.randint(1000,10001)
db = {1020: "hola",
      1030: "como",
      1040: "estas",
      1050: "5000",
      1060: "teclado",
      1070: "144"}

def funcion_thread(connection):
    while True:
        print ("Cliente se ha conectado")
        mensaje = connection.recv(1024).decode()
        print (mensaje)
        
        if not mensaje:
            break
    
    connection.close()
    return
    
    
    
HOST =socket.gethostname()
PORT = 55001  

# Se crea el socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Se hace bind al PORT
server_address = (HOST, PORT)
print ('Server iniciado en {} puerto {}'.format(HOST,PORT))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(5)

while True:
    #ESperar conexiones hasta el infinito
    connection, client_address = sock.accept()
    _thread.start_new_thread(funcion_thread,(connection,))
    