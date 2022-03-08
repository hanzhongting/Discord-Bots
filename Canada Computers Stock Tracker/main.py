#Author: Nikola Gavric

#This bot checks stock for popular items on CanadaComputers and sends a message when new inventory is updated

import requests
from bs4 import BeautifulSoup
import json
import discord

#sd_list = [['Kingston Canvas Select Plus, 256GB microSDXC Memory Card, Class 10, UHS-I, U3, V30, A1, Up to 100MB/s Read and 85MB/s Write (SDCS2/256GBCR)', '1+', '-', '3', '1', '2', '2', '-', '-', '-', '4', '5+', '4', '-', '5+', '4', '1', '4', '2', '-', '-', '-', '-', '5+', '3', '-', '-', '-', '-', '5+']]
links = ["https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=195323", "https://www.canadacomputers.com/product_info.php?cPath=22_700_1103&item_id=139967", "https://www.canadacomputers.com/product_info.php?cPath=21_279_1950&item_id=137217"]

client = discord.Client()

@client.event
async def on_ready():
    #while(True):
#def cc():
    for xyz in range(len(links)):
        result = requests.get(links[xyz])

#print(result.status_code)

#weird type
        web = (result.content)

#String
        web1 = str(web, 'UTF-8')


# Open a file with access mode 'a'
#file_object = open('content.txt', 'a')
# Append 'hello' at the end of file
#file_object.write(web1)
# Close the file
#file_object.close()


        soup = BeautifulSoup(web, 'lxml')
#links = soup.find_all("a")
#print(links)
#print('\n')

        name = soup.find_all('h1', class_ = 'h3 mb-0')
        price = soup.find_all('span', class_ = 'h2-big open__box__color')
    #.find('strong').get_text()
        mydivs1 = soup.find_all("div", {"id": "prov-ONLINE"}) 
        mydivs2 = soup.find_all("div", {"class": "col-md-4 col-sm-6 item__avail__num ON"})
        mydivs3 = soup.find_all("div", {"class": "col-md-4 col-sm-6 item__avail__num ON stock-detail"})
        list = name + mydivs1 + mydivs2 + mydivs3 + price

    #print(mydivs)
    #print(type(mydivs2))

    #locations = {'Online' : "", 'Waterloo': "", 'Cambridge' : "", 'Burlington' : "", 'Hamilton' : "", 'Oakville' : "", 'Brampton' : "", 'Mississauga' : "", 'Etobicoke' : "", 'North London' : "", 'London' : " : ", 'Downtown Toronto' : "", 'Midtown Toronto' : "", 'North York' : "", 'Richmond Hill' : "", 'Scarborough' : "", 'Markham' : "", 'St.Catharines' : "", 'Newmarket' : "", 'Barrie' : "", 'Ajax' : "", 'Whitby' : "", 'Oshawa' : "", 'Kingston' : "", 'Kanata' : "", 'Ottawa Merivale' : "", 'Downtown Ottawa' : "", 'Ottawa Orleans' : ""}
    #cities = {"Product" : "", "Online" : "", "Waterloo": "", "Cambridge" : "", "Burlington" : "", "Hamilton" : "", "Oakville'" : "", "Brampton" : "", "Mississauga" : "", "Etobicoke" : "", "North London" : "", "London" : " : ", "Downtown Toronto" : "", "Midtown Toronto" : "", "North York" : "", "Richmond Hill" : "", "Scarborough" : "", "Markham" : "", "St.Catharines" : "", "Newmarket" : "", "Barrie" : "", "Ajax" : "", "Whitby" : "", "Oshawa" : "", "Kingston" : "", 'Kanata' : "", "Ottawa Merivale" : "", "owntown Ottawa" : "", "Ottawa Orleans" : ""}
        cities = ["Product", "Online", "Waterloo", "Cambridge", "Burlington", "Hamilton", "Oakville", "Brampton", "Mississauga", "Etobicoke", "North London", "London", "Vaughan", "Downtown Toronto", "Midtown Toronto", "North York", "Richmond Hill", "Scarborough", "Markham", "St.Catharines", "Newmarket", "Barrie", "Ajax", "Whitby", "Oshawa", "Kingston", 'Kanata', "Ottawa Merivale", "Downtown Ottawa", "Ottawa Orleans"]
        list1 = []
   #locations = list(cities.keys())

    #value = mydivs0.find('strong').text
    #print(name)
    
        #Product
        for x in range(1):
            #for locations in mydivs1:
            value = list[x].find('strong').text
            list1.append(value)
            #print(f"Product: {value}")

        #Online Stock
        for x in range(1,2):
            #for locations in mydivs1:
            value = list[x].find('strong').text
            list1.append(value)


            """for x in range(2,8):
            #for locations in mydivs2:
            value = list[x].find('strong').text
            print(f"{cities[x]}: {value}")


        for x in range(8,30):
            value = list[x].find('strong').text
            print(f"{cities[x]}: {value}")
            """           

        for x in range(2,30):
            value = list[x].find('strong').text
            list1.append(value)

        #Price
        for x in range(30,31):
            value = list[x].find('strong').text
            list1.append(value)
        #print(list1)
            #print(f"{cities[x]}: {value}")
        #print(list1[2])
        #print()
        #print(sd_list)
        #print()

    #print(sd_list[xyz][2])


        #Check if list is in stock.json (When new link is added to list of links)
        f = open('stock.json', 'r')
        db = json.load(f)
        products = []
        for list in db:
            products.append(list[0])
        if list1[0] not in products:
            with open("stock.json", "r") as file:
                data = json.load(file)
                # 2. Update json object
                data.append(list1)
                # 3. Write json file
            with open("stock.json", "w") as file:
                json.dump(data, file)


        for y in range(1,31):
            f = open('stock.json', 'r')
            db = json.load(f)

            #print(f"{cities[y]}: {list1[y]}")
            #print(f"{cities[y]}: {db[xyz][y]}")

        
            if list1[y] == (db[xyz][y]):
                print("same")
            else:
                #print("Different")
                #print(f"Previous stock: {db[xyz][y]}")
                #print(f"New stock: {list1[y]}")

                #Create Embed 
                channel = client.get_channel(927000526841860186)

                embed = discord.Embed(title= (f"{list1[0]}"), url = f"{links[xyz]}", description= f"📍 {cities[y]}", color=0xe74c3c if list1[y] == "-" else 0x2ecc71) #,color=Hex code

                previous_stock = db[xyz][y]
                if previous_stock == "-":
                    previous_stock = "0"

                current_stock = list1[y]
                if current_stock == "-":
                    current_stock = "0"
                    
                embed.add_field(name=f"Previous Stock", value=f"{previous_stock}", inline = True)
                embed.add_field(name=f"New Stock", value=f"{current_stock}", inline = True)
                embed.add_field(name=f"Price", value=f"{db[xyz][30]}", inline = False)
                
                
                await channel.send(embed=embed)

                    #change data in stock.json
                db[xyz][y] = list1[y]
                with open("stock.json", "w") as jsonFile:
                    json.dump(db, jsonFile)
            print()


#while True:
    #cc()
client.run("OTI3MzM2MjM2ODc0NjAwNDU5.YdIvKw.TszRAy05fhaJ9JlK_nFx5yUhfrk")

#cc()
#print("---------------------------------------------------------------------------")
#cc()
