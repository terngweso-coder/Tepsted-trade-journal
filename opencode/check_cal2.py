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
for e in data['result']:
    imp = e.get('importance', -1)
    if imp == 1:
        print(f"IMP={imp} cur={e.get('currency','')} title={e['title']} date={e['date'][:16]}")
