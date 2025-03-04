from typing import Optional

import argparse
import logging
import os
import random

import aiohttp
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


def get_fact_trigger(message: str) -> Optional[str]:
    for fact_trigger in fact_triggers:
        if fact_trigger in message.lower():
            return fact_trigger

    return None


def get_random_fact():
    return random.choice(facts)


@client.event
async def on_ready():
    pass


weather_token = os.environ.get("WEATHER_TOKEN")


async def get_weather() -> str:
    url = f"http://api.weatherapi.com/v1/current.json?key={weather_token}&q=New Haven&aqi=no"
    # timeout is 30s by default
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try:
                json_response = await response.json()

                condition = json_response["current"]["condition"]["text"]
                temp_f = json_response["current"]["temp_f"]
                return f"It's currently {temp_f} degrees farenheight and {condition} at SCSU"
            except Exception as ex:
                logger.exception("Failure when getting weather", ex)
                return "something bad happened when getting the weather!"


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    logger.debug('Got message "%s"', message.content)

    if message.content == "owls":
        await message.channel.send("hello world!")
        return

    if message.content == "flip coin":
        resp = "heads" if random.random() > 0.5 else "tails"
        await message.channel.send(resp)
        return

    fact_trigger = get_fact_trigger(message.content)
    if fact_trigger is not None:
        resp = f"You said {fact_trigger} so I'll tell you a random scsu fact: "
        resp += get_random_fact()
        await message.channel.send(resp)
        return

    if "weather" in message.content.lower():
        weather = await get_weather()
        await message.channel.send(weather)
        return


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
