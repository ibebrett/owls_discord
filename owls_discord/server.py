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

pizza_admins = {333064292737875968, 985018113919692820}
already_voted = set()
available_toppings = ['cheese', 'pepperoni', 'sausage', 'meatball', 'bacon', 'chicken', 
                      'shrimp', 'broccoli', 'onion', 'mushroom', 'olive', 'veggie_bomb',
                      'roasted_pepper', 'hot_pepper', 'garlic', 'basil']
topping_votes = dict()

facts_path = os.path.join(os.path.dirname(__file__), "scsu_facts.txt")
with open(facts_path, "r") as f:
    facts = f.readlines()
fact_triggers = ["scsu", "southern", "cs club"]


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
    
    if "icpc" in message.content.lower():
        print(f'{message.author=}')
        print(f'{client.user=}')
        await message.channel.send("ICPC is Tuesdays at 6:00 in Morrill 122!")
        return
    
    if "-pizza_start" in message.content.lower():
        
        print(f'{client.user=}')
        if message.author.id not in pizza_admins:
            await message.channel.send("Unauthorized user.")
            return

        topping_votes = dict()
        already_voted = set()
    
        await message.channel.send("Authorized.")
        return

    if "-pizza_vote" in message.content.lower():

        if message.author.id in already_voted:
            await message.channel.send("You have already voted :(")
            return

        topping = message.content.lower().split()[1]

        if topping not in available_toppings:
            await message.channel.send(f"Topping {topping} is not available.")
            return
        
        if topping not in topping_votes:
            topping_votes[topping] = 0
        topping_votes[topping] += 1
        already_voted.add(message.author.id)

        await message.channel.send(f"Placed your vote for {topping}.")
        return

    if "-show_toppings" in message.content.lower():
        newMessage = []
        for i in available_toppings:
            newMessage.append(i)
        await message.channel.send(", ".join(newMessage))
        return
    
    if "-show_votes" in message.content.lower():
        
        if not topping_votes:
            await message.channel.send("No votes cast yet.")
            return
        
        msg = []
        for k, v in topping_votes.items():
            msg.append(f'{k} : {v} vote(s)')

        await message.channel.send("\n".join(msg))
        return

    if "-help" in message.content.lower():

        await message.channel.send(
"COMMANDS:\n\
-show_toppings: shows all available pizza toppings.\n\
-pizza_vote: vote for a topping using '-pizza_vote {topping name}'.\n\
-show_votes: shows current pizza topping votes.\n"
        )
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
