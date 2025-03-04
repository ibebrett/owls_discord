import argparse
import logging
import os
import random

import discord

logging.basicConfig()
logger = logging.getLogger()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


facts_path = os.path.join(os.path.dirname(__file__), "scsu_facts.txt")
with open(facts_path, "r") as f:
    facts = f.readlines()
fact_triggers = ["scsu", "southern", "cs club", "icpc"]


@client.event
async def on_ready():
    pass


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    logger.debug('Got message "%s"', message.content)

    if message.content == "owls":
        await message.channel.send("hello world!")

    if message.content == "flip coin":
        resp = "heads" if random.random() > 0.5 else "tails"
        await message.channel.send(resp)

    for fact_trigger in fact_triggers:
        if fact_trigger in message.content.lower():
            resp = f"You said `{fact_trigger}` so I'll tell you a random scsu fact: "
            resp += random.choice(facts)
            await message.channel.send(resp)
            break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("discord_token")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
    client.run(args.discord_token)


if __name__ == "__main__":
    main()
