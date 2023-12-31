import zmq
import os
import time

class Server:

    def __init__(self):
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind("tcp://*:5556")
        self.collector = self.context.socket(zmq.PULL)
        self.collector.bind("tcp://*:5557")

    def recv_message(self):
        try:
            while True:
                msg = self.collector.recv()
                print("server received:", msg)
                if msg == b"END":
                    break
                self.publisher.send(msg)

        except Exception as e:
            print(f"Error receiving message: {e}")

def main():
    print("Server is running...")

    server = Server()

    server.recv_message()

    cpu_usage = os.times()[0]
    print(f"CPU Usage: {cpu_usage} seconds")

if __name__ == '__main__':
    main()