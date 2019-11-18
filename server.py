import socket
import random
import _thread
import random
#Generador de palabras aleatorias para el codigo del mensaje
def Code(palabra,largo):
        palabra = list(palabra)
        lpalabra = []
        while True:
            while int(len(lpalabra)) < largo:
                dword = random.randint(0,len(palabra))
                rword = str(palabra[dword-1])
                lpalabra.append(rword)
            if largo < int(len(lpalabra)):
                break
            break
        return "".join(lpalabra)

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

lock= _thread.allocate_lock()

def funcion_thread(connection,client_address):
    print ("Cliente {} se ha conectado".format(client_address[0]))
    while True:
        code = Code("XJS654ZK",6)
        mensaje = connection.recv(4096).decode()
        
        if not mensaje:
            break
        
        else:
            elementos_protocolo=mensaje.split("\n")
            llave=0
            valor=""
            
            mensaje_salida=""
            COMMAND=""
            ADD=""
            KEY=""
            VALUE=""
            RESPUESTA = ""
            ERROR=""
            
            
            #HEADER:
            header= elementos_protocolo[0].split("/")
            ID = header[0]
            IP = header[1]
            ROR = int(header[2])
            CODE = header[3]
            ESTADO = header[4]
            FORMATO = header[5]
            SUBFORMATO = header[6]
            
            #Request
            req_res= elementos_protocolo[1].split("/")
            if ROR == 0:
                COMMAND=req_res[0]
                ADD=int(req_res[1])
                KEY=int(req_res[2])
                VALUE=int(req_res[3])
                
                #informacion adicional
                info_adi=elementos_protocolo[2].split("/")
                if KEY==1:

                    try:
                        llave=int(info_adi[0])
                    except:
                        ERROR = "Error: La Key debe ser un valor numerico"
                                        #ID/IP/ROR/CODE/ESTADO/FORMATO/SUBFORMATO\n RESPONCE\n INFO_ADI
                        mensaje_salida = "{}/{}/1/{}/100/text/plain\n \n{}".format(ID,HOST,code,ERROR)
                        connection.sendall(mensaje_salida.encode())
                        continue
                        
                
                    if VALUE==1:
                        valor=info_adi[1]
                
                elif KEY==0:
                    if VALUE==1:
                        valor=info_adi[0]
                    
            ##################################
            #Comandos:
            if COMMAND=="disconnect":
                break
            
            elif COMMAND == "insert":
                if KEY==1: #insert(key,value)
                    #Seccion critica empieza
                    lock.acquire()
                    #Revisamos primero si la key ya existe
                    if llave in db:
                        ERROR = "Error: La Key ya se encuentra en la BD"
                                        #ID/IP/ROR/CODE/ESTADO/FORMATO/SUBFORMATO\n RESPONSE\n INFO_ADI
                        mensaje_salida = "{}/{}/1/{}/150/text/plain\n \n{}".format(ID,HOST,code,ERROR)
                        connection.sendall(mensaje_salida.encode())
                    
                    else:
                        db[llave]=valor
                        RESPUESTA = "Se insertó correctamente"
                                         #ID/IP/ROR/CODE/ESTADO/FORMATO/SUBFORMATO\n RESPONSE
                        mensaje_salida = "{}/{}/1/{}/500/text/plain\n{}".format(ID,HOST,code,RESPUESTA)
                        connection.sendall(mensaje_salida.encode())
                    #Seccion critia termina
                    lock.release()
            
                elif KEY== 0:  #insert(value)
                    #Revisamos primero si la clave autogerenada ya existe
                    #Seccion critica empieza
                    lock.acquire()
                    global clave_autogenerada
                    while clave_autogenerada in db:
                        clave_autogenerada+=1
                    
                    db[clave_autogenerada]=valor
                    RESPUESTA= "La Key generada es {}".format(clave_autogenerada)
                                     #ID/IP/ROR/CODE/ESTADO/FORMATO/SUBFORMATO\n RESPONSE
                    mensaje_salida = "{}/{}/1/{}/500/text/plain/\n{}/".format(ID,HOST,code,RESPUESTA)
                    connection.sendall(mensaje_salida.encode())
                    #Seccion critia termina
                    lock.release()
            
            elif COMMAND == "get":   #get(key)
                    #Seccion critica empieza
                    lock.acquire()
                    if llave in db:
                        RESPUESTA= "El valor de la key {} es {}".format(llave,db[llave])
                                        #ID/IP/ROR/CODE/ESTADO/FORMATO/SUBFORMATO\n RESPONCE
                        mensaje_salida = "{}/{}/1/{}/500/text/plain\n{}".format(ID,HOST,code,RESPUESTA)
                        connection.sendall(mensaje_salida.encode())
                        
                    else:
                        ERROR = "Error: La Key no se encuentra en la BD"
                                        #ID/IP/ROR/CODE/ESTADO/FORMATO/SUBFORMATO\n RESPONSE\n INFO_ADI
                        mensaje_salida = "{}/{}/1/{}/200/text/plain\n \n{}".format(ID,HOST,code,ERROR)
                        connection.sendall(mensaje_salida.encode())
                    #Seccion critia termina
                    lock.release()   
                        
            elif COMMAND == "peek":  #peek(key)
                    #Seccion critica empieza
                    lock.acquire()
                    if llave in db:
                        RESPUESTA= "True"
                    else:
                        RESPUESTA= "False"
                        
                                    #ID/IP/ROR/CODE/ESTADO/FORMATO/SUBFORMATO\n RESPONCE
                    mensaje_salida = "{}/{}/1/{}/500/text/plain\n{}".format(ID,HOST,code,RESPUESTA)
                    connection.sendall(mensaje_salida.encode())
                    #Seccion critia termina
                    lock.release() 
                    
            elif COMMAND == "update":  #update(key,value)
                    #Seccion critica empieza
                    lock.acquire()
                    if llave in db:
                        db[llave]=valor
                        RESPUESTA= "El valor ha sido actualizado"
                                        #ID/IP/ROR/CODE/ESTADO/FORMATO/SUBFORMATO\n RESPONSE
                        mensaje_salida = "{}/{}/1/{}/500/text/plain\n{}".format(ID,HOST,code,RESPUESTA)
                        connection.sendall(mensaje_salida.encode())
                        
                    else:
                        ERROR = "Error: La Key no se encuentra en la BD"
                                        #ID/IP/ROR/CODE/ESTADO/FORMATO/SUBFORMATO\n RESPONSE\n INFO_ADI
                        mensaje_salida = "{}/{}/1/{}/300/text/plain\n \n{}".format(ID,HOST,code,ERROR)
                        connection.sendall(mensaje_salida.encode())
                    #Seccion critia termina
                    lock.release() 
                    
            elif COMMAND == "delete":  #delete(key)
                    #Seccion critica empieza
                    lock.acquire()
                    if llave in db:
                        del db[llave]
                        RESPUESTA= "La key ha sido eliminada con exito"
                                        #ID/IP/ROR/CODE/ESTADO/FORMATO/SUBFORMATO\n RESPONSE
                        mensaje_salida = "{}/{}/1/{}/500/text/plain\n{}".format(ID,HOST,code,RESPUESTA)
                        connection.sendall(mensaje_salida.encode())
                        
                    else:
                        ERROR = "Error: La Key no se encuentra en la BD"
                                        #ID/IP/ROR/CODE/ESTADO/FORMATO/SUBFORMATO\n RESPONSE\n INFO_ADI
                        mensaje_salida = "{}/{}/1/{}/350/text/plain\n \n{}".format(ID,HOST,code,ERROR)
                        connection.sendall(mensaje_salida.encode())
                    #Seccion critia termina
                    lock.release()
                        
            elif COMMAND == "list":  #list
                #Seccion critica empieza
                lock.acquire()
                RESPUESTA +="["
                for clave in db:
                    RESPUESTA += " " + str(clave)+ " "
                RESPUESTA +="]"
                                #ID/IP/ROR/CODE/ESTADO/FORMATO/SUBFORMATO\n RESPONCE
                mensaje_salida = "{}/{}/1/{}/500/text/plain\n{}".format(ID,HOST,code,RESPUESTA)
                connection.sendall(mensaje_salida.encode())
                #Seccion critia termina
                lock.release()

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
    _thread.start_new_thread(funcion_thread,(connection,client_address))