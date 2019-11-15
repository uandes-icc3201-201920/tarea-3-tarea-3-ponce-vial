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

lista_arg=[]
for arg in sys.argv:
    lista_arg.append(arg)
   
dir_socket="/tmp/db.tuples.sock"
if lista_arg[0] == "-s":
    dir_socket = lista_arg[1]

hostname=socket.gethostname()
HOST = socket.gethostbyname(hostname)   # The server's hostname or IP address
PORT = 55001      # The port used by the server

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

conectado=False
cmd=""
while cmd!= "quit":
    cmd=input()
    comand = cmd.replace("("," ").replace(")","").replace(","," ")
    #Deja el comando en una lista
    list_cmd = comand.split(" ")
    #Genera un codigo para el mensaje
    code = Code("dfhajfhajdf",6)
    if(list_cmd[0] == "connect"):
			#Se conecta el socket
        server_address = (HOST, PORT)
        print ('Conectandose a {} puerto {}'.format(HOST,PORT))
        sock.connect(server_address)
        conectado = True;
        print("Conectado con exito al servidor")
    if(conectado == False):
        if(list_cmd[0] == "insert"):
            #insert(value)
            if(len(list_cmd) == 2):
                print("10/{}/0/{}/100\ninsert/1/0/1/\n/{}/".format(HOST,code,list_cmd[1]))
            #insert(key,value)
            elif(len(list_cmd) == 3):
                print("10/{}/0/dhasfe/100\ninsert/1/1/1/\n{}/{}/".format(HOST,code,list_cmd[1],list_cmd[2]))
            else:
                print("Formato del comando incorrecto!")
        elif(list_cmd[0] == "get"):
            if(len(list_cmd) == 2):
                print("10/{}/0/{}/100\nget/1/1/0/\n{}/".format(HOST,code,list_cmd[1]))
            else:
                print("Formato del comando incorrecto!")
    
        elif(list_cmd[0] == "peek"):
            if(len(list_cmd) == 2):
                print("10/{}/0/{}/100\npeek/1/1/0/\n{}/".format(HOST,code,list_cmd[1]))
            else:
                print("Formato del comando incorrecto!")
        elif(list_cmd[0] == "update"):
            if(len(list_cmd) == 3):
                print("10/{}/0/{}/100\nupdate/1/1/1/\n{}/{}/".format(HOST,code,list_cmd[1],list_cmd[2]))
            else:
                print("Formato del comando incorrecto!")
        elif(list_cmd[0] == "delete"):
            if(len(list_cmd) == 2):
                print("10/{}/0/{}/100\ndelete/1/1/0/\n{}/".format(HOST.code,list_cmd[1]))
            else:
                print("Formato del comando incorrecto!")
        elif(list_cmd[0] == "list"):
            if(len(list_cmd) == 1):
                print("10/{}/0/{}/100\nlist/0/0/0/\n".format(HOST,code))
            else:
                print("Formato del comando incorrecto!")
        elif(list_cmd[0] == "disconnect"):
            sock.close()
    else:
        print("Conexion no establecida o comando incorrecto")