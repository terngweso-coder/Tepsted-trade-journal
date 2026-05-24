import urllib.request, json, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
req = urllib.request.Request(
    'https://economic-calendar.tradingview.com/events?from=2026-05-25&to=2026-05-29',
    headers={'User-Agent': 'Mozilla/5.0', 'Origin': 'https://www.tradingview.com', 'Referer': 'https://www.tradingview.com/'}
)
r = urllib.request.urlopen(req, context=ctx, timeout=10)
data = json.loads(r.read())
results = data['result']
print(f"Total events: {len(results)}")
importances = set(e.get('importance') for e in results)
print(f"Importance values seen: {sorted(importances)}")
high = [e for e in results if e.get('importance', -1) >= 2]
print(f"Medium/High events: {len(high)}")
for e in high[:10]:
    print(f"  [{e['importance']}] {e['title']} ({e['country']}) - {e['date'][:10]} {e.get('currency','')}")
