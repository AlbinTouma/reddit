import requests
import json
import time

url = "https://www.reddit.com/r/OSINT.json"
headers = {
    "User-Agent": "Mozilla/5.0 (compatible; RedditScraper/1.0)",
    "Accept": "application/json"
}

after = None
page = 1

while True:
    params = {"after": after, "limit": 100} if after and page >1 else {}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()["data"]

    print(f"Page {page}, got {len(data['children'])} subreddits")

    after = data["after"]
    if not after:
        print(f"Reached last page ({page})")
        break

    for child in data['children']:
        with open('subreddit.jsonl','a') as f:
            r = json.dumps(child['data'])
            f.write(r + "\n")

    page += 1
    time.sleep(2)

