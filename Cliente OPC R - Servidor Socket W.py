import time
import opcua
import threading
import socket
import queue
import json
from DBconsultasOPC import clienteDBOPC
import signal
import select
import asyncio

def vaciar_cola(q):
    while not q.empty():
        try:
            q.get_nowait()  # Desencola un elemento
        except queue.Empty:
            break

def conectarOPC(conexion):
    client = opcua.Client(conexion)
    client.session_timeout = 30000  #30000
    sw = False
    try:
        if client.connect() is None:
            sw = True
    except:
        print("Ha ocurrido un error de conexion a ", conexion)
        print("")
        sw = False
    time.sleep(0.01)
    if sw:
        return client
    else:
        try:
            client.close_session()
        except:
            print("Error de cierre de sesión")
        return None
    
def lectura(idServidor, opc_db, timeout):
    servidor_info = opc_db.get_server_by_id(idServidor)
    data_matrix = opc_db.get_data_matrix(idServidor)
    #field_names = opc_db.get_field_names()
    arbol = {}
    cliente = conectarOPC(servidor_info['url'])
    if cliente is None:
        print("Error de conexion en " + servidor_info['url'])
        arbol["url"] = servidor_info['url']
        arbol["error"] = "Error de conexion"
        return arbol
    else:
        arbol["url"] = servidor_info['url']
        arbol["tags"] = []
        print("Conectando a " + servidor_info['url'])
        nodosAddress = []
        nodosName = []
        for tupla in data_matrix:
            nodosAddress.append(tupla[2])
            nodosName.append(tupla[1])
        for Name, Address in zip(nodosName, nodosAddress):
            try:
                var = cliente.get_node(Address)
                arbol["tags"].append({Name:var.get_value()})
                print(Name," : ",var.get_value())

            except Exception as e:
                arbol["error"] = str(e)
        cliente.close_session()
        if not arbol:
            return None
        else:
            return arbol

def clienteOPC(q, timeout):
    db_host = "127.0.0.1"
    db_user = "root"
    db_password = ""
    db_database = "dbclienteopc"
    #vaciar_cola(q)
    arbol = {}
    arbol["servidores"] = []
    global debe_continuar
    global servidor_Socket
    global cliente_OPC
    global hilo_tecla
    while debe_continuar:
        arbol["servidores"] = []
        vaciar_cola(q)
        opc_db = clienteDBOPC(db_host, db_user, db_password, db_database)
        id_servidor_opc = opc_db.get_servers()
        for id in id_servidor_opc:
            arbolrRetornado = lectura(id['id'], opc_db, timeout)
               # Convertir el diccionario a formato JSON pretty
            #pretty_json = json.dumps(arbolrRetornado, indent=5)

            # Imprimir el JSON en formato pretty
            #print("pretty_json",pretty_json)
            if arbolrRetornado != None:
                arbol["servidores"].append(arbolrRetornado) 
        #print(arbol)
        # Convertir el diccionario a formato JSON pretty
        print("arbol ",type(arbol))
        pretty_json = json.dumps(arbol)
        print("pretty_json ", type(pretty_json))
        # Imprimir el JSON en formato pretty
        q.put( arbol)
        print("arbol TOTAL")
        print(arbol)
        time.sleep(0.1)
    else:
        print("No entra  a clienteOPC()")


def servidorSocket(q):
    global debe_continuar
    
    # Configuración del servidor
    host = '127.0.0.1'
    port = 12345

    # Crear un socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reutilización de socket


    # Enlazar el socket a la dirección y puerto
    try:
        server_socket.bind((host, port))
        # Escuchar conexiones entrantes
        server_socket.listen(1)
        print("Esperando conexiones...")

        # Aceptar la conexión entrante
        while debe_continuar:
            print("debe_continuar")
            client_socket, client_address = server_socket.accept()
            print("Conexión establecida desde:", client_address)
            ready_to_read, _, _ = select.select([client_socket], [], [], 5)  # Espera hasta 5 segundos
            if not ready_to_read:
                print()
                print("El socket está caído o no hay datos para leer.")
                print()
                break
            i = 0
            while debe_continuar:
                
                data = client_socket.recv(1).decode()
                if not data:

                    print("Dato de cocket no recibido correctamentre", data)
                    break
                else:
                    print("pasando por socket")
                item = q.get()

                try:
                    if data == "r":

                        #envioJASON(client_socket, item)
                        json_data = json.dumps(item)
                        print("json_data", json_data, type(json_data))
                        
                        client_socket.send(json_data.encode())
                        #client_socket.send(item.encode())
                    elif data == "e":
                        datax = {
                                "Error": "El campo de solicitud viene vacio"
                            }
                        #envioJASON(client_socket, datax)
                        json_str = json.dumps(datax)
                        print("Recibido:", datax)
                        client_socket.send(json_str.encode())
                    else:
                        datax = {
                                "Info": "Peticion de seguridad de conexion"
                            }
                        #envioJASON(client_socket, datax)
                        json_str = json.dumps(datax)
                        print("Recibido:", datax)
                        client_socket.send(json_str.encode())
                except ConnectionResetError:
                    print("El cliente cerró la conexión de forma abrupta")
                    break
                
            # Cerrar la conexión
            client_socket.close()
        server_socket.close()
    except Exception as e:
        # Manejar cualquier excepción relacionada con la creación o configuración del servidor socket
        print(f"Error en el servidor socket: {e}")

    finally:
        # Cerrar el socket del servidor al finalizar
        server_socket.close()
        print("Error potencial en bind o listen: Reiniciando servidor ")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        # Escuchar conexiones entrantes
        server_socket.listen(1)
        print("Esperando conexiones...")
def signal_handler(signum, frame):
    global debe_continuar
    print("Señal de interrupción recibida. Deteniendo hilos...")

    #debe_continuar = False

def escuchar_tecla():
    global debe_continuar
    while debe_continuar:
        entrada = input("Presiona 'q' para salir: ")
        if entrada == 'q':
            debe_continuar = False
            print("Cerrando por modo normal")


def main():
    global debe_continuar
    global servidor_Socket
    debe_continuar = True
    # Crear una cola
    cola = queue.Queue()
    #cola = {}
    # Configurar el manejador de señales
    timeout = 0.5
    signal.signal(signal.SIGINT, signal_handler)
    hilo_tecla = threading.Thread(target=escuchar_tecla)
    cliente_OPC = threading.Thread(target=clienteOPC, args=(cola, timeout) )
    servidor_Socket = threading.Thread(target=servidorSocket, args=(cola,))
    

    hilo_tecla.start()
    cliente_OPC.start()
    servidor_Socket.start()
        
    hilo_tecla.join()
    cliente_OPC.join()
    servidor_Socket.join()

    while debe_continuar:
        
        if not hilo_tecla.is_alive():
            print("El hilo de teclado no está activo. La conexión puede haberse perdido.")
            hilo_tecla = threading.Thread(target=servidorSocket, args=(cola,))
            hilo_tecla.start()
            hilo_tecla.join()
        else:
            print("Prueba de hilo serviddor socket")

        if not cliente_OPC.is_alive():
            print("El hilo de cliente OPC no está activo. La conexión puede haberse perdido.")
            cliente_OPC = threading.Thread(target=servidorSocket, args=(cola,timeout))
            cliente_OPC.start()
            cliente_OPC.join()
        else:
            print("Prueba de hilo serviddor socket")

        if not servidor_Socket.is_alive():
            print("El hilo de servidor socket no está activo. La conexión puede haberse perdido.")
            servidor_Socket = threading.Thread(target=servidorSocket, args=(cola,))
            servidor_Socket.start()
            servidor_Socket.join()
        else:
            print("Prueba de hilo serviddor socket")
        
        #time.sleep(3)

    # Agregar señales de finalización a la cola para que el consumidor se detenga
    #cola.put(None)
    #cola.put(None)

    print("Cierre de programa")
    
        
if __name__ == "__main__":
    main()
    