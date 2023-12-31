import asyncio
import os
import time
import grpc
import chat_pb2 as chat
import chat_pb2_grpc as rpc

class Client:
    def __init__(self, username: str, server_address: str):
        self.username = username
        self.server_address = server_address
        self.channel = None
        self.conn = None
        self.message_count = 0
        self.initialize_channel()

    def initialize_channel(self):
        if not self.channel:
            self.channel = grpc.aio.insecure_channel(self.server_address)
            self.conn = rpc.ChatServerStub(self.channel)


    async def send_message(self, message_size):
        for _ in range(10):
            n = chat.Note()
            n.name = self.username
            n.message = os.urandom(message_size)
            self.conn.SendNote(n)
            await asyncio.sleep(0.05)


    async def _listen_for_messages(self):
        async for note in self.conn.ChatStream(chat.Empty()):
            self.message_count += 1
            print("[{}]->[{}] {}".format(note.name, self.username, note.message))


async def main():
    #server_address = #ip:11912"
    results = []

    # 4, 16, 64, 256, 512 (Bytes)
    message_sizes = 512

    receiver_instance = [Client("receiver", server_address) for _ in range(1,301)]
    sender_instance = Client("sender", server_address)


    start_time = time.perf_counter()
    sender_task = asyncio.create_task(sender_instance.send_message(message_sizes))
    await asyncio.sleep(0.5)
    receive_task = [asyncio.create_task(receiver._listen_for_messages()) for receiver in receiver_instance]

    await asyncio.gather(*receive_task, sender_task)

    end_time = time.perf_counter()



    duration = end_time - start_time
    total_received_messages = sum(receiver.message_count for receiver in receiver_instance)
    throughput = total_received_messages / duration


    for receiver in receiver_instance:
        print("receiver message count: ", receiver.message_count)


    print("Total Received Messages:", total_received_messages)
    print("Duration:", duration, "seconds")
    print("Throughput (messages/second):", throughput)

if __name__ == "__main__":
    asyncio.run(main())
