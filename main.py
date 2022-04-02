from time import sleep
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

_30MinInSec = 30*60

def lastNote(rawNotes):
    soup = BeautifulSoup(rawNotes,'html.parser')
    lastnote = soup.find('tr').find_all('span')[1].text
    return lastnote

def connectAndGetNotes(username,password):
    # print(username,password)
    baseURL = 'https://aurion.junia.com'

    cookies = Cookies(POSTlogin(username,password))
    viewS = ViewState(GETmain(cookies,baseURL))

    GETmain(cookies,baseURL)
    POSTmain(viewS,cookies,baseURL)
    POSTmainn(viewS,cookies,baseURL)
    GETnote(cookies,baseURL)
    return lastNote((POSTnote(viewS,cookies,baseURL)))




if __name__ == '__main__':
    client = discord.Client()
    @client.event
    async def on_ready():
        lastnote = connectAndGetNotes(username,password)
        print('Connection : successful')
        #channelID for my private test channel
        channel = await client.fetch_channel(706808514953216020)
        while(True):
            tmpNote = connectAndGetNotes(username,password)
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")    
            print(timestamp,' - last note :',lastnote,'tmp note :',tmpNote)
            if(tmpNote != lastnote):
                print('Nouvelle note :',tmpNote)
                lastnote = tmpNote
                await channel.send('||@everyone||Nouvelle note : ',lastnote)
            sleep(_30MinInSec)
    client.run(token)