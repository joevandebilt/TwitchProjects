# websocket_server.py
import asyncio
import websockets
import os

# A simple WebSocket server that echoes received messages back to the client
async def echo(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(message)

# Start WebSocket server on localhost:8765
async def start_server():
    server = await websockets.serve(echo, "localhost", 8765)
    await server.wait_closed()

# Write the process id (pid) to a file so the second script can find and kill it
if __name__ == "__main__":
    pid = os.getpid()
    with open("server_pid.txt", "w") as f:
        f.write(str(pid))
    print(f"WebSocket server started. PID: {pid}")
    
    try:
        asyncio.get_event_loop().run_until_complete(start_server())
    except KeyboardInterrupt:
        print("Server shutting down...")