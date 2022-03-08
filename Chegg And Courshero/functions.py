#Author: Nikola Gavric

#Imports
from config import *
import discord
from discord import guild, message
from discord.ext import commands
from discord.ext.commands import Bot, CommandNotFound, CheckFailure
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
import json
from datetime import datetime, timedelta
import datetime as dt
import time
import re
import mimetypes
import aiohttp
from aiohttp_retry import RetryClient
import sys
import traceback
from docx import Document
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.pdf import ContentStream
from PyPDF2.generic import TextStringObject, NameObject
from PyPDF2.utils import b_
import io
from bs4 import BeautifulSoup
from docx import Document
import random
import asyncio
import os
import httpx
import requests
from re import X
from typing import Counter

#Document gen lists
courseList = ["MU", "MATH", "PHYS", "CHEM", "BIO", "NURS", "FASH", "COMS", "JOUR", "ASTR", "URBN", "ANT", "JAP", "ENG", "GEO", "AERO", "BMED", "ARCH", "LAW", "WGS", "FILM", "ECON", "FIN", "PHIL", "FASH", "HIST", "STAT", "ENVI"]
documentType = ["Chapter_", "doc_", "Extra_Credit_", "Report_", "Lecture-", "Research-", "Guide-", "Test-", "Review_", "Analysis-", "Assessment-", "Exam-", "Project-"]
fileTopics = ["Crypto", "Integrals", "Technology", "Chemistry", "Biology", "Covid", "Culture", "Racism", "Physics", "World War", "Environment", "Space"]

class notAdmin(commands.CommandError):
    def __init__(self, server, *args, **kwargs):
        self.server = server
        super().__init__(*args, **kwargs)

#Admin check
def adminPrivileges():
    def predicate(ctx):
        if ctx.message.author.id == 423260993276346388 or ctx.message.author.id == 910209900028760146:
            return True
        else:
            raise notAdmin(ctx.message.author)
    return commands.check(predicate)

#Cookies 
async def accountCookies():
    headers = {
    'Host': 'proxy.chegg.com',
    'X-PX-AUTHORIZATION': '3:fae1deac55fe753e3b1ffa93611835e79fa90f324d008a0e80009cab89afc710:JJ4fpJZNJ/d1J25cziwyAoh/1d+xwuZVNZDLhE0/1ZrQRe1nEJbOH/gRL/BG7oqOCzr6Eo37FD1nV1/2bmPdWQ==:1000:JOhL58NnGJUA71nzLKq7fqjZ3y2sge2jniukRlqYkU+xOtXPsWqSFw7Ad5we2ghfet1pYw7ptddYyCuLqg1keOjeHM6/4TpkO6HB76syx1fYmtZgT+NdHnq5S/cKuSR0cz9/HAw+Yk5sHDB/WN58FF3CL5LVttcJqmfbStz+aZVCui1/C51EwyEYJy4SYAcr4Uk70gNA0+cYSSVlAQ/TQA==',
    'Accept': 'application/json',
    'Authorization': 'Basic T2pRdTVES0g5Y3dhSVBvS1JyYUZYTllBZDNtclhQdTc6NDFQcnZkc0FWckF5bFRydw==',
    'X-CHEGG-UUID': '7f7cfd2c-f30d-491f-b04c-057f6e134eb0',
    'X-CHEGG-DEVICEID': '0b89ecf0a6d7d481b8b1dfcc512d4adefcfc3140',
    'X-CHEGG-SESSIONID': 'BE9D22A8-94CB-465E-B67A-93C3DCD174B7',
    'Accept-Language': 'en-CA;q=1.0',
    'X-ADOBE-MC-ID': '35501240466901328941553184682435157068',
    'Content-Length': '71',
    'User-Agent': 'Prep/1.17.3 (com.chegg.mobile.prep; build:1.17.3.0; iOS 15.3.1) Alamofire/5.2.2',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
}

#Chegg accounts
    accountList = [
        {
            "username": "empwmws@gmail.com",
            "password": "password"
        },
        {
            "username": "evan.budnyk@gmail.com",
            "password": "password"
        },
        {
            "username": "elviamajano@yahoo.com",
            "password": "password"
        },
        {
            "username": "elyahovhannisyan@gmail.com",
            "password": "password"
        },
        {
            "username": "brittanycx333@gmail.com",
            "password": "password"
        },
        {
            "username": "karinarubin123@gmail.com",
            "password": "password"
        },
        {
            "username": "codybby6794@gmail.com",
            "password": "password"
        },
        {
            "username": "camille.yyc86@gmail.com",
            "password": "password"
        },
        {
            "username": "asatpulat@gmail.com",
            "password": "password"
        },
    ]
    #Pick random account
    accountToUse = random.choice(accountList)

    #Proxy
    p1={"http":"http://esgnzoky:0u3n43hw5toj@23.250.57.243:8750",
        "https":"http://esgnzoky:0u3n43hw5toj@23.250.57.243:8750"
    }

    data = {
      'grant_type': 'password',
      'password': accountToUse['password'],
      'source_page': 'ios Flashtools 1.17.3|prep',
      'source_product': 'ios|prep',
      'username': accountToUse['username']
    }

    #Login to chegg
    loginToChegg = requests.post('https://proxy.chegg.com/oidc/token', headers=headers, data=data).json()

    if loginToChegg == {'debug': None, 'errorCode': 'invalid_user_credentials', 'error': 'No user exists for provided user credentials(username/password), or password is not valid. Please provide valid username/password pair'}:
        print(f"The account with username: {accountToUse['username']} has invalid credentials. Please remove this from the bot or update the account with correct credentials.")
    else:
        try:
            accessToken = loginToChegg['access_token']
            return accessToken
        except:
            print(loginToChegg)

#Coursehero doc gen
def filenameGenerator():
    courseType = random.choice(courseList)
    courseNumber = random.randint(101,399)
    docType = random.choice(documentType)
    documentNumber = random.randint(0,9)
    payload = {
        "name": "{}{}-{}{}".format(courseType, courseNumber, docType, documentNumber),
        "courseType": courseType
    }
    return payload

#Remove watermark from coursehero doc
def removeWatermark(resp):
    firstHalf_text = 'This study resource was'
    secondHalf_text = 'shared via CourseHero.com'
    footer_text = 'This study source was downloaded by'
    replace_with = ''

    memory_file = io.BytesIO(resp)
    source = PdfFileReader(memory_file)
    output = PdfFileWriter()

    for page in range(source.getNumPages()):
        page = source.getPage(page)
        content_object = page["/Contents"].getObject()
        content = ContentStream(content_object, source)

        for operands, operator in content.operations:
            if operator == b_("TJ"):
                text = operands[0][0]
                if isinstance(text, TextStringObject) and text.startswith(firstHalf_text) or isinstance(text, TextStringObject) and text.startswith(secondHalf_text) or isinstance(text, TextStringObject) and text.startswith(footer_text):
                    operands[0] = TextStringObject(replace_with)
        page.__setitem__(NameObject('/Contents'), content)
        output.addPage(page)

    fileTest = io.BytesIO()
    output.write(fileTest)
    return fileTest.getvalue()
