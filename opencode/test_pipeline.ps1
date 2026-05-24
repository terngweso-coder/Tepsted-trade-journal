cd C:\Users\katak\Documents\football-signal-hub
python -c @"
import sys
sys.path.insert(0, '.')
from src.ingestors.jackpot_scraper import JackpotScraper, JACKPOT_PAGES
from src.ingestors.kickoff_enricher import SportSRCKickoffClient, normalize_team, match_team

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

# 3. Verify total jackpot target
total_expected = sum(expected.values())
total_actual = sum(JACKPOT_PAGES[k]['games'] for k in expected if k in JACKPOT_PAGES)
print(f"\n  Total games configured: {total_actual} (expected {total_expected})")

# 4. Test team normalization
print('\n=== Team Normalization Samples ===')
samples = [('Chelsea','Chelsea'),('Man City','Manchester City'),('Tottenham','Tottenham Hotspur'),('Wolves','Wolverhampton'),('Brighton','Brighton & Hove Albion'),('AC Milan','Milan'),('Inter Milan','Inter'),('Barca','Barcelona'),('Roma','AS Roma'),('Leicester','Leicester City')]
for a, b in samples:
    na, nb = normalize_team(a), normalize_team(b)
    m = match_team(a, b)
    print(f"  {a:25s} -> {na:25s} | {b:25s} -> {nb:25s} | match={m}")
all_match = all(match_team(a,b) for a,b in samples)
print(f"  All samples match: {all_match}")

# 5. SportSRC API test
print('\n=== SportSRC API Test ===')
kc = SportSRCKickoffClient()
matches = kc.fetch_all()
print(f"  Total matches: {len(matches)}")
non_ppv = [m for m in matches if not m.get('id','').startswith('ppv-')]
print(f"  Non-PPV matches: {len(non_ppv)}")
if non_ppv:
    m = non_ppv[0]
    print(f"  Sample: {m.get('title','')} date_ms={m.get('date','')}")

# 6. Pipeline scrape test
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

# 7. Kickoff enrichment test
print('\n=== Kickoff Enrichment Test ===')
if predictions:
    kickoff_map = kc.enrich(predictions)
    updated = sum(1 for p in predictions if p.match_id in kickoff_map)
    print(f"  Matched: {updated}/{len(predictions)}")
    if updated:
        sample = next(p for p in predictions if p.match_id in kickoff_map)
        print(f"  Sample: {sample.home_team} vs {sample.away_team} kickoff={sample.kickoff}")
        # Show old placeholder for comparison
        print(f"  New kickoff (EAT): {sample.kickoff.astimezone()}")
    else:
        # Show first few predictions with their current times
        print(f"  No matches found. Showing first 3 predictions:")
        for p in predictions[:3]:
            print(f"    {p.home_team} vs {p.away_team} kickoff={p.kickoff}")

# 8. Lifecycle test
print('\n=== Tournament Lifecycle Test ===')
from src.utils.timezone import is_tournament_concluded, now_eat
if predictions:
    concluded = is_tournament_concluded(predictions)
    print(f"  Tournament concluded: {concluded}")
    if concluded:
        print("  (Expected: old matches from previous round)")
    else:
        print("  (Expected: upcoming/active matches)")

print('\n=== DONE ===')
"@
