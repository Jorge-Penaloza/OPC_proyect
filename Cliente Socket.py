import socket
import json
import time
import queue
import signal
import threading
# Configuración del cliente
host = '127.0.0.1'
port = 12345
debe_continuar = True

# Crear un socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def conectar_servidor():
    global client_socket
    global debe_continuar
    while debe_continuar:
        try:
            client_socket.connect((host, port))
            print("Conexión establecida con el servidor.")
            break
        except socket.error:
            
            client_socket.close()
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Error al conectar con el servidor. Reintentando en 5 segundos...")
            time.sleep(5)

# Conectar al servidor
#client_socket.connect((host, port))

def clienteSocket(q):
    global debe_continuar
    global client_socket
    while debe_continuar:
        #if not verificar_conexion():
        #    conectar_servidor()
        #    print("Error de conexion a Servidor Socket")
        #    continue
        try:
            i = 0
            while debe_continuar:
                #message = input("Ingrese un mensaje: ")
                message = "r"
            
                client_socket.send(message.encode())
                response = client_socket.recv(1024).decode()
                #print("Respuesta del servidor:", response)

                try:
                    #json_data = json.loads(json.loads(response))
                    json_data = json.loads(response)
                    #pretty_json = json.dumps(json_data, indent=5)
                    print("Datos recibidos:")
                    print( json_data)
                    #print( pretty_json)
                except json.JSONDecodeError:
                    print("Error al decodificar la respuesta como JSON. Respuesta recibida:", response)
                i = i + 1
                print(i)
        
        except socket.error:
            print("Error en la comunicación con el servidor. Intentando reconectar...")
            conectar_servidor()
            
            #time.sleep(0.1)
            



    # Cerrar la conexión
    client_socket.close()

def signal_handler(signum, frame):
    global debe_continuar
    print("Señal de interrupción recibida. Deteniendo hilos...")
    debe_continuar = False

def escuchar_tecla():
    global debe_continuar
    while debe_continuar:
        entrada = input("Presiona 'q' para salir: ")
        if entrada == 'q':
            debe_continuar = False
            print("Cerrando por modo normal")

if __name__ == "__main__":
    # Crear una cola
    cola = queue.Queue()
    #cola = {}
    # Configurar el manejador de señales
    signal.signal(signal.SIGINT, signal_handler)

    hilo_tecla = threading.Thread(target=escuchar_tecla)
    #cliente_OPC = threading.Thread(target=clienteOPC, args=(cola,) )
    cliente_Socket = threading.Thread(target=clienteSocket, args=(cola,))

    hilo_tecla.start()
    #cliente_OPC.start()
    cliente_Socket.start()

    hilo_tecla.join()
    #cliente_OPC.join()
    cliente_Socket.join()

    # Agregar señales de finalización a la cola para que el consumidor se detenga
    #cola.put(None)
    #cola.put(None)

    print("Cierre de programa")