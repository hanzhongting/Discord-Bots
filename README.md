# Discord-Bots

Heres a quick overview of what each bot is designed to do.

**CanadaComputers Stock Tracker**  
This bot infinitely checks high demand products on CanadaCompuers site and sends a message when an item becomes in or out of stock.

**Chegg And Coursehero**  
This bot detects when a chegg or coursehero link is send to a discord channel. Once a link is detected the bot will use the appropriate account to access and download the html/pdf answer file using the appropriate api. The answer file is then uploaded to a server that stores the files(I have also provided the code for the server in this repository) and sends back the answer file link to the user.

**Server For Chegg And Coursehero Answers**  
This code stores chegg and coursehero answer files that can be accessed if you have the corresponding link for that file.

**Socials Manager**  
This bot is a social media manager bot. When the user types in the setup command, a new private ticket is created where the user is able to select which social media accounts they have. After they select the appropriate accounts, the bot will ask them to enter their usernames and the bot will create a embeded massage containing all of their usernames along with a link to all their social media sites. The bot will then post this embeded message into a specific channel.
