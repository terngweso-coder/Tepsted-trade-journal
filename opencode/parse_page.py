import re
with open(r'C:\Users\katak\AppData\Local\Temp\opencode\page.html', encoding='utf-8') as f:
    text = f.read()

# Find all <ol> (ordered lists) and their preceding content
parts = re.split(r'(<ol[^>]*>)', text)
for i, part in enumerate(parts[:10]):
    print(f"--- [{i}] {len(part)} chars ---")
    print(part[:300])
    print()

# Find content between <li> tags that might have odds
lis = re.findall(r'<li[^>]*>(.*?)</li>', text, re.DOTALL)
print(f"\nTotal <li> items: {len(lis)}")
for li in lis[:3]:
    print(re.sub(r'<[^>]+>', '', li).strip()[:150])
