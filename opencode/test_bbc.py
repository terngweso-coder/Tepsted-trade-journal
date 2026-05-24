import sys
sys.path.insert(0, r'C:\Users\katak\Documents\football-signal-hub')
import cloudscraper, json, re
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper(browser={'browser':'chrome','platform':'windows','mobile':False})
r = scraper.get('https://www.bbc.com/sport/football/scores-fixtures/2026-05-17', timeout=20)
print(f'Status: {r.status_code}')

if r.status_code == 200:
    soup = BeautifulSoup(r.text, 'lxml')
    
    # Check JSON-LD
    ld_count = 0
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get('@type') == 'SportsEvent':
                        ld_count += 1
                        home = item.get('competitor', [{}])[0].get('name','') if item.get('competitor') else ''
                        away = item.get('competitor', [{}])[1].get('name','') if item.get('competitor') else ''
                        score = item.get('result', {}).get('score','') if item.get('result') else ''
                        print(f'  [{ld_count}] {home} vs {away}: {score}')
        except:
            pass
    print(f'Total LD SportsEvents: {ld_count}')
    
    # Check for data-attributes or other common patterns
    match_elements = soup.select('[data-testid^="match"]')
    print(f'Match elements by data-testid: {len(match_elements)}')
    
    # Check for embedded JSON in other patterns
    for script in soup.find_all('script'):
        if script.string and '"score"' in script.string[:200]:
            print(f'Script with scores: {len(script.string)} chars, starts: {script.string[:100]}')
            break
    
    # Check for orbit data (BBC uses orbit)
    for script in soup.find_all('script', id=re.compile(r'orbit', re.I)):
        print(f'Orbit script found: {len(script.string)} chars')
        break
    
    # Just dump the first 2000 chars of relevant HTML
    scores_section = soup.find(string=re.compile(r'Scores|Fixtures'))
    if scores_section:
        parent = scores_section.parent
        if parent:
            print(f'Found section header: {scores_section[:50]}')
