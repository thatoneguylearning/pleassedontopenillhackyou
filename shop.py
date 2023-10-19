

  
@bot.command()
async def buy_incense(ctx):
    # Send "buy incense" on all channel IDs
    for channel_id in channel_ids:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send('<@716390085896962058> buy incense')
            await asyncio.sleep(2)  # Add a delay between messages if needed
    await ctx.send("i bought incense in all channels.")
 
async def process_responses():
    while True:
        if response_queue:
            response = response_queue.popleft()
            await response()
        await asyncio.sleep(1)  # Adjust the delay between responses if needed


