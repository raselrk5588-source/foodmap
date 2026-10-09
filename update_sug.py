import json
import re

with open('foods.json', 'r', encoding='utf-8') as f:
    foods_bn = json.load(f)

with open('foodmap.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

ds_match = re.search(r'"dist":\[(.*?)\]\};', html_content)
dist_str = '[' + ds_match.group(1) + ']'
dist_list = json.loads(dist_str)

bn_to_en = {d['bn']: d['en'] for d in dist_list}

corrections = {
    'মুন্সীগঞ্জ': 'মুন্সিগঞ্জ',
    'নারায়ণগঞ্জ': 'নারায়াণগঞ্জ',
    'রাজবাড়ী': 'রাজবাড়ি',
    'কক্সবাজার': 'কক্স বাজার',
    'রাঙামাটি': 'রাঙ্গামাটি',
    'নেত্রকোনা': 'নেত্রকোণা',
    'চাঁপাইনবাবগঞ্জ': 'নবাবগঞ্জ'
}

new_sug = {}
for bn_name, foods in foods_bn.items():
    corrected_bn = corrections.get(bn_name, bn_name)
    en_name = bn_to_en.get(corrected_bn)
    if en_name:
        new_sug[en_name] = foods
    else:
        print(f"Still missing: {bn_name} ({corrected_bn})")

new_sug_str = "const SUG=" + json.dumps(new_sug, ensure_ascii=False)
new_content = re.sub(r'const SUG=\{.*?\};', new_sug_str + ';', html_content, count=1)

with open('foodmap.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("SUG updated successfully!")
