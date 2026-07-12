#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta

ITEMS = [
    {"group": "股市指數", "name": "台灣加權指數", "symbol": "^TWII"},
    {"group": "股市指數", "name": "中國A50", "symbol": "XIN9.FGI"},
    {"group": "股市指數", "name": "小道瓊", "symbol": "YM=F"},
    {"group": "股市指數", "name": "小那斯達克", "symbol": "NQ=F"},
    {"group": "股市指數", "name": "德國DAX", "symbol": "^GDAXI"},
    {"group": "股市指數", "name": "恆生指數", "symbol": "^HSI"},
    {"group": "商品", "name": "黃金", "symbol": "GC=F"},
    {"group": "商品", "name": "輕原油", "symbol": "CL=F"},
    {"group": "匯率", "name": "美元", "symbol": "TWD=X"},
    {"group": "匯率", "name": "歐元", "symbol": "EURTWD=X"},
    {"group": "匯率", "name": "人民幣", "symbol": "CNYTWD=X"},
    {"group": "匯率", "name": "比特幣", "symbol": "BTC-USD"},
]

def fetch_one(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.load(resp)
    meta = data["chart"]["result"][0]["meta"]
    price = meta["regularMarketPrice"]
    prev = meta.get("previousClose") or meta.get("chartPreviousClose")
    change = price - prev if prev else None
    pct = (change / prev * 100) if prev else None
    return {
        "price": price,
        "previousClose": prev,
        "change": change,
        "changePercent": pct,
        "currency": meta.get("currency"),
    }

def main():
    results = []
    for item in ITEMS:
        try:
            q = fetch_one(item["symbol"])
            results.append({**item, **q})
        except Exception as e:
            results.append({**item, "error": str(e)})

    tz = timezone(timedelta(hours=8))
    out = {
        "updatedAt": datetime.now(tz).strftime("%Y-%m-%d %H:%M"),
        "items": results,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
