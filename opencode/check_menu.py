import json, os
path = r'C:\Users\katak\Documents\football-signal-hub\output'
fs = sorted([f for f in os.listdir(path) if f.startswith('menu_') and f.endswith('.json')], reverse=True)
d = json.load(open(os.path.join(path, fs[0])))
print("Tactical Slip:")
for i, s in enumerate(d.get('tactical_double', [])):
    print(f"  {i+1}. {s['home_team']} vs {s['away_team']} pred={s['prediction']} conf={s['avg_confidence']} dc={s.get('double_chance','')}")
print(f"\nMetric Focus: {len(d.get('metric_focus', []))} picks")
for m in d.get('metric_focus', []):
    print(f"  {m['home_team']} vs {m['away_team']} tags={m.get('tags',[])}")
