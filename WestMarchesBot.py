# -*- coding: utf-8 -*-

# Imports
import json
import discord
import random
import datetime
import asyncio
client = discord.Client()

# Readiness Indicator


@client.event
async def on_ready():
    print("The bot is ready!")
    await client.change_presence(game=discord.Game(name="roulette with your money"))


# Reminder Message
# CURRENTLY NOT WORKING AS INTENDED
# Intended to send the message every Monday


@client.event
async def background_loop():
    await client.wait_until_ready()
    while not client.is_closed:
        if datetime.weekday == 0:
            channel = client.get_channel("397349083318059010")
            message = "Don't forget downtime!"
            await client.send_message(channel, message)
            await asyncio.sleep(604800)


# Main Functionality


@client.event
async def on_message(message):
    with open('banks2.txt') as bankin:
        bank = json.load(bankin)

    # Banking Functions

    if message.content.startswith('/bank'):
        user = str(message.author)
        operation = message.content.split()[1]
        if operation in ['add', 'subtract']:
            metal = message.content.split()[2]
            amount = message.content.split()[3]
        if user in bank.keys():
            if operation == 'add':
                if metal == 'gold':
                    bank[user][metal] += int(amount)
                elif metal == 'silver':
                    bank[user][metal] += int(amount)
                elif metal == 'copper':
                    bank[user][metal] += int(amount)
                await client.send_message(message.channel,
                                          f'You have deposited {amount} {metal}. You now have {bank[user][metal]} '
                                          f'{metal} in your account.')
            elif operation == 'subtract':
                if metal == 'gold':
                    bank[user][metal] -= int(amount)
                elif metal == 'silver':
                    bank[user][metal] -= int(amount)
                elif metal == 'copper':
                    bank[user][metal] -= int(amount)
                await client.send_message(message.channel,
                                          f'You have withdrawn {amount} {metal}. You now have {bank[user][metal]} '
                                          f'{metal} in your account.')
            elif operation == ('balance'):
                await client.send_message(message.channel, f'Your balance is {bank[user]["gold"]} gold, '
                                                           f'{bank[user]["silver"]} silver, and {bank[user]["copper"]}'
                                                           f' copper.')
            elif operation == ('clear'):
                bank[user]["gold"] = 0
                bank[user]["silver"] = 0
                bank[user]["copper"] = 0
                await client.send_message(message.channel, 'You have cleared your balance.')
            elif operation == ('condense'):
                silver, copper = divmod(bank[user]["copper"], 10)
                bank[user]["silver"] += silver
                bank[user]["copper"] = copper
                gold, silver = divmod(bank[user]["silver"], 10)
                bank[user]["gold"] += gold
                bank[user]["silver"] = silver
                await client.send_message(message.channel,
                                          f'Your balance has been condensed to {bank[user]["gold"]} gold, '
                                          f'{bank[user]["silver"]} silver, and {bank[user]["copper"]} copper.')
        else:
            bank.update({user: {'gold': 0, 'silver': 0, 'copper': 0}})
            await client.send_message(message.channel,
                                      'You did not have an account. You now have an account with a balance of 0')
    with open('banks2.txt', 'w') as bankout:
        json.dump(bank, bankout)

    # Dice Rolling Functions

    if message.content.startswith('/roll'):
        if "-" in message.content:
            operator = "-"
        elif "+" in message.content:
            operator = "+"
        else:
            operator = str()
        if "-" in message.content:
            bonus = 0 - int(message.content.split('-')[1])
        elif "+" in message.content:
            bonus = 0 + int(message.content.split('+')[1])
        else:
            bonus = int(0)
        if operator != "":
            sidesEnd = message.content.find(operator)
        elif operator == "":
            sidesEnd = len(message.content)
        numberofDice = message.content[message.content.find('/roll') + 5:message.content.find('d')]
        numberofSides = message.content[message.content.find('d') + 1:sidesEnd]
        rolls = 0
        rawrolls = []
        bonusRolls = []
        dice = 0
        try:
            dice = int(numberofDice)
        except ValueError:
            dice = 1
            pass
 
        while dice > rolls:
            rawrolls.append(random.randint(1, int(numberofSides)))
            rolls += 1
        for r in rawrolls:
            bonusRolls.append(r + bonus)
        await client.send_message(message.channel,
                                  f'You rolled **{rawrolls}**. Your bonus of **[{bonus}]** brings that to **{bonusRolls}'
                                  f'**.')
    elif message.content.startswith('/r'):
        if "-" in message.content:
            operator = "-"
        elif "+" in message.content:
            operator = "+"
        else:
            operator = str()
        if "-" in message.content:
            bonus = 0 - int(message.content.split('-')[1])
        elif "+" in message.content:
            bonus = 0 + int(message.content.split('+')[1])
        else:
            bonus = int(0)
        if operator != "":
            sidesEnd = message.content.find(operator)
        elif operator == "":
            sidesEnd = len(message.content)
        numberofDice = message.content[message.content.find('/r') + 2:message.content.find('d')]
        numberofSides = message.content[message.content.find('d') + 1:sidesEnd]
        rolls = 0
        rawrolls = []
        bonusRolls = []
        dice = 0
        try:
            dice = int(numberofDice)
        except ValueError:
            dice = 1
            pass
        while dice > rolls:
            rawrolls.append(random.randint(1, int(numberofSides)))
            rolls += 1
        for r in rawrolls:
            bonusRolls.append(r + bonus)
        await client.send_message(message.channel,
                                  f'You rolled **{rawrolls}**. Your bonus of **[{bonus}]** brings that to **{bonusRolls}'
                                  f'**.')

    # Help Section

    if message.content.startswith('/help'):
        with open('helps.txt') as file:
            helps = json.load(file)
        for h in helps:
            await client.send_message(message.channel, f'**{h}** - {helps[h]}\n')

    # Command List

    if message.content.startswith('/commands'):
        with open('commands.txt') as file:
            commands = json.load(file)
        for c in commands:
            await client.send_message(message.channel, f'**{c}** - {commands[c]}\n')

    # Communal Banking

    if message.content.startswith('/communal'):
        with open ('communalbank.txt') as communalIn:
            communal  = json.load(communalIn)
            operation = message.content.split()[1]
            if operation in ['add', 'subtract']:
                metal = message.content.split()[2]
                amount = message.content.split()[3]
                if operation == 'add':
                    if metal == 'gold':
                        communal[metal] += int(amount)
                    elif metal == 'silver':
                        communal[metal] += int(amount)
                    elif metal == 'copper':
                        communal[metal] += int(amount)
                    await client.send_message(message.channel, f'You have deposited {amount} {metal} in the communal account')
            elif operation == ('balance'):
                await client.send_message(message.channel, f'The Communal Balance is {communal["gold"]} gold, {communal["silver"]} silver, and {communal["copper"]} copper')
            elif operation == ('condense'):
                silver, copper = divmod(communal["copper"], 10)
                communal["silver"] += silver
                communal["copper"] = copper
                gold, silver = divmod(communal["silver"], 10)
                communal["gold"] += gold
                communal["silver"] = silver
                await client.send_message(message.channel, f'The Communal Balance is {communal["gold"]} gold, {communal["silver"]} silver, and {communal["copper"]} copper')
        with open ('communalbank.txt', 'w') as communalOut:
            json.dump(communal, communalOut)

# Run the bot
token = 'Your Token'
client.run(token)