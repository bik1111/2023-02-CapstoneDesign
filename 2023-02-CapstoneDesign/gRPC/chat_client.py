import asyncio
import random
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

    async def _listen_for_messages(self):
        async for note in self.conn.ChatStream(chat.Empty()):
            if note.name != self.username:
                self.message_count += 1
                print("[{}]->[{}] {}".format(note.name,
                      self.username, note.message))

    async def send_message(self, message: str):
        n = chat.Note()
        n.name = self.username
        n.message = message
        print("Sent [{}], {}".format(n.name, n.message))
        self.conn.SendNote(n)

    async def send_exit_message(self, message: str):
        print("Sending exit message...")
        exit_message = chat.ExitMessage()
        exit_message.exit_reason = message
        try:
            print("Sent [{}]".format(exit_message.exit_reason))
            await self.conn.SendExitMessage(exit_message)
        except grpc.aio.AioRpcError as e:
            print(f"An error occurred: {e}")
        finally:
            await self.channel.close()
            print("Exit message sent.")


async def main():

    #server_address = "#ip:11912"
    allClients = [Client(f"sender-{i}", server_address) for i in range(1, 500)]
    random_clients = random.sample(allClients, 20)

    send_tasks = []

    for client in random_clients:
        send_tasks.append(asyncio.create_task(client.send_message("Hello")))

    start_time = time.perf_counter()

    await asyncio.gather(*send_tasks)

    #await asyncio.sleep(1)

    receive_tasks = [asyncio.create_task(client._listen_for_messages()) for client in allClients]

    await asyncio.gather(*receive_tasks)

    end_time = time.perf_counter()

    for client in allClients:
        print(f"{client.username} received {client.message_count} messages")

    print(f"Total time: {end_time - start_time:0.4f} seconds")

    try:
        await random_clients[0].send_exit_message("EXIT")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
