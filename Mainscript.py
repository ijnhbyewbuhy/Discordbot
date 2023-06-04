import discord
import random
import asyncio

bot_token = 'YOUR_BOT_TOKEN'
target_channel_id = 'TARGET_CHANNEL_ID'

# Create a Discord client
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
client = discord.Client(intents=intents)

# Generate a random math problem
def generate_math_problem():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    operator = random.choice(['+', '-', '*', '/'])
    problem = f"What is {a} {operator} {b}?"
    return problem, eval(f"{a}{operator}{b}")

# Send the math problem to the specified channel
async def send_math_problem(channel):
    problem, answer = generate_math_problem()
    await channel.send("Math problem sent to chat:")
    await channel.send(problem)

    # Wait for 20 seconds for an answer
    await asyncio.sleep(20)

    # Check for answers
    async for message in channel.history(limit=10):
        if message.author.bot:
            continue
        content = message.content.strip()
        if content.startswith("&answer"):
            user_answer = content.split(" ", 1)[1]
            if user_answer.isdigit() and int(user_answer) == answer:
                await channel.send("The answer is:")
                await channel.send(str(answer))
            else:
                await channel.send("Sorry, that's incorrect.")

# Event triggered when the bot is ready
@client.event
async def on_ready():
    print('Bot is ready.')

    # Find the target channel
    target_channel = client.get_channel(target_channel_id)

    if target_channel:
        await send_math_problem(target_channel)
    else:
        print(f"Target channel ({target_channel_id}) not found.")

# Run the bot
client.run(bot_token)
