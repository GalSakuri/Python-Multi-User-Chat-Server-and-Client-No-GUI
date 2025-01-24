import socket 
import threading

clients = [] #pool of all the clients added to the server
client_usernames = {} #pool of all usernames of the clients

def start_server():
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #TCP connection
    host = socket.gethostname() #for local connections.
    port = 9999
    server_socket.bind((host,port)) #connects the socket to the host
    server_socket.listen(5) #waiting for connection requests from up to 5 clients

    print(f"Chat Server Activated on {host}:{port}")

    while True: #always looking for new clients
        client_socket, addr = server_socket.accept() #accepts new client
        clients.append(client_socket) #once it accepted a certain client, it will add his socket to the clients list
        print(f"Made a connection with {addr}")

        thread = threading.Thread(target=client_handler, args =(client_socket,addr)) #connects the newly added client the the thread of the other clients 
        thread.start()
        
def client_handler(client_socket,client_address):
    try:
        username = client_socket.recv(1024).decode('utf-8')        
        if not username:
            remove_connection(client_socket)
            return
        client_usernames[client_socket] = username
        print(f"{client_address} set their username to: {username}")
    except: #couldn't read the message. disconnected/crash/... etc
        print(f"Error reading username from {client_address}")
        remove_connection(client_socket)
        return

    while True:
        try:
            data = client_socket.recv(1024) #receiving the message from a certain client socket
            if not data:
                remove_connection(client_socket)
                break

            message = data.decode('utf-8')

            if message.startswith('@'): #if the message starts with '@', it defines the message as a direct/private one
                tokens = message.split(' ', 1)
                if len(tokens) < 2:
                    client_socket.send("Invalid private message format.\n".encode('utf-8'))
                    continue

                target_name = tokens[0][1:]
                private_msg = tokens[1]
                send_private_message(client_socket,target_name,private_msg) #send the private message to the username that came after the '@'
            else:
                broadcast_text = f"{username}: {message}" #broadcast message to all usernames/clients
                print(f"{broadcast_text}")
                broadcast_message(broadcast_text,client_socket)
        except:
            remove_connection(client_socket)
            break

def broadcast_message(message,sender_socket): 
    for client in clients:
        if client != sender_socket:  #to avoid sending the message back to the sender
            try:
                client.send(message.encode('utf-8'))
            except: #checks for errors, removes clients with errors.
                print(f"Error broadcasting to a client")
                client.close()
                remove_connection(client)

def send_private_message(sender_socket, target_username, private_msg):
    sender_name = client_usernames[sender_socket]
    target_socket = None
    for sock, uname in client_usernames.items(): #checks for username in the usernames pool
        if uname == target_username:
            target_socket = sock
            break
    if target_socket is None:
        error_msg = f"User '{target_username}' does not exist.\n" #incase the username wasn't found
        sender_socket.send(error_msg.encode('utf-8'))
    else:
        message_to_target = f"[private from {sender_name}]: {private_msg}" #send the message directly to the username that stated in the sender's message after the '@'
        try:
            target_socket.send(message_to_target.encode('utf-8'))
        except:
            remove_connection(target_socket)
            sender_socket.send(f"Couldn't send message to {target_username}.\n".encode('utf-8'))

def remove_connection(client_socket):
    if client_socket in clients: #removes the client socket from the clients pool
        clients.remove(client_socket) 
    if client_socket in client_usernames:
        del client_usernames[client_socket]
    client_socket.close()

if __name__ =='__main__':
    start_server()