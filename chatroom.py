import socket
import threading
import select
import sys
# --------------------- TCP Chatroom Implementation ---------------------

class ServerTCP:
    def __init__(self, server_port):
        self.is_shutting_down = False  # This flag tracks if the server is shutting down
        self.server_port = server_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((socket.gethostbyname(socket.gethostname()), self.server_port))
        self.server_socket.listen()
        self.server_socket.settimeout(1.0)  # Set timeout to periodically check for server shutdown
        self.clients = {}  # Dictionary to hold client sockets and their usernames
        self.run_event = threading.Event()
        self.handle_event = threading.Event()  # New event to control message handling
        self.run_event.set()
        self.handle_event.set()  # Initially set to handle messages

    def accept_client(self):
        try:
            # Use select to check if there's a connection available
            ready, _, _ = select.select([self.server_socket], [], [], 1.0)  # 1s timeout
            if ready:
                client_socket, client_addr = self.server_socket.accept()
                name = client_socket.recv(1024).decode()  # Get client name
                if name in self.clients.values():
                    client_socket.send("Name already taken".encode())
                    client_socket.close()  # Close socket if name taken
                    return False
                client_socket.send("Welcome".encode())
                self.clients[client_socket] = name
                self.broadcast(client_socket, 'join')
                return True
        except socket.timeout:
            return False

    def close_client(self, client_socket):
        # Close the connection for a client but don't broadcast if the server is shutting down
        if client_socket in self.clients:
            name = self.clients[client_socket]
            del self.clients[client_socket]
            if not self.is_shutting_down:  # Only broadcast if the server is not shutting down
                self.broadcast_message(f'User {name} left')
            client_socket.close()
            return True
        return False

    def broadcast(self, client_socket_sent, message):
        # Broadcast a message from one client to all other clients
        name = self.clients.get(client_socket_sent, "Unknown")
        if message == 'join':
            broadcast_message = f'User {name} joined'
        elif message == 'exit':
            broadcast_message = f'User {name} left'
        else:
            broadcast_message = f'{name}: {message}'  # Normal chat messages are prefixed with the client's name
        
        if message in ['join', 'exit']:
            print(broadcast_message)  # Print join/leave messages on the server console
        
        # Send the broadcast message to all other clients, except the sender
        for client_socket in list(self.clients):
            if client_socket != client_socket_sent:
                try:
                    client_socket.send(broadcast_message.encode())
                except:
                    self.close_client(client_socket)  # Close the connection if sending the message fails

    def broadcast_message(self, message):
        # Utility method to send a message from the server to all clients
        print(message)
        for client_socket in list(self.clients):
            try:
                client_socket.send(message.encode())
            except:
                self.close_client(client_socket)

    def shutdown(self):
        # Signal that the server is shutting down
        self.is_shutting_down = True
        self.handle_event.clear()  # Stop handling messages
        print("Shutting down the server...")

        # Notify all clients about the shutdown
        for client_socket in list(self.clients):
            try:
                client_socket.send("server-shutdown".encode())
            except:
                pass
            self.close_client(client_socket)  # Close each client without broadcasting "User left"

        self.run_event.clear()  # Signal that the server is no longer running
        self.server_socket.close()

    def handle_client(self, client_socket):
        try:
            while self.run_event.is_set() and self.handle_event.is_set():
                ready, _, _ = select.select([client_socket], [], [], 1.0)  # Check if client has sent data
                if ready:
                    message = client_socket.recv(1024).decode()
                    if message == "exit":
                        self.close_client(client_socket)
                        break
                    self.broadcast(client_socket, message)
        except (ConnectionResetError, BrokenPipeError, socket.timeout):
            self.close_client(client_socket)

    def get_clients_number(self):
        # Return the number of currently connected clients
        return len(self.clients)

    def run(self):
        print(f"TCP CHATROOM\nThis is the server side.\nI am ready to receive connections on port {self.server_port}")
        print("Press Ctrl+C to shut down the server\nWaiting for clients to connect...")
        # Main server loop to accept clients and start new threads to handle them
        try:
            while self.run_event.is_set():
                if self.handle_event.is_set():  # Only accept clients if handle_event is set
                    client_connected = self.accept_client()  # Try to accept a new client
                    if client_connected:
                        client_socket = list(self.clients.keys())[-1]  # Get the most recent client
                        threading.Thread(target=self.handle_client, args=(client_socket,)).start()
        except KeyboardInterrupt:
            self.shutdown()  # Shut down the server if Ctrl+C is pressed


class ClientTCP:
    def __init__(self, client_name, server_port):
        # Initialize the client, set the server address, and prepare the socket for connection
        self.server_addr = socket.gethostbyname(socket.gethostname())
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_port = server_port
        self.client_name = client_name
        self.exit_run = threading.Event()  # Event to signal when to stop the client
        self.exit_receive = threading.Event()  # Event to signal when to stop receiving messages

    def connect_server(self):
        # Connect the client to the server and send the username
        try:
            self.client_socket.connect((self.server_addr, self.server_port))
            self.client_socket.send(self.client_name.encode())  # Send the client's name to the server
            response = self.client_socket.recv(1024).decode()
            if response == "Welcome":
                return True
            else:
                print(response)
                return False
        except:
            print("Connection failed.")
            return False

    def send(self, text):
        # Send a message to the server
        try:
            self.client_socket.send(text.encode())
        except (BrokenPipeError, ConnectionResetError):
            self.exit_run.set()  # If the connection breaks, stop the client

    def receive(self):
        # Continuously receive messages from the server
        while not self.exit_receive.is_set():
            try:
                message = self.client_socket.recv(1024).decode()  # Receive the message
                if message == "server-shutdown":
                    print("\rServer is shutting down...")  # Print the shutdown message without reprinting the prompt
                    self.exit_run.set()
                    self.exit_receive.set()
                    break
                else:
                    print(f"\r{message}")  # Print the received message
                    if not self.exit_run.is_set():  # Only reprint the prompt if the client is still running
                        sys.stdout.write(f'{self.client_name}: ')
                        sys.stdout.flush()
            except (ConnectionResetError, BrokenPipeError):
                self.exit_run.set()
                self.exit_receive.set()
                break

    def run(self):
        print(f"TCP CHATROOM\nThis is the client side.\nWelcome")
        print(f"You are now connected to the chatroom")
        print('Type "exit" to leave the chatroom')
        # Main client loop for sending and receiving messages
        if self.connect_server():
            receiver_thread = threading.Thread(target=self.receive)
            receiver_thread.start()  # Start the thread to receive messages
            while not self.exit_run.is_set():
                sys.stdout.write(f'{self.client_name}: ')  # Show prompt with the client's name
                sys.stdout.flush()
                text = input()
                if text == "exit":
                    self.send("exit")
                    self.exit_receive.set()
                    self.exit_run.set()
                else:
                    self.send(text)
            receiver_thread.join()
        self.client_socket.close()

# --------------------- UDP Chatroom Implementation ---------------------

class ServerUDP:
    def __init__(self, server_port):
        self.server_port = server_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = socket.gethostbyname(socket.gethostname())
        self.server_socket.bind((self.addr, self.server_port))
        self.clients = {}  # Dictionary to store client addresses and names
        self.messages = []  # List to store messages to be broadcasted


    def accept_client(self, client_addr, message):
        try:
            name = message.split(":")[0]
            if name not in self.clients.values():
                self.clients[client_addr] = name
                self.server_socket.sendto("Welcome".encode(), client_addr)
                self.messages.append(f"User {name} joined'")
                self.broadcast()
                return True
            self.server_socket.sendto("Name already taken".encode(), client_addr)
        except Exception as e:
            print(f"Error at ServerUDP accept_client: {e}")
        return False

    def close_client(self, client_addr):
        try:
            name = self.clients.pop(client_addr)
            self.messages.append((client_addr, f"User {name} left"))
            self.broadcast()
            return True
        except Exception as e:
            print(f"Error at ServerUDP close_client: {e}")
        return False

    def broadcast(self):
        try:
            recent_msg = self.messages[-1]
            name = self.clients[recent_msg[0]]
            msg = recent_msg[1]
            for client_iter in self.clients.keys():
                if recent_msg[0] != client_iter:
                    self.server_socket.sendto(msg.encode(), client_iter)
        except Exception as e:
            print(f"Error at ServerUDP broadcast: {e}")

    def shutdown(self):
        try:
            all_clients = list(self.clients.keys())
            for client_iter in all_clients:
                self.server_socket.sendto("server-shutdown".encode(), client_iter)
                self.clients.pop(client_iter)
            self.server_socket.close()

        except Exception as e:
            print(f"Error at ServerUDP shutdown: {e}")

    def get_clients_number(self):
        return len(self.clients)

    def run(self):
        print(f"UDP Chatroom\nThis is the server side\nI am ready to receive connections on port {self.server_port}\nPress Ctrl+C to shut down the server\nWaiting for clients to connect...")
        while True:
            try:
                if select.select([self.server_socket],[],[],1)[0]:
                    message, client_addr = self.server_socket.recvfrom(1024)
                    message = message.decode()

                    if "join" in message.split(":")[1].strip():
                        self.accept_client(client_addr, message)
                    if "exit" in message.split(":")[1].strip():
                        self.close_client(client_addr)
                    else:
                        self.messages.append((client_addr, message))
                        self.broadcast()

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error at ServerUDP run: {e}")
                break
        self.shutdown()

class ClientUDP:
    def __init__(self, client_name, server_port):
        # Instance variables
        self.server_addr = (socket.gethostbyname(socket.gethostname()), server_port)  # Localhost address with the specified port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket
        self.client_socket.settimeout(5.0)  # 5-second timeout for recvfrom to prevent infinite blocking
        self.server_port = server_port
        self.client_name = client_name
        self.exit_run = threading.Event()  # Controls the main loop
        self.exit_receive = threading.Event()  # Controls the receiving loop

    def connect_server(self):
        # Attempts to connect to the server by sending a 'join' message
        try:
            self.send("join")
            response, _ = self.client_socket.recvfrom(1024)
            if response.decode() == "Welcome":
                return True
            else:
                print("Failed to connect to the server.")
                return False
        except socket.timeout:
            print("Connection attempt timed out.")
            return False
        except Exception as e:
            print(f"Error at ClientUDP connect_server: {e}")
            return False

    def send(self, text):
        # Sends a message to the server with the format '{client_name}:{text}'
        message = f"{self.client_name}:{text}"
        try:
            self.client_socket.sendto(message.encode(), self.server_addr)
        except Exception as e:
            print(f"Error at ClientUDP send: {e}")

    def receive(self):
        # Listens for messages from the server until 'exit_receive' is set
        try:
            while not self.exit_receive.is_set():
                try:
                    data, _ = self.client_socket.recvfrom(1024)
                    message = data.decode()
                    if message == "server-shutdown":
                        print("Server is shutting down.")
                        self.exit_run.set()
                        self.exit_receive.set()
                        break
                    print(message)
                except socket.timeout:
                    # Continue listening if timeout occurs, check the exit_receive flag
                    continue
        except Exception as e:
            if not self.exit_receive.is_set():
                print(f"Error at ClientUDP receive: {e}")

    def run(self):
        print(f'UDP Chatroom\nThis is the client side\nWelcome\nYou are now connected to the chatroom\nType "exit" to leave the chatroom')
        # The main loop for the client, handles connecting, sending, and receiving
        if not self.connect_server():
            return

        # Start the receive thread
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        # Main loop for sending messages
        try:
            while not self.exit_run.is_set():
                text = input()
                if text.lower() == "exit":
                    self.send("exit")
                    self.exit_run.set()
                    self.exit_receive.set()
                    break
                self.send(text)
        except KeyboardInterrupt:
            # Gracefully handle a manual interruption
            self.send("exit")
            self.exit_run.set()
            self.exit_receive.set()

        # Wait for the receiving thread to finish
        receive_thread.join()

        # Close the socket
        self.client_socket.close()
