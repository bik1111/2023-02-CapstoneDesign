import asyncio
import time
import grpc
import os
import psutil
import chat_pb2 as chat
import chat_pb2_grpc as rpc

class ChatServer(rpc.ChatServerServicer):
    def __init__(self, server):
        self.chats = []
        self.server = server

    async def ChatStream(self, request_iterator, context):
        lastindex = 0
        while len(self.chats) > lastindex:
            n = self.chats[lastindex]
            lastindex += 1
            yield n


    async def SendNote(self, request: chat.Note, context):
        print("[{}] {}".format(request.name, request.message))
        self.chats.append(request)
        return chat.Empty()

    async def SendExitMessage(self, request: chat.ExitMessage, context):
        try:
            print("Received exit message: {}".format(request.exit_reason))
            if self.server:
                await self.server.stop(0)
        except asyncio.CancelledError:
            print("SendExitMessage coroutine was cancelled.")
        except Exception as e:
            print(f"An error occurred in SendExitMessage: {e}")
        except grpc._cython.cygrpc.ExecuteBatchError as e:
            print(f"ExecuteBatchError: {e}")
            print(f"Details: {e.details()}")

async def main():
    port = 11912
    server = grpc.aio.server(maximum_concurrent_rpcs=300)
    chat_server = ChatServer(server)
    rpc.add_ChatServerServicer_to_server(chat_server, server)

    print('Starting server. Listening...')
    server.add_insecure_port('[::]:' + str(port))

    process_id = os.getpid()

    try:
        await server.start()
    except KeyboardInterrupt:
        print("Shutting down server...")
        await server.stop(0)
    finally:
        await server.wait_for_termination()
        cpu_usage = os.times()[1]
        memory_usage = psutil.Process(process_id).memory_info().rss
        print(f"Memory Usage: {memory_usage} bytes")
        print(f"CPU Usage: {cpu_usage} seconds")


if __name__ == '__main__':
    asyncio.run(main())


