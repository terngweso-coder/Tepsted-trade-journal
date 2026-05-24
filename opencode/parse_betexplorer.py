import cloudscraper, re
s=cloudscraper.create_scraper(browser={'browser':'chrome','platform':'windows','mobile':False})
r=s.get('https://www.betexplorer.com/soccer/spain/primera-division/', timeout=20)
html = r.text

# Look for API URLs
urls = re.findall(r'["\'](https?://[^"\']*?/soccer/[^"\']*?\.json[^"\']*?)["\']', html)
print(f'JSON API URLs found: {len(urls)}')
for u in urls[:10]:
    print(f'  {u}')

# Look for any /soccer/ rest API calls
rest_urls = re.findall(r'["\'](/[^"\']*soccer[^"\']*?\.json[^"\']*?)["\']', html)
print(f'\nRelative API URLs: {len(rest_urls)}')
for u in rest_urls[:10]:
    print(f'  {u}')

# Look for proxy calls
proxy_calls = re.findall(r'["\']([^"\']*?get[^"\']*?match[^"\']*?)["\']', html, re.IGNORECASE)
print(f'\nMatch-related routes: {len(proxy_calls)}')
for u in proxy_calls[:10]:
    print(f'  {u}')

# Look for 'proxy' or 'ajax' in page
if 'proxy' in html.lower():
    proxies = re.findall(r'["\']([^"\']*?proxy[^"\']*?)["\']', html, re.IGNORECASE)
    print(f'\nProxy routes: {len(proxies)}')
    for p in proxies[:10]:
        print(f'  {p}')
