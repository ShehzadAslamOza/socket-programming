import socket
from tqdm import tqdm

# For colored outputs
class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    
# Constants 
IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
SOCKET = (IP, PORT)
PACKET_SIZE = 1024
FORMAT = "utf-8"
 
def main():
    
    # Starting the Server
    server = startServer()
  
    # Listening for connections
    print(f"{bcolors.OKGREEN}[+] Listening... at {SOCKET}")
    server.listen()
    
    # When client is trying to connect
    conn, addr = server.accept()
  
    # Read the filename and the filesize the client wants to send
    FILENAME, FILESIZE = readFileNameSize(conn,addr)

    # Receiving file from the client and writing it on the server
    if writeFile(conn,FILENAME,FILESIZE):
        print(f"{bcolors.OKGREEN}[+] File {FILENAME} Successfully received!\n")
    else:
        print(f"{bcolors.FAIL}[-] Error: Client Disconnected!\n")
       
    # Closing the connection
    conn.close()
   
    
# Starting the Server
def startServer():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(SOCKET)
    return server
    
# Getting the Filename and Filesize from the Client
def readFileNameSize(conn,socket):
    print(f"{bcolors.OKGREEN}[+] Client connected from {socket[0]}:{socket[1]}")
    packet = conn.recv(PACKET_SIZE).decode(FORMAT)
    splited_packet = packet.split("_")
    FILENAME = splited_packet[0]
    FILESIZE = int(splited_packet[1])
 
    print(f"[+] Filename and Filesize received from the Client.")
    conn.send("Filename and Filesize received".encode(FORMAT))

    return FILENAME, FILESIZE

# Getting data from the client and writing it on the server
def writeFile(conn,FILENAME,FILESIZE):
    
    # For loading animation
    bar = tqdm(range(FILESIZE), f"{bcolors.WARNING}[+] Receiving {FILENAME}", unit="B", unit_scale=True, unit_divisor=PACKET_SIZE)

    # Total packets to be received
    pieceCount = FILESIZE / PACKET_SIZE
    
    try:
        with open(f"recv_{FILENAME}", "wb") as file:
            while True:
                packet = conn.recv(PACKET_SIZE)

                # All packets are received
                if not packet:
                    break

                # Write the received packet
                file.write(packet)
                conn.send("Packet received.".encode(FORMAT))

                bar.update(len(packet))
                pieceCount -=1
    finally:
        # if the connection is stopped before all packets are sent return false
        return (pieceCount < 1)
    
if __name__ == "__main__":
    while True:
        main()