import asyncio
import os
import psutil
from datetime import datetime
from aiohttp import web
import aiohttp

_process = psutil.Process()

MAX_QUEUE = 100
message_queue = []

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    print("WebSocket client connected!")
    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                print(f"WebSocket received: {msg.data}")
                message_queue.append({
                    "source": "websocket",
                    "content": msg.data,
                    "time": datetime.now().isoformat(),
                })
                if len(message_queue) > MAX_QUEUE:
                    message_queue.pop(0)
                await ws.send_str(f"Server received: '{msg.data} your message at {datetime.now().isoformat()}'")
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print(f"WebSocket error: {ws.exception()}")
    finally:
        print("WebSocket client disconnected.")
    return ws

async def poll_handler(_):
    return web.json_response({
        "status": "ok",
        "time": datetime.now().isoformat(),
        "messages": message_queue[-10:],
    })

async def metrics_handler(_):
    mem = _process.memory_info()
    return web.json_response({
        "cpu_percent": _process.cpu_percent(interval=None),
        "ram_mb": round(mem.rss / 1024 / 1024, 2),
        "ram_percent": round(_process.memory_percent(), 2),
        "time": datetime.now().isoformat(),
        "num_messages": len(message_queue),
    })

async def main():
    port = int(os.environ.get("PORT", 8765))
    app = web.Application()
    app.router.add_get("/ws", websocket_handler)
    app.router.add_get("/poll", poll_handler)
    app.router.add_get("/metrics", metrics_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print(f"Server running on port {port}")
    print(f"  WebSocket : ws://localhost:{port}/ws")
    print(f"  HTTP poll : http://localhost:{port}/poll")
    print(f"  Metrics   : http://localhost:{port}/metrics")
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
