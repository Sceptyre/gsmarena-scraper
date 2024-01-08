from gsmarena_scraper import GSMArenaClient
from gsmarena_scraper.classes import GSMArenaPhone
from gsmarena_scraper.classes.phone import GSMArenaPhoneBasic
from gsmarena_scraper.utils import to_json, user_agents
import time

import random

client = GSMArenaClient()
# phone_list = client.list_phones()

# random.shuffle(phone_list)
# with open("list.json", "w+") as f:
#     f.write(to_json(phone_list))

import json
phone_list = []
with open("list.json", "r") as f:
    data = json.load(f)
    for phone_json in data:
        phone_list.append(GSMArenaPhoneBasic(**phone_json))


print("Discovered ",len(phone_list), " devices")

out = []
failed_devices = []

i = 10650
block_size = 50
ua_index = 0
client.headers.update({
    "User-Agent": user_agents[ua_index]
})
while i < len(phone_list):
    phone = phone_list[i]
    i += 1
    print(phone.url)

    # Get phone specs html
    phone_res = client.get(phone.url)
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

    if not i % block_size or i == len(phone_list):
        ua_index = len(user_agents) % (ua_index + 1)

        client.headers.update({
            "User-Agent": user_agents[ua_index]
        })

        with open(f"found.{i}.json", "w+") as f:
            f.write(to_json(out))
        
        with open(f"failed.{i}.json", "w+") as f:
            f.write(to_json(failed_devices))

        out = []
        failed_devices=[]

        print(f"Block {i} complete, waiting 10 seconds...")
        time.sleep(10)