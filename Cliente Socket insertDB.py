import socket
import json
import time
import queue
import signal
import threading
import pyodbc
from datetime import datetime

# Configuración del cliente
host = '127.0.0.1'
port = 12345
debe_continuar = True

# Crear un socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configuración de la conexión
server_name = "opc-pruebas0001-server.database.windows.net"
database_name = "opc-pruebas0001"
username = ""
password = ""

# Cadena de conexión
connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER=tcp:{server_name},1433;"
    f"DATABASE={database_name};"
    f"UID={username};"
    f"PWD={password};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)


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
                    #print("Datos recibidos:")
                    #print( json_data)
                    #print(type(response))
                    if isinstance(json_data, dict) and "servidores" in json_data:
                        for servidor in json_data["servidores"]:
                            print("URL del servidor:", servidor.get("url", "N/A"))
                            
                            # Verifica si hay un error en el servidor
                            if "error" in servidor:
                                print("Error en el servidor:", servidor["error"])
                            else:
                                # Si no hay error, recorre los tags de cada servidor
                                tags = servidor.get("tags", [])
                                tupla = {}  
                                for tag in tags:
                                    for key, value in tag.items():
                                        print(f"Tag: {key}, Valor: {value}")
                                        tupla.update({key:value})
                                if servidor.get("url", "N/A") == "opc.tcp://192.168.0.20:49320":
                                    fecha_actual = datetime.now()
                                    conn = pyodbc.connect(connection_string)
                                    cursor = conn.cursor()
                                    cursor.execute(
                                        "INSERT INTO [dbo].[excel] ([Fecha], [temperatura], [humedad], [motor]) "
                                        "VALUES (?, ?, ?, ?)",
                                        fecha_actual,
                                        tupla["Temperatura"],
                                        tupla["Humedad"],
                                        tupla["Motor"],
                                    )
                                    conn.commit()
                                    cursor.close()   
                                    conn.close()
                                    print("Ingesta")
                                    time.sleep(5)

                    else:
                        print("El JSON recibido no contiene la estructura esperada.")
                    
                except json.JSONDecodeError:
                    print("Error al decodificar la respuesta como JSON. Respuesta recibida:", response)
                time.sleep(10)
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
