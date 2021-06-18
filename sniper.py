print(f"""
░██████╗███╗░░░███╗░█████╗░██████╗░████████╗  ░██████╗███╗░░██╗██╗██████╗░███████╗██████╗░
██╔════╝████╗░████║██╔══██╗██╔══██╗╚══██╔══╝  ██╔════╝████╗░██║██║██╔══██╗██╔════╝██╔══██╗
╚█████╗░██╔████╔██║███████║██████╔╝░░░██║░░░  ╚█████╗░██╔██╗██║██║██████╔╝█████╗░░██████╔╝
░╚═══██╗██║╚██╔╝██║██╔══██║██╔══██╗░░░██║░░░  ░╚═══██╗██║╚████║██║██╔═══╝░██╔══╝░░██╔══██╗
██████╔╝██║░╚═╝░██║██║░░██║██║░░██║░░░██║░░░  ██████╔╝██║░╚███║██║██║░░░░░███████╗██║░░██║
╚═════╝░╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░  ╚═════╝░╚═╝░░╚══╝╚═╝╚═╝░░░░░╚══════╝╚═╝░░╚═╝""")
print('Reloaded by a hippo')
print('Auth by Coolkidmacho')
print('Brain damage by a self imposed accident...')
import argparse
import asyncio
import json
import os
import time
import urllib.request
from datetime import datetime, timezone
import http.client, json, threading, ssl
import aiohttp
import requests
from colorama import Fore, Style, init
from dateutil.parser import isoparse

#from msauth import login
name = input("Email: ")  
passw = input('Password: ')

def inp(text):
    print(f"{Fore.YELLOW}{text}", end="")
    ret = input("")
    return ret
async def get_mojang_token(email: name, password: passw):
    # Login code is partially from mcsniperpy thx!
    questions = []

    async with aiohttp.ClientSession() as session:
        authenticate_json = {"username": email, "password": password}
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",
                   "Content-Type": "application/json"}
        async with session.post("https://authserver.mojang.com/authenticate", json=authenticate_json,
                                headers=headers) as r:
            # print(r.status)
            if r.status == 200:
                resp_json = await r.json()
                # print(resp_json)
                auth = {"Authorization": "Bearer: " + resp_json["accessToken"]}
                access_token = resp_json["accessToken"]
                # print(f"{Fore.LIGHTGREEN_EX}Auth: {auth}\n\nAccess Token: {access_token}")
            else:
                print(f"{Fore.LIGHTRED_EX}INVALID CREDENTIALS{Fore.RESET}")

        async with session.get("https://api.mojang.com/user/security/challenges", headers=auth) as r:
            answers = []
            if r.status < 300:
                resp_json = await r.json()
                if resp_json == []:
                    async with session.get("https://api.minecraftservices.com/minecraft/profile/namechange",
                                           headers={"Authorization": "Bearer " + access_token}) as nameChangeResponse:
                        ncjson = await nameChangeResponse.json()
                        print(ncjson)
                        try:
                            if ncjson["nameChangeAllowed"] is False:
                                print(
                                    "Your Account is not"
                                    " eligible for a name change!"
                                )
                                exit()
                            else:
                                print(f"{Fore.LIGHTGREEN_EX}Logged into your account successfully!{Fore.RESET}")
                                print("Your bearer token is: " + access_token)
                        except Exception:
                            print("logged in correctly")
                            print("Your bearer token is: " + access_token)
                else:
                    try:
                        for x in range(3):
                            ans = inp({resp_json[x]["question"]["question"]})
                            answers.append({"id": resp_json[x]["answer"]["id"], "answer": ans})
                    except IndexError:
                        print(f"{Fore.LIGHTRED_EX}Please provide answers to the security questions{Fore.RESET}")
                        return
                    async with session.post("https://api.mojang.com/user/security/location", json=answers,
                                            headers=auth) as r:
                        try:
                            if r.status < 300:
                                print(f"{Fore.LIGHTGREEN_EX}Logged in{Fore.RESET}")
                                print("Your bearer token is: " + access_token)
                        except RuntimeError:
                            print("")
                        if r.status > 300:
                            print(
                                f"{Fore.LIGHTRED_EX}Security Questions answers were incorrect, restart the program!{Fore.RESET}")
    global bearer
    bearer = access_token


asyncio.run(get_mojang_token(name, passw))
name = input("Name: ")
delay = int(input("Delay: "))
try:
    jj = requests.get(f'https://mojang-api.teun.lol/droptime/{name}').json()
except Exception:
    print("Unexpected Error")
    exit()
droptime = jj['UNIX']
print(droptime)
e = threading.Event()
def runRequest():
    headers = {"Accept": "application/json", "Authorization": "Bearer " + bearer}
    #jsn     = {"profileName": name}
    #jsn     = json.dumps(jsn)
    conn    = http.client.HTTPSConnection("api.minecraftservices.com")
    conn.request("GET", "/")
    conn.getresponse().read()
    e.wait()
    conn.request("PUT", "/minecraft/profile/name/" + name, None, headers)
    response = conn.getresponse()
    print("Got answer at", time.time(), "with response", response.status)

if droptime + - time.time() > 60:
    print('Sniping ' + name + ' in ' + str(round((droptime + - time.time()) / 60 )) + ' minutes!')
if droptime + - time.time() < 60:
    print('Sniping ' + name + ' in ' + str(round(droptime + - time.time())) + ' seconds!')

threads = []
for i in range(2):
    threads += [threading.Thread(target=runRequest)]
for t in threads:
    t.start()
time.sleep(droptime + - time.time() - (delay / 1000))
print("Starting requests at", time.time())
e.set()