import sys
sys.path.insert(0, r'C:\Users\katak\Documents\football-signal-hub')

from src.ingestors.jackpot_scraper import JackpotScraper, JACKPOT_PAGES
from src.ingestors.kickoff_enricher import SportSRCKickoffClient, normalize_team, match_team
from src.utils.timezone import is_tournament_concluded

# 1. Verify all 5 jackpot configs
print('=== Jackpot Configs ===')
for key, cfg in JACKPOT_PAGES.items():
    print(f"  {key:25s} games={cfg['games']:2d}  platform={cfg['platform']:10s} type={cfg['card_type']:10s}")

# 2. Game count verification
print('\n=== Game Count Verification ===')
expected = {'sportpesa_mega':17,'sportpesa_midweek':13,'betika_mega':17,'betika_midweek':15,'betika_sababisha':5}
for key, exp in expected.items():
    actual = JACKPOT_PAGES.get(key, {}).get('games', 0)
    status = 'OK' if actual == exp else 'MISMATCH'
    print(f"  {key:25s} expected={exp:2d} actual={actual:2d} [{status}]")

total_expected = sum(expected.values())
total_actual = sum(JACKPOT_PAGES[k]['games'] for k in expected if k in JACKPOT_PAGES)
print(f"\n  Total games configured: {total_actual} (expected {total_expected})")

# 3. Test team normalization
print('\n=== Team Normalization Samples ===')
samples = [('Chelsea','Chelsea'),('Man City','Manchester City'),('Tottenham','Tottenham Hotspur'),
           ('Wolves','Wolverhampton'),('Brighton','Brighton & Hove Albion'),
           ('AC Milan','Milan'),('Inter Milan','Inter'),('Barcelona','Barcelona'),
           ('Roma','AS Roma'),('Leicester','Leicester City')]
all_ok = True
for a, b in samples:
    na, nb = normalize_team(a), normalize_team(b)
    m = match_team(a, b)
    if not m: all_ok = False
    print(f"  {a:25s} -> {na:25s} | {b:25s} -> {nb:25s} | match={m}")
print(f"  All samples match: {all_ok}")

# 4. SportSRC API test
print('\n=== SportSRC API Test ===')
kc = SportSRCKickoffClient()
matches = kc.fetch_all()
print(f"  Total matches: {len(matches)}")
non_ppv = [m for m in matches if not m.get('id','').startswith('ppv-')]
print(f"  Non-PPV matches: {len(non_ppv)}")
if non_ppv:
    m = non_ppv[0]
    from datetime import datetime, timezone
    dt = datetime.fromtimestamp(m['date']/1000, tz=timezone.utc)
    print(f"  Sample: {m.get('title','')} -> {dt} UTC")

# 5. Pipeline scrape test
print('\n=== Jackpot Scrape Test ===')
platforms = [('sportpesa','mega'),('sportpesa','midweek'),('betika','mega'),('betika','midweek')]
predictions = []
for platform, card_type in platforms:
    try:
        s = JackpotScraper(platform=platform, card_type=card_type)
        p = s.fetch_predictions()
        predictions.extend(p)
        print(f"  {platform}_{card_type}: {len(p)} games")
    except Exception as e:
        print(f"  {platform}_{card_type}: ERROR {e}")

# 6. Kickoff enrichment test
print('\n=== Kickoff Enrichment Test ===')
if predictions:
    kickoff_map = kc.enrich(predictions)
    updated = sum(1 for p in predictions if p.match_id in kickoff_map)
    print(f"  Matched: {updated}/{len(predictions)}")
    if updated:
        sample = next(p for p in predictions if p.match_id in kickoff_map)
        from datetime import timezone, timedelta
        EAT = timezone(timedelta(hours=3))
        print(f"  Sample: {sample.home_team} vs {sample.away_team}")
        print(f"    UTC: {sample.kickoff}")
        print(f"    EAT: {sample.kickoff.astimezone(EAT).strftime('%d/%m %H:%M')} EAT")
    else:
        print(f"  No matches found. First 3 predictions:")
        for p in predictions[:3]:
            print(f"    {p.home_team} vs {p.away_team} kickoff={p.kickoff}")

# 7. Lifecycle test
print('\n=== Tournament Lifecycle Test ===')
if predictions:
    concluded = is_tournament_concluded(predictions)
    print(f"  Tournament concluded: {concluded}")

print('\n=== DONE ===')
