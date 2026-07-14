import json
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "news.json"

with open(path, encoding="utf-8") as f:
    data = json.load(f)

over_limit = False
for group in data["groups"]:
    for item in group["items"]:
        length = len(item["commentary"])
        flag = " <-- OVER 300" if length > 300 else ""
        if length > 300:
            over_limit = True
        print(length, item["title"][:30], flag)

print("OK" if not over_limit else "FAIL: some commentary exceeds 300 chars")
