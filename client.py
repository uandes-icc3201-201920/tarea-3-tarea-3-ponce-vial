import socket
import sys
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

#Interpreta el mensaje de respuesta que manda el servidor
def InterpreteRespose(respuesta):
    resp = respuesta.split("\n")
    header = resp[0].split("/")
    respuesta = resp[1].split("/")
    #Respuesta ok
    if(header[4] == "500"):
        print(respuesta[0])
    else:
        add = resp[2]
        #Error insert
        if(header[4] == "150"):
            print(add)
        #Error get
        elif(header[4] == "200"):
            print(add)
        #Error peek
        elif(header[4] == "250"):
            print(add)
        #Error update
        elif(header[4] == "300"):
            print(add)
        #Error delete
        elif(header[4] == "350"):
            print(add)
        #Error list
        elif(header[4] == "400"):
            print(add)
lista_arg=[]
for arg in sys.argv:
    lista_arg.append(arg)
   
dir_socket="/tmp/db.tuples.sock"
if lista_arg[0] == "-s":
    dir_socket = lista_arg[1]

hostname=socket.gethostname()
HOST = socket.gethostbyname(hostname)
PORT = 55001

sock = None

conectado=False
cmd=""
id_msj = 100
while True:
    cmd=input(">>>")
    comand = cmd.replace("("," ").replace(")","").replace(","," ")
    #Deja el comando en una lista
    list_cmd = comand.split(" ")
    #Genera un codigo para el mensaje
    code = Code("XJS654ZK",6)
    if(list_cmd[0] == "connect"):
        # Se crea el socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #Se conecta el socket
        server_address = (HOST, PORT)
        print ('Conectandose a {} puerto {}'.format(HOST,PORT))
        sock.connect(server_address)
        conectado = True;
        print("Conectado con exito al servidor")
    elif(conectado == True):
        if(list_cmd[0] == "insert"):
            #insert(value)
            if(len(list_cmd) == 2):
                msj = "{}/{}/0/{}/100/text/plain\ninsert/1/0/1/\n/{}/".format(id_msj,HOST,code,list_cmd[1])
                sock.send(msj.encode())
                resp = sock.recv(4096)
                InterpreteRespose(resp.decode())
                id_msj += 1
            #insert(key,value)
            elif(len(list_cmd) == 3):
                msj = "{}/{}/0/{}/100/text/plain\ninsert/1/1/1/\n{}/{}/".format(id_msj,HOST,code,list_cmd[1],list_cmd[2])
                sock.send(msj.encode())
                resp = sock.recv(4096)
                InterpreteRespose(resp.decode())
                id_msj += 1
            else:
                print("Formato del comando incorrecto!")
        elif(list_cmd[0] == "get"):
            if(len(list_cmd) == 2):
                msj = "{}/{}/0/{}/100/text/plain\nget/1/1/0/\n{}/".format(id_msj,HOST,code,list_cmd[1])
                sock.send(msj.encode())
                resp = sock.recv(4096)
                InterpreteRespose(resp.decode())
                id_msj += 1
            else:
                print("Formato del comando incorrecto!")
    
        elif(list_cmd[0] == "peek"):
            if(len(list_cmd) == 2):
                msj = "{}/{}/0/{}/100/text/plain\npeek/1/1/0/\n{}/".format(id_msj,HOST,code,list_cmd[1])
                sock.send(msj.encode())
                resp = sock.recv(4096)
                InterpreteRespose(resp.decode())
                id_msj += 1
            else:
                print("Formato del comando incorrecto!")
        elif(list_cmd[0] == "update"):
            if(len(list_cmd) == 3):
                msj = "{}/{}/0/{}/100/text/plain\nupdate/1/1/1/\n{}/{}/".format(id_msj,HOST,code,list_cmd[1],list_cmd[2])
                sock.send(msj.encode())
                resp = sock.recv(4096)
                InterpreteRespose(resp.decode())
                id_msj += 1
            else:
                print("Formato del comando incorrecto!")
        elif(list_cmd[0] == "delete"):
            if(len(list_cmd) == 2):
                msj = "{}/{}/0/{}/100/text/plain\ndelete/1/1/0/\n{}/".format(id_msj,HOST,code,list_cmd[1])
                sock.send(msj.encode())
                resp = sock.recv(4096)
                InterpreteRespose(resp.decode())
                id_msj += 1
            else:
                print("Formato del comando incorrecto!")
        elif(list_cmd[0] == "list"):
            if(len(list_cmd) == 1):
                msj = "{}/{}/0/{}/100/text/plain\nlist/0/0/0/\n".format(id_msj,HOST,code)
                sock.send(msj.encode())
                resp = sock.recv(4096)
                InterpreteRespose(resp.decode())
                id_msj += 1
            else:
                print("Formato del comando incorrecto!")
        elif(list_cmd[0] == "disconnect"):
            sock.close()
            conectado=False
            
        elif list_cmd[0]=="quit":
            sock.close()
            break
        else:
            print("Conexion no establecida o comando incorrecto")
    elif list_cmd[0]=="quit":
            break
    
    else:
        print("Conexion no establecida o comando incorrecto")