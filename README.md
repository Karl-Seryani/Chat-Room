# Chat-Room

A TCP and UDP chatroom implementation using Python's `socket` and `threading` modules.

## Features
- Supports both **TCP** and **UDP** connections.
- Multi-client messaging.
- Server-side client management.
- Graceful shutdown handling.

## Installation
Ensure you have **Python 3** installed. Clone this repository:

## Running the code
- Type python server.py in terminal
- Type python client.py --name yourname
- Start chatting!

## How it works
- The server listens for incoming connections.
- Clients can send and receive messages in real time.
- The server broadcasts messages to all connected clients.
- Clients can exit by typing "exit".
