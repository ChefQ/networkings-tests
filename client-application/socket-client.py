import asyncio
import websockets

async def connect_to_cloud():
    # Replace this with YOUR actual Render URL. 
    # Notice we change "https://" to "wss://"
    uri = "wss://my-python-websocket-test.onrender.com"
    
    print(f"Attempting to connect to {uri}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected successfully!")
            
            # Send a message to the cloud
            message_to_send = "Hello from my laptop!"
            print(f"Sending: {message_to_send}")
            await websocket.send(message_to_send)
            
            # Wait for the response
            response = await websocket.recv()
            print(f"Received: {response}")
            
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    asyncio.run(connect_to_cloud())