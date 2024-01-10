import asyncio
import websockets
import json
import matplotlib.pyplot as plt

async def data_receiver():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            data = json.loads(await websocket.recv())
            plot_data`(data)
            await asyncio.sleep(1)  # Update frequency (in seconds)

def plot_data(data):
    languages = [row[1] for row in data]
    scores = [row[2] for row in data]
    plt.bar(languages, scores, color='skyblue')
    plt.xlabel('Languages')
    plt.ylabel('Scores')
    plt.title('Programming Language Scores')
    plt.pause(0.1)
    plt.clf()

if __name__ == "__main__":
    plt.ion()  # Turn on interactive mode for live plotting
    asyncio.get_event_loop().run_until_complete(data_receiver())
