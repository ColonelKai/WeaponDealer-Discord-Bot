import discord
import asyncio
import random
import json
import time


client = discord.Client()




def register_user(user):
    with open("playerdata.json", "r") as file:
        userdata = json.load(file)

    if user.id in userdata.keys():
        return "The user has already been registered."
    
    else:
        new_entry_inventory = {
        "bread" : 5,
        "glock" : 1}

        new_entry_info = {
            "inventory" : new_entry_inventory,
            "Money" : 500,
            "health" : 100,
            "RP" : 100,
            "fighting" : False
        }
        
        new_entry = {
            "username" : user.display_name,
        "data" : new_entry_info}

        userdata[user.id] = new_entry
        with open("playerdata.json", "w") as file:
            json.dump(userdata, file)
        return "Succesfully created player data."
    
def balance_read(user):
    with open("playerdata.json", "r") as file:
        userdata = json.load(file)
    return f"You have {userdata[str(user.id)]['data']['Money']} Retard Bucks.\nYou have {userdata[str(user.id)]['data']['health']} health"    

def money_set(user, message):
    if message.channel.permissions_for(user).administrator:
        with open("playerdata.json", "r") as file:
            userdata = json.load(file)
        split_message = message.content.split( )
        amount = split_message[1]
        person_id = split_message[2]

        userdata[str(person_id)]["data"]["Money"] = int(amount)

        with open("playerdata.json", "w") as file:
            json.dump(userdata, file)

        return f"Target's balance has been set to {amount}" 

    else:
        return "You need to be an admin to use this command."

def inventory_read(user, message):
    with open("playerdata.json", "r") as file:
        userdata = json.load(file)
    
    inventory = userdata[str(user.id)]["data"]["inventory"]
    split_message = message.content.split( )
    pages = len(inventory.keys()) // 5
    mod = len(inventory.keys()) % 5 
    if mod > 0:
        pages += 1

    try:
        split_message[1] = int(split_message[1])
        page = split_message[1]
        if page > pages: 
            return f"There is only {pages} pages!"

    except:
        page = 1

    range_min = (page-1) * 5
    range_max = range_min + 5

    final_items = {}
    counter = 0
    for i in inventory.keys():
        counter += 1
        if counter < range_max and counter > range_min:
            final_items[i] = inventory[i]

    message = "Your items: \n\n"
    for i in final_items.keys():
        message += f"{i} x{final_items[i]} \n"

    message += f"\nPage {page}/{pages}"
    return message

def shop_read(user, message):
    with open("shopitems.json", "r") as file:
        userdata = json.load(file)
    
    inventory = userdata
    split_message = message.content.split( )
    pages = len(inventory.keys()) // 5
    mod = len(inventory.keys()) % 5 
    if mod > 0:
        pages += 1


    try:
        split_message[1] = int(split_message[1])
        page = split_message[1]
        if page > pages: 
            return f"There is only {pages} pages!"

    except:
        page = 1



    range_min = (page-1) * 5
    range_max = range_min + 5

    final_items = {}
    counter = 0
    for i in inventory.keys():
        counter += 1
        if counter < range_max and counter > range_min:
            final_items[i] = inventory[i]

    message = "Shop: \n\n"
    for i in final_items.keys():
        message += f"{i} for {final_items[i]} \n"

    message += f"\nPage {page}/{pages}"
    return message

def buy_item(user, message):
    split_message = message.content.split( )
    if len(split_message) < 2:
        return "You need to specify name and amount of items you want to buy."
    elif len(split_message) < 3:
        buy_amount = 1
    elif len(split_message) < 4:
        buy_amount = split_message[2]
        
    buy_item = split_message[1]

    with open("shopitems.json", "r") as file:
        shopdata = json.load(file)
        
    with open("playerdata.json", "r") as file:
        userdata = json.load(file)

    total_price = shopdata[buy_item] * int(buy_amount)

    print("total price:")
    print(total_price)

    if not buy_item in shopdata.keys():
        return "The item you want to buy does not exist in shop, retard."

    if userdata[str(user.id)]["data"]["Money"] < int(total_price):
        return "You dont have enough money, poor ass."
    
    userdata[str(user.id)]["data"]["Money"] = userdata[str(user.id)]["data"]["Money"] - total_price

    if buy_item in userdata[str(user.id)]["data"]["inventory"].keys():
        userdata[str(user.id)]["data"]["inventory"][str(buy_item)] += int(buy_amount)

    else:
        userdata[str(user.id)]["data"]["inventory"][str(buy_item)] = int(buy_amount)

    with open("playerdata.json", "w") as file:
        json.dump(userdata, file)

    return f"You bought {buy_amount} {buy_item}(s)."

def use_item(user, message):
    with open("playerdata.json", "r") as file:
        userdata = json.load(file)

    split_message = message.content.split( )
    if len(split_message) < 2:
        return "You need to specify an item to use."
    item = split_message[1]
    if not item in userdata[str(user.id)]["data"]["inventory"]:
        return "You dont have that item, retard."
    
    if item == "bread":
        if userdata[str(user.id)]["data"]["health"] == 100:
            return "You already have full health."
        elif userdata[str(user.id)]["data"]["health"] > 94:
            userdata[str(user.id)]["data"]["health"] = 100
        else:
            userdata[str(user.id)]["data"]["health"] += 5
        with open("playerdata.json", "w") as file:
            json.dump(userdata, file)
        return "You ate a bread and gained 5 health!"
    
    if item == "adrenaline":
        if userdata[str(user.id)]["data"]["health"] == 200:
            return "You already have 200 health."
        elif userdata[str(user.id)]["data"]["health"] > 294:
            userdata[str(user.id)]["data"]["health"] = 200
        else:
            userdata[str(user.id)]["data"]["health"] += 20
        with open("playerdata.json", "w") as file:
            json.dump(userdata, file)
        return "You ate a bread and gained 5 health!"
    
def kill_someone(user):
    with open("playerdata.json", "r") as file:
        userdata = json.load(file)
    userdata[str(user.id)]["data"]["Money"] = 0
    userdata[str(user.id)]["data"]["health"] = 100
    userdata[str(user.id)]["data"]["inventory"] = {}
    userdata[str(user.id)]["data"]["RP"] = 100
    with open("playerdata.json", "w") as file:
        json.dump(userdata, file)
    
async def fight(user, message) -> None:
    global client

    with open("playerdata.json", "r") as file:
        userdata = json.load(file)

    if userdata[str(user.id)]["data"]["RP"] < 5:
        await message.channel.send(f"```{user.display_name}, you dont have enough Respect Points.```")
        return

    if len(message.mentions) > 1:
        await message.channel.send(f"```{user.display_name}, you cannot fight more than 1 person!```")
        return
    elif len(message.mentions) < 1: 
        await message.channel.send(f"```{user.display_name}, you need to tag someone to fight!```")
        return

    target = message.mentions[0]

    userdata[str(user.id)]["data"]["RP"] -= 5


    print(target.id)

    await message.channel.send(f"```{target.display_name}, please do ?accept to accept the fight, otherwise you are a certified pussy.```")

    def check1(msg):
        return msg.content == "?accept" and msg.author == target

    try:
        msg = await client.wait_for('message', timeout=30.0, check=check1)
    except asyncio.TimeoutError:
        await message.channel.send(f"```{target.display_name} did not accept the request in time. He lost respect points...```")
        userdata[str(target.id)]["data"]["RP"] -= 5
        with open("playerdata.json", "w") as file:
            json.dump(userdata, file)
        
        return

    userdata[str(target.id)]["data"]["fighting"] = True
    userdata[str(user.id)]["data"]["fighting"] = True
    with open("playerdata.json", "w") as file:
        json.dump(userdata, file)
    
    #Fight starts!
    stupidrandint = random.randint(1, 2)
    if stupidrandint == 1:
        attacker = user
        defender = target
    else:
        attacker = target
        defender = user

    while True:

        if userdata[str(attacker.id)]["data"]["health"] <= 0:
            kill_someone(attacker)
            await message.channel.send(f"```{attacker} died. RIP.```")
            return

        if userdata[str(defender.id)]["data"]["health"] <= 0:
            kill_someone(defender)
            await message.channel.send(f"```{defender} died. RIP.```")
            return
        
        await message.channel.send(f"```{attacker}, please --fire [gun], --use [item]```")

        def check2(msg):
            return msg.content.startswith("--") and msg.author == attacker

        try:
            msg = await client.wait_for('message', timeout=60.0, check=check2)
        except asyncio.TimeoutError:
            await message.channel.send(f"```Retard {attacker} didnt do anything for 60 seconds smh.```")
            return
        split_message = msg.content.split( )
        if split_message[0] == "--use":
            rv = use_item(attacker, msg)
            await message.channel.send(f"```{rv}```")
                        
            if attacker == user:
                attacker = target
                defender = user

            elif attacker == target:
                attacker = user
                defender = target
            continue

        elif split_message[0] == "--fire":
            guns = userdata[str(attacker.id)]["data"]["inventory"]

            with open("gundamages.json", "r") as file:
                gundata = json.load(file)

            if not split_message[1] in gundata.keys():
                await message.channel.send(f"```{split_message[1]} is not a valid weapon.```")
                continue
            if not split_message[1] in guns.keys():
                await message.channel.send(f"```You dont have a {split_message[1]}.```")
                continue
            
            damage = gundata[split_message[1]]

            max_randomizer = damage / 4
            min_randomizer = max_randomizer * -1

            bruh = random.randint(min_randomizer, max_randomizer)

            damage += bruh

            userdata[str(defender.id)]["data"]["health"] -= damage

            with open("playerdata.json", "w") as file:
                json.dump(userdata, file)
            
            await message.channel.send(f"````{attacker} used an {split_message[1]} to against {defender} and dealt {damage} damage! {defender} now has {userdata[str(defender.id)]['data']['health']} health!```")
            
            if attacker == user:
                attacker = target
                defender = user

            elif attacker == target:
                attacker = user
                defender = target

            continue




#region Command handler
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    with open("playerdata.json", "r") as file:
        userdata = json.load(file)

    try:
        if userdata[str(message.author.id)]["data"]["fighting"] == True and message.startswith("?"):
            await message.channel.send("```You cannot use normal commands in a fight!```")
            return
    except:
        pass


    if message.content.startswith('?'):
        if message.content == "?ping":
            await message.channel.send('```Bot is running!```')
        elif message.content == "?register":
            rv = register_user(message.author)
            await message.channel.send(f"```{rv}```")
        elif message.content == "?stat":
            rv = balance_read(message.author)
            await message.channel.send(f"```{rv}```")
        elif message.content.startswith("?moneyset"):
            rv = money_set(message.author, message)
            await message.channel.send(f"```{rv}```")
        elif message.content.startswith("?inventory"):
            rv = inventory_read(message.author, message)
            await message.channel.send(f"```{rv}```")
        elif message.content.startswith("?shop"):
            rv = shop_read(message.author, message)
            await message.channel.send(f"```{rv}```")
        elif message.content.startswith("?buy"):
            rv = buy_item(message.author, message)
            await message.channel.send(f"```{rv}```")
        elif message.content.startswith("?use"):
            rv = use_item(message.author, message)
            await message.channel.send(f"```{rv}```")
        elif message.content.startswith("?fight"):
            await fight(message.author, message)
        elif message.content.startswith("?accept"):
            pass
        else:
            await message.channel.send(f"```Thats not an option, please use ?help```")

#endregion

client.run("NzA0OTc1NjQ4NDgwODIxMjQ5.Xqk92w.d9SQ6G4G9enJF_xWQ0xN_UkHeso")