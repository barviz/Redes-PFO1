import socket
import datetime
import threading
from bdd import init_bdd, guardar_mensaje

def initialize_socket():
    """
    se inicializa y configura el socket del servidor
    """
    try:
        # se crea socket TCP/IP
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # se configurar opción para reutilizar dirección
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # se enlaza socket a localhost:5000
        server_address = ('localhost', 5000)
        server_socket.bind(server_address)
        
        # se escucha conexiones entrantes (máximo 5 en cola)
        server_socket.listen(5)
        
        print("servidor iniciado en {}:{}".format(*server_address))
        return server_socket
        
    except socket.error as e:
        print(f"error al inicializar el socket: {e}")
        return None

def handle_cliente(cliente_socket, cliente_address):
    """
    se maneja la comunicación con un cliente conectado
    """
    try:
        print(f"conexión establecida con {cliente_address}")
        
        while True:
            # recibe mensaje del cliente
            mensaje = cliente_socket.recv(1024).decode('utf-8')
            
            if not mensaje or mensaje.lower() == 'éxito':
                print(f"el cliente {cliente_address} se desconectó")
                break
            
            # timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # se guarda mensaje en base de datos
            try:
                guardar_mensaje(mensaje, timestamp, cliente_address[0])
                print(f"mensaje guardado: {mensaje}")
            except Exception as e:
                print(f"error al guardar en base de datos: {e}")
            
            # se envía confirmación al cliente
            response = f"mensaje recibido: {timestamp}"
            cliente_socket.send(response.encode('utf-8'))
            
    except Exception as e:
        print(f"error en comunicación con cliente {cliente_address}: {e}")
    finally:
        cliente_socket.close()

def main():
    """
    función principal del servidor
    """
    # se inicializa base de datos
    try:
        init_bdd()
    except Exception as e:
        print(f"error al inicializar base de datos: {e}")
        return
    
    # se nicializa socket
    servidor_socket = initialize_socket()
    if not servidor_socket:
        return
    
    try:
        while True:
            print("esperando conexiones...")
            
            # se acepta nueva conexión
            cliente_socket, cliente_address = servidor_socket.accept()
            
            # se crea hilo para manejar cliente
            cliente_thread = threading.Thread(
                target=handle_cliente, 
                args=(cliente_socket, cliente_address)
            )
            cliente_thread.daemon = True
            cliente_thread.start()
            
    except KeyboardInterrupt:
        print("\nservidor detenido por el usuario")
    except Exception as e:
        print(f"error en servidor: {e}")
    finally:
        servidor_socket.close()

if __name__ == "__main__":
    main()