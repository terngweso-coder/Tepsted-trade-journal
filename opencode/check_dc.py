import json, os
path = r'C:\Users\katak\Documents\football-signal-hub\output'
files = sorted([x for x in os.listdir(path) if x.startswith('signals_') and x.endswith('.json')])
with open(os.path.join(path, files[-1])) as f:
    data = json.load(f)

print(f"Total: {len(data)} signals")
print(f"With double_chance: {sum(1 for s in data if s.get('double_chance'))}")
print(f"With home_prob: {sum(1 for s in data if s.get('home_prob'))}")
print()

for s in data[:5]:
    dc = s.get('double_chance', '')
    hp = s.get('home_prob', '')
    dp = s.get('draw_prob', '')
    ap = s.get('away_prob', '')
    print(f'{s["home_team"][:16]:16} vs {s["away_team"][:16]:16}  pred={s["prediction"]}  dc={dc}  probs=H:{hp} D:{dp} A:{ap}')
