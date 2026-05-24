import cloudscraper, re
s=cloudscraper.create_scraper(browser={'browser':'chrome','platform':'windows','mobile':False})

# Try footystats for a specific match - search by team
url = 'https://www.footystats.org/fixtures'
r = s.get(url, timeout=20)
html = r.text

# Save for analysis
with open(r'C:\Users\katak\AppData\Local\Temp\opencode\footystats.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Footystats fixtures: {len(html)} bytes')

# Look for match cards
matches = re.findall(r'(<div[^>]*class="[^"]*fixture[^"]*"[^>]*>.*?</div>\s*</div>)', html, re.DOTALL)
print(f'Fixture matches: {len(matches)}')

# Look for team names in context
for search in ['Rayo', 'Villarreal', 'Barcelona', 'Real']:
    if search in html:
        pos = html.index(search)
        print(f'\n--- Context for {search} ---')
        print(html[max(0,pos-300):pos+300])
        print()
        break

# Look for odds pattern
odds_values = re.findall(r'(\d+\.\d+)\s*[-–]\s*(\d+\.\d+)\s*[-–]\s*(\d+\.\d+)', html)
print(f'\nOdds patterns found: {len(odds_values)}')
if odds_values:
    print('Sample:', odds_values[:5])
