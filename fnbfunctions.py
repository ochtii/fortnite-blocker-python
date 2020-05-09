import json, datetime

def read_metrics():
    """
    Gets the content from metrics.json file. The file must be located in the same directory as the root file.
    """
    try:
        with open('metrics.json') as metrics_file:
            metrics = json.load(metrics_file)
            return metrics
    except Exception as e:
        print(e)

def write_metrics(var):
    """
    Writes the content of var to metrics.json. The file must be located in the same directory as the root file.
    """
    try:
        with open('metrics.json', 'w') as outfile:
            json.dump(var, outfile, indent=4)
    except Exception as e:
        print(e)

def read_guildsFile():
    """
    Gets the content from guilds.json file. The file must be located in the same directory as the root file.
    """
    try:
        with open('guilds.json') as guilds_file:
            guilds = json.load(guilds_file)
            return guilds
    except Exception as e:
        print(e)

def write_guildsFile(var):
    """
    Writes the content of var to guilds.json. The file must be located in the same directory as the root file.
    """
    try:
        with open('guilds.json', 'w') as outfile:
            json.dump(var, outfile, indent=4)
            return True
    except Exception as e:
        print(e)
        return False

def no_perms(msg):
    """
    Sends a message to notify the User that he is not permitted to use this command.
    msg = The message the user sent
    """
    msg1 = 'Missing Permission! This command is reserved for the Bot admins/owner!'
    message = msg.channel.send(msg1)
    return message

def owner_only(msg):
    """
    Sends a message to notify the User that he is not permitted to use this command.
    msg = The message the user sent
    """
    msg1 = "Missing Permission! This command is reserved for the Bot owner!"
    message = msg.channel.send(msg1)
    return message

def all_guilds(client):
    """
    Get all guilds where the Bot is on.
    """
    guilds = client.guilds
    return guilds

def catch_guilds(client):
    catched = 0
    guildsFile = read_guildsFile()
    guilds = all_guilds(client)
    guildList = []

    for x in guildsFile:
        guildList.append(x['id'])

    for y in guilds:
        now = datetime.datetime.now()
        if y.id not in guildList:
            data = {
                'id': y.id,
                'owner': y.owner.id,
                'blacklist':['fortnite'],
                'enabled': "yes",
                'admins': [],
                'whitelist': [],
                'bannedpeople': 0,
                'premium': 'no',
                'firstjoined': now.strftime("%Y-%m-%d %H:%M:%S")
            }
            guildsFile.append(data)
            catched += 1
    
    w = write_guildsFile(guildsFile)
    if w:
        if catched == 0:
            return None
        elif catched > 0:    
            return catched
        else:
            return False
    else:
        return False
        