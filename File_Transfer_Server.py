import socket
import tqdm
import os

#Client's IP address
Server_Host = "0.0.0.0"
Server_Port = 5001

#recieve 4096 bytes each time
BUFFER_SIZE = 4096
separator = "<SEPARATOR>"

#Create the TCP socket
s = socket.socket()

#bind the socket to our local address
s.bind((Server_Host, Server_Port))

#enable our server to accept connections
#5 here is the number of unaccepted connections that
#the system will allow before refusing new connections
s.listen(5)
print(f"[*] Listening as {Server_Host}:{Server_Port}")

#accept connection if there is any
client_socket, address = s.accept()
#if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")

#recieve the file infos
#recieve using client socket, not server socket
recieved = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = recieved.split(separator)
#remove absolute path if there is
filename = os.path.basename(filename)
#convert to integer
filesize = int(filesize)

# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

# close the client socket
client_socket.close()
# close the server socket
s.close()
