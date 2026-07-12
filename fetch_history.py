#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse

SYMBOLS = [
    "^TWII", "XIN9.FGI", "YM=F", "NQ=F", "^GDAXI", "^HSI",
    "GC=F", "CL=F", "TWD=X", "EURTWD=X", "CNYTWD=X", "BTC-USD",
]

def fetch_history(symbol, range_="6mo", interval="1d"):
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}"
        f"?range={range_}&interval={interval}"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.load(resp)
    result = data["chart"]["result"][0]
    timestamps = result["timestamp"]
    quote = result["indicators"]["quote"][0]
    candles = []
    for i, t in enumerate(timestamps):
        o, h, l, c = quote["open"][i], quote["high"][i], quote["low"][i], quote["close"][i]
        if None in (o, h, l, c):
            continue
        candles.append({"t": t, "o": round(o, 4), "h": round(h, 4), "l": round(l, 4), "c": round(c, 4)})
    return candles

def main():
    out = {}
    for symbol in SYMBOLS:
        try:
            out[symbol] = fetch_history(symbol)
        except Exception as e:
            out[symbol] = []
    print(json.dumps(out, ensure_ascii=False))

if __name__ == "__main__":
    main()
