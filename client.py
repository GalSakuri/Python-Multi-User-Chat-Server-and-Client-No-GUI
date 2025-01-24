import socket 
import threading

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP socket connection
    host = socket.gethostname() #gethostname for local networks connection
    port = 9999
    
    try:
        client_socket.connect((host,port)) #connecting to the server
        print(f"Connected to {host}:{port}")
    except Exception as e:
        print(f"Could not connect to server: {e}")
        return    

    thread = threading.Thread(target=receive_messages, args=(client_socket,)) #connects to a thread to start receiving messages
    thread.start()

    username = input("Enter your username: ") #the client decides his username on the server
    print(f"Your username was set to |{username}|\n")
    client_socket.send(username.encode("utf-8"))

    while True:
        message = input("Type your message here ('LEAVE' to quit): ")
        if message == 'LEAVE': #if the client types LEAVE as his message, he will exit the server
            print("You typed 'LEAVE' therefore the connection is LOST with the server") #print to inform the client 
            client_socket.close()
            break
        if not message:
            print("Empty message, not sent.")
            continue
        client_socket.send(f"{message}".encode('utf-8')) #sends the username + message.

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8') #the clients receives message
            if not message:
                print("Server closed the connection.")
                client_socket.close()
                break

            print("\r" + " " *100, end="\r") #helps the chat of the client look more clean ('reset' any keystrokes and place the line without overlapping other messages)
            print(message)
            print("Type your message here ('LEAVE' to quit): ", end="", flush=True)

        except:
            print("Error! Couldn't receive the message, connection lost")
            client_socket.close()
            break

if __name__ == '__main__':
    start_client()
