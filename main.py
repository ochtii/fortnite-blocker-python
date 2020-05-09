import discord
import datetime, json, asyncio, array
import psutil, time, cpuinfo
import fnbfunctions

# Get Data from config.json
try:
    with open('config.json') as json_file:
        config = json.load(json_file)
        token = config["token"]
        banLogChannel = config['banLogChannelId']
        prefix = config['prefix']
        selectedGame = config['selectedGame']
        maintenance = config['maintenance']
        adminRole = config['adminRole']
        ownerId = config['ownerId']
except Exception as e:
    print(e)

class MyClient(discord.Client): 

    async def on_ready(self):
        
        if maintenance:
            activity = discord.Game(name="Maintenance......")
            await client.change_presence(status=discord.Status.online, activity=activity)
        else:
            metrics = fnbfunctions.read_metrics()
            activity = discord.Game(name="Active in " + metrics['guilds'] + " Servers")
            await client.change_presence(status=discord.Status.online, activity=activity)

        # read metrics.json
        metrics = fnbfunctions.read_metrics()
        
        # Set startuptime
        try:
            metrics['online_since'] = str(time.ctime())
            with open('metrics.json', 'w') as outfile1:
                json.dump(metrics, outfile1, indent=4)
        except Exception as e:
            print(e)

        async def check_Guilds(self, guilds):
            channel = client.get_channel(banLogChannel)
            userCount = 0
            serverCount = 0
            start = time.time()
            print('------------- starting Scan -------------')
            guilds2 = fnbfunctions.read_guildsFile()
            for x in guilds:
                if x.id != 264445053596991498: #Discord Botlist Server
                    for z in guilds2:
                        if z['id'] == x.id:
                            if z['enabled'] == 'yes':
                                serverCount += 1
                                for y in x.members:
                                    userCount += 1
                                    if hasattr(y.activity, 'name'):
                                        if str(y.activity.name).lower() in z['blacklist']:
                                            user = client.get_user(y.id)
                                            try:
                                                print('\n' + 'Blacklisted activity detected (' + y.activity.name + ') User: ' + str(y) + ' (' + str(y.id) + ") || Server: " + str(y.guild) + " (" + str(y.guild.id) + ")")
                                                await y.ban()
                                                print('User banned: ' + y.name)
                                                try:
                                                    banMessage = discord.Embed(title="FortniteBlocker Ban Report", colour=discord.Colour(0x741016))
                                                    banMessage.add_field(name = "User", value = str(y) + "\n" + str(y.id))
                                                    banMessage.set_thumbnail(url=y.avatar_url)
                                                    banMessage.add_field(name = "Server", value = str(y.guild) + "\n" + str(y.guild.id))
                                                    banMessage.set_author(name = client.user.name, icon_url = client.user.avatar_url)
                                                    banMessage.set_footer(text="User has been banned automatically!")
                                                    await channel.send(embed = banMessage)
                                                except:
                                                    pass
                                            except Exception as e:
                                                print("Can't ban this user. Reason: " + str(e) + '\n')
                                                pass
                
                                    elif str(y.activity).lower() in z['blacklist']:
                                        user = client.get_user(y.id)
                                        try:   
                                            print('\n' + 'Blacklisted activity detected (' + str(y.activity) + ') User: ' + str(y) + ' (' + str(y.id) + ") || Server: " + str(y.guild) + " (" + str(y.guild.id) + ")")
                                            await y.ban()
                                            print('User banned: ' + y.name)                            
                                            try:
                                                banMessage = discord.Embed(title="FortniteBlocker Ban Report", colour=discord.Colour(0x741016))
                                                banMessage.add_field(name = "User", value = str(y) + "\n" + str(y.id))
                                                banMessage.set_thumbnail(url=y.avatar_url)
                                                banMessage.add_field(name = "Server", value = str(y.guild) + "\n" + str(y.guild.id))
                                                banMessage.set_author(name = client.user.name, icon_url = client.user.avatar_url)
                                                banMessage.set_footer(text="User has been banned automatically!")
                                                await channel.send(embed=banMessage)
                                            except Exception as e:
                                                print(e)
                                                pass
                                            try:
                                                await user.send('You have been banned from **' + str(y.guild.name) + '** for playing ' + selectedGame)
                                            except Exception as e:
                                                print(e)
                                                pass                                                                                          
                                        except Exception as e:
                                            print("Can't ban this user. Reason: " + str(e) + '\n')
                                            pass
            end = time.time()
            diff = str('{:5.4f}'.format(end-start))
            print(str(userCount) + ' Users from ' + str(serverCount) + ' Servers in ' + diff + 's scanned\n')
            print('------------- finished Scan -------------\n')

            metrics['guilds'] = str(serverCount)
            metrics['users'] = str(userCount)
            metrics['last_scan_time'] = diff
            fnbfunctions.write_metrics(metrics)
            
            await asyncio.sleep(15)
            #time.sleep(15)

        print('Bot logged in..')
        print('Servers: ' + str(len(client.guilds)) + '\n')
        print('Catching guilds...')
        catchGuilds = fnbfunctions.catch_guilds(client)
        if catchGuilds == None:
            print('All guilds catched.\n')
        elif catchGuilds == False:
            print('Error catching guilds. Try catch_guilds and see what happens')
        else:
            print('Found uncatched guilds..\n' + str(catchGuilds) + ' Guild(s) catched.\n')
        while client.is_ready:
            await check_Guilds(self, fnbfunctions.all_guilds(client))
        
    async def on_guild_join(self, guild):
        metrics = fnbfunctions.read_metrics()
        guilds = fnbfunctions.read_guildsFile()
        guildList = []
        for x in guilds:
            guildList.append(x['id'])
        now = datetime.datetime.now()
        if guild.id not in guildList:
            data = {
                'id': guild.id,
                'owner': guild.owner.id,
                'blacklist':['fortnite'],
                'enabled': "yes",
                'admins': [],
                'whitelist': [],
                'bannedpeople': 0,
                'premium': 'no',
                'firstjoined': now.strftime("%Y-%m-%d %H:%M:%S")
            }
            guilds.append(data)
            w = fnbfunctions.write_guildsFile(guilds)
            if w:
                print('Guild catched!')


        metrics['guilds'] = str(int(metrics['guilds']) + 1)
        print('Server joined: ' + str(guild.name) + ' (' + str(guild.id) + ')')
        activity = discord.Game(name="Active in " + metrics['guilds'] + " Servers")
        await client.change_presence(status=discord.Status.online, activity=activity)
        fnbfunctions.write_metrics(metrics)
        
    async def on_guild_remove(self, guild):
        metrics = fnbfunctions.read_metrics()
        metrics['guilds'] = str(int(metrics['guilds']) - 1)
        print('Server left: ' + str(guild.name) + ' (' + str(guild.id) + ')')
        activity = discord.Game(name="Active in " + metrics['guilds'] + " Servers")
        await client.change_presence(status=discord.Status.online, activity=activity)
        fnbfunctions.write_metrics(metrics)

    async def on_message(self, message):
                 
        if message.author == client.user:
            return
        
        if message.content.startswith(prefix):

            admin = False
            owner = False

            # Check if message author is admin
            for i in message.author.roles:
                if i.id == adminRole:
                    admin = True
            
            # Check if message author is bot owner
            if message.author.id == ownerId:
                owner = True
            
            # Split message into an array
            messageArgs = message.content.lower().split()

            # bot command in message (first argument after prefix)
            if len(messageArgs) > 1:
                command = messageArgs[1]
            else:
                command = False

            ##############################
            ##  Commands starting here  ##

            # Help command
            if command == "help" or command == "?":

                helpMessage = discord.Embed(title = client.user.name + " - Help", description = "Welcome to " + client.user.name + "'s Help. Here you can find all available commands.\n\nHow to use the Bot:\n`<prefix> <command>`\n\nPrefix:\n`" + prefix + "`",timestamp=datetime.datetime.utcfromtimestamp(datetime.datetime.now().timestamp()), colour=discord.Colour(0x129220))
                helpMessage.set_thumbnail(url=client.user.avatar_url)
                helpMessage.add_field(name = 'Commands', value =    '`' + prefix + ' ?` or `' + prefix + ' help` - View this message\n' +
                                                                    '`' + prefix + ' info` or `' + prefix + ' stats` - Show some infos and stats\n' + 
                                                                    '`' + prefix + ' status` - Some  actual status information\n' + 
                                                                    '`' + prefix + ' blacklist` - Blacklist handling (Server owner)\n' +
                                                                    '`' + prefix + ' disable` - Disable scanning (Server owner)\n' +
                                                                    '`' + prefix + ' enable` - Enable scanning (Server owner)\n', 
                                                                    inline=False)
                if owner:
                    helpMessage.add_field(name = 'Owner commands', value =  '`maintenance` - Maintenance status\n' + 
                                                                            '`catch_guilds` - required if guilds missing in guilds.json', inline=False)
                await message.channel.send(embed=helpMessage)

            # Bot information
            if command == "info" or command == "stats":

                # read metrics.json
                metrics = fnbfunctions.read_metrics()

                cpuInfo = cpuinfo.get_cpu_info()

                infoMessage = discord.Embed(title = client.user.name + "'s Info Board", colour=discord.Colour(0x129220))
                infoMessage.add_field(name = 'Number of users and servers', value = metrics['users'] + " User in " + metrics['guilds'] + " Servers", inline=False)
                infoMessage.add_field(name = 'System memory usage', value = str(psutil.virtual_memory().percent) +  "% --- " + str(int(int(psutil.virtual_memory().used)  / 1048576 )) + ' MB / ' + str(int(int(psutil.virtual_memory().total)  / 1048576 )) + ' MB', inline=False)
                infoMessage.add_field(name = 'Cpu cores / Architecture', value = str(psutil.cpu_count()) + ' Cores / ' + cpuInfo['arch'], inline = False)
                infoMessage.add_field(name = 'Cpu type', value = str(cpuInfo['brand']), inline = False)
                infoMessage.add_field(name = 'Cpu Usage (% per core)', value = psutil.cpu_percent(interval=None, percpu=True), inline = False)
                infoMessage.add_field(name = 'Python Version', value = str(cpuInfo['python_version']), inline = False)
                await message.channel.send(embed=infoMessage)

            # Bot status
            if command == "status":

                metrics = fnbfunctions.read_metrics() # read metrics.json

                statusMessage = discord.Embed(title = client.user.name + "'s Status Information", colour=discord.Colour(0x00aa00))
                statusMessage.add_field(name = 'Online since', value = metrics['online_since'], inline = False)
                statusMessage.add_field(name = 'Runtime last scan', value= metrics['last_scan_time'] + ' seconds (' + str(float(metrics['last_scan_time']) * 1000) + 'ms)' , inline = False)
                await message.channel.send(embed=statusMessage)



            ########################################
            #
            # Admin / Owner Commands
            #

            # Maintenance (admin + owner)
            if command == "maintenance":

                if admin or owner:

                    with open('config.json') as json_file:
                        data = json.load(json_file)
                        maintenance = data['maintenance']

                    if len(messageArgs) > 2:
                        if messageArgs[2] == 'false':
                            metrics = fnbfunctions.read_metrics() # read metrics
                            maintenance = False
                            data['maintenance'] = False
                            with open('config.json', 'w') as outfile:
                                json.dump(data, outfile, indent=4)
                            await message.channel.send('Bot status set to `Active in ' + metrics['guilds'] + ' Servers` !')
                            activity = discord.Game(name="Active in " + metrics['guilds'] + " Servers")
                            await client.change_presence(status=discord.Status.online, activity=activity)
                            
                        elif messageArgs[2] == 'true':
                            maintenance = True
                            data['maintenance'] = True
                            with open('config.json', 'w') as outfile:
                                json.dump(data, outfile, indent=4)
                            await message.channel.send('Bot status set to `Maintenance......` !')
                            activity = discord.Game(name="Maintenance......")
                            await client.change_presence(status=discord.Status.online, activity=activity)
                    else:
                        if maintenance:
                            color = 0xF3C764
                        else:
                            color = 0x009B02
                        maintenanceMessage = discord.Embed(title = 'Maintenance Status', description = 'Actual Maintenance status:\n`' + str(maintenance) + '`', colour=discord.Colour(color))
                        maintenanceMessage.add_field(name = 'Commands', value= '`' + prefix + ' maintenance true` - to activate\n`' + prefix + ' maintenance false` - to deactivate\n')
                        await message.channel.send(embed=maintenanceMessage)
                else:
                    await fnbfunctions.no_perms(message)

            # Catch all guilds into guilds.json (only bot owner)
            if command == "catch_guilds":
                if owner:
                    catch = fnbfunctions.catch_guilds(client)
                    if catch == False:
                        await message.channel.send('An Error occured. Please try again!') 
                    else:
                        await message.channel.send(str(catch) + ' Guild(s) catched!')

                else:
                    await fnbfunctions.owner_only(message)

            # Blacklist handling for banning conditions (only server owner)
            if command == "blacklist":
                if message.author.id == message.guild.owner.id:
                    blacklistHelp = discord.Embed(title = "Blacklist Handling", description = "Welcome to the FortniteBlocker Blacklist-Handling. Here you can add additional activities to your blacklist. All self added activities can be removed again. It is not possible to delete **Fortnite** from your blacklist. In the list below you can find all available commands for your blacklist.\nIf the bot detects an activity from your blacklist on a User's Presence, the User will banned immediately :)", colour=discord.Colour(0xff8400))
                    blacklistHelp.add_field(name = "Commands", value =  "Do not use the brackets. Just type the name of your activity. Spaces are allowed.\n\n" +
                                                                        "`" + prefix + " blacklist show` - Show your blacklist\n" +
                                                                        "`" + prefix + " blacklist add <activity>` - Add an activity to your blacklist\n" + 
                                                                        "`" + prefix + " blacklist del <activity>` - Delete an activity from your blacklist")
                    if len(messageArgs) > 2:
                        
                        # show blacklist
                        if messageArgs[2] == "show":
                            guilds = fnbfunctions.read_guildsFile()
                            for x in guilds:
                                if x['id'] == message.guild.id:
                                    s = "\n"
                                    blacklist = s.join(x['blacklist'])
                                    blacklistEmbed = discord.Embed(title = "FortniteBlocker Blacklist", colour=discord.Colour(0xff8400))
                                    blacklistEmbed.add_field(name = "Server", value = message.guild.name + "\n(" + str(message.guild.id) + ")", inline=False)
                                    blacklistEmbed.set_thumbnail(url = message.guild.icon_url)
                                    blacklistEmbed.add_field(name = "Activities on blacklist", value=str(len(x['blacklist'])), inline=False)
                                    blacklistEmbed.add_field(name = 'List:\n', value = blacklist, inline=False)
                                    await message.channel.send(embed = blacklistEmbed)

                        # add an antry to blacklist
                        elif messageArgs[2] == "add":
                            s = " "
                            game = s.join(messageArgs)[len(prefix) + 15:]
                            if not game or game == " ":
                                await message.channel.send("Please enter an activity which should be added to your blacklist..")
                            else:
                                guilds = fnbfunctions.read_guildsFile()
                                for x in guilds:
                                    if x['id'] == message.guild.id:
                                        if game not in x['blacklist']:
                                            x['blacklist'].append(game)               
                                            w = fnbfunctions.write_guildsFile(guilds)
                                            if w:
                                                await message.channel.send('`' + game + '` added to blacklist!')
                                        else:
                                            await message.channel.send("This activity is already on your blacklist.")

                        # remove an entry from blacklist
                        elif messageArgs[2] == "del":
                            s = " "
                            game = s.join(messageArgs)[len(prefix) + 15:]
                            if not game or game == " ":
                                await message.channel.send("Please enter an activity which should be removed from your blacklist..")
                            else:
                                if game == "fortnite":
                                    await message.channel.send("You can't remove Fortnite!")
                                else:
                                    guilds = fnbfunctions.read_guildsFile()
                                    for x in guilds:
                                        if x['id'] == message.guild.id:
                                            if game not in x['blacklist']:
                                                await message.channel.send('Game not found on your blacklist.')
                                            else:
                                                x['blacklist'].remove(game)
                                                w = fnbfunctions.write_guildsFile(guilds)
                                                if w:
                                                    await message.channel.send('`' + game + '` removed from blacklist!')

                        else:
                            await message.channel.send(embed = blacklistHelp)

                    else:
                        await message.channel.send(embed = blacklistHelp)

                else:
                    await message.channel.send('Only the Server Owner is permitted to use this command!')

            # Disable FortnitBlocker for this server (only server owner)
            if command == "disable":
                if message.author.id == message.guild.owner.id:
                    guilds = fnbfunctions.read_guildsFile()
                    for x in guilds:
                        if x['id'] == message.guild.id:
                            if x['enabled'] == 'yes':
                                x['enabled'] = "no"
                                w = fnbfunctions.write_guildsFile(guilds)
                                if w:
                                    await message.channel.send('FortniteBlocker disabled for *' + message.guild.name + '* !! Type `' + prefix + ' enable` to activate FortniteBlocker.')
                                    # metrics = fnbfunctions.read_metrics()
                                    # metrics['guilds'] = str(int(metrics['guilds']) - 1)
                                    # activity = discord.Game(name="Active in " + metrics['guilds'] + " Servers")
                                    # await client.change_presence(status=discord.Status.online, activity=activity)
                                    # fnbfunctions.write_metrics(metrics)
                            else:
                                await message.channel.send('Scanning already disabled. Type `' + prefix + ' enable` to activate FortniteBlocker.')
                else:
                    await message.channel.send('Only the Server Owner is permitted to use this command!')

                                           
            # Enable FortnitBlocker for this server (only server owner)
            if command == "enable":
                if message.author.id == message.guild.owner.id:
                    guilds = fnbfunctions.read_guildsFile()
                    for x in guilds:
                        if x['id'] == message.guild.id:
                            if x['enabled'] == 'no':
                                x['enabled'] = 'yes'
                                w = fnbfunctions.write_guildsFile(guilds)
                                if w:
                                    await message.channel.send('FortniteBlocker enabled for *' + message.guild.name + '* !! Type `' + prefix + ' disable` to disable FortniteBlocker for this Server.')
                                    # metrics = fnbfunctions.read_metrics()
                                    # metrics['guilds'] = str(int(metrics['guilds']) + 1)
                                    # activity = discord.Game(name="Active in " + metrics['guilds'] + " Servers")
                                    # await client.change_presence(status=discord.Status.online, activity=activity)
                                    # fnbfunctions.write_metrics(metrics)
                            else:
                                await message.channel.send('Scanning already enabled. Type `' + prefix + ' disable` to disable FortniteBlocker for this Server.')
                else:
                    await message.channel.send('Only the Server Owner is permitted to use this command!')
            

    
client = MyClient()
client.run(token)