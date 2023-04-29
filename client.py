import os
import socket,sys
from tqdm import tqdm
from tkinter.filedialog import askopenfilename

# For colored outputs
class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'


# Constants 
IP = socket.gethostbyname(socket.gethostname())         # The IP SOCKETess
PORT = 4456                                             # The PORT Number
SOCKET = (IP, PORT)                                     # The SOCKET
PACKET_SIZE = 1024                                      # PACKET SIZE    
FORMAT = "utf-8"                                        # FORMAT
FULLFILENAME = str(askopenfilename())                   # Complete Absolute Path
FILENAME = FULLFILENAME.split("/")[-1]  

if not FULLFILENAME:
        print(f"{bcolors.FAIL}[-] File not Selected! Please Select a FILE!")
        sys.exit(0)
        
FILESIZE = os.path.getsize(FULLFILENAME)                # File Size
 
def main():

    

    # Establishing Connection with the Server
    client = establishConnection()
   
    # Sending the Filename and the Size
    data = sendFileNameSize(client)
   
    # Sending the File
    if not sendFile(client, data):
        print(f"{bcolors.FAIL}[-] Connection Interrupted! An existing connection was forcibly closed by the remote host")
    else:
        print(f"{bcolors.OKGREEN}[+] File Successfully Sent!")
        
    # Closing the connection
    client.close()
 
 
# Function to Establish Connection between HOST and CLIENT  
def establishConnection():
    print(f"{bcolors.WARNING}[+] Establishing Connection")
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(SOCKET)
    except:
        print(f"{bcolors.FAIL}[-] Server Offline")
        sys.exit()

    print(f"{bcolors.OKGREEN}[+] Connection Established")
    
    return client


# Function to Send File Name and Size to the server to begin sending the file
def sendFileNameSize(client):
    try:
        data = f"{FILENAME}_{FILESIZE}"
        client.send(data.encode(FORMAT))
        msg = client.recv(PACKET_SIZE).decode(FORMAT)
        print(f"[+] SERVER: {msg}")
    except:
        print(f"{bcolors.FAIL}[-] Connection Interrupted!")   
    
    return data


# Function to send the file
def sendFile(client,data):
    bar = tqdm(range(FILESIZE), f"{bcolors.WARNING}[+] Sending {FILENAME}", unit="B", unit_scale=True, unit_divisor=PACKET_SIZE)
 
    try:
        with open(FULLFILENAME, "rb") as file:
            while True:
                packet = file.read(PACKET_SIZE)
    
                # All packets are sent
                if not packet:
                    break
    
                client.send(packet)
                client.recv(PACKET_SIZE).decode(FORMAT)
    
                bar.update(len(packet))
    
        return True
    except:
       return False   
    
if __name__ == "__main__":
    main()