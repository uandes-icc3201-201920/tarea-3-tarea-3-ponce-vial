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

hostname= socket.gethostname()
HOST =socket.gethostbyname(hostname)
PORT = 55001  

def funcion_thread(connection):
    while True:
        print ("Cliente se ha conectado")
        mensaje = connection.recv(4096).decode()
        print (mensaje)
        
        if not mensaje:
            break
        
        else:
            lista_elementos=mensaje.split("/")
            mensaje_salida=""
            COMMAND=""
            ADD=""
            KEY=""
            VALUE=""
            key=0
            value=""
            RESPUESTA = ""
            ERROR=""
            
            
            #HEADER:
            ID = lista_elementos[0]
            IP = lista_elementos[1]
            ROR = lista_elementos[2]
            CODE = lista_elementos[3]
            ESTADO = lista_elementos[4]
            FORMATO = lista_elementos[5]
            SUBFORMATO = lista_elementos[6]
            
            #Request
            if ROR == 0:
                COMMAND=lista_elementos[7]
                ADD=int(lista_elementos[8])
                KEY=int(lista_elementos[9])
                VALUE=int(lista_elementos[10])
                
                #informacion adicional
                if KEY==1:
                    key=int(lista_elementos[11])
                
                    if VALUE==1:
                        value=lista_elementos[12]
                
                elif KEY==0:
                    if VALUE==1:
                        value=lista_elementos[11]
                    
            #############
            #Comandos:
            if COMMAND=="DISCONNECT":
                break
            
            elif COMMAND == "INSERT":
                if VALUE==1: #insert(key,value)
                    #Revisamos primero si la key ya existe
                    if key in db:
                        ERROR = "/La Key ya se encuentra en la BD"
                        mensaje_salida = "{}/{}/1/{}/150/text/plain/ /{}/".format(ID,HOST,random.randint(1000,5000),ERROR)
                        connection.sendall(mensaje_salida)
                    
                    else:
                        db[key]=value
                        RESPUESTA = "/Se insertó correctamente"
                        mensaje_salida = "{}/{}/1/{}/500/text/plain/{}/".format(ID,HOST,random.randint(1000,5000),RESPUESTA)
                        connection.sendall(mensaje_salida)
            
                elif VALUE== 0:  #insert(value)
                    #Revisamos primero si la clave autogerenada ya existe
                    global clave_autogenerada
                    while clave_autogenerada in db:
                        clave_autogenerada+=1
                    
                    db[clave_autogenerada]=value
                    RESPUESTA= "La Key generada es {}".format(clave_autogenerada)
                    print(RESPUESTA)
                    mensaje_salida = "{}/{}/1/{}/500/text/plain/{}/".format(ID,HOST,random.randint(1000,5000),RESPUESTA)
                    connection.sendall(mensaje_salida)
    
    
    connection.close()
    return


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
    