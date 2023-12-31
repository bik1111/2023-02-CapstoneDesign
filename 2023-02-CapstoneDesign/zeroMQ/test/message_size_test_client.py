import zmq
import time
import os
import threading

class Client:
    def __init__(self, clientID):
        self.clientID = clientID
        self.ctx = zmq.Context()
        self.subscriber = self.ctx.socket(zmq.SUB)
        self.publisher = self.ctx.socket(zmq.PUSH)
        self.subscriber.setsockopt(zmq.SUBSCRIBE, b"")
        #self.subscriber.connect("tcp://#ip:5556")
        #self.publisher.connect("tcp://#ip:5557")
        self.message_count = 0
        self.stop_event = threading.Event()

    def listen_for_message(self):
        while not self.stop_event.is_set():
            if self.subscriber.poll(10) & zmq.POLLIN:
                msg = self.subscriber.recv()
                time.sleep(0.05)
                self.message_count += 1
                print(f"Receiver {self.clientID}: Received message {msg}")


    def send_message(self, message_size):
        for _ in range(10):
            message = os.urandom(message_size)
            self.publisher.send(message)
            #print(f"Sender: Sent message {message}")

    def stop(self):
        self.stop_event.set()


if __name__ == '__main__':
    results = []
    # 4, 16, 64, 256, 512 (Bytes)
    message_size = 512

    receiver_instance = [Client(i) for i in range(1,301)]
    sender_instance = Client("sender")

    receiver_threads = [threading.Thread(target=receiver.listen_for_message, daemon=True) for receiver in receiver_instance]
    for receiver_thread in receiver_threads:
        receiver_thread.start()

    sender_thread = threading.Thread(target=sender_instance.send_message, daemon=True, args=(message_size,))

    sender_thread.start()

    start_time = time.perf_counter()

    time.sleep(0.64)

    for receiver in receiver_instance:
         receiver.stop()

    for receiver_thread in receiver_threads:
        receiver_thread.join()

    sender_thread.join()

    sender_instance.publisher.send(b"END")

    end_time = time.perf_counter()

    duration = end_time - start_time
    total_received_messages = sum(receiver.message_count for receiver in receiver_instance)
    throughput = total_received_messages / duration

    for receiver in receiver_instance:
        print("receiver message count:", receiver.message_count)

    print("Total Received Messages:", total_received_messages)
    print("Duration:", duration, "seconds")
    print("Throughput (messages/second):", throughput)