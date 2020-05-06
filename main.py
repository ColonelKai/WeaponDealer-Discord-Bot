import discord
import asyncio
import random
import json
import time


client = discord.Client()


def check_group_member(user):
    with open("groupdata.json", "r") as file:
        groupdata = json.load(file)

    for i in groupdata.keys():
        if user.id in groupdata[i]["members"]:
            return True, i
        
    return False, None

def check_group_owner(user):
    with open("groupdata.json", "r") as file:
        groupdata = json.load(file)

    for i in groupdata.keys():
        if user.id == groupdata[i]["owner"]:
            return True, i
        
    return False, None

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
            "fighting" : False,
            "last_search" : 00000
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
    return f"You have {userdata[str(user.id)]['data']['Money']} Retard Bucks.\nYou have {userdata[str(user.id)]['data']['health']} health\nYou have {userdata[str(user.id)]['data']['RP']} Respect Points."    

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
        if counter <= range_max and counter > range_min:
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
        if counter <= range_max and counter > range_min:
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
        if userdata[str(user.id)]["data"]["inventory"][item] == 1:
            del userdata[str(user.id)]["data"]["inventory"][item]
        else:
            userdata[str(user.id)]["data"]["inventory"][item] -= 1
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
        if userdata[str(user.id)]["data"]["inventory"][item] == 1:
            del userdata[str(user.id)]["data"]["inventory"][item]
        else:
            userdata[str(user.id)]["data"]["inventory"][item] -= 1
        with open("playerdata.json", "w") as file:
            json.dump(userdata, file)
        return "You ate used an adrenaline and got 20 health!"
    
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

    await message.channel.send(f"```{target.display_name}, please do --accept to accept the fight, otherwise you are a certified pussy.```")

    def check1(msg):
        return msg.content == "--accept" and msg.author == target

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

            print(damage)

            max_randomizer = damage / 4
            min_randomizer = max_randomizer * -1

            bruh = random.randint(int(min_randomizer), int(max_randomizer))

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

async def create_group(user, message) -> None:
        with open("groupdata.json", "r") as file:
            groupdata = json.load(file)

        with open("playerdata.json", "r") as file:
            userdata = json.load(file)

        split_message = message.content.split( )

        if len(split_message) < 2:
            await message.channel.send("```You need to enter a name to create a group.```")  
            return
        
        factionname = split_message[1]

        if userdata[str(user.id)]["data"]["Money"] < 250:
            await message.channel.send("```You dont have enough Retard Bucks to create a group.```")
            return

        does_own_group, tempvar1 = check_group_owner(user)

        if does_own_group:
            await message.channel.send("```You already own a group.```")
            return

        is_in_group, tempvar2 = check_group_member(user)

        if is_in_group:
            await message.channel.send("```You are already in a group.```")
            return

        if factionname in groupdata.keys():
            await message.channel.send("```That groupname is already being used.```")
            return

        await message.channel.send(f"```{user.display_name}, this is going to cost 250 Retard Bucks, are you sure? (do --accept to accept and do nothing to deny)```")

        def check3(msg):
            return msg.content == "--accept" and msg.author == user
        
        try:
            msg = await client.wait_for('message', timeout=30.0, check=check3)
        except asyncio.TimeoutError:
            await message.channel.send(f"```Cancelled group creation.```")
            return

        #actual creation
        groupdata[factionname] = {}
        groupdata[factionname]["owner"] = user.id
        groupdata[factionname]["members"] = {}
        groupdata[factionname]["money"] = 0
        groupdata[factionname]["inventory"] = {}

        print(groupdata)

        userdata[str(user.id)]["data"]["Money"] -= 250

        with open("groupdata.json", "w") as file:
            json.dump(groupdata, file)

        with open("playerdata.json", "w") as file:
            json.dump(userdata, file)

        await message.channel.send(f"```Faction {factionname} has been created.```")

async def invite_group(user, message) -> None:
    with open("groupdata.json", "r") as file:
        groupdata = json.load(file)


    split_message = message.content.split( )
    if len(message.mentions) > 1:
        await message.channel.send(f"```{user.display_name}, you cannot invite more than 1 person!```")
        return
    elif len(message.mentions) < 1: 
        await message.channel.send(f"```{user.display_name}, you need to tag someone to invite!```")
        return

    target = message.mentions[0]

    isingroup, tempvar3 = check_group_member(target)

    if isingroup:
        await message.channel.send(f"```He is already in a group, bruh.```")
        return

    doesownagroup, tempvar4 = check_group_owner(target)

    if doesownagroup:
        await message.channel.send(f"```He owns a group, bruh.```")
        return

    doesowngroupuser, group_bruh = check_group_owner(user)

    if not doesowngroupuser:
        await message.channel.send(f"```You need to own a group to add them.```")


    await message.channel.send(f"```{target.display_name}, please do --accept to accept the invite.```")

    def check4(msg):
        return msg.content == "--accept" and msg.author == target

    try:
        msg = await client.wait_for('message', timeout=30.0, check=check4)
    except asyncio.TimeoutError:
        await message.channel.send(f"```{target.display_name} did not accept the request in time. RIP...```")
        return


    groupdata[group_bruh]["members"][str(target.id)] = 1

    with open("groupdata.json", "w") as file:
        json.dump(groupdata, file)
    
    await message.channel.send(f"```{target.display_name} has been added to {group_bruh}.```")
    return

async def leave_group(user, message) -> None:
    isingroup, groupname = check_group_member(user)
    if not isingroup:
        await message.channel.send(f"```You need to be in a group to leave it, retard.```")
        return

    with open("groupdata.json", "r") as file:
        groupdata = json.load(file)

    del groupdata[groupname]["members"][user.id]

    with open("groupdata.json", "w") as file:
        json.dump(groupdata, file)

    await message.channel.send(f"```You succesfully left {groupname}.```")

async def dep_group(user, message) -> None:
    
    split_message = message.content.split( )
    if len(split_message) < 2:
        await message.channel.send(f"```Please specify an amount to deposit.```")
        return

    dep_amount = int(split_message[1])
    
    with open("playerdata.json", "r") as file:
        playerdata = json.load(file)

    if dep_amount > playerdata[str(user.id)]["data"]["Money"]:
        await message.channel.send(f"```You dont have that much money, retard.```")
        return

    is_in_group, groupname_1 = check_group_member(user)
    does_own_group, groupname_2 = check_group_owner(user)

    if not is_in_group and not does_own_group:
        await message.channel.send(f"```You are not in a group.```")
        return
    
    print(groupname_1)
    print(groupname_2)

    if is_in_group:
        groupname = groupname_1

    elif does_own_group:
        groupname = groupname_2

    with open("groupdata.json", "r") as file:
        groupdata = json.load(file)

    groupdata[groupname]["money"] += dep_amount

    playerdata[str(user.id)]["data"]["Money"] -= dep_amount

    with open("groupdata.json", "w") as file:
        json.dump(groupdata, file)

    with open("playerdata.json", "w") as file:
        json.dump(playerdata, file)

    await message.channel.send(f"```You deposited {dep_amount} to group {groupname}!```")
    return

async def disband_group(user, message) -> None:
    does_own_group, groupname = check_group_owner(user)

    if not does_own_group:
        await message.channel.send(f"```You dont own a faction, dumbass.```")
        return

    with open("groupdata.json", "r") as file:
        groupdata = json.load(file)

    def check5(msg):
        return msg.content == "--accept" and msg.author == user

    await message.channel.send(f"```Are you sure? (do --accept to confirm)```")

    try:
        msg = await client.wait_for('message', timeout=30.0, check=check5)
    except asyncio.TimeoutError:
        await message.channel.send(f"```{user.display_name} Cancelled group disbanding.```")
        return

    del groupdata[groupname]

    with open("groupdata.json", "w") as file:
        json.dump(groupdata, file)

    await message.channel.send(f"```Group {groupname} has been disbanded```")
    
async def withdraw_group(user, message) -> None:
    split_message = message.content.split( )
    if len(split_message) < 2:
        await message.channel.send(f"```Please specify an amount to deposit.```")
        return

    dep_amount = int(split_message[1])

    is_in_group, groupname_1 = check_group_member(user)
    does_own_group, groupname_2 = check_group_owner(user)

    if not is_in_group and not does_own_group:
        await message.channel.send(f"```You are not in a group.```")
        return
    
    print(groupname_1)
    print(groupname_2)

    if is_in_group:
        groupname = groupname_1

    elif does_own_group:
        groupname = groupname_2

    with open("groupdata.json", "r") as file:
        groupdata = json.load(file)
    
    with open("playerdata.json", "r") as file:
        playerdata = json.load(file)

    if dep_amount > groupdata[groupname]["money"]:
        await message.channel.send(f"```Your Group doesnt have that much, retard.```")
        return


    groupdata[groupname]["money"] -= dep_amount

    playerdata[str(user.id)]["data"]["Money"] += dep_amount

    with open("groupdata.json", "w") as file:
        json.dump(groupdata, file)

    with open("playerdata.json", "w") as file:
        json.dump(playerdata, file)

    await message.channel.send(f"```You withdrew {dep_amount} from group {groupname}!```")
    return

async def group_stat(user, message) -> None:
    global client
    is_in_group, groupname_1 = check_group_member(user)
    does_own_group, groupname_2 = check_group_owner(user)

    if not is_in_group and not does_own_group:
        await message.channel.send(f"```You are not in a group.```")
        return
    

    if is_in_group:
        groupname = groupname_1

    elif does_own_group:
        groupname = groupname_2

    with open("groupdata.json", "r") as file:
        groupdata = json.load(file)

    result_str = ""
    result_str += f"Group Name: {groupname}\n"
    result_str += f"Group Owner: {client.get_user(groupdata[groupname]['owner']).display_name}\n"
    result_str += f"Group Balance: {groupdata[groupname]['money']}\n"
    result_str += f"do ?groupinv for inventory and ?grouplist for member list."

    await message.channel.send(f"```{result_str}```")

async def group_inv(user, message) -> None:

    channel = message.channel

    with open("groupdata.json", "r") as file:
        groupdata = json.load(file)

    is_in_group, groupname_1 = check_group_member(user)
    does_own_group, groupname_2 = check_group_owner(user)

    if not is_in_group and not does_own_group:
        await message.channel.send(f"```You are not in a group.```")
        return
    

    if is_in_group:
        groupname = groupname_1

    elif does_own_group:
        groupname = groupname_2

    inventory = groupdata[groupname]["inventory"]

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
        if counter <= range_max and counter > range_min:
            final_items[i] = inventory[i]

    message = "Your items: \n\n"
    for i in final_items.keys():
        message += f"{i} x{final_items[i]} \n"

    message += f"\nPage {page}/{pages}"
    
    await channel.send(f"```{message}```")

async def group_kick(user, message) -> None:
    isowner, groupname = check_group_owner(user)
    if not isowner:
        await message.channel.send(f"```You are not a group owner.```")
        return  

    if len(message.mentions) > 1:
        await message.chanel.send(f"```You can only kick one person at a time.```")
        return

    if len(message.mentions) < 1:
        await message.channel.send(f"```You need to tag someone to kick.```")

    target = message.mentions[0]

    istargetingroup, targetgroup = check_group_member(target)

    if not  istargetingroup or targetgroup != groupname:
        await message.channel.send(f"```The person you want to kick is not in your group, retard.```")
        return
    
    with open("groupdata.json", "r") as file:
        groupdata = json.load(file)

    del groupdata[groupname]["members"][target.id]

    with open("groupdata.json", "w") as file:
        json.dump(groupdata, file)

    await message.channel.send(f"```{target.display_name} has been kicked from {groupname}, that poor guy.```")

async def group_itemdep(user, message) -> None:

    is_in_group, groupname_1 = check_group_member(user)
    does_own_group, groupname_2 = check_group_owner(user)

    if not is_in_group and not does_own_group:
        await message.channel.send(f"```You are not in a group.```")
        return
    

    if is_in_group:
        groupname = groupname_1

    elif does_own_group:
        groupname = groupname_2

    split_message = message.content.split( )
    if len(split_message) < 2:
        await message.channel.send(f"```You need to specify an item to deposit.```")
        return
    elif len(split_message) < 3:
        dep_amount = 1
    elif len(split_message) < 4:
        dep_amount = split_message[2]
    dep_item = split_message[1]

    with open("playerdata.json", "r") as file:
        playerdata = json.load(file)

    with open("groupdata.json", "r") as file:
        groupdata = json.load(file)

    if not dep_item in playerdata[str(user.id)]["data"]["inventory"]:
        await message.channel.send(f"```You dont have that item.```")
        return

    if playerdata[str(user.id)]["data"]["inventory"][dep_item] < dep_amount:
        await message.channel.send(f"```You dont have that many of that item.```")
        return

    if dep_item in groupdata[groupname]["inventory"]:
        groupdata[groupname]["inventory"][dep_item] += dep_amount
    else:
        groupdata[groupname]["inventory"][dep_item] = dep_amount

    if playerdata[str(user.id)]["data"]["inventory"][dep_item] == dep_amount:
        del playerdata[str(user.id)]["data"]["inventory"][dep_item]
    else:
        playerdata[str(user.id)]["data"]["inventory"][dep_item] -= dep_amount


    with open("groupdata.json", "w") as file:
        json.dump(groupdata, file)

    await message.channel.send(f"```You deposited {dep_amount} {dep_item}(s) to your group.```")
    return

async def group_itemwithdraw(user, message) -> None:
    is_in_group, groupname_1 = check_group_member(user)
    does_own_group, groupname_2 = check_group_owner(user)

    if not is_in_group and not does_own_group:
        await message.channel.send(f"```You are not in a group.```")
        return
    

    if is_in_group:
        groupname = groupname_1

    elif does_own_group:
        groupname = groupname_2

    split_message = message.content.split( )
    if len(split_message) < 2:
        await message.channel.send(f"```You need to specify an item to deposit.```")
        return
    elif len(split_message) < 3:
        dep_amount = 1
    elif len(split_message) < 4:
        dep_amount = split_message[2]
    dep_item = split_message[1]

    with open("playerdata.json", "r") as file:
        playerdata = json.load(file)

    with open("groupdata.json", "r") as file:
        groupdata = json.load(file)

    if not dep_item in groupdata[groupname]["inventory"]:
        await message.channel.send(f"```Your group doesent have that item.```")
        return

    if groupdata[groupname]["inventory"][dep_item] < dep_amount:
        await message.channel.send(f"```Your group doesent have that many of that item.```")
        return

    
    if dep_item in playerdata[str(user.id)]["data"]["inventory"]:
        playerdata[str(user.id)]["data"]["inventory"][dep_item] += dep_amount
    else:
        playerdata[str(user.id)]["data"]["inventory"][dep_item] = dep_amount

    if groupdata[groupname]["inventory"][dep_item] == dep_amount:
        del groupdata[groupname]["inventory"][dep_item]
    else:
        groupdata[groupname]["inventory"][dep_item] -= dep_amount



    with open("groupdata.json", "w") as file:
        json.dump(groupdata, file)

    await message.channel.send(f"```You deposited {dep_amount} {dep_item}(s) to your group.```")
    return

async def grouplist(user, message) -> None:

    channel = message.channel

    with open("groupdata.json", "r") as file:
        groupdata = json.load(file)
    
    is_in_group, groupname_1 = check_group_member(user)
    does_own_group, groupname_2 = check_group_owner(user)

    if not is_in_group and not does_own_group:
        await message.channel.send(f"```You are not in a group.```")
        return
    
    print(groupname_1)
    print(groupname_2)

    if is_in_group:
        groupname = groupname_1

    elif does_own_group:
        groupname = groupname_2


    inventory = groupdata[groupname]["members"]
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
        if counter <= range_max and counter > range_min:
            final_items[i] = inventory[i]

    message = f"{groupname} Members: \n\n"
    for i in final_items.keys():
        message += f"{i} \n"

    message += f"\nPage {page}/{pages}"
    await channel.send(f"```{message}```")

async def sell_itme(user, message) -> None:
    split_message = message.content.split( )
    if len(split_message) < 2:
        await message.channel.send("```You need to specify name and amount of items you want to sell.```")
        return
    elif len(split_message) < 3:
        buy_amount = 1
    elif len(split_message) < 4:
        buy_amount = split_message[2]
        
    buy_item = split_message[1]

    with open("shopitems.json", "r") as file:
        shopdata = json.load(file)
        
    with open("playerdata.json", "r") as file:
        userdata = json.load(file)

    total_price = (shopdata[buy_item] * int(buy_amount)) / 2

    print("total price:")
    print(total_price)

    if not buy_item in userdata["data"]["inventory"].keys():
        await message.channel.send("```You don't have the item you want to sell, retard.```")
        return

    if userdata["data"]["inventory"][buy_item] < buy_amount:
        await message.channel.send("```You dont have that many, retard.```")
        return
    
    userdata[str(user.id)]["data"]["Money"] = userdata[str(user.id)]["data"]["Money"] + total_price


    userdata[str(user.id)]["data"]["inventory"][str(buy_item)] -= int(buy_amount)


    with open("playerdata.json", "w") as file:
        json.dump(userdata, file)

    await message.channel.send(f"You sold {buy_amount} {buy_item}(s).")

async def search(user, message) -> None:
    with open("playerdata.json", "r") as file:
        playerdata = json.load(file)

    if time.time() - 600 < playerdata[str(user.id)]["data"]["last_search"]:
        await message.channel.send("```You need to wait 10 minutes between parameter searches!```")
        return

    #real randomization begins

    #how much money will he get? (between 0 and 100)
    found_money = random.randint(0, 100)

    #will he get a item? (0-100, 0-50 means no, 50-100 has items assigned.)
    item_rand = random.randint(0, 100)

    if item_rand > 50:
        if item_rand > 50 and item_rand <= 70:
            item_get = "bread"
        elif item_rand > 70 and item_rand <= 80:
            item_get = "glock"
        elif item_rand > 80 and item_rand <= 90:
            item_get = "adrenaline"
        elif item_rand > 90 and item_rand <= 100:
            item_get = "m4"
    else:
        item_get = False

    if not item_get == False:
        await message.channel.send(f"```You found {found_money} Retard Bucks and a {item_get} while searching the parameter!```")
        playerdata[str(user.id)]["data"]["Money"] += found_money
        if item_get in playerdata[str(user.id)]["data"]["inventory"].keys():
            playerdata[str(user.id)]["data"]["inventory"][item_get] += 1
        else:
            playerdata[str(user.id)]["data"]["inventory"][item_get] = 1
    
    if item_get == False:
        await message.channel.send(f"```You found {found_money} Retard Bucks while searching the perimeter!```")
        playerdata[str(user.id)]["data"]["Money"] += found_money

    playerdata[str(user.id)]["data"]["last_search"] = time.time()

    with open("playerdata.json", "w") as file:
        json.dump(playerdata, file)

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
        elif message.content.startswith("?creategroup"):
            await create_group(message.author, message)
        elif message.content.startswith("?invitegroup"):
            await invite_group(message.author, message)
        elif message.content.startswith("?leavegroup"):
            await leave_group(message.author, message)
        elif message.content.startswith("?depgroup"):
            await dep_group(message.author, message)
        elif message.content.startswith("?disband"):
            await disband_group(message.author, message)
        elif message.content.startswith("?withdrawgroup"):
            await withdraw_group(message.author, message)
        elif message.content.startswith("?groupstat"):
            await group_stat(message.author, message)
        elif message.content.startswith("?groupinv"):
            await group_inv(message.author, message)
        elif message.content.startswith("?group_itemdep"):
            await group_itemdep(message.author, message)
        elif message.content.startswith("?group_itemwithdraw"):
            await group_itemwithdraw(message.author, message)
        elif message.content.startswith("?grouplist"):
            await grouplist(message.author, message)
        elif message.content.startswith("?sell"):
            await sell_itme(message.author, message)
        elif message.content.startswith("?search"):
            await search(message.author, message)
        else:
            await message.channel.send(f"```Thats not an option, please use ?help```")

#endregion

client.run("NzA0OTc1NjQ4NDgwODIxMjQ5.Xqq4Eg.qbe5rQOsqnZUeDqsq9Q8YLEqysU")