import json

with open('foods.json', 'r', encoding='utf-8') as f:
    foods = json.load(f)

html_injection = """
<div class="c" id="food_checklist" style="margin-top:16px">
  <h3 style="margin-top:0; border-bottom:1px solid var(--bd); padding-bottom:8px; display:flex; justify-content:space-between; align-items:center; cursor:pointer;" id="cl_toggle">
    <span>✅ জেলার বিখ্যাত খাবারের চেকলিস্ট</span>
    <span id="cl_arrow">▼</span>
  </h3>
  <div id="cl_container" style="display:none; max-height:400px; overflow-y:auto; padding-right:8px;">
  </div>
</div>
"""

js_injection = """
const FOODS_LIST = """ + json.dumps(foods, ensure_ascii=False) + """;

const clContainer = document.getElementById('cl_container');
document.getElementById('cl_toggle').onclick = () => {
    const isHidden = clContainer.style.display === 'none';
    clContainer.style.display = isHidden ? 'block' : 'none';
    document.getElementById('cl_arrow').textContent = isHidden ? '▲' : '▼';
};

let clHtml = '';
for (const dist in FOODS_LIST) {
    clHtml += `
    <div style="margin-bottom:12px; border:1px solid var(--bd); border-radius:8px; overflow:hidden;">
        <div style="margin:0; border:none; border-radius:0; padding:10px 12px; font-weight:bold; background:color-mix(in srgb, var(--ac) 15%, var(--card)); cursor:pointer; display:flex; justify-content:space-between;" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none'">
            ${dist} <span style="font-size:0.8em; color:var(--mut)">▼</span>
        </div>
        <div style="display:none; padding:8px 12px; background:var(--card);">
            ${FOODS_LIST[dist].map(food => `
                <label style="display:flex; align-items:center; gap:8px; margin-bottom:6px; cursor:pointer;">
                    <input type="checkbox" class="food-cb" data-dist="${dist}" value="${food}">
                    <span>${food}</span>
                </label>
            `).join('')}
        </div>
    </div>`;
}
clContainer.innerHTML = clHtml;

let checkedFoods = JSON.parse(localStorage.getItem('fm_checked_foods') || '{}');

// Map bengali dist names to english
const bnToEnDist = {};
DS.forEach(d => {
    bnToEnDist[d.bn] = d.en;
});

// Fix spelling mismatches between foods.json and DS if any
// "চাঁপাইনবাবগঞ্জ" in foods.json vs "চাঁপাইনবাবগঞ্জ" in DS
// "কক্সবাজার" vs "কক্সবাজার"

document.querySelectorAll('.food-cb').forEach(cb => {
    if (checkedFoods[cb.dataset.dist] && checkedFoods[cb.dataset.dist].includes(cb.value)) {
        cb.checked = true;
    }
    cb.addEventListener('change', (e) => {
        const distBn = cb.dataset.dist;
        const food = cb.value;
        const distEn = bnToEnDist[distBn] || distBn; // Fallback to BN if EN not found
        
        if (!checkedFoods[distBn]) checkedFoods[distBn] = [];
        if (e.target.checked) {
            checkedFoods[distBn].push(food);
            
            // Add to E
            if (distEn) {
                if (!E[distEn]) E[distEn] = {s: 'ate', f: []};
                else if (E[distEn].s !== 'ate') E[distEn].s = 'ate';
                
                if (!E[distEn].f.includes(food)) {
                    E[distEn].f.push(food);
                }
                if (!ord.includes(distEn)) ord.push(distEn);
            }
        } else {
            checkedFoods[distBn] = checkedFoods[distBn].filter(f => f !== food);
            
            // Remove from E
            if (distEn && E[distEn]) {
                E[distEn].f = E[distEn].f.filter(f => f !== food);
                // We keep it in E and ord even if f is empty, as they might have tapped it manually, 
                // but usually if food is unchecked we just leave the district in the list with empty foods.
            }
        }
        localStorage.setItem('fm_checked_foods', JSON.stringify(checkedFoods));
        render();
        persist();
    });
});

restore();render();
</script></body></html>
"""

with open('foodmap.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Insert HTML before <div class="c" id="stats" style="margin-top:16px"></div>
content = content.replace('<div class="c" id="stats" style="margin-top:16px"></div>', html_injection + '<div class="c" id="stats" style="margin-top:16px"></div>')

# Replace the ending
content = content.replace('restore();render();\n</script></body></html>', js_injection)

with open('foodmap.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Injection complete")
