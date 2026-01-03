import json
import os

# --- [설정 구간] ---
json_path = 'herodata_95918_kokr.json' 
img_cdn_base = "https://raw.githubusercontent.com/SIN0NIS/images/main/abilitytalents/"
output_file = 'index.html'
# ------------------

def generate_html():
    if not os.path.exists(json_path):
        print(f"오류: '{json_path}' 파일을 찾을 수 없습니다.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    hero_list = sorted([{"id": k, "name": v['name'], "hId": v.get('hyperlinkId', k)} for k, v in data.items() if 'name' in v], key=lambda x: x['name'])

    html_head = r"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>히오스 빌드 메이커 Pro</title>
    <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
    <style>
        :root { --p: #a333ff; --bg: #0b0b0d; --card: #16161a; --blue: #00d4ff; --gold: #ffd700; --green: #00ff00; }
        body { margin: 0; background: var(--bg); color: white; font-family: sans-serif; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        #header { padding: 10px; background: #1a1a1e; border-bottom: 1px solid #333; flex-shrink: 0; position: relative; }
        .search-group { display: flex; gap: 8px; }
        .search-box { flex: 1; padding: 12px; background: #222; color: white; border: 1px solid var(--p); border-radius: 6px; font-size: 14px; outline: none; }
        .load-btn { padding: 0 15px; background: var(--p); color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; }
        
        #hero-list-dropdown { position: absolute; width: calc(100% - 20px); max-height: 300px; background: #2a2a2a; overflow-y: auto; z-index: 3000; border-radius: 4px; display: none; border: 1px solid var(--p); margin-top: 5px; }
        .hero-item { padding: 12px; border-bottom: 1px solid #333; cursor: pointer; }
        .hero-item:hover { background: var(--p); }

        #capture-area { flex: 1; display: flex; flex-direction: column; overflow-y: auto; padding-bottom: 220px; }
        #hero-stat-container { background: #1a1a20; margin: 10px; padding: 15px; border-radius: 8px; border: 1px solid #333; display: none; }
        #hero-title-area { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
        #hero-info-title { font-size: 20px; font-weight: bold; color: var(--p); }
        .role-tag { font-size: 11px; color: var(--blue); border: 1px solid var(--blue); padding: 2px 6px; border-radius: 4px; }
        
        #level-control { background: #25252b; padding: 10px; border-radius: 6px; margin-bottom: 12px; display: flex; align-items: center; gap: 15px; }
        #level-slider { flex: 1; accent-color: var(--p); }
        #level-display-group { display: flex; flex-direction: column; align-items: center; min-width: 90px; }
        #level-display { font-weight: bold; color: var(--gold); font-size: 16px; }
        #level-growth-total { font-size: 10px; color: var(--green); }

        .stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
        .stat-item { background: #111; padding: 8px; border-radius: 4px; font-size: 12px; display: flex; flex-direction: column; gap: 2px; }
        .stat-header { display: flex; justify-content: space-between; align-items: center; }
        .stat-label { color: #888; }
        .stat-value { color: #fff; font-weight: bold; font-size: 13px; }
        .scale-info { color: var(--green); font-size: 10px; }

        .tier-row { display: flex; align-items: center; background: var(--card); padding: 8px 10px; border-radius: 6px; border-left: 5px solid var(--p); gap: 10px; min-height: 65px; margin: 3px 5px; }
        .tier-label { color: var(--blue); font-weight: bold; width: 35px; flex-shrink: 0; font-size: 12px; text-align: center; }
        .talent-icons { display: flex; gap: 6px; flex-shrink: 0; }
        .t-icon { width: 40px; height: 40px; border: 1px solid #444; cursor: pointer; border-radius: 5px; background: #000; }
        .t-icon.selected { border-color: var(--gold); box-shadow: 0 0 10px var(--gold); transform: scale(1.1); z-index: 10; }
        .t-info-display { flex: 1; font-size: 11px; color: #ccc; line-height: 1.4; padding-left: 10px; border-left: 1px solid #444; height: 46px; overflow-y: auto; }
        .t-info-name { font-size: 13px; font-weight: bold; color: #fff; display: block; margin-bottom: 2px; }

        #footer { position: fixed; bottom: 0; width: 100%; background: rgba(0,0,0,0.95); border-top: 2px solid var(--p); padding: 10px; box-sizing: border-box; display: flex; flex-direction: column; align-items: center; gap: 8px; backdrop-filter: blur(10px); z-index: 1500; }
        #selected-summary { display: flex; gap: 6px; justify-content: center; min-height: 40px; }
        .summary-img { width: 34px; height: 34px; border: 1px solid var(--gold); border-radius: 4px; background: #111; }
        .btn-group { display: flex; gap: 10px; width: 98%; }
        #build-code { flex: 3; font-size: 15px; color: var(--gold); background: #1a1a1a; padding: 10px; border-radius: 6px; border: 1px dashed var(--gold); text-align: center; cursor: pointer; white-space: nowrap; overflow: hidden; }
        #btn-capture { flex: 1; background: var(--p); color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div id="header">
        <div class="search-group">
            <input type="text" id="hero-search" class="search-box" placeholder="영웅 검색 또는 코드 입력..." onclick="showList()" oninput="handleSearch(this.value)">
            <button class="load-btn" onclick="loadFromCode()">코드 불러오기</button>
        </div>
        <div id="hero-list-dropdown"></div>
    </div>
    
    <div id="capture-area">
        <div id="hero-stat-container">
            <div id="hero-title-area">
                <div id="hero-info-title">영웅 이름</div>
                <div id="hero-role-badge" class="role-tag">역할군</div>
            </div>
            <div id="level-control">
                <label style="font-size:11px; color:#888;">LV</label>
                <input type="range" id="level-slider" min="1" max="30" value="1" oninput="updateLevel(this.value)">
                <div id="level-display-group">
                    <span id="level-display">LV 1</span>
                    <span id="level-growth-total">(+0.00%)</span>
                </div>
            </div>
            <div class="stat-grid" id="stat-grid"></div>
        </div>
        <div id="main-content"></div>
    </div>

    <div id="footer">
        <div id="selected-summary"></div>
        <div class="btn-group">
            <div id="build-code" onclick="copyCode()">[영웅을 선택하세요]</div>
            <button id="btn-capture" onclick="takeScreenshot()">📸 저장</button>
        </div>
    </div>
    <script>
"""

    html_script = r"""
        const hotsData = __JSON_DATA__;
        const heroList = __HERO_LIST__;
        const imgBase = "__IMG_BASE__";

        let currentHeroData = null;
        let currentLevel = 1;
        let selectedTalents = []; 
        let currentTalentNodes = [];

        function getChosung(str) {
            const cho = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"];
            let result = "";
            for(let i=0; i<str.length; i++) {
                let code = str.charCodeAt(i) - 44032;
                if(code > -1 && code < 11172) result += cho[Math.floor(code/588)];
                else result += str.charAt(i);
            }
            return result;
        }

        function handleSearch(val) {
            const v = val.replace(/\s/g, "").toLowerCase();
            if (v.includes("[t")) return; // 코드 입력 중이면 리스트 안 띄움
            const choV = getChosung(v);
            const filtered = heroList.filter(h => {
                const name = h.name.replace(/\s/g, "").toLowerCase();
                return name.includes(v) || getChosung(name).includes(choV);
            });
            renderList(filtered);
            document.getElementById("hero-list-dropdown").style.display = "block";
        }

        // 빌드 코드 분석 및 로딩 기능 [T123,HeroName]
        function loadFromCode() {
            const input = document.getElementById("hero-search").value;
            const match = input.match(/\[T(\d+),(.+?)\]/);
            if (!match) return alert("올바른 코드 형식이 아닙니다. 예: [T123,Hogger]");
            
            const codeTalents = match[1].split("");
            const heroHId = match[2];
            
            // hyperlinkId 매칭 영웅 찾기
            const heroEntry = Object.entries(hotsData).find(([id, data]) => data.hyperlinkId === heroHId);
            if (!heroEntry) return alert("해당 영웅을 찾을 수 없습니다.");
            
            selectHero(heroEntry[0], codeTalents);
        }

        function calcFromLv1(base, scale, level) {
            if (!base) return 0;
            return (base * Math.pow(1 + (scale || 0.04), level - 1)).toFixed(1);
        }

        function updateLevel(lv) {
            currentLevel = parseInt(lv);
            document.getElementById("level-display").innerText = "LV " + currentLevel;
            const totalGrowth = (Math.pow(1.04, currentLevel - 1) - 1) * 100;
            document.getElementById("level-growth-total").innerText = "(+" + totalGrowth.toFixed(2) + "%)";
            if(currentHeroData) {
                renderStats();
                refreshTalentTooltips();
            }
        }

        function renderStats() {
            const h = currentHeroData;
            const grid = document.getElementById("stat-grid");
            const life = h.life;
            const energy = h.energy || { amount: 0, regenRate: 0, type: "마나" };
            const weapon = (h.weapons && h.weapons[0]) ? h.weapons[0] : { damage: 0, range: 0, period: 1, damageScale: 0.04 };

            const stats = [
                { label: "체력", val: calcFromLv1(life.amount, life.scale, currentLevel), scale: life.scale },
                { label: energy.type, val: calcFromLv1(energy.amount, 0.04, currentLevel), scale: 0.04 },
                { label: energy.type + " 재생", val: calcFromLv1(energy.regenRate, 0.04, currentLevel), scale: 0.04 },
                { label: "공격력", val: calcFromLv1(weapon.damage, weapon.damageScale, currentLevel), scale: weapon.damageScale },
                { label: "공격 주기", val: weapon.period + "초", scale: 0 },
                { label: "사거리", val: weapon.range, scale: 0 },
                { label: "충돌 범위", val: h.innerRadius, scale: 0 },
                { label: "피격 범위", val: h.radius, scale: 0 }
            ];

            grid.innerHTML = stats.map(s => `
                <div class="stat-item">
                    <div class="stat-header">
                        <span class="stat-label">${s.label}</span>
                        ${s.scale > 0 ? `<span class="scale-info">(+${(s.scale*100).toFixed(2)}%)</span>` : ''}
                    </div>
                    <span class="stat-value">${s.val}</span>
                </div>
            `).join("");
        }

        function selectHero(heroId, codeTalents = null) {
            document.getElementById("hero-list-dropdown").style.display = "none";
            const hero = hotsData[heroId];
            currentHeroData = hero;
            document.getElementById("hero-search").value = hero.name;
            document.getElementById("hero-info-title").innerText = hero.name;
            document.getElementById("hero-role-badge").innerText = hero.expandedRole || "미분류";
            document.getElementById("hero-stat-container").style.display = "block";
            
            const levels = Object.keys(hero.talents)
                .filter(lv => hero.talents[lv] && hero.talents[lv].length > 0)
                .sort((a,b) => parseInt(a.replace(/[^0-9]/g, "")) - parseInt(b.replace(/[^0-9]/g, "")));
            
            selectedTalents = new Array(levels.length).fill(0);
            currentTalentNodes = [];
            
            let html = '';
            levels.forEach((level, idx) => {
                let lvNum = level.replace(/[^0-9]/g, "");
                if (hero.hyperlinkId === "Chromie") {
                    const chromieLevels = ["1", "2", "5", "8", "11", "14", "18"];
                    if (chromieLevels[idx]) lvNum = chromieLevels[idx];
                }
                currentTalentNodes.push(hero.talents[level]);
                html += `<div class="tier-row"><div class="tier-label">${lvNum}LV</div><div class="talent-icons">`;
                hero.talents[level].forEach((t, tIdx) => {
                    html += `<img src="${imgBase}${t.icon}" class="t-icon t-row-${idx} t-node-${idx}-${tIdx+1}" onclick="toggleTalent(${idx}, ${tIdx+1}, this)">`;
                });
                html += `</div><div class="t-info-display" id="desc-${idx}">특성을 선택하세요.</div></div>`;
            });
            document.getElementById("main-content").innerHTML = html;
            
            // 코드로부터 특성 자동 선택
            if (codeTalents) {
                codeTalents.forEach((tVal, idx) => {
                    const val = parseInt(tVal);
                    if (val > 0) {
                        const target = document.querySelector(`.t-node-${idx}-${val}`);
                        if (target) toggleTalent(idx, val, target);
                    }
                });
            }

            renderStats();
            updateUI();
        }

        function toggleTalent(tierIdx, talentNum, el) {
            const infoBox = document.getElementById("desc-"+tierIdx);
            if (selectedTalents[tierIdx] === talentNum) {
                selectedTalents[tierIdx] = 0;
                el.classList.remove("selected");
                infoBox.innerHTML = "특성을 선택하세요.";
            } else {
                selectedTalents[tierIdx] = talentNum;
                document.querySelectorAll(".t-row-"+tierIdx).forEach(img => img.classList.remove("selected"));
                el.classList.add("selected");
                const t = currentTalentNodes[tierIdx][talentNum-1];
                infoBox.innerHTML = `<span class="t-info-name">${t.name}</span><span>${t.fullTooltip.replace(/<[^>]*>?/gm, "")}</span>`;
            }
            updateUI();
        }

        function updateUI() {
            const summary = selectedTalents.map((tIdx, tier) => {
                if(tIdx === 0) return `<div class="summary-placeholder"></div>`;
                const t = currentTalentNodes[tier][tIdx-1];
                return `<img src="${imgBase}${t.icon}" class="summary-img">`;
            }).join("");
            document.getElementById("selected-summary").innerHTML = summary;
            document.getElementById("build-code").innerText = "[T" + selectedTalents.join("") + "," + (currentHeroData ? currentHeroData.hyperlinkId : "") + "]";
        }

        function renderList(list) {
            document.getElementById("hero-list-dropdown").innerHTML = list.map(h => 
                `<div class="hero-item" onclick="selectHero('${h.id}')">${h.name}</div>`
            ).join("");
        }
        function showList() { document.getElementById("hero-list-dropdown").style.display = "block"; renderList(heroList); }
        function copyCode() {
            const txt = document.getElementById("build-code").innerText;
            const temp = document.createElement("textarea");
            document.body.appendChild(temp); temp.value = txt; temp.select();
            document.execCommand("copy"); document.body.removeChild(temp);
            alert("복사 완료!");
        }
        function takeScreenshot() {
            html2canvas(document.getElementById("capture-area"), { useCORS: true, backgroundColor: "#0b0b0d" }).then(canvas => {
                const link = document.createElement('a');
                link.download = "build.png"; link.href = canvas.toDataURL(); link.click();
            });
        }
    </script>
</body>
</html>"""

    full_html = html_head + html_script
    full_html = full_html.replace("__JSON_DATA__", json.dumps(data, ensure_ascii=False))
    full_html = full_html.replace("__HERO_LIST__", json.dumps(hero_list, ensure_ascii=False))
    full_html = full_html.replace("__IMG_BASE__", img_cdn_base)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"🎉 마나 성장 및 코드 불러오기 기능 완료: '{output_file}' 생성!")

if __name__ == "__main__":
    generate_html()