import socket


def send_instruction(host_ip, port, instruction):
    HOST = host_ip  # Server IP address
    PORT = port  # Port number

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((HOST, PORT))

    # Send instructions to the server
    client_socket.sendall(instruction.encode())

    # Receive feedback from the server
    feedback = client_socket.recv(1024).decode()

    # Close the socket
    client_socket.close()

    return feedback


feedback = send_instruction("IP address", "port as int", "the first test")
print(feedback)
