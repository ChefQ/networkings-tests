import asyncio
import websockets
import os

# This function handles the incoming WebSocket connection
async def echo(websocket):
    print("A client just connected!")
    try:
        async for message in websocket:
            print(f"Received from local laptop: {message}")
            # Echo the message back to the client
            await websocket.send(f"Cloud says: I received '{message}'")
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected.")

async def main():
    # Cloud providers assign a dynamic port, which they expose via the PORT environment variable.
    # If it's not found (like when testing locally), it defaults to 8765.
    port = int(os.environ.get("PORT", 8765))
    
    # 0.0.0.0 binds the server to all available IP addresses, which is required for cloud hosting.
    async with websockets.serve(echo, "0.0.0.0", port):
        print(f"Cloud WebSocket Server running on port {port}...")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())