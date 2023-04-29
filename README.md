# Socket Programming Assignment

**Objective:**

The objective of this assignment is to implement a socket programming solution that can transfer files between two hosts

**Instructions:**

- You can use C++, Java, or Python for this assignment.

- You are allowed to use any library or framework for socket programming in your chosen
  programming language.
- Your solution should consist of two programs: a client program and a server program.
- The client program should be able to connect to the server program over a network and
  send a file to the server.
- The server program should be able to receive the file sent by the client and save it on its
  local filesystem.
- Your solution should be able to handle large files.
- Your solution should implement error checking and handling to ensure that files are
  transferred correctly.
- Your solution should handle the case when the server is offline or cannot be reached.
- Your code should be well-documented, with clear and concise comments explaining the
  purpose and function of each section of code.

---

### Open the terminal and first install the Requirements

```
pip3 install -r .\requirements.txt
```

### Open the terminal then Run the Server

```
python .\server.py
```

The server would be listening for clients to establish connection

### Open another terminal in parallel then run the client

```
python .\client.py
```

Select the desired file to send and Done!

[Took help from here](https://idiotdeveloper.com/large-file-transfer-using-tcp-socket-in-python/)
