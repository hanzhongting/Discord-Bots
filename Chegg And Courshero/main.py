#Coursehero Document Unlocker Bot
#Author: Nikola Gavric

from config import *
from functions import *

#Discord configs
botPrefix = "."
Client = discord.Client()
intents = discord.Intents.default()
intents.members = True
client = Bot(command_prefix=botPrefix, intents=intents)
client.remove_command('help')

#Proxy
proxy = 'http://185.250.39.235:8754'
proxy_auth = aiohttp.BasicAuth('esgnzoky', '0u3n43hw5toj')

#print when bot is launched
@client.event
async def on_ready():
    print("Discord.py Version: " + str(discord.__version__))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    autoUploadCoursehero.start()

#Check for admin privileges
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, notAdmin):
        embed = (discord.Embed(title="Missing Permissions", description="Sorry, you are not authorized to use this command.", color=0x78CFF5))
        embed.set_footer(text="Coursehero Bot")
        await ctx.send(embed=embed)
    elif isinstance(error, CommandNotFound) is False:
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

#Coursehero automatic document uploader
@tasks.loop(count=None, minutes=120, reconnect=True)
async def autoUploadCoursehero():
    for account in courseheroHeaderList:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.coursehero.com/api/v1/users/unlocks/uploads/', headers=account) as resp:
                unlocksJSON = await resp.json(content_type=None)

        unlocksRemaining = unlocksJSON['unlocks_remaining']
        if unlocksRemaining < 15:
            print(f"Coursehero Account: {account['Authorization']} has {unlocksRemaining} unlocks remaining.")
            async with aiohttp.ClientSession() as session:
                async with session.get('https://www.coursehero.com/api/v1/users/uploads/?dashboardBucket=1&limit=40&offset=0&filterVaccineTags=true', headers=account) as resp:
                    uploadHistory = await resp.json(content_type=None)
            numOfPreviouslyUploaded = len(uploadHistory['uploads'])
            if numOfPreviouslyUploaded > 0:
                dateOfOldestUpload = uploadHistory['uploads'][numOfPreviouslyUploaded-1]['doc_date']
                getDate = dt.datetime.strptime(dateOfOldestUpload, "%Y-%m-%d %H:%M:%S")
                now = dt.datetime.now()
                hourDifference = round(((now-getDate).total_seconds() / 3600), 2)
            else:
                hourDifference = 25
                print(f"No upload history on account: {account['Authorization']}")

            if hourDifference > 24.5:
                print(f"Starting upload for account: {account['Authorization']}")
                for currentFile in range(40):
                    print(f"On file: {currentFile + 1}")
                    fileHolder = io.BytesIO()
                    document = Document()
                    fileName = filenameGenerator()['name']
                    fileTopic = filenameGenerator()['courseType']
                    deepaiKeys = ['5247d513-b8c3-4f21-8bb0-007fb50f42f2', 'b619596e-ae76-491f-b596-3859134940ab']
                    apiKey = random.choice(deepaiKeys)
                    for i in range(3):
                        newFileTopic = random.choice(fileTopics)
                        async with aiohttp.ClientSession() as session:
                            async with session.post("https://api.deepai.org/api/text-generator", headers={'api-key': apiKey}, data={'text': newFileTopic}) as sendfile:
                                r = await sendfile.json(content_type=None)
                        paragraph = document.add_paragraph(r['output'])
                    document.save(fileHolder)
                    channel = client.get_channel(949392206970646568)
                    fileHolder.seek(0)
                    fileNameAndExtention = "{}.docx".format(fileName)
                    fileMsg = await channel.send(file=discord.File(fileHolder, filename=fileNameAndExtention))
                    fileLink = fileMsg.attachments[0].url
                    metadata = json.dumps({"submitted":True,"client_id":"ab7d6ad4328c376c6fa84cb2d885b929","title": fileName, "doctype":"Notes", "course_id":14580711, "category_tags":[]})

                    data = {
                        "data": metadata,
                        "method": "filepicker",
                        "filepicker_url": fileLink,
                        "filepicker_filename": fileNameAndExtention
                    }

                    async with aiohttp.ClientSession() as sendFile:
                    #async with httpx.AsyncClient() as sendFile:
                        response = await sendFile.post('https://www.coursehero.com/api/v1/uploads/', headers=account, json=data)
                        if response.status_code != 200:
                            print(response.content)
                print(f"File uploading completed on {account['Authorization']}")
            else:
                hoursLeft = 25 - hourDifference
                print(f"{hoursLeft} hours left before upload on account: {account['Authorization']}")

#Help command
@client.command()
async def help(ctx):
    embed = (discord.Embed(title="Bot Help", color=0x10226D))
    embed.set_author(name=ctx.author, icon_url=ctx.message.author.avatar_url)
    embed.add_field(name=".ch ``link``",value="Unlock a CH document.", inline=False)
    embed.set_footer(text="Coursehero Bot")
    await ctx.send(embed=embed)

#Document unlock command
@client.command(aliases=['coursehero'])
async def ch(ctx, *, unlockUrl=None):
    #Check if user has premium role
    role = discord.utils.get(ctx.guild.roles, name='premium')
    await ctx.channel.set_permissions(role, view_channel=True, send_messages=True, read_messages=True,read_message_history=True)

    if unlockUrl is None:
        embed = (discord.Embed(title="No URL Provided", description="<@!{}> Please provide a CH document link to unlock.".format(ctx.author.id), color=0xFFBC33))
        await ctx.send(embed=embed)
    else:
        searchDocId = re.search('file/(.+?)/', unlockUrl)
        if searchDocId and "https://www.coursehero.com" in unlockUrl:
            embed = (discord.Embed(title="Unlocking your Document | {}".format(ctx.author), description="<a:loading:915444710196260885> Please wait...", color=0x10226D))
            embed.set_footer(text="Coursehero Bot")
            msg = await ctx.send("<@!{}>".format(ctx.author.id), embed=embed)

            availableAccounts = []
            for account in courseheroHeaderList:
                async with aiohttp.ClientSession() as session:
                    async with session.get('https://www.coursehero.com/api/v1/users/unlocks/uploads/', headers=account) as resp:
                        unlocksJSON = await resp.json(content_type=None)
                try:
                    if unlocksJSON['unlocks_remaining'] > 0:
                        availableAccounts.append(account)
                except:
                    pass
            if len(availableAccounts) > 0:
                courseheroAccount = random.choice(availableAccounts)

            documentID = searchDocId.group(1)
            async with aiohttp.ClientSession() as session:
                #Search for document on courshero api
                async with session.get("https://www.coursehero.com/api/v1/documents/{}/".format(documentID), headers=courseheroAccount) as resp:
                    if resp.status == 200:
                        documentJSON = await resp.json(content_type=None)
                        documentID = documentJSON['db_filename']
                        documentName = documentJSON['title']
                        documentThumbnail = documentJSON['thumbnail']
                        documentCHURL = documentJSON['resource_url']
                        embed = (discord.Embed(title="Unlocking {}".format(documentName), description="<a:loading:915444710196260885> Please wait...", color=0x10226D))
                        embed.set_author(name=ctx.author, icon_url=ctx.message.author.avatar_url)
                        embed.set_thumbnail(url=documentThumbnail)
                        embed.set_footer(text="Coursehero Bot")
                        await msg.edit(embed=embed)

                        #Unlock doc
                        async with aiohttp.ClientSession() as session:
                            async with session.post("https://www.coursehero.com/api/v1/users/unlocks/content/document/id/{}/".format(documentID), headers=courseheroAccount) as resp:
                                unlockDoc = await resp.json(content_type=None)

                        async with aiohttp.ClientSession() as session:
                            async with session.get("https://www.coursehero.com/api/v1/documents/download/{}/".format(documentID), headers=courseheroAccount) as resp:
                                if resp.status == 200:
                                    extension = mimetypes.guess_extension(resp.headers['content-type'])
                                    if extension == ".pdf":
                                        try:
                                            content = await resp.content.read()
                                            documentContent = removeWatermark(content)
                                        except:
                                            documentContent = resp.content
                                    else:
                                        documentContent = resp.content
                                    documentFile = '{}{}'.format(documentName, extension)

                                    #Create data to send to server
                                    contentType = resp.headers['content-type']
                                    data = aiohttp.FormData()
                                    data.add_field('file', documentContent,
                                                   filename=documentFile,
                                                   content_type=contentType)


                                    #Upload document data to my server
                                    async with session.post("https://NidzoSiasky.nidzoball.repl.co/upload", data=data) as sendfile:
                                    #Get link for document on server
                                      filelink=await sendfile.text()
                                      print(filelink)

                                    #Send document link from server to user
                                    embed = (discord.Embed(title="{} Unlocked".format(documentName), description="[CH URL]({})".format(documentCHURL), color=0x51C994))
                                    embed.set_author(name=ctx.author, icon_url=ctx.message.author.avatar_url)
                                    embed.set_thumbnail(url=documentThumbnail)
                                    embed.add_field(name="Files :white_check_mark:", value="[Download]({})".format(filelink), inline=False)
                                    embed.set_footer(text="Coursehero Bot")
                                    await msg.edit(embed=embed)
                                    #await msg.channel.id.send(embed=embed)
                                else:
                                    embed = (discord.Embed(title="Error Unlocking Document", description="<@!{}> There was an error trying to unlock this document.".format(ctx.author.id), color=0xFFBC33))
                                    await msg.edit(embed=embed)
                    else:
                        embed = (discord.Embed(title="Error Unlocking Document", description="<@!{}> There was an error trying to unlock this document.".format(ctx.author.id), color=0xFFBC33))
                        await msg.edit(embed=embed)
        #Courshero Tutor Problems
        elif "https://www.coursehero.com/tutors-problems/" in unlockUrl:
            documentID = re.findall("/(.+?)-.*?/", unlockUrl)[1]
            embed = (discord.Embed(title="Unlocking your Tutor Question", description="<a:loading:915444710196260885> Please wait...", color=0x10226D))
            embed.set_author(name=ctx.author, icon_url=ctx.message.author.avatar_url)
            embed.set_footer(text="Coursehero Bot")
            msg = await ctx.send("<@!{}>".format(ctx.author.id), embed=embed)

            availableAccounts = []
            for account in courseheroHeaderList:
                async with aiohttp.ClientSession() as session:
                    async with session.get('https://www.coursehero.com/api/v1/users/unlocks/uploads/', headers=account) as resp:
                        unlocksJSON = await resp.json(content_type=None)
                try:
                    if unlocksJSON['unlocks_remaining'] > 0:
                        availableAccounts.append(account)
                except:
                    pass
            if len(availableAccounts) > 0:
                courseheroAccount = random.choice(availableAccounts)

            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.coursehero.com/api/v1/questions/{}/".format(documentID), headers=courseheroAccount) as resp:
                    if resp.status == 200:
                        documentCheck = await resp.json(content_type=None)
                        if documentCheck['question']['derived_question_status'] != "Cancelled" or documentCheck['question']['derived_question_status'] != "Requires Edit":
                            async with aiohttp.ClientSession() as session:
                                async with session.post("https://www.coursehero.com/api/v1/users/unlocks/content/question/id/{}/".format(documentID), headers=courseheroAccount) as resp:
                                    unlockTutorQ = await resp.json(content_type=None)
                            async with aiohttp.ClientSession() as session:
                                async with session.get("https://www.coursehero.com/api/v1/questions/{}/".format(documentID), headers=courseheroAccount) as resp:
                                    if resp.status == 200:
                                        getDocument = await resp.json(content_type=None)
                                        answer = None
                                        for thread in getDocument['threads']:
                                            if thread['type'] == "question":
                                                question = thread['display_text'].replace("\\", '')
                                                questionAttachmentHTML = ""
                                                if len(thread['attachment']) > 0:
                                                    questionID = thread['question_id']
                                                    for attachment in thread['attachment']:
                                                        attachmentID = attachment['question_attachment_id']
                                                        attachmentFileName = attachment['users_filename']
                                                        async with aiohttp.ClientSession() as session:
                                                            async with session.get("https://www.coursehero.com/pdf/attachment/{aID}/?question_id={qID}".format(aID=attachmentID, qID=questionID), headers=courseheroAccount) as resp:
                                                                if resp.status == 200:
                                                                    extension = mimetypes.guess_extension(resp.headers['content-type'])
                                                                    documentFile = 'attachment{}'.format(extension)
                                                                    documentContent = resp.content
                                                                    contentType = resp.headers['content-type']
                                                                    data = aiohttp.FormData()
                                                                    data.add_field('file', documentContent,
                                                                                   filename=documentFile,
                                                                                   content_type=contentType)
                                                                    async with aiohttp.ClientSession() as session:
                                                                        async with session.post("https://NidzoSiasky.nidzoball.repl.co/upload", data=data) as sendfile:
                                                                            filelink = await sendfile.text()
                                                                            #siaskyJSON = await sendfile.json(content_type=None)
                                                                    #print(siaskyJSON)
                                                                    #attachmentLink = 'https://NidzoSiasky.nidzoball.repl.co/{}'.format(siaskyJSON['skylink'])
                                                        questionAttachmentHTML += '<form action={} method="get" target="_blank"><button class="btn"><i class="fa fa-download"></i> Download {}</button></form>'.format(filelink, attachmentFileName)
                                            elif thread['type'] == "answer":
                                                answer = thread['display_text'].replace("\\", '')
                                                answerAttachmentHTML = ""
                                                if len(thread['attachment']) > 0:
                                                    questionID = thread['question_id']
                                                    for attachment in thread['attachment']:
                                                        attachmentID = attachment['question_attachment_id']
                                                        attachmentFileName = attachment['users_filename']
                                                        async with aiohttp.ClientSession() as session:
                                                            async with session.get("https://www.coursehero.com/pdf/attachment/{aID}/?question_id={qID}".format(aID=attachmentID, qID=questionID), headers=courseheroAccount) as resp:
                                                                if resp.status == 200:
                                                                    extension = mimetypes.guess_extension(resp.headers['content-type'])
                                                                    documentFile = 'attachment{}'.format(extension)
                                                                    documentContent = resp.content
                                                                    contentType = resp.headers['content-type']
                                                                    data = aiohttp.FormData()
                                                                    data.add_field('file', documentContent,
                                                                                   filename=documentFile,
                                                                                   content_type=contentType)
                                                                    async with aiohttp.ClientSession() as session:
                                                                        async with session.post("https://NidzoSiasky.nidzoball.repl.co/upload", data=data) as sendfile:
                                                                            filelink = await sendfile.text()
                                                                            #siaskyJSON = await sendfile.json(content_type=None)
                                                                    #print(siaskyJSON)
                                                                    #attachmentLink = 'https://NidzoSiasky.nidzoball.repl.co/{}'.format(siaskyJSON['skylink'])
                                                        answerAttachmentHTML += '<form action={} method="get" target="_blank"><button class="btn"><i class="fa fa-download"></i> Download {}</button></form>'.format(filelink, attachmentFileName)

                                        if answer is not None:
                                            startingHTML = "<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'><link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'><style>.collapsible {  background-color: #777;  color: white;  cursor: pointer;  padding: 18px;  width: 100%;  border: none;  text-align: left;  outline: none;  font-size: 15px;}.active, .collapsible:hover {  background-color: #555;}.content {  padding: 0 18px;  display: none;  overflow: hidden;  background-color: #f1f1f1;}.btn {  background-color: DodgerBlue;  border: none;  color: white;  padding: 12px 30px;  cursor: pointer;  font-size: 20px;}.btn:hover {  background-color: RoyalBlue;}</style></head><body><h2>Hero Reborn Tutor Question</h2><p>Question:</p><button type='button' class='collapsible'>Open Question</button><div class='content'>"
                                            answerHTML= "</div><p>Answer & Explaination</p><button type='button' class='collapsible'>Open Answer</button><div class='content'>"
                                            endingHTML = "</div><script>var coll = document.getElementsByClassName('collapsible');var i;for (i = 0; i < coll.length; i++) {  coll[i].addEventListener('click', function() {    this.classList.toggle('active');    var content = this.nextElementSibling;    if (content.style.display === 'block') {      content.style.display = 'none';    } else {      content.style.display = 'block';    }  });}</script></body></html>"
                                            html = startingHTML + question + questionAttachmentHTML + answerHTML + answer + answerAttachmentHTML + endingHTML

                                            data = aiohttp.FormData()
                                            data.add_field('file', html,
                                                           filename='file.html',
                                                           content_type="text/html; charset=utf-8")
                                            async with aiohttp.ClientSession() as session:
                                                async with session.post("https://NidzoSiasky.nidzoball.repl.co/upload", data=data) as sendfile:
                                                    filelink=await sendfile.text()
                                                    #siaskyJSON = await sendfile.json(content_type=None)
                                            #siaskyLink = "https://NidzoSiasky.nidzoball.repl.co/{}".format(siaskyJSON['skylink'])
                                            embed = (discord.Embed(title="Tutor Question Unlocked", description="[CH URL]({})".format(getDocument['question']['resource_url']), color=0x51C994))
                                            embed.set_author(name=ctx.author, icon_url=ctx.message.author.avatar_url)
                                            embed.add_field(name="Files :white_check_mark:", value="[View in Browser]({})".format(filelink), inline=False)
                                            embed.set_footer(text="Coursehero Bot")
                                            await msg.edit(embed=embed)
                                        else:
                                            embed = (discord.Embed(title="No Answer", description="<@!{}> This tutor question hasn't been answered yet.".format(ctx.author.id), color=0xFFBC33))
                                            embed.set_footer(text="Coursehero Bot")
                                            await msg.edit(embed=embed)
                        else:
                            embed = (discord.Embed(title="No Answer", description="<@!{}> This tutor question hasn't been answered yet. No credit was deducted.".format(ctx.author.id), color=0xFFBC33))
                            embed.set_footer(text="Coursehero Bot")
                            await msg.edit(embed=embed)
                    else:
                        embed = (discord.Embed(title="Error Unlocking Document", description="<@!{}> There was an error trying to unlock this document. Your credits have not been deducted. Please create a ticket or message Spike#5052 to report this issue.".format(ctx.author.id), color=0xFFBC33))
                        embed.set_author(name=ctx.author, icon_url=ctx.message.author.avatar_url)
                        await msg.edit(embed=embed)
        else:
            embed = (discord.Embed(title="Invalid URL", description="<@!{}> Make sure your Coursehero URL is formatted correctly.".format(ctx.author.id), color=0xFFBC33))
            embed.set_author(name=ctx.author, icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)

#Check how many unnlocks are left on all courshero vaccounts
@client.command()
@adminPrivileges()
async def botstats(ctx):
    totalUnlocks = 0
    description_message = "**Coursehero Accounts**\n"
    for account in courseheroHeaderList:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.coursehero.com/api/v1/users/details/', headers=account) as resp:
                accountJSON = await resp.json(content_type=None)
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.coursehero.com/api/v1/users/unlocks/uploads/', headers=account) as resp:
                unlocksJSON = await resp.json(content_type=None)

        try:
            email = accountJSON['email']
            unlocksRemaining = unlocksJSON['unlocks_remaining']
            description_message += f"■ {email}: {unlocksRemaining} unlocks\n"
            totalUnlocks += unlocksRemaining
        except:
            print(f"Issue with account: {account['Authorization']}")
    description_message  += f"Total Coursehero Unlocks: {totalUnlocks}\n"
    description_message  += "**Bot Tasks**\n"

    autoCourseheroUploaderStatus = autoUploadCoursehero.is_running()
    if autoCourseheroUploaderStatus is True:
        description_message += "Auto Coursehero Uploader: **Active**\n"
    else:
        description_message += "Auto Coursehero Uploader: **Failed!**\n"

    embed = (discord.Embed(title=f"{botName} Admin Panel", description=description_message, color=0x38389A))
    await ctx.send(embed=embed)

#Command to check when docum ents were last uploaded on all accounts
@client.command()
@adminPrivileges()
async def lastupload(ctx):
    description_message = "Coursehero Accounts\n"
    for account in courseheroHeaderList:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.coursehero.com/api/v1/users/details/', headers=account) as resp:
                accountJSON = await resp.json(content_type=None)
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.coursehero.com/api/v1/users/unlocks/uploads/', headers=account) as resp:
                unlocksJSON = await resp.json(content_type=None)

        email = accountJSON['email']
        unlocksRemaining = unlocksJSON['unlocks_remaining']

        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.coursehero.com/api/v1/users/uploads/?dashboardBucket=1&limit=40&offset=0&filterVaccineTags=true', headers=account) as resp:
                uploadHistory = await resp.json(content_type=None)
        numOfPreviouslyUploaded = len(uploadHistory['uploads'])
        if numOfPreviouslyUploaded > 0:
            dateOfOldestUpload = uploadHistory['uploads'][numOfPreviouslyUploaded-1]['doc_date']
            getDate = dt.datetime.strptime(dateOfOldestUpload, "%Y-%m-%d %H:%M:%S")
            now = dt.datetime.now()
            hourDifference = round(((now-getDate).total_seconds() / 3600), 2)
        description_message += f"■ {email}: {25 - hourDifference} hours left\n"

    embed = (discord.Embed(title=f"{botName} Admin Panel", description=description_message, color=0x38389A))
    await ctx.send(embed=embed)



for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        name = file[:-3]
        client.load_extension(f"cogs.{name}")


client.run(botToken)
