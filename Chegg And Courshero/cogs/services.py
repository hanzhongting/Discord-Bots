#Chegg Answers Bot
#Author: Nikola Gavric

import discord
from discord.ext import commands
from functions import *
from config import *
from main import *

counter1 = 0

class Example(commands.Cog):
    def __init__(self, client):
        self.client = client

#Chegg if chegg link is sent to channel
    @commands.Cog.listener()
    async def on_message(self, message):
        link = message.content
        #When q&a type question is send to channel
        if "questions-and-answers" in link and "https://www.chegg.com" in link:
            role = discord.utils.get(message.guild.roles, name='premium')
            await message.channel.set_permissions(role, view_channel=True, send_messages=True, read_messages=True,read_message_history=True)
            global counter1
            counter1 += 1
            print(f"Chegg Unlock: {counter1}")

            #Send message when a chegg link is send to chennel
            embed = (discord.Embed(title="Unlocking your Cheg Q&A", description=f"Please wait while the bot unlocks your [link]({link}).", color=0xFF4B4B))
            embed.set_footer(text=f"{botName}")
            msg = await message.channel.send(f"<@!{message.author.id}>", embed=embed)

            #q&a header
            searchHeaders = {
                'Host': 'proxy.chegg.com',
                'content-type': 'application/json',
                'x-chegg-dfid': 'mobile|2E5D1C7F-12DE-47F7-9684-C4789A736017',
                'x-px-authorization': '3:1f3e61059e600bb97b0678e14bd77036624c56cfca1006502f983c83a4c72707:RIgF4y3JJO0BxLZWa+yiSP/vE78eH729zwZiD2ZDiIUOT6bQyIzrD51fK8RpdR+jFLFRWdkJGd3e9ps1VdKPXQ==:1000:l6Jsieu6m8/beUmSMCI1StN0t+w32Oy16bWxGM6fTS8WVWcjRGCK0yV7U0gMXR9wbO0F9rM5QTAMIGG0gLvyCSbrkaQWYW1yCWO9dEIpF1Qak+89E8iMR/bgx0JbVjpOTBdcnrJ41RwOtiZMS9C/mF6Qm3EE8LjbT/0TDEyJE0exi/pEcuWm/K82yJ+5qw1xNnZumnpwX7dmvx7BTSRmsw==',
                'accept': 'application/json',
                'authorization': 'Basic MFQxOE5HYmFsUURGYzBnWkh6b3ZwZVJkN0E1Y3BMQ3g6dnRnamFZa3Ric2p4OUFPUg==',
                'x-chegg-deviceid': '2ec9bb5465d4d28cf4c71de1bbe456dedf8713ac',
                'x-chegg-sessionid': 'A37EF7AC-EE88-4C4F-B9CB-7216519C77D5',
                'accept-language': 'en-CA;q=1.0',
                'x-adobe-mc-id': '00221641897576732531639057585934046896',
                'user-agent': 'CheggApp/4.4.1 (com.chegg.mobile.consumer; build:4.4.1.0; iOS 15.1.1) Alamofire/5.2.2',
                'x-chegg-auth-mfa-supported': 'true',
            }

            questionID = link.split("-")[-1].split("?")[0]
            if questionID[0] == "q":
                questionUUID = None

                searchQuery = {
                    "variables": {
                        "id": questionID[1:]
                    },
                    "operationName": "getQuestionUuidById"
                }
                async with aiohttp.ClientSession() as session:
                    async with session.post("https://proxy.chegg.com/mobile-study-bff/graphql", json=searchQuery, headers=searchHeaders) as resp:
                        queryResult = await resp.json()
                if queryResult['data']['getQuestionUuidById'] is None:
                    embed = (discord.Embed(title="Error Unlocking Cheg Q&A", description=f"<@!{message.author.id}> This Cheg question and answer cannot be found. Please create a ticket to report this issue.", color=0xFFBC33))
                    embed.set_footer(text=f"{botName}")
                    await msg.edit(embed=embed)
                else:
                    questionUUID = queryResult['data']['getQuestionUuidById']['uuid']
                    questionData = {
                      'id': 'getQuestionByUuid',
                      'operationName': 'getQuestionByUuid',
                      'variables': {
                          'questionUuid': questionUUID
                      }
                    }

                    accessToken = await accountCookies()
                    await asyncio.sleep(2)

                    questionHeaders = {
                        'Host': 'proxy.chegg.com',
                        'User-Agent': 'Chegg Study/12.8.1 (Linux; U; Android 8.1.0; LM-Q710.FGN Build/OPM1.171019.019)',
                        'authorization': 'Basic aGxEcFpBUEYwNW1xakFtZzdjcXRJS0xPaFVyeUI4cDE6dUJqemFrbXhHeDZXdHFBcg==',
                        'X-PX-AUTHORIZATION': '3:b4f2906f544db2aedaacef7cb9ffab65d8d4721344c115fb6f6d2e09baa3f0cf:WR+yrp1THDPVYbqksXrBkaFQkCeMrXsN3RaPPcG+sq+d6eRIPsWEsmhxMzEr88eZ5tU7Mhif5lGTD9NCKsTk3Q==:1000:ZLS3xqRvS46lwoskEch1EoGdt1+uw7sZyylJu/lsYyiUnBkB1WsvXSCWhpKE8K0jwCgpK150BV3StQCUZOgY+h0cmUEfz8p57c4Vm57mEXdmmCFvrfinGDKlVneK8tIojB4cO/QinKTfyc4H4cHcgYfZnjQTPXkQ8DCVMP/BmPzeO+SrkLJutgKVUpwQzD/ksnldfj5+j9uPWDmXEWEfaw==',
                        'X-PX-BYPASS-REASON': 'bad%20URL',
                        'Content-Type': 'application/json',
                        'x-chegg-auth-mfa-supported': "true",
                        'X-CHEGG-DEVICEID': '98ea5768de4e1d0b4d9f1fe407b54f9a67dd2162',
                        'Connection': 'keep-alive',
                        'Accept-Language': 'en-CA;q=1.0',
                        'accept-encoding': 'gzip',
                        'access_token': accessToken
                    }

                    #Bypass Chegg login and extract answer
                    async with httpx.AsyncClient() as resp:
                        response = await resp.post("https://proxy.chegg.com/mobile-study-bff/graphql/", json=questionData, headers=questionHeaders)
                        try:
                            js = response.json()
                        except:
                            print(response.text)
                            embed = (discord.Embed(title="Cheg Server Issues", description=f"<@!{message.author.id}> There was an error trying to unlock [this Q&A]({link}) as Cheg seems to be having some server problems. Try typing the command again to resolve the error.", color=0xFFBC33))
                            embed.set_footer(text=f"{botName}")
                            await msg.edit(embed=embed)

                    if js == {'debug': None, 'errorCode': 'invalid_token', 'error': 'Invalid Access Token'}:
                        embed = (discord.Embed(title="Error Unlocking Cheg Q&A", description=f"<@!{message.author.id}> There was an error trying to unlock [this Q&A]({link}). Please create a ticket to report this issue.", color=0xFFBC33))
                        embed.set_footer(text=f"{botName}")
                        await msg.edit(embed=embed)
                    else:
                        question = js['data']['getQuestionByUuid']['content']['content']
                        question = question.replace("&nbsp;", " ")
                        question = question.replace('"//d2vlcm61l7u1fs', '"https://d2vlcm61l7u1fs')

                        if js['data']['getQuestionByUuid']['answers'] is not None and js['data']['getQuestionByUuid']['answers'] != []:
                            if js['data']['getQuestionByUuid']['answers'][0]['answerTemplate']['templateName'] == "HTML_ONLY":
                                answer = js['data']['getQuestionByUuid']['answers'][0]['body']
                                answer = answer.replace("&nbsp;", " ")
                                answer = answer.replace('"//d2vlcm61l7u1fs', '"https://d2vlcm61l7u1fs')
                                answer = answer.replace("\\\\[", "~")
                                answer = answer.replace("\\\\]", "~")
                                answer = answer.replace("\\\\", "\\")
                            elif js['data']['getQuestionByUuid']['answers'][0]['answerTemplate']['templateName'] in ["ENHANCED_CONTENT_V1", "ENHANCED_CONTENT_V2"]:
                                response = js['data']['getQuestionByUuid']['answers'][0]['body']
                                answerJSON = json.loads(response)
                                answer = ""
                                for step in answerJSON['steps']:
                                  answer += step['text']

                            startingHTML = "<!DOCTYPE html><html><head>  <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/katex@0.15.1/dist/katex.min.css' integrity='sha384-R4558gYOUz8mP9YWpZJjofhk+zx0AS11p36HnD2ZKj/6JR5z27gSSULCNHIRReVs' crossorigin='anonymous'>  <script defer src='https://cdn.jsdelivr.net/npm/katex@0.15.1/dist/katex.min.js' integrity='sha384-z1fJDqw8ZApjGO3/unPWUPsIymfsJmyrDVWC8Tv/a1HeOtGmkwNd/7xUS0Xcnvsx' crossorigin='anonymous'></script>  <script defer src='https://cdn.jsdelivr.net/npm/katex@0.15.1/dist/contrib/auto-render.min.js' integrity='sha384-+XBljXPPiv+OzfbB3cVmLHf4hdUFHlWNZN5spNQ7rmHTXpd7WvJum6fIACpNNfIR' crossorigin='anonymous'></script><meta name='viewport' content='width=device-width, initial-scale=1'><link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'><style>.collapsible {  background-color: #777;  color: white;  cursor: pointer;  padding: 18px;  width: 100%;  border: none;  text-align: left;  outline: none;  font-size: 15px;}.active, .collapsible:hover {  background-color: #555;}.content {  padding: 0 18px;  display: none;  overflow: hidden;  background-color: #f1f1f1;}.btn {  background-color: DodgerBlue;  border: none;  color: white;  padding: 12px 30px;  cursor: pointer;  font-size: 20px;}.btn:hover {  background-color: RoyalBlue;}</style></head><body><h2>Chegg Question & Answer Solution</h2><p>Question:</p><button type='button' class='collapsible'>Open Question</button><div class='content'>"
                            answerHTML= "</div><p>Answer & Explaination</p><button type='button' class='collapsible'>Open Answer</button><div class='content'>"
                            endingHTML = "</div>  <script>    var coll = document.getElementsByClassName('collapsible');    var i;    for (i = 0; i < coll.length; i++) {      coll[i].addEventListener('click', function() {        this.classList.toggle('active');        var content = this.nextElementSibling;        if (content.style.display === 'block') {          content.style.display = 'none';        } else {          content.style.display = 'block';        }      });    }  </script>  <script>      document.addEventListener('DOMContentLoaded', function() {          renderMathInElement(document.body, {            delimiters: [                {left: '~', right: '~', display: true}            ],            throwOnError : false          });      });  </script></body></html>"

                            html = startingHTML + question + answerHTML + answer + endingHTML
                            file = open("ans.html", "w", encoding="utf-8")
                            file.write(html)
                            file.close()
                            #html = io.BytesIO(html.encode('utf-8'))

                            #Send html file to my server
                            async with httpx.AsyncClient() as client:
                                limb = await client.post('https://nidzosiasky.nidzoball.repl.co/upload', files={'file': open('ans.html', 'rb')})

                            #limb = requests.post('https://nidzosiasky.nidzoball.repl.co/upload', files={'file': open('ans.html', 'rb')}).text.strip('')
                            limb = limb.text
                            print(limb)
                            #fileMsg = await message.author.send(file=discord.File(html, filename="answer.html"))

                            #Send Html link from server to user
                            embed = (discord.Embed(title="Cheg Q&A Unlocked", description=f"Chegg link: [Link]({link})", color=0x51C994))
                            embed.set_author(name=message.author, icon_url=message.author.avatar_url)
                            try:
                                embed.add_field(name="Answer :white_check_mark:", value="[Answer Link]({})".format(limb), inline=False)
                            except:
                                pass
                            embed.set_footer(text=f"{botName}")
                            await msg.edit(embed=embed)

                        else:
                            embed = (discord.Embed(title="No Answer", description=f"<@!{message.author.id}> [This question]({link}) hasn't been answered yet by an expert.", color=0xFFBC33))
                            embed.set_footer(text=f"{botName}")
                            await msg.edit(embed=embed)
            else:
                embed = (discord.Embed(title="Error Unlocking Document", description=f"<@!{message.author.id}> There was an error trying to unlock [this Q&A]({link}). Please create a ticket to report this issue.", color=0xFFBC33))
                embed.set_footer(text=f"{botName}")
                await msg.edit(embed=embed)
        #When textbook question is sent to channel
        elif 'homework-help' in link and "https://www.chegg.com" in link:
            role = discord.utils.get(message.guild.roles, name='premium')
            await message.channel.set_permissions(role, view_channel=True, send_messages=True, read_messages=True,read_message_history=True)
            counter1 += 1
            print(f"Chegg Unlock: {counter1}")
            embed = (discord.Embed(title="Unlocking your Cheg Textbook Solution", description=f"Please wait while the bot unlocks your [link.]({link})", color=0xFF4B4B))
            embed.set_footer(text=f"{botName}")
            msg = await message.channel.send(f"<@!{message.author.id}>", embed=embed)
            splitLink = link.split('-')
            locationOfSolution = splitLink.index('solution')
            problemQuestion = splitLink[locationOfSolution-1].upper()
            bookISBN = splitLink[locationOfSolution+1]
            chapterOfProblem = splitLink[locationOfSolution-3].upper()
            queryHeaders = {
                'Host': 'proxy.chegg.com',
                'X-CHEGG-DFID': 'mobile|2E5D1C7F-12DE-47F7-9684-C4789A736017',
                'X-PX-AUTHORIZATION': '3',
                'Accept': 'application/json',
                'Authorization': 'Basic MFQxOE5HYmFsUURGYzBnWkh6b3ZwZVJkN0E1Y3BMQ3g6dnRnamFZa3Ric2p4OUFPUg==',
                'X-CHEGG-DEVICEID': '0394ebf698a802f7f54fb4cd533e8f0d12e62fa7',
                'X-CHEGG-SESSIONID': 'B1A68867-AC03-43ED-A76E-BA72C7E50392',
                'Accept-Language': 'en-CA;q=1.0',
                'User-Agent': 'CheggApp/4.9.0 (com.chegg.mobile.consumer; build:4.9.0.1; iOS 15.3.1) Alamofire/5.2.2',
                'Connection': 'keep-alive',
                'X-PX-ORIGINAL-TOKEN': '3:39c69ff830472f396cd703c7b728a07e8d60a0aad1ad9eec7954cdea6ba12892:3DMBL0+k/0RSG/C43WZsN/8yJgspiqVpzP04hdfslu2eSE0b2F/Y/cMdkn1b/z9rs0oFjlPw/jc6AMM7pz2t0w==:1000:4NZcC2ltVMPRCHsKQXPsgqKIkIAj2EjcdX1F/uo197hgC6mzBzv08wT5ZC9uQEs6r6vjxB3dKkPlVSWR9sjw1csALsCfVCSk/7hZoU7WxcsxUbK6d89cSm7Kkh7SCNzJCKDDNcSNlzOD6IN4MWvOgNa/540wL0ma9LQcJTYhaj4f2ouoQDczmp9GrBcbveCPxsAdMCfcTTXcrtEHRo4hTA==',
                'x-chegg-auth-mfa-supported': 'true',
                'Content-Type': 'application/json',
            }

            #Textbook questions
            async with httpx.AsyncClient() as resp:
                response = await resp.get(f'https://proxy.chegg.com/v1/book/{bookISBN}/chapters?limit=100', headers=queryHeaders)
                chapterSearch = response.json()
            for chapter in chapterSearch['result']:
                if chapter['name'] == chapterOfProblem:
                    chapterID = chapter['id']
            async with httpx.AsyncClient() as resp:
                response = await resp.get(f'https://proxy.chegg.com/v1/chapter/{chapterID}/problems?limit=100', headers=queryHeaders)
                problemSearch = response.json()
            problemID = None
            for problem in problemSearch['result']:
                if problem['name'] == problemQuestion:
                    problemID = problem['id']
                    problemLink = problem['link']
                    break
            if problemID is None:
                while True:
                    if 'nextPage' in problemSearch.keys():
                        async with httpx.AsyncClient() as resp:
                            response = await resp.get(problemSearch['nextPage'], headers=queryHeaders)
                            problemSearch = response.json()
                        for problem in problemSearch['result']:
                            if problem['name'] == problemQuestion:
                                problemID = problem['id']
                                problemLink = problem['link']
                                break
                    else:
                        break
                    if problemID is not None:
                        break
            for problem in problemSearch['result']:
                if problem['name'] == problemQuestion:
                    problemID = problem['id']
                    problemLink = problem['link']
            accessToken = await accountCookies()
            await asyncio.sleep(2)

            # Textbook Header
            solutionHeaders = {
                'Host': 'proxy.chegg.com',
                'X-PX-AUTHORIZATION': '3',
                'User-Agent': 'Chegg Study/12.8.1 (Linux; U; Android 8.1.0; LM-Q710.FGN Build/OPM1.171019.019)',
                'X-CHEGG-DEVICEID': '98ea5768de4e1d0b4d9f1fe407b54f9a67dd2162',
                'newrelic': 'eyJ2IjpbMCwyXSwiZCI6eyJkLnR5IjoiTW9iaWxlIiwiZC5hYyI6IjUwMTM1NiIsImQuYXAiOiI3MjAzMTA2NCIsImQudHIiOiJkYjk5OTZlMGYyMDg0ZjgxYjkxM2E2OTNlZmYyZmFkNyIsImQuaWQiOiIyODRhYzg2ZmRiZWM0NDJlIiwiZC50aSI6MTY0NTQ3NzkwMTU2Nn19',
                'X-CHEGG-UUID': '7f7cfd2c-f30d-491f-b04c-057f6e134eb0',
                'X-CHEGG-SESSIONID': '4c26ac71-2873-462f-9748-509ee4fce81e',
                'x-chegg-auth-mfa-supported': 'true',
                'X-PX-ORIGINAL-TOKEN': '3:adc9176c069e436728c8901712c5324f7364b4b81002a2bbde2163a9e211e09d:N06tgLqafVWsn3xsfmQa1vrBvtpjEvOZip4Wjdlz/WanfAqNDeWi7yOlPaF2cy91Mll30OArxuNfkm3w3DTj3Q==:1000:xeCGTSEhMGEC+e25Aw5Ryc80EPc0VGOJjHaf+p1UIALNbVTDCb8dKe3xNHX4NOcDXz7mu2Am64ulkTRgX1EjF7i6qY2B4MfWsY89qPH/cD6SmYIaUx8WhTPwKeIEcJqLvwcdgpyOE3lnMp18Mscvag9Qx/58Sis+89fhAAeitQIoMLCFsUIBQmgRmo4Sc0OyYb8QZlzwC2j4WMxNQmuaoA==',
                'Authorization': 'Basic aGxEcFpBUEYwNW1xakFtZzdjcXRJS0xPaFVyeUI4cDE6dUJqemFrbXhHeDZXdHFBcg==',
                'tracestate': '@nr=0-2-501356-72031064-----1645477901562',
                'Accept-Language': 'en-CA,en-US;q=0.9,en;q=0.8',
                'traceparent': '00-db9996e0f2084f81b913a693eff2fad7--00',
                'Accept': '*/*',
                'x-chegg-dfid': 'mobile|dbae12a9-b180-3834-ab6f-95801828898c',
                'X-NewRelic-ID': 'UQYGUlNVGwQCVFJTBwcD',
                'access_token': accessToken,
                'Content-Type': 'application/json',
            }

            payload = {
                'isbn13': bookISBN,
                'userAgent': 'Mobile',
                'problemId': problemID,
            }
            async with httpx.AsyncClient() as resp:
                response = await resp.post('https://proxy.chegg.com/v1/tbs/_/solution', headers=solutionHeaders, json=payload)
                solutionJSON = response.json()

            if solutionJSON == {'debug': None, 'errorCode': 'invalid_token', 'error': 'Invalid Access Token'} or solutionJSON == {'errorCode': 'invalid_token', 'error': 'Invalid Token'}:
                accessToken = await accountCookies()
                await asyncio.sleep(2)
                solutionHeaders['access_token'] = accessToken
                async with httpx.AsyncClient() as resp:
                    response = await resp.post('https://proxy.chegg.com/v1/tbs/_/solution', headers=solutionHeaders, json=payload)
                    solutionJSON = response.json()

            startingHTML = "<!DOCTYPE html><html><head>  <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/katex@0.15.1/dist/katex.min.css' integrity='sha384-R4558gYOUz8mP9YWpZJjofhk+zx0AS11p36HnD2ZKj/6JR5z27gSSULCNHIRReVs' crossorigin='anonymous'>  <script defer src='https://cdn.jsdelivr.net/npm/katex@0.15.1/dist/katex.min.js' integrity='sha384-z1fJDqw8ZApjGO3/unPWUPsIymfsJmyrDVWC8Tv/a1HeOtGmkwNd/7xUS0Xcnvsx' crossorigin='anonymous'></script>  <script defer src='https://cdn.jsdelivr.net/npm/katex@0.15.1/dist/contrib/auto-render.min.js' integrity='sha384-+XBljXPPiv+OzfbB3cVmLHf4hdUFHlWNZN5spNQ7rmHTXpd7WvJum6fIACpNNfIR' crossorigin='anonymous'></script><meta name='viewport' content='width=device-width, initial-scale=1'><link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'><style>.collapsible {  background-color: #777;  color: white;  cursor: pointer;  padding: 18px;  width: 100%;  border: none;  text-align: left;  outline: none;  font-size: 15px;}.active, .collapsible:hover {  background-color: #555;}.content {  padding: 0 18px;  display: none;  overflow: hidden;  background-color: #f1f1f1;}.btn {  background-color: DodgerBlue;  border: none;  color: white;  padding: 12px 30px;  cursor: pointer;  font-size: 20px;}.btn:hover {  background-color: RoyalBlue;} img { max-width: 100%; height: auto;}</style></head><body><h2>Chegg Textbook Solution</h2><p>Question:</p><button type='button' class='collapsible'>Open Question</button><div class='content'>"
            answerHTML= "</div><p>Answer & Explaination</p><button type='button' class='collapsible'>Open Answer</button><div class='content'>"
            endingHTML = "</div>  <script>    var coll = document.getElementsByClassName('collapsible');    var i;    for (i = 0; i < coll.length; i++) {      coll[i].addEventListener('click', function() {        this.classList.toggle('active');        var content = this.nextElementSibling;        if (content.style.display === 'block') {          content.style.display = 'none';        } else {          content.style.display = 'block';        }      });    }  </script>  <script>      document.addEventListener('DOMContentLoaded', function() {          renderMathInElement(document.body, {            delimiters: [                {left: '~', right: '~', display: true}            ],            throwOnError : false          });      });  </script></body></html>"
            question = ""
            answer = ""
            if problemLink is None:
                question += "No question data."
            else:
                async with httpx.AsyncClient() as resp:
                    response = await resp.get(problemLink)
                    question += response.text
            counter = 1
            contentType = solutionJSON['result']['solutions'][0]['contentType']
            for step in solutionJSON['result']['solutions'][0]['steps']:
                async with httpx.AsyncClient() as resp:
                    answer += f"<h1>Step {counter}</h1>"
                    if contentType == "text/html":
                        response = await resp.get(step['link'])
                        answer += response.text
                    elif contentType == "image/png" or contentType == "image/jpg" or contentType == "image/jpeg":
                        answer += '<img alt="" src="' + step['link'] + '"<br>'
                counter += 1
            html = startingHTML + question + answerHTML + answer + endingHTML
            file = open("ans.html", "w", encoding="utf-8")
            file.write(html)
            file.close()

            #limb = requests.post('https://nidzosiasky.nidzoball.repl.co/upload', files={'file': open('ans.html', 'rb')}).text.strip('')                            
            # #limb = limb.text

            #Upload html file to my server
            async with httpx.AsyncClient() as client:
                limb = await client.post('https://nidzosiasky.nidzoball.repl.co/upload', files={'file': open('ans.html', 'rb')})

            #Receive link for html on server
            limb = limb.text
            print(limb)

            #Send html server link to user
            embed = (discord.Embed(title="Cheg Textbook Solution Unlocked", description=f"Chegg link: [Link]({link})", color=0x51C994))
            embed.set_author(name=message.author, icon_url=message.author.avatar_url)
            try:
                embed.add_field(name="Answer :white_check_mark:", value="[Answer Link]({})".format(limb), inline=False)
            except:
                pass
            embed.set_footer(text=f"{botName}")
            await msg.edit(embed=embed)

def setup(client):
    client.add_cog(Example(client))
