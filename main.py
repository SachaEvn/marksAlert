from time import sleep
import time
from requestsAndShit import *
from datetime import datetime
from bs4 import BeautifulSoup
import discord
import sys

token_arg_id = 1
username_arg_id = 2
pass_arg_id = 3

token = sys.argv[token_arg_id]
username = sys.argv[username_arg_id]
password = sys.argv[pass_arg_id]

#channels id & role
_id_private_channel = 706808514953216020
_id_school_channel = 899648994614071306
_pingRole = 'botNote'


print('\ntoken : {}\nusername : {}\npassword : {}\n'.format(token,username,password))

_30MinInSec = 30*60

def parseLastNote(rawNotes):
    soup = BeautifulSoup(rawNotes,'html.parser')
    lastnotes = soup.find_all('tr')#.find_all('span')#[1].text
    return len(lastnotes)

def connectAndGetNotes(username,password):
    cookies = Cookies(POSTlogin(username,password))
    _mainn = GETmain(cookies,baseURL)
    viewS = ViewState(_mainn)

    POSTmain(viewS,cookies,baseURL)
    POSTmainn(viewS,cookies,baseURL)
    GETnote(cookies,baseURL)
    return parseLastNote((POSTnote(viewS,cookies,baseURL)))


if __name__ == '__main__':
    client = discord.Client()
    @client.event
    async def on_ready():
        print('Connection : successful')
        lastnote = connectAndGetNotes(username,password)
        print('Nb notes at launch :',lastnote)

        #channelID for my private test channel
        privateChan = await client.fetch_channel(_id_private_channel)
        while(True):
            sleep(_30MinInSec)
            tmpNote = connectAndGetNotes(username,password)
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            if(tmpNote != lastnote):
                lastnote = tmpNote
                msg = '||@{}|| {} - Nouvelle note !'.format(_pingRole,timestamp)
                print(msg[12:])
                await privateChan.send(msg)
            else:
                print(timestamp,'- Aucune nouvelle note.')
    client.run(token)
    