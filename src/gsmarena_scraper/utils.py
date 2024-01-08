import json

def to_json(obj: any) -> str:
    return json.dumps(obj, default=lambda obj: obj.__dict__, indent=4)


user_agents = [
    "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/120.0.6099.200 Safari/537.36",
    # "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012; Storebot-Google/1.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.200 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
]