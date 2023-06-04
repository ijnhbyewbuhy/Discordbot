import nextcord
import random
import asyncio

bot_token = 'YOUR_BOT_TOKEN'
target_guild_id = TARGET_GUILD_ID
target_channel_id = TARGET_CHANNEL_ID
answer_prefix = '!'

intents = nextcord.Intents.default()
intents.message_content = True

client = nextcord.Client(intents=intents)

@client.event
async def on_ready():
    print('Bot is ready.')
    target_guild = nextcord.utils.get(client.guilds, id=target_guild_id)
    if target_guild is None:
        print('Target guild not found.')
        return
    target_channel = nextcord.utils.get(target_guild.channels, id=target_channel_id)
    if target_channel is None:
        print('Target channel not found.')
        return
    print(f'Target channel found: {target_channel.name}')
    math_problem = generate_math_problem()
    await target_channel.send(f"Math problem: {math_problem}\nTo answer, use the prefix '{answer_prefix}' followed by your answer.")
    print("Math problem sent to chat.")
    await asyncio.sleep(30)  # Wait for 30 seconds
    await check_answers(target_channel, math_problem)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(answer_prefix):
        answer = message.content[len(answer_prefix):].strip()
        username = message.author.name
        await message.channel.send(f"{username} answered: {answer}")
        print(f"Answer received: {username} - {answer}")
        await asyncio.sleep(2)  # Wait for 2 seconds to avoid rate limiting
        await check_answers(message.channel, answer)

def generate_math_problem():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(['+', '-', '*', '/'])
    return f"{num1} {operator} {num2}"

async def check_answers(channel, problem):
    correct_answers = []
    async for message in channel.history(limit=100):
        if message.content.startswith(answer_prefix) and message.content[len(answer_prefix):].strip() == problem:
            correct_answers.append(message.author.name)
    if correct_answers:
        await channel.send(f"The correct answer was: {problem}\nCorrect answers from: {', '.join(correct_answers)}")

client.run(bot_token)
