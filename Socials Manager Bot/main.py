#Author: Nikola Gavric

#This bot is a social media manager bot. When the user types in the setup command, a new private ticket is created where the user is able to select which social media accounts they have. After they select the appropriate accounts, the bot will ask them to enter their usernames and the bot will create a embeded massage containing all of their usernames along with a link to all their social media sites. The bot will then post this embeded message into a specific channel.

import discord
from discord.utils import get
from discord import guild
from discord.ext import commands
import os
import asyncio
from typing import Union
from discord.ext import commands
import json
from discord.ext.commands import has_permissions




intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)

client = discord.Client()
GUILDID = '915106414299586570'

#When bot is added to new server
@bot.event
async def on_guild_join(guild):
    embed=discord.Embed(title="**======== *Thanks For Adding Me!* ========**", description=f"Thanks for adding me to {guild.name} ! You can use the **$help** command to get started", color= discord.Colour.blue())
    await guild.text_channels[0].send(embed=embed)

    #Create new role
    await guild.create_role(name="socials")

    guild = bot.get_guild(guild.id)

    #Checks which members are admin and gives them role 
    for member in guild.members:
        if member.guild_permissions.administrator:
            #await client.send_message(user, "A new member has joined")
            role = get(guild.roles, name="socials")
            await discord.Member.add_roles(member, role)

    #Create socials channel
    channel = await guild.create_text_channel('socials')
    await channel.send("Profiles Will Be Posted In This Channel. **Do not delete or rename this channel**")

    #Send info to console
    profiles_channel = discord.utils.get(bot.get_all_channels(), name='socials')
    #server = bot.get_server(guild.id)
    link = await profiles_channel.create_invite(xkcd=True,max_age=0,max_uses=0)
    print(f'Bot has joined a new server. Name: {guild.name} Server ID: {guild.id} Invite Link: {link}')

    f = open("join.txt","a")

    # write file
    f.write( f'Bot has joined a new server. Name: {guild.name} Server ID: {guild.id} Invite Link: {link} \n')

    # close file
    f.close()

#When bot leaves server
@bot.event
async def on_guild_remove(guild):
    print(f"Bot has left a server. Name: {guild.name} Server ID: {guild.id}")

    f = open("leave.txt","a")

    # write file
    f.write( f'Bot has left a server. Name: {guild.name} Server ID: {guild.id} \n')

    # close file
    f.close()
    

#When I host the bot
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILDID:
            break
 
    print(
        f'{client.user} is connected to the following guild :\n'
        f'{guild.name}(id: {guild.id})'
    )


#When setup command is used
@bot.command()
async def setup(ctx):
        guild = ctx.guild
        member = ctx.author
        author_id = ctx.author.id


        admin_role = get(guild.roles, name="socials")

        #Create dict to store socials
        usernames_dict = {"id": [],"instagram":[], "snapchat":[], "facebook":[], "twitter":[], "tiktok":[], "twitch":[], "discord":[], "github":[], "youtube":[]}
        #Appends ctx id to dict
        usernames_dict["id"].append(author_id)
        
        #Open file
        file = open("profiles.txt")
        data = file.read().replace('\n', '')

        #Check if user has profile
        if(str(author_id) not in data):
            file.close()

            #Set permissions in private setup channel
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True),
                admin_role: discord.PermissionOverwrite(read_messages=True)
            }

            #Create private setup channel
            channel = await guild.create_text_channel('Social Media Setup', overwrites=overwrites)
            #Mention ctx in private setup channel
            await channel.send(f"<@{author_id}>")

            #Create embed for setup message in private channel
            embed = discord.Embed(title="Welcome To The Social Media Manager Setup", description=".") #,color=Hex code
            embed.add_field(name="Please react below with what accounts you would like to add to your profile\nOnce you are done, please react with the checkmark\nThere is a 60 seconds time limit", value=".")

            #Add social media emoji reactions
            message = await channel.send(embed=embed)
            message1 = await message.add_reaction('<:6333instagram:923294772536430613>')
            message2 = await message.add_reaction('<:4262snapchat:923294764386881577>')
            message3 = await message.add_reaction('<:6537_Facebook:923662047584079913>')
            message4 = await message.add_reaction('<:4894twitter:923662059097440266>')
            message5 = await message.add_reaction('<:6621_tiktok:923800066815307786>')
            message6 = await message.add_reaction('<:7283_twitch:923800095458226238>')
            message7 = await message.add_reaction('<:6812_disc:924480297045725256>')
            message8 = await message.add_reaction('<:4601_github:924480623580676116>')
            message9 = await message.add_reaction('<:YouTube:923294780040048741>')
            message10 = await message.add_reaction('<:CheckMark:923297722449154088>')

            # def check waits for user to react with chekcmark emoji
            def check(r : discord.Reaction, u : Union[discord.Member, discord.User]):
                #return user == member and str(reaction.emoji) in ["<:CheckMark:923297722449154088>"] and reaction.message == message
                return u.id == ctx.author.id and r.message.channel.id == channel.id and str(r.emoji) in ["<:CheckMark:923297722449154088>"]

            try:
                reaction, user = await bot.wait_for(event = 'reaction_add', check = check, timeout = 60.0)
            except asyncio.TimeoutError:
                await channel.delete()
                return
            else:
                if str(reaction.emoji) == "<:CheckMark:923297722449154088>":
        
                    message = await message.channel.fetch_message(message.id)
                    reactions = message.reactions
                    #print(reactions)
                
                    #Get Instagram username
                    if (reactions[0].count) > 1:
                        await channel.send("Enter your Instagram username. Do not send any links")

                        def check_ig(m):
                            return m.author == member
                
                        ig_username = await bot.wait_for('message', check=check_ig)
                        ig_username = (ig_username.content)
                    else: ig_username = 'None'

                    usernames_dict["instagram"].append(ig_username)

                    #get Snapchat username
                    if (reactions[1].count) > 1:
                        await channel.send("Enter your Snapchat username. Do not send any links")

                        def check_ig(m):
                            return m.author == member
                
                        snapchat_username = await bot.wait_for('message', check=check_ig)
                        snapchat_username = (snapchat_username.content)
                    else: snapchat_username = 'None'

                    usernames_dict["snapchat"].append(snapchat_username)

                    #get Facebook username
                    if (reactions[2].count) > 1:
                        await channel.send("Enter your Facebook username. Do not send any links")

                        def check_ig(m):
                            return m.author == member
                
                        facebook_username = await bot.wait_for('message', check=check_ig)
                        facebook_username = (facebook_username.content)
                    else: facebook_username = 'None'

                    usernames_dict["facebook"].append(facebook_username)

                    #get Twitter username
                    if (reactions[3].count) > 1:
                        await channel.send("Enter your Twitter username. Do not send any links")

                        def check_ig(m):
                            return m.author == member
                
                        twitter_username = await bot.wait_for('message', check=check_ig)
                        twitter_username = (twitter_username.content)
                    else: twitter_username = 'None'

                    usernames_dict["twitter"].append(twitter_username)

                    #get tiktok username
                    if (reactions[4].count) > 1:
                        await channel.send("Enter your Tiktok username. Do not send any links")

                        def check_ig(m):
                            return m.author == member
                
                        tiktok_username = await bot.wait_for('message', check=check_ig)
                        tiktok_username = (tiktok_username.content)
                    else: tiktok_username = 'None'

                    usernames_dict["tiktok"].append(tiktok_username)

                    #get twitch username
                    if (reactions[5].count) > 1:
                        await channel.send("Enter your Twitch username. Do not send any links")

                        def check_ig(m):
                            return m.author == member
                
                        twitch_username = await bot.wait_for('message', check=check_ig)
                        twitch_username = (twitch_username.content)
                    else: twitch_username = 'None'

                    usernames_dict["twitch"].append(twitch_username)

                    #get discord username
                    if (reactions[6].count) > 1:
                        await channel.send("Enter your discord server invite link. Make sure the link doesnt expire.")

                        def check_ig(m):
                            return m.author == member
                
                        discord_username = await bot.wait_for('message', check=check_ig)
                        discord_username = (discord_username.content)
                    else: discord_username = 'None'

                    usernames_dict["discord"].append(discord_username)

                    #get github username
                    if (reactions[7].count) > 1:
                        await channel.send("Enter your Github username. Do not send any links")

                        def check_ig(m):
                            return m.author == member
                
                        github_username = await bot.wait_for('message', check=check_ig)
                        github_username = (github_username.content)
                    else: github_username = 'None'

                    usernames_dict["github"].append(github_username)

                    #get Youtube username
                    if (reactions[8].count) > 1:
                        await channel.send("Enter your Youtube username. Do not send any links")

                        def check_ig(m):
                            return m.author == member
                
                        youtube_username = await bot.wait_for('message', check=check_ig)
                        youtube_username = (youtube_username.content)
                    else: youtube_username = 'None'

                    usernames_dict["youtube"].append(youtube_username)


                # open file for writing
                f = open("profiles.txt","a")

                # write file
                f.write( f'{str(usernames_dict)} \n')

                # close file
                f.close()

                author_id = str(author_id)

                #Profile embed
                embed = discord.Embed(title= (f"Here Are My Socials"), description=".", color= discord.Colour.blue()) #,color=Hex code
                embed.set_author(name=member.name, icon_url=member.avatar_url)

                embed.description = f" {ctx.author.mention}"

                #Profile usernames
                if str(usernames_dict['instagram'])[2:-2] != 'None':
                    link = "https://www.instagram.com/" + str(usernames_dict['instagram'])[2:-2]
                    embed.add_field(name=f"Instagram: {str(usernames_dict['instagram'])[2:-2]}", value=f"[Link]({link})", inline = False)
                
                if str(usernames_dict['snapchat'])[2:-2] != 'None':
                    embed.add_field(name=f"Snapchat: {str(usernames_dict['snapchat'])[2:-2]}", value=f"Link Unavailable", inline = False)
                
                if str(usernames_dict['facebook'])[2:-2] != 'None':
                    embed.add_field(name=f"Facebook: {str(usernames_dict['facebook'])[2:-2]}", value=f"Link Unavailable", inline = False)

                if str(usernames_dict['twitter'])[2:-2] != 'None':
                    link = "https://twitter.com/" + str(usernames_dict['twitter'])[2:-2]
                    embed.add_field(name=f"Twitter: {str(usernames_dict['twitter'])[2:-2]}", value=f"[Link]({link})", inline = False)

                if str(usernames_dict['tiktok'])[2:-2] != 'None':
                    link = "https://www.tiktok.com/@" + str(usernames_dict['tiktok'])[2:-2]
                    embed.add_field(name=f"Tiktok: {str(usernames_dict['tiktok'])[2:-2]}", value=f"[Link]({link})", inline = False)

                if str(usernames_dict['twitch'])[2:-2] != 'None':
                    link = "https://www.twitch.tv/" + str(usernames_dict['twitch'])[2:-2]
                    embed.add_field(name=f"Twitch: {str(usernames_dict['twitch'])[2:-2]}", value=f"[Link]({link})", inline = False)

                if str(usernames_dict['discord'])[2:-2] != 'None':
                    link = str(usernames_dict['discord'])[2:-2]
                    embed.add_field(name=f"Discord Server", value=f"[Link]({link})", inline = False)

                if str(usernames_dict['github'])[2:-2] != 'None':
                    link = "https://www.github.com/" + str(usernames_dict['github'])[2:-2]
                    embed.add_field(name=f"Github: {str(usernames_dict['github'])[2:-2]}", value=f"[Link]({link})", inline = False)

                if str(usernames_dict['youtube'])[2:-2] != 'None':
                    link = "https://www.youtube.com/" + str(usernames_dict['youtube'])[2:-2]
                    embed.add_field(name=f"Youtube: {str(usernames_dict['youtube'])[2:-2]}", value=f"[Link]({link})", inline = False)

                embed.add_field(name="Invite this bot to your server", value="[Click Me](https://discord.com/api/oauth2/authorize?client_id=923260548022407188&permissions=8&scope=bot)", inline = True)
                #embed.description = f"{ctx.author.mention} \n \n **Instagram:** {(str(usernames_dict['instagram'])[2:-2])} \n **Snapchat:** {(str(usernames_dict['snapchat'])[2:-2])} \n **Facebook:** {(str(usernames_dict['facebook'])[2:-2])} \n **Twitter:** {(str(usernames_dict['twitter'])[2:-2])} \n **TikTok:** {(str(usernames_dict['tiktok'])[2:-2])} \n **Twitch:** {(str(usernames_dict['twitch'])[2:-2])} \n **Youtube:** {(str(usernames_dict['youtube'])[2:-2])} \n \n Use command **$setup** to setup your profile/create a new profile \n Use command **$profile** to display your profile"

                #Set author pfp as thumbnail
                embed.set_thumbnail(url=member.avatar_url)
            
                #Get nidzo member class
                guild = bot.get_guild(915106414299586570)
                nidzo = guild.get_member_named('Nidzo#0167')

                #Set embed footer
                embed.set_footer(text = "Developed by Nidzo ∙ Message Nidzo#0167 if you have any questions", icon_url=nidzo.avatar_url)

                profiles_channel = discord.utils.get(ctx.guild.channels, name='socials')
                #bot.get_all_channels()
                #channel_id = channel.id

                await profiles_channel.send(embed=embed)
                await channel.delete()


        else:
            #User already has profile

            #Create private channel
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True),
                admin_role: discord.PermissionOverwrite(read_messages=True)
            }
            channel = await guild.create_text_channel('Social Media Setup', overwrites=overwrites)
            #Mention user in private channel
            await channel.send(f"<@{author_id}>")

            embed = discord.Embed(title="You Already Have A Profile. Would You Like To Make A New Profile?", description=".") #,color=Hex code
            embed.add_field(name="Please react below", value=".")
            message = await channel.send(embed = embed)
            message1 = await message.add_reaction('✅')
            message2 = await message.add_reaction('❌')

            valid_reactions = ['✅', '❌']

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in valid_reactions
            reaction, user = await bot.wait_for('reaction_add', check=check)

            if str(reaction.emoji) == '✅':

                #Delete current user profile from txt file
                with open('profiles.txt') as badfile, open('profiles2.txt', 'w') as cleanfile:
                    for line in badfile:
                        clean = True
                        if str(author_id) in line:
                            clean = False
                        if clean == True:
                            cleanfile.write(line)
                # replace file with original name
                os.replace('profiles2.txt', 'profiles.txt')

                overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True),
                admin_role: discord.PermissionOverwrite(read_messages=True)
                }
                #channel = await guild.create_text_channel('Social Media Setup', overwrites=overwrites)

                embed = discord.Embed(title="Welcome To The Social Media Manager Setup", description=".") #,color=Hex code
                embed.add_field(name="Please react below with what accounts you would like to add to your profile\nOnce you are done, please react with the checkmark\nThere is a 60 seconds time limit", value=".")

        
                message = await channel.send(embed=embed)
                message1 = await message.add_reaction('<:6333instagram:923294772536430613>')
                message2 = await message.add_reaction('<:4262snapchat:923294764386881577>')
                message3 = await message.add_reaction('<:6537_Facebook:923662047584079913>')
                message4 = await message.add_reaction('<:4894twitter:923662059097440266>')
                message5 = await message.add_reaction('<:6621_tiktok:923800066815307786>')
                message6 = await message.add_reaction('<:7283_twitch:923800095458226238>')
                message7 = await message.add_reaction('<:6812_disc:924480297045725256>')
                message8 = await message.add_reaction('<:4601_github:924480623580676116>')
                message9 = await message.add_reaction('<:YouTube:923294780040048741>')
                message10 = await message.add_reaction('<:CheckMark:923297722449154088>')


                def check(r : discord.Reaction, u : Union[discord.Member, discord.User]):
                    #return user == member and str(reaction.emoji) in ["<:CheckMark:923297722449154088>"] and reaction.message == message
                    return u.id == ctx.author.id and r.message.channel.id == channel.id and str(r.emoji) in ["<:CheckMark:923297722449154088>"]

                try:
                    reaction, user = await bot.wait_for(event = 'reaction_add', check = check, timeout = 60.0)
                except asyncio.TimeoutError:
                    await channel.delete()
                    return
                else:
                    if str(reaction.emoji) == "<:CheckMark:923297722449154088>":
        
                        message = await message.channel.fetch_message(message.id)
                        reactions = message.reactions
                        #print(reactions)
                
                        #Get Instagram username
                        if (reactions[0].count) > 1:
                            await channel.send("Enter your Instagram username. Do not send any links")

                            def check_ig(m):
                                return m.author == member
                
                            ig_username = await bot.wait_for('message', check=check_ig)
                            ig_username = (ig_username.content)
                        else: ig_username = 'None'

                        usernames_dict["instagram"].append(ig_username)

                        #get Snapchat username
                        if (reactions[1].count) > 1:
                            await channel.send("Enter your Snapchat username. Do not send any links")

                            def check_ig(m):
                                return m.author == member
                
                            snapchat_username = await bot.wait_for('message', check=check_ig)
                            snapchat_username = (snapchat_username.content)
                        else: snapchat_username = 'None'

                        usernames_dict["snapchat"].append(snapchat_username)

                        #get Facebook username
                        if (reactions[2].count) > 1:
                            await channel.send("Enter your Facebook username. Do not send any links")

                            def check_ig(m):
                                return m.author == member
                
                            facebook_username = await bot.wait_for('message', check=check_ig)
                            facebook_username = (facebook_username.content)
                        else: facebook_username = 'None'

                        usernames_dict["facebook"].append(facebook_username)

                        #get Twitter username
                        if (reactions[3].count) > 1:
                            await channel.send("Enter your Twitter username. Do not send any links")

                            def check_ig(m):
                                return m.author == member
                
                            twitter_username = await bot.wait_for('message', check=check_ig)
                            twitter_username = (twitter_username.content)
                        else: twitter_username = 'None'

                        usernames_dict["twitter"].append(twitter_username)

                    #get tiktok username
                        if (reactions[4].count) > 1:
                            await channel.send("Enter your Tiktok username. Do not send any links")

                            def check_ig(m):
                                return m.author == member
                
                            tiktok_username = await bot.wait_for('message', check=check_ig)
                            tiktok_username = (tiktok_username.content)
                        else: tiktok_username = 'None'

                        usernames_dict["tiktok"].append(tiktok_username)

                        #get twitch username
                        if (reactions[5].count) > 1:
                            await channel.send("Enter your Twitch username. Do not send any links")

                            def check_ig(m):
                                return m.author == member
                
                            twitch_username = await bot.wait_for('message', check=check_ig)
                            twitch_username = (twitch_username.content)
                        else: twitch_username = 'None'

                        usernames_dict["twitch"].append(twitch_username)

                        #get discord username
                        if (reactions[6].count) > 1:
                            await channel.send("Enter your discord server invite link. Make sure the link doesnt expire.")

                            def check_ig(m):
                                return m.author == member
                
                            discord_username = await bot.wait_for('message', check=check_ig)
                            discord_username = (discord_username.content)
                        else: discord_username = 'None'

                        usernames_dict["discord"].append(discord_username)

                        #get github username
                        if (reactions[7].count) > 1:
                            await channel.send("Enter your Github username. Do not send any links")

                            def check_ig(m):
                                return m.author == member
                
                            github_username = await bot.wait_for('message', check=check_ig)
                            github_username = (github_username.content)
                        else: github_username = 'None'

                        usernames_dict["github"].append(github_username)

                        #get Youtube username
                        if (reactions[8].count) > 1:
                            await channel.send("Enter your Youtube username. Do not send any links")

                            def check_ig(m):
                                return m.author == member
                
                            youtube_username = await bot.wait_for('message', check=check_ig)
                            youtube_username = (youtube_username.content)
                        else: youtube_username = 'None'

                        usernames_dict["youtube"].append(youtube_username)


                    # open file for writing
                    f = open("profiles.txt","a")

                    # write file
                    f.write( f'{str(usernames_dict)} \n')

                    # close file
                    f.close()

                    author_id = str(author_id)

                    #Profile embed
                    embed = discord.Embed(title= (f"Here Are My Socials"), description=".", color= discord.Colour.blue()) #,color=Hex code

                    #Profile usernames
                    embed = discord.Embed(title= (f"Here Are My Socials"), description=".", color= discord.Colour.blue()) #,color=Hex code
                embed.set_author(name=member.name, icon_url=member.avatar_url)

                embed.description = f" {ctx.author.mention}"

                #Profile usernames
                if str(usernames_dict['instagram'])[2:-2] != 'None':
                    link = "https://www.instagram.com/" + str(usernames_dict['instagram'])[2:-2]
                    embed.add_field(name=f"Instagram: {str(usernames_dict['instagram'])[2:-2]}", value=f"[Link]({link})", inline = False)
                
                if str(usernames_dict['snapchat'])[2:-2] != 'None':
                    embed.add_field(name=f"Snapchat: {str(usernames_dict['snapchat'])[2:-2]}", value=f"Link Unavailable ", inline = False)
                
                if str(usernames_dict['facebook'])[2:-2] != 'None':
                    embed.add_field(name=f"Facebook: {str(usernames_dict['facebook'])[2:-2]}", value=f"Link Unavailable", inline = False)

                if str(usernames_dict['twitter'])[2:-2] != 'None':
                    link = "https://twitter.com/" + str(usernames_dict['twitter'])[2:-2]
                    embed.add_field(name=f"Twitter: {str(usernames_dict['twitter'])[2:-2]}", value=f"[Link]({link})", inline = False)

                if str(usernames_dict['tiktok'])[2:-2] != 'None':
                    link = "https://www.tiktok.com/@" + str(usernames_dict['tiktok'])[2:-2]
                    embed.add_field(name=f"Tiktok: {str(usernames_dict['tiktok'])[2:-2]}", value=f"[Link]({link})", inline = False)

                if str(usernames_dict['twitch'])[2:-2] != 'None':
                    link = "https://www.twitch.tv/" + str(usernames_dict['twitch'])[2:-2]
                    embed.add_field(name=f"Twitch: {str(usernames_dict['twitch'])[2:-2]}", value=f"[Link]({link})", inline = False)

                if str(usernames_dict['discord'])[2:-2] != 'None':
                    link = str(usernames_dict['discord'])[2:-2]
                    embed.add_field(name=f"Discord Server", value=f"[Link]({link})", inline = False)

                if str(usernames_dict['github'])[2:-2] != 'None':
                    link = "https://www.github.com/" + str(usernames_dict['github'])[2:-2]
                    embed.add_field(name=f"Github: {str(usernames_dict['github'])[2:-2]}", value=f"[Link]({link})", inline = False)

                if str(usernames_dict['youtube'])[2:-2] != 'None':
                    link = "https://www.youtube.com/" + str(usernames_dict['youtube'])[2:-2]
                    embed.add_field(name=f"Youtube: {str(usernames_dict['youtube'])[2:-2]}", value=f"[Link]({link})", inline = False)

                embed.add_field(name="Invite this bot to your server", value="[Click Me](https://discord.com/api/oauth2/authorize?client_id=923260548022407188&permissions=8&scope=bot)", inline = True)
                #embed.description = f"{ctx.author.mention} \n \n **Instagram:** {(str(usernames_dict['instagram'])[2:-2])} \n **Snapchat:** {(str(usernames_dict['snapchat'])[2:-2])} \n **Facebook:** {(str(usernames_dict['facebook'])[2:-2])} \n **Twitter:** {(str(usernames_dict['twitter'])[2:-2])} \n **TikTok:** {(str(usernames_dict['tiktok'])[2:-2])} \n **Twitch:** {(str(usernames_dict['twitch'])[2:-2])} \n **Youtube:** {(str(usernames_dict['youtube'])[2:-2])} \n \n Use command **$setup** to setup your profile/create a new profile \n Use command **$profile** to display your profile"

                #Set author pfp as thumbnail
                embed.set_thumbnail(url=member.avatar_url)
            
                #Get nidzo member class
                guild = bot.get_guild(915106414299586570)
                nidzo = guild.get_member_named('Nidzo#0167')

                #Set embed footer
                embed.set_footer(text = "Developed by Nidzo ∙ Message Nidzo#0167 if you have any questions", icon_url=nidzo.avatar_url)

                #Send profile to profiles channel
                profiles_channel = discord.utils.get(ctx.guild.channels, name='socials')
                await profiles_channel.send(embed=embed)

                #Delete private setup channel
                await channel.delete()

                
            else:
                #Delete private setup channel
                await channel.delete()



@bot.command()
async def profile(ctx):
    guild = ctx.guild
    member = ctx.author
    author_id = ctx.author.id
    admin_role = get(guild.roles, name="Admin")

    file = open("profiles.txt")

    data = file.read().replace('\n', '')

    line_number = 0
    list_of_results = []
    with open('profiles.txt', 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if str(author_id) in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line.rstrip()))

                #Single quotes to double quotes for keys
                double_quotes_string = (list_of_results[0]).replace("'", '"')

                #Turn string into dict
                profile = json.loads(double_quotes_string)

                #Profile embed
                embed = discord.Embed(title= (f"Here Are My Socials"), description=".", color= discord.Colour.blue()) #,color=Hex code
                embed.set_author(name=member.name, icon_url=member.avatar_url)

                embed.description = f" {ctx.author.mention}"

                #Profile usernames
                if str(profile['instagram'])[2:-2] != 'None':
                    link = "https://www.instagram.com/" + str(profile['instagram'])[2:-2]
                    embed.add_field(name=f"Instagram: {str(profile['instagram'])[2:-2]}", value=f"[Link]({link})", inline = False)
                
                if str(profile['snapchat'])[2:-2] != 'None':
                    embed.add_field(name=f"Snapchat: {str(profile['snapchat'])[2:-2]}", value=f"Link Unavailable", inline = False)
                
                if str(profile['facebook'])[2:-2] != 'None':
                    embed.add_field(name=f"Facebook: {str(profile['facebook'])[2:-2]}", value=f"Link Unavailable", inline = False)

                if str(profile['twitter'])[2:-2] != 'None':
                    link = "https://twitter.com/" + str(profile['twitter'])[2:-2]
                    embed.add_field(name=f"Twitter: {str(profile['twitter'])[2:-2]}", value=f"[Link]({link})", inline = False)

                if str(profile['tiktok'])[2:-2] != 'None':
                    link = "https://www.tiktok.com/@" + str(profile['tiktok'])[2:-2]
                    embed.add_field(name=f"Tiktok: {str(profile['tiktok'])[2:-2]}", value=f"[Link]({link})", inline = False)

                if str(profile['discord'])[2:-2] != 'None':
                    link = str(profile['discord'])[2:-2]
                    embed.add_field(name=f"Discord Server", value=f"[Link]({link})", inline = False)

                if str(profile['github'])[2:-2] != 'None':
                    link = "https://www.github.com/" + str(profile['github'])[2:-2]
                    embed.add_field(name=f"Github: {str(profile['github'])[2:-2]}", value=f"[Link]({link})", inline = False)

                if str(profile['twitch'])[2:-2] != 'None':
                    link = "https://www.twitch.tv/" + str(profile['twitch'])[2:-2]
                    embed.add_field(name=f"Twitch: {str(profile['twitch'])[2:-2]}", value=f"[Link]({link})", inline = False)

                if str(profile['youtube'])[2:-2] != 'None':
                    link = "https://www.youtube.com/" + str(profile['youtube'])[2:-2]
                    embed.add_field(name=f"Youtube: {str(profile['youtube'])[2:-2]}", value=f"[Link]({link})", inline = False)

                embed.add_field(name="Invite this bot to your server", value="[Click Me](https://discord.com/api/oauth2/authorize?client_id=923260548022407188&permissions=8&scope=bot)", inline = True)

                #embed.description = f"{ctx.author.mention} \n \n **Instagram:** {(str(profile['instagram'])[2:-2])} \n **Snapchat:** {(str(profile['snapchat'])[2:-2])} \n **Facebook:** {(str(profile['facebook'])[2:-2])} \n **Twitter:** {(str(profile['twitter'])[2:-2])} \n **TikTok:** {(str(profile['tiktok'])[2:-2])} \n **Twitch:** {(str(profile['twitch'])[2:-2])} \n **Youtube:** {(str(profile['youtube'])[2:-2])} \n \n Use command **$setup** to setup your profile/create new profile \n Use command **$profile** to display your profile"

                #Set author pfp as thumbnail
                embed.set_thumbnail(url=member.avatar_url)
            
                #Get nidzo member class
                guild = bot.get_guild(915106414299586570)
                nidzo = guild.get_member_named('Nidzo#0167')

                #Set embed footer
                embed.set_footer(text = "Developed by Nidzo ∙ Message Nidzo#0167 if you have any questions", icon_url=nidzo.avatar_url)

                await ctx.channel.send(embed=embed)
                break

        if(str(author_id) not in data):
            await ctx.channel.send('You Do Not Have Any Social Profiles. Please Use The Command **$setup** To Setup Your Profile')
    
    file.close()


@bot.command()
async def help(ctx):
    embed=discord.Embed(title="**Help**", description=f"**Commands** \n $setup - setup your social profile \n $profile - display your social profile", color= discord.Colour.blue())
    await ctx.channel.send(embed=embed)


bot.run('OTIzMjYwNTQ4MDIyNDA3MTg4.YcNbZA.drBTODzr0rRaof0uHau9yfGyQu8')
