import argparse
import logging

import discord

logging.basicConfig()
logger = logging.getLogger()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    pass

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    logger.debug('Got message "%s"', message.content)
    if message.content == 'owls':
        await message.channel.send('hello world!')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('discord_token')
    parser.add_argument('--debug', action="store_true")
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
    client.run(args.discord_token)

if __name__ == '__main__':
    main()


