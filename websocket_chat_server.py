#!/usr/bin/env python

import asyncio
import websockets
from urllib.parse import parse_qs
import os


HOST = '0.0.0.0'
PORT = 35770

connected = set()


async def handler(websocket, path):
    # Register.
    connected.add(websocket)
    try:
        while True:
            msg = await websocket.recv()
            await asyncio.wait([ws.send(msg) for ws in connected])
            print(msg)
    finally:
        # Unregister.
        connected.remove(websocket)

        

start_server = websockets.serve(handler, HOST, PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

