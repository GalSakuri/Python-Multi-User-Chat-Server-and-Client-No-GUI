Gal Sakuri, ID: 207970344
Tamir Yakuti, ID: 208154864

How to Run the Chat Application:
Process Overview - 

Server:
- Listens(waits) on its socket for new clients connections. (Only locally in this code, could change to '0.0.0.0',... etc)
- Accepts each client(up to 5 in this scenario), read their username, then waits for incoming messages.
- Broadcasting public messages to all clients, or forwards private messages if your messages starts with '@{username}'.

Client:
- Connects to the server and sends its username.
- Runs a background thread to continuously receive and display new messages.
- Accepts user input in the main thread and sends those messages to the server.
- Close the connection when the user types the quit command ('LEAVE') or if the server disconnects. 

#Added pictures of this application running on my machine to the moodle.
