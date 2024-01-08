from gsmarena_scraper import GSMArenaClient
from gsmarena_scraper.classes import GSMArenaPhone
from gsmarena_scraper.classes.phone import GSMArenaPhoneBasic
from gsmarena_scraper.utils import to_json, user_agents
import time
import os
import json
import random

LIST_START = 0
BLOCK_SIZE = 50

CLIENT = GSMArenaClient()

phone_list = []

if os.path.exists("list.json"):
    with open("list.json", "r") as f:
        data = json.load(f)
        for phone_json in data:
            phone_list.append(GSMArenaPhoneBasic(**phone_json))

else: 
    phone_list = CLIENT.list_phones()
    random.shuffle(phone_list)
    with open("list.json", "w+") as f:
        f.write(to_json(phone_list))


print("Discovered ",len(phone_list), " devices")

out = []
failed_devices = []

i = LIST_START
ua_index = 0
CLIENT.headers.update({
    "User-Agent": user_agents[ua_index]
})
while i < len(phone_list):
    phone = phone_list[i]
    i += 1
    print(phone.url)

    # Get phone specs html
    phone_res = CLIENT.get(phone.url)
    try:
        phone_res.raise_for_status()
        phone_data = GSMArenaPhone.from_html_response(phone_res.content, basic_details=phone)

        out.append(phone_data)

        # wait random 1-5 sec interval
        wait_interval = random.random() + random.randint(1,2)
        print(f"Waiting {wait_interval} seconds")
        time.sleep(wait_interval)
    except: 
        print(f"Failed {phone.url} with code {phone_res.status_code}")
        failed_devices.append(phone)
        continue

    # If reached end of block or end of list, dump contents, clear containers
    if not i % BLOCK_SIZE or i == len(phone_list):
        ua_index = len(user_agents) % (ua_index + 1)

        CLIENT.headers.update({
            "User-Agent": user_agents[ua_index]
        })

        with open(f"found.{i}.json", "w+") as f:
            f.write(to_json(out))
        out = []

        with open(f"failed.{i}.json", "w+") as f:
            f.write(to_json(failed_devices))
        failed_devices=[]

        print(f"Block {i} complete, waiting 10 seconds...")
        time.sleep(10)