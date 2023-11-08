import aiosqlite
from discord.ext import commands
import os
import json
import re
import asyncio
import numpy as np
from PIL import Image
from io import BytesIO
from tensorflow.keras.models import load_model
import aiohttp
import discord
from collections import deque

TOKEN = "MTA3MzY0MjM1OTI4MTE3MjU1MA.Gmcz8u.kufTWnMDMAQJeu5f5izEuIafuomx8iuGJWh3xE"
server_id = 1169676280640315544
poketwo = 716390085896962058
bot_prefix = "."
bot = commands.Bot(command_prefix=bot_prefix, self_bot=True)
loaded_model = load_model('model.h5', compile=False)
with open('classes.json', 'r') as f:
    classes = json.load(f)

response_queue = deque()

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.offline)
    print('We have logged in as {0.user}'.format(bot))

async def process_responses():
    while True:
        if response_queue:
            response = response_queue.popleft()
            try:
                await response()
            except Exception as e:
                print(f"Error processing response: {e}")
        await asyncio.sleep(0.5)

@bot.event
async def on_message(message):
    if message.guild.id == server_id:
        if len(message.embeds) > 0:
            embed = message.embeds[0]
            if "appeared!" in embed.title:
                if "human" not in message.content.lower():
                    if embed.image:
                        url = embed.image.url
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url=url) as resp:
                                if resp.status == 200:
                                    content = await resp.read()
                                    image_data = BytesIO(content)
                                    image = Image.open(image_data)
                    preprocessed_image = await preprocess_image(image)
                    predictions = loaded_model.predict(preprocessed_image)
                    classes_x = np.argmax(predictions, axis=1)
                    name = list(classes.keys())[classes_x[0]]

                    async def send_response():
                        async with message.channel.typing():
                            await asyncio.sleep(0.3)

                        await message.channel.send(f'<@{poketwo}> catch {name.lower()}')

                    response_queue.append(send_response)

        else:
            await bot.process_commands(message)

async def preprocess_image(image):
    image = image.resize((64, 64))
    image = np.array(image)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image

async def run_bot():
    while True:
        try:
            await bot.start(TOKEN)
        except Exception as e:
            print(f"Bot encountered an error: {e}")
            await asyncio.sleep(60)  # Retry after a delay

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(process_responses())
    loop.run_until_complete(run_bot())
