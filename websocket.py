import asyncio
import websockets
import pyautogui
import json
import os
import sys
from collections import deque

# Super fast typing speed
typing_speed = 0.001  # Very fast typing (can adjust for speed)
word_space_delay = 0.001  # Small delay after each word

# Create a queue to store words to be typed
word_queue = deque()

async def typing_simulation(websocket, path):
    try:
        # Wait for a message from the JavaScript client
        message = await websocket.recv()

        if message == "ping":
            # Acknowledge the ping message to keep the connection alive
            await websocket.send("pong")
            return

        # If the message is not a ping, it should contain words to type
        data = json.loads(message)
        words = data["words"]

        print(f"Received words: {' '.join(words)}")

        # Add new words to the queue
        word_queue.extend(words)
        print(f"Added to queue: {' '.join(words)}")

        # **Wait for 3 seconds before starting typing**, allowing time to focus on the input field
        print("Waiting for 3 seconds to allow you to focus on the input tab...")
        await asyncio.sleep(3)  # 3-second delay before typing starts

        # Simulate typing all the words at once
        while word_queue:
            word = word_queue.popleft()  # Get the next word from the queue
            print(f"Typing word: {word}")

            # Simulate typing the entire word at once (no delay between letters)
            pyautogui.write(word)  # Type the entire word without a delay between letters
            
            # After each word, simulate typing a space
            pyautogui.write(' ')
            await asyncio.sleep(word_space_delay)  # Short delay after each word (simulate space between words)

        print("Finished typing all words.")

        # After typing is finished, close the CMD/Terminal window
        print("Closing the terminal...")
        if sys.platform == "win32":
            os._exit(0)  # Close the terminal (Windows)
        else:
            sys.exit(0)  # Close the terminal (Linux/Mac)

    except Exception as e:
        print(f"Error: {e}")

# Start the WebSocket server
async def main():
    server = await websockets.serve(typing_simulation, "localhost", 8765)
    print("WebSocket server running on ws://localhost:8765")
    await server.wait_closed()

# Run the server
asyncio.run(main())
