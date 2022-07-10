import socket
import tqdm
import os

separator = "<SEPARATOR>"
BUFFER_SIZE = 4096 #send 4096 bytes each time step

#the ip address or hostname of the server, the reciever
host = "35.177.44.174"
#the port
port = 5001
# the name of file
filename = input("File Path> ")
#get the file size
filesize = os.path.getsize(filename)


#create the client socket
s = socket.socket()

#connecting to the server
print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

#send the filename and filesize
s.send(f"{filename}{separator}{filesize}".encode())

#start sending the file
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B")
with open(filename, "rb") as f:
    while True:
        #read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            #file transmitting is done
            break
        #we use sendall to assure transmitting if __name__ == '__main__':
        #busy networks
        s.sendall(bytes_read)
        #update the progress bar
        progress.update(len(bytes_read))

#close the socket
s.close()
