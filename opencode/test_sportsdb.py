import sys, time
sys.path.insert(0, r'C:\Users\katak\Documents\football-signal-hub')
from src.ingestors.thesportsdb_client import TheSportsDBClient
import cloudscraper

# Test with delays
scraper = cloudscraper.create_scraper(browser={'browser':'chrome','platform':'windows','mobile':False})

teams = ['Chelsea', 'Liverpool', 'Arsenal', 'Manchester City', 'Manchester United']
for team in teams:
    print(f'Fetching {team}...')
    try:
        r = scraper.get(f'https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={team}', timeout=15)
        print(f'  Status: {r.status_code}')
        if r.status_code == 200:
            data = r.json()
            t = data.get('teams', [{}])[0]
            team_id = t.get('idTeam', '')
            print(f'  Found: {t.get("strTeam")} (ID: {team_id})')
            if team_id:
                time.sleep(3)
                r2 = scraper.get(f'https://www.thesportsdb.com/api/v1/json/3/eventslast.php?id={team_id}', timeout=15)
                print(f'  Events status: {r2.status_code}')
                if r2.status_code == 200:
                    ev_data = r2.json()
                    results = ev_data.get('results', [])
                    print(f'  Last {len(results)} results:')
                    for ev in results[:3]:
                        print(f'    {ev.get("strHomeTeam")} {ev.get("intHomeScore")}-{ev.get("intAwayScore")} {ev.get("strAwayTeam")}')
        elif r.status_code == 429:
            print(f'  Rate limited, waiting 10s...')
            time.sleep(10)
    except Exception as e:
        print(f'  Error: {e}')
    time.sleep(2)
