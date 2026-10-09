import json
import re

with open('foodmap.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

ds_match = re.search(r'"dist":\[(.*?)\]\};', html_content)
dist_str = '[' + ds_match.group(1) + ']'
dist_list = json.loads(dist_str)

bns = [d['bn'] for d in dist_list]
print("Bangla names in DS:", bns)
