import random
import threading
import zmq
import time

class Client:
    def __init__(self, clientID):
        self.clientID = clientID
        self.ctx = zmq.Context()
        self.subscriber = self.ctx.socket(zmq.SUB)
        self.publisher = self.ctx.socket(zmq.PUSH)
        self.subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
        self.subscriber.connect("tcp://localhost:5556")
        self.publisher.connect("tcp://localhost:5557")
        self.stop_event = threading.Event()
        self.message_count = 0

    def listen_for_message(self):
        while not self.stop_event.is_set():
            try:
                if self.subscriber.poll(0) & zmq.POLLIN:
                    time.sleep(0.08)
                    message = self.subscriber.recv_string()
                    sender_clientID, received_message = message.split(" : ", 1)
                    if self.clientID != sender_clientID:
                        self.message_count += 1
                        print("{0}: received message => {1}".format(self.clientID, message))
            except zmq.error.ZMQError as e:
                print(f"Error receiving message: {e}")


    def send_message(self, message):
        msg = f"{self.clientID} : {message}"
        print("{0}: send message {1}".format(self.clientID, message))
        self.publisher.send_string(msg)

    def stop(self):
        self.stop_event.set()


if __name__ == '__main__':
    allClients_threads = []
    sender_threads = []

    allClients = [Client(f"c-{i}") for i in range(1, 500)]


    for client in allClients:

        client_thread = threading.Thread(target=client.listen_for_message, daemon=True)
        allClients_threads.append(client_thread)
        client_thread.start()

    senders = random.sample(allClients, 20)

    for sender in senders[0:]:
        sender_thread = threading.Thread(target=sender.send_message, args=("Hello",), daemon=True)
        sender_threads.append(sender_thread)
        sender_thread.start()


    start_time = time.perf_counter()

    time.sleep(1)

    for client in allClients:
        client.stop()

    for thread in allClients_threads:
        thread.join()

    for thread in sender_threads:
        thread.join()

    end_time = time.perf_counter()

    for client in allClients:
        print(f"{client.clientID} : {client.message_count}")

    senders[0].send_message("EXIT")

    print(f"Total elapsed time: {end_time - start_time} seconds")

