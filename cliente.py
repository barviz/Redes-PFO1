import socket

def start_cliente():
    """
    el cliente que se conecta al servidor y envía mensajes
    """
    try:
        # se crea socket TCP/IP
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # se conecta al servidor
        servidor_address = ('localhost', 5000)
        print(f"conectando a {servidor_address[0]}:{servidor_address[1]}...")
        cliente_socket.connect(servidor_address)
        
        print("conexión establecida. escribe 'éxito' para salir")
        
        while True:
            # se lee el mensaje del usuario
            mensaje = input("Tu mensaje: ")
            
            # se envía mensaje al servidor
            cliente_socket.send(mensaje.encode('utf-8'))
            
            if mensaje.lower() == 'éxito':
                print("saliendo...")
                break
            
            # se recibe respuesta del servidor
            response = cliente_socket.recv(1024).decode('utf-8')
            print(f"servidor: {response}")
            
    except ConnectionRefusedError:
        print("error: no se pudo conectar al servidor. verificar que se esté ejecutando")
    except Exception as e:
        print(f"error en cliente: {e}")
    finally:
        cliente_socket.close()

if __name__ == "__main__":
    start_cliente()