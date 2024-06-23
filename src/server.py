import asyncio
import os
from aiohttp import ClientSession
from typing import AnyStr
from UTILITY import read_token
from Client import Client
from multiprocessing import Process

token = read_token()





async def start(channel_id: int, message_id: int,
                file: AnyStr, action: int, loop: bool, mode: int = 0, interval: float = 1.0) -> None:

    loop = loop

    action = action

    session = ClientSession()
    client = Client(token, session, channel_id, message_id)

    file_path = os.path.abspath(file)

    with (open(file_path, encoding='utf-8') as file):
        params = file.readline()
        width, height, fps = params.split(' ')

        first_frame = True
        line = "l"

        delay = 1 / int(fps)

        if mode != 0:
            delay = float(interval)

        while True:
            print(loop)

            render = []

            if first_frame is True:
                frame = int(file.readline())
                first_frame = False

            while True:
                if (line is None or line == '') and loop is True:
                    print("\nWOWOWOWOW\n")
                    file.seek(0)
                    file.readline()
                    frame = int(file.readline())
                elif (line is None or line == '') and loop is False:
                    exit()

                line = file.readline()
                print(line)

                try:
                    frame = int(line)
                    break
                except Exception:
                    pass

                render.append(line)

            render = ''.join(render)

            if action == 0:
                action = 1
                client = Client(token, session, channel_id, await client.sendWithID(render))
            elif action == 1:
                await client.edit(render)
            else:
                await client.send(render)

            await asyncio.sleep(delay)


def run(channel_id: int, message_id: int, file: AnyStr, action: int, loop: bool, mode: int = 0, interval: float = 1.0) -> None:
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(start(channel_id, message_id, file, action, loop, mode, interval))

def run_background(channel_id: int, message_id: int, file: AnyStr, action: int, loop: bool, mode: int = 0, interval: float = 1.0) -> None:
    process = Process(target=run, args=(channel_id, message_id, file, action, loop, mode, interval))
    Process.daemon = False
    process.start()
