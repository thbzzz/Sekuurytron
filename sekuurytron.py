#!/usr/bin/env python3

import asyncio
from os import getenv

import discord
from discord.ext import commands
from dotenv import load_dotenv

from logger import log
from utils import msg

PREFIX = ">"
DESCRIPTION = "Sekuurytron Discord bot"


sekuurytron = commands.Bot(
    command_prefix=PREFIX,
    description=DESCRIPTION
)


# Events

@sekuurytron.event
async def on_ready():
    log.info(f"Logged in as {sekuurytron.user}")

    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="you"
    )
    status = discord.Status.online

    await sekuurytron.change_presence(activity=activity, status=status)


@sekuurytron.event
async def on_message(message):
    # Ignore the message if it's from the bot himself
    if message.author == sekuurytron.user:
        return

    # Handle commands
    await sekuurytron.process_commands(message)


# Commands

@sekuurytron.command()
async def poweroff(ctx):
    log.info(f"Poweroff requested by {ctx.message.author}")

    message = msg("sleeping", "Bye")

    await ctx.send(message)
    await sekuurytron.logout()


@sekuurytron.command()
async def hello(ctx):
    message = msg("nerd", "Yes, master?")

    await ctx.send(message)


if __name__ == "__main__":
    load_dotenv(".env")
    sekuurytron.run(getenv("TOKEN"))
