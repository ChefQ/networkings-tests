import asyncio
import websockets

async def receive_messages(websocket):
    async for message in websocket:
        print(f"Received: {message}")

async def connect_to_cloud():
    # Replace this with YOUR actual Render URL.
    # Notice we change "https://" to "wss://"
    uri = "wss://my-python-websocket-test.onrender.com"

    print(f"Attempting to connect to {uri}...")
    print("Type your messages and press Enter to send. Type !END! to quit.")

    try:
        async with websockets.connect(uri) as websocket:
            print("Connected successfully!")

            loop = asyncio.get_event_loop()
            receiver = asyncio.create_task(receive_messages(websocket))

            while True:
                message = await loop.run_in_executor(None, input, "> ")
                if message == "!END!":
                    print("Disconnecting...")
                    break
                await websocket.send(message)

            receiver.cancel()

    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    asyncio.run(connect_to_cloud())