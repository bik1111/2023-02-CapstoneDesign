import zmq
import psutil
import os
import time
import sys

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
                msg =  self.collector.recv_string()
                print("server received: ", msg)
                time.sleep(0.01)

                self.publisher.send_string(msg)
                if "EXIT" in msg:
                    break
        except Exception as e:
            print(f"Error receiving message: {e}")

def main():
    print("Server is running...")
    process_id = os.getpid()

    server = Server()

    try:
        start_time = time.perf_counter()
        server.recv_message()

    finally:
        cpu_usage = os.times()[0]

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        memory_usage = psutil.Process(process_id).memory_info().rss
        print(f"Total time: {elapsed_time} seconds")
        print(f"Memory Usage: {memory_usage} bytes")
        print(f"CPU Usage: {cpu_usage} seconds")

if __name__ == '__main__':
    main()
