import asyncio
import grpc
import time
import os
import chat_pb2 as chat
import chat_pb2_grpc as rpc
import cProfile

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
        with cProfile.Profile() as pr:
            await server.start()        # cProfile을 사용하여 코드 실행 측정
            # 기다리기 위해 무한 루프 추가
            while True:
                await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("Shutting down server...")
        await server.stop(0)

    finally:
        await server.wait_for_termination()
        user_time, kernel_time, _, _, _ = os.times()
        print(f"User Mode CPU Usage: {user_time} seconds")
        print(f"Kernel Mode CPU Usage: {kernel_time} seconds")
        pr.print_stats(sort='cumulative')  # 누적된 시간을 기준으로 정렬

if __name__ == '__main__':
    asyncio.run(main())

