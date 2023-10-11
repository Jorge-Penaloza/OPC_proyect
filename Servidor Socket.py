import socket

# Configuración del servidor
host = '127.0.0.1'
port = 12345

# Crear un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlazar el socket a la dirección y puerto
server_socket.bind((host, port))

# Escuchar conexiones entrantes
server_socket.listen(1)

print("Esperando conexiones...")

# Aceptar la conexión entrante
client_socket, client_address = server_socket.accept()
print("Conexión establecida desde:", client_address)

while True:
    data = client_socket.recv(1024).decode()
    if not data:
        break
    print("Recibido:", data)
    client_socket.send(data.upper().encode())

# Cerrar la conexión
client_socket.close()
server_socket.close()
