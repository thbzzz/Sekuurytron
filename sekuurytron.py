#!/usr/bin/env python3
#coding: utf-8

import discord
from discord.ext import commands

from requests import get
from requests.exceptions import ConnectionError
from json import loads
from urllib.parse import quote_plus
from binascii import hexlify, unhexlify, Error
from base64 import b64encode, b64decode
from re import search as re_search
from random import choice, randint
from string import ascii_lowercase
from random import choice
from datetime import datetime


TOKEN = "" # add yours
PREFIX = '>'
DESCRIPTION = "Sekuurytrön Discord bot"

client = commands.Bot(command_prefix=PREFIX, description=DESCRIPTION)


# EVENTS
@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name=randomGameStatus()))
    print("[+] Login successful")
    print("[+] Username:", client.user.name)
    print("[+] ID:", client.user.id)
    print("[+] Command prefix:", PREFIX)
    print("====================")

@client.event
async def on_command_error(error, ctx):
    channel = ctx.message.channel
    author  = ctx.message.author
    exception_name = type(error).__name__

    # catch errors
    if isinstance(error, commands.errors.MissingRequiredArgument):
        logException(author, exception_name)
        await client.send_message(channel, ":cry: `missing argument(s)`")
        return
    elif isinstance(error, commands.errors.CommandNotFound):
        logException(author, exception_name)
        await client.send_message(channel, ":grimacing: `command not found`")
        return
    elif isinstance(error, commands.errors.CommandInvokeError):
        logException(author, exception_name)
        await client.send_message(channel, ":thermometer_face: `internal error`")
        return

    # other errors
    else:
        logUncaughtException(author, exception_name)
        return

@client.event
async def on_message(message):
    channel = message.channel
    author = message.author
    content = message.content

    # bonus
    if author == "Hash-ill#2969":
        if not content:
            return
        elif content[-1] == '?':
            link = "http://lmgtfy.com/?q=" + quote_plus(content)
            await client.send_message(channel, ":thinking: {}".format(link))

    # commands handling
    await client.process_commands(message)


# BASIC COMMANDS
@client.command()
async def hey():
    """ Just to remember it is your slave. """
    msg = ":nerd: `yes, master?`"
    await client.say(msg)

@client.command(pass_context=True)
async def off(ctx):
    """ Puts the bot in a coma. """
    authorized_users = [
        'thbz#4563'
    ]

    # check if the user can shutdown the bot
    author = ctx.message.author
    if not author in authorized_users:
        await client.say(":kissing_heart: `you cannot do that`")
        return

    await client.logout()

@client.command(pass_context=True)
async def clear(ctx, amount=1):
    """ Clears the last <amount> messages (can be dangerous). Default is 1.
    Note:
        <amount> must be between 1 and 1000 included
    """
    # check the amount
    if amount < 2 or amount > 99:
        await client.say(":angry: `the amount must be between 1 and 99`")
        return

    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount)+1):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say(":wastebasket: `{} cleared the last {} messages`".format(ctx.message.author, amount))


# CONVERT
@client.command()
async def convert(conversion, data):
    """ Performs basic conversions, may help. """
    available_conversions = [
    'frombin',
    'tobin',
    'fromhex',
    'tohex',
    'frombase64',
    'tobase64'
    ]

    # help message if wrong conversion
    if conversion not in available_conversions:
        error_msg = ":angry: `available conversions: {}`".format(' | '.join(available_conversions))
        await client.say(error_msg)
        return

    # binary -> string
    if conversion == 'frombin':
        try:
            converted = ''.join(chr(int(data[i:i+8], 2)) for i in range(0, len(data), 8))
        except ValueError:
            await client.say(":angry: `invalid binary data`")
            return

    # string -> binary
    elif conversion == 'tobin':
        converted = ""
        for x in data:
            byt = str(bin(ord(x)))[2:]
            l = len(byt)
            if l < 8:
                byt = '0'*(8 - l) + byt
            converted += byt

    # hex -> string
    elif conversion == 'fromhex':
        try:
            converted = str(unhexlify(data))[2:-1]
        except Error: # binascii.Error
            await client.say(":angry: `invalid hexadecimal data`")
            return

    # string -> hex
    elif conversion == 'tohex':
        converted = str(hexlify(data.encode('utf_8')))[2:-1]

    # base64 -> string
    elif conversion == 'frombase64':
        try:
            converted = str(b64decode(data))[2:-1]
        except Error:
            await client.say(":angry: `invalid base64 data`")
            return

    # string -> base64
    elif conversion == 'tobase64':
        converted = str(b64encode(data.encode('utf-8')))[2:-1]

    await client.say(":gear: `{}`".format(converted))


# PLAY
@client.command()
async def play(game):
    """ The biggest decisions are taken here. """
    available_games = [
        'coinflip',
        'dice',
    ]

    # help message if wrong game
    if game not in available_games:
        await client.say(":angry: `available games: {}`".format(' | '.join(available_games)))
        return

    if game == 'coinflip':
        if randint(0, 1) == 0:
            emoji, side = ":arrow_heading_up:", "TAILS"
        else:
            emoji, side = ":arrow_heading_down:", "HEADS"
        await client.say("{} `{}!`".format(emoji, side))

    elif game == 'dice':
        nb = randint(0, 6)
        await client.say(":game_die: `{}`".format(nb))


# SURVEY
@client.command()
async def survey(question, *responses):
    """ This is what democracy looks like. """
    # check responses : minimum 2 maximum 10 + all different
    if len(responses) < 2:
        await client.say(":angry: `you must provide at least 2 possible responses`")
        return
    elif len(responses) > 10:
        await client.say(":angry: `you must provide a maximum of 10 responses`")
        return
    for response in responses:
        if responses.count(response) > 1:
            await client.say(":angry: `all responses must be different`")
            return

    # making it beautiful
    embed = discord.Embed(
        title = "React to answer",
        description = "",
        colour = discord.Colour.default()
    )

    embed.set_author(name="{}".format(question)) # author is used as title, prettier
    embed.set_thumbnail(url="https://cloud.0xthbz.fr/index.php/s/rFMC7kpqgdyNB2m/preview")

    # 1 field per response
    for response in responses:
        letter = ascii_lowercase[responses.index(response)]
        embed.add_field(name=":regional_indicator_{}: `{}`".format(letter, response), value="`Response {}`".format(letter.upper()), inline=True)

    await client.say(embed=embed)


# CTF
@client.command(pass_context=True)
async def ctf(ctx, ctftime_url, login=None, password=None):
    """ Proper way to represent a CTF event, using CTFTime API.
    Note:
        2 kinds of URLs can be used:
        - https://ctftime.org/event/{event_id}
        - https://ctftime.org/api/v1/events/{event_id}/
    """
    # is the data a simple event link or an api link?
    regex_evt = r'^https://ctftime\.org/event/\d{1,4}/?$'
    regex_api = r'^https://ctftime\.org/api/v1/events/\d{1,4}/$'

    if re_search(regex_evt, ctftime_url):
        # conversion from event link to api link
        event_id = ctftime_url.rstrip('/').split('/')[-1]
        ctftime_url = "https://ctftime.org/api/v1/events/{}/".format(event_id)
    elif re_search(regex_api, ctftime_url):
        # api link is ok
        pass
    else:
        # url is invalid
        await client.say(":angry: `invalid url`")
        return

    # check credentials
    if (not login and password) or (login and not password):
        await client.say(":angry: `you must enter both login and password`")
        return

    # get data from ctftime.org api
    headers = {"User-Agent": "Sekuurytrön"} # doesn't work with default (python-requests/x.x.x)
    try:
        data = get(ctftime_url, headers=headers).text
    except ConnectionError:
        # the id is certainly wrong -> 404 error
        await client.say(":x: `connection error, check your event id`")
        return

    # parse this data
    json = loads(data)
    title = json['title']
    id = json['id']
    start = json['start']
    finish = json['finish']
    duration = json['duration']
    url = json['url']
    format = json['format']
    logo = json['logo']
    # adjustments
    if logo == "": logo = "https://cloud.0xthbz.fr/index.php/s/tz7WZLgozp4rgzi/preview"
    if login == None: login = "[login]"
    if password == None: password = "[password]"

    # making it beautiful
    embed = discord.Embed(
        title = url,
        description = format
    )

    embed.set_author(name="{} | #{}".format(title, id)) # author is used as title, prettier
    embed.set_thumbnail(url=logo)

    # date stuff
    date_start, hour_start = start.split('T')
    hour_start = "{} +{}".format(':'.join(hour_start.split(':')[:2]), hour_start.split('+')[1][:2])
    date_finish, hour_finish = finish.split('T')
    hour_finish = "{} +{}".format(':'.join(hour_finish.split(':')[:2]), hour_finish.split('+')[1][:2])
    days, hours = duration['days'], duration['hours']
    embed.add_field(name=":date: `{}`".format(date_start), value=":alarm_clock: `{}`".format(hour_start))
    embed.add_field(name=":date: `{}`".format(date_finish), value=":alarm_clock: `{}`".format(hour_finish))
    embed.add_field(name=":timer: `{} days {} hours`".format(days, hours), value="___")
    embed.add_field(name="`{}`".format(login), value="`{}`".format(password))

    await client.say(embed=embed)

    # pin the message
    channel = ctx.message.channel
    async for msg in client.logs_from(channel, limit=1):
        await client.pin_message(msg)


# RANDOM TEAMS
@client.command()
async def random_teams(nb):*
    """ To choose is to renounce """
    nicknames = [
        '0xShiroKuma',
        'Amalrik',
        'Bookie',
        'Guigui',
        'Hash-ill',
        'Mudcam',
        'Nerodale',
        'Sicarius',
        'switch',
        'thbz'
    ]

    # prevent errors
    if not nb.isdigit():
        await client.say(":angry: `{} isn't a number`".format(nb))
        return
    nb = int(nb)
    if nb > len(nicknames):
        await client.say(":angry: `number of teams is greater than number of players ({} players)`".format(len(nicknames)))
        return

    # create teams
    team_basename = "Hackatsuki"
    teams = {}
    for i in range(1, nb+1):
        team = "{} {}".format(team_basename, i)
        teams[team] = []

    # add a player, then remove it from the list
    while nicknames:
        for i in range(nb):
            if nicknames:
                current_team = list(teams.keys())[i]
                random_player = choice(nicknames)
                teams[current_team].append(random_player)
                nicknames.remove(random_player)
            else:
                pass

    # displayed message
    msg = ""
    for team in teams:
        msg += "`{}`\n".format(team)
        msg += "```\n"
        msg += "{}".format(' '.join(teams[team]))
        msg += "```\n"

    await client.say(msg)


# EGG
@client.command(pass_context=True, aliases=['eg'])
async def egg(ctx, nickname):
    """ egg """
    channel = ctx.message.channel
    async for message in client.logs_from(channel, limit=100):
        if message.author.display_name == nickname:
            await client.add_reaction(message, "🥚")
            return


# MISC
def logException(author, exception):
    """ Proper way to log exceptions """
    now = date()
    now.pop('year')
    now = now.values()
    log = "[x] {}/{} at {}:{}:{} {} raised a {} exception".format(*now, author, exception)
    print(log)

def logUncaughtException(author, exception_name):
    """ Proper way to spot uncaught exceptions """
    now = date(); now.pop('year'); now = now.values()
    log = "[x] {}/{} at {}:{}:{}: Uncaught exception\n".format(*now)
    log += "  [>] Author: {}\n".format(author)
    log += "  [>] Exception: {}\n".format(exception_name)
    print(log)

def randomGameStatus():
    """ Not enough random yet """
    games = [
        "Jumanji",
        "Fallout New Vegas",
        "Pokemon Fire Red",
        "Adibou",
        "Ecco the Dolphin",
        "Steganography (== guessing)",
        "Forensics (== greping)",
        "Half-Life 3",
        "Call of Duty: Black Ops XVIII",
        "Minecraft",
        "Root Me",
        "Hackthebox",
        "Newbie Contest",
        "Overthewire",
        "Age of Mythology",
        "Age of Empire III",
        "Far Cry 3",
        "IS",
        "Demonstrating Fermat's Last Theorem",
        "Farming Simulator",
        "H4CK1NG",
        "Wii Sports"
    ]
    return choice(games)

def date():
    """ So it's done """
    now = datetime.now()
    year, month, day = now.year, '%02d'%now.month, '%02d'%now.day
    hour, minute, second = '%02d'%now.hour, '%02d'%now.minute, '%02d'%now.second
    dic = {
        'year': year,
        'month': month,
        'day': day,
        'hour': hour,
        'minute': minute,
        'second': second
    }
    return dic

### EXECUTION ###
client.run(TOKEN)
