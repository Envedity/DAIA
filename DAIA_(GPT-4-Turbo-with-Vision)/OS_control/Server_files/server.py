import socket


HOST = "0.0.0.0"  # Client IP address
PORT = 1234  # Port number

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(1)

# Accept a connection from a client
client_socket, client_address = server_socket.accept()

# Receive instructions from the client
instructions = client_socket.recv(1024).decode()

# Example: Process instructions and perform actions
feedback = ""
if instructions == "do_action":
    print("Do action (test)")
# ... add more instructions and corresponding feedback as needed

# Take a screen_shot and save it as feedback
feedback = "screen-shot*"

# Send feedback back to the client
client_socket.sendall(feedback.encode())

# Close the connection
client_socket.close()
server_socket.close()
