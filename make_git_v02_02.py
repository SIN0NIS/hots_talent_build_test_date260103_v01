import json
import os
from string import Template

# --- [사용자 설정 구간] ---
json_path = 'herodata_95918_kokr.json' 
img_cdn_base = "https://raw.githubusercontent.com/SIN0NIS/images/main/abilitytalents/"
output_file = 'index.html'
# ------------------------

def generate_html():
    if not os.path.exists(json_path):
        print(f"오류: '{json_path}' 파일을 찾을 수 없습니다.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    hero_list = sorted([{"id": k, "name": v['name']} for k, v in data.items()], key=lambda x: x['name'])
    
    options = []
    for h in hero_list:
        options.append(f'<option value="{h["id"]}">{h["name"]}</option>')
    hero_options_html = "\n".join(options)

    html_skeleton = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>HOTS Build Maker Pro</title>
    <style>
        :root { 
            --primary: #6441a5; 
            --accent: #00d4ff;
            --bg: #0f0f12;
            --card-bg: #1a1a20;
            --selected: #2d2d3d;
            --border: #333;
        }
        body { 
            margin: 0; background: var(--bg); color: #ececec; 
            font-family: 'Pretendard', 'Malgun Gothic', sans-serif; 
            display: flex; flex-direction: column; height: 100vh; 
        }
        
        #header { 
            background: #16161a; padding: 15px; border-bottom: 2px solid var(--primary);
            position: sticky; top: 0; z-index: 100;
        }
        select { 
            width: 100%; padding: 12px; background: #25252b; color: white; 
            border: 1px solid var(--primary); border-radius: 8px; font-size: 16px; 
        }

        #main-content { flex: 1; overflow-y: auto; padding: 10px; padding-bottom: 160px; }
        .hero-name-title { color: var(--accent); font-size: 1.5rem; margin: 10px 0 20px 5px; font-weight: bold; }

        .tier-section { margin-bottom: 25px; }
        .tier-label { 
            font-size: 0.9rem; color: var(--accent); margin-bottom: 8px; 
            padding-left: 5px; font-weight: bold; border-left: 3px solid var(--accent);
        }

        .talent-item {
            display: flex; align-items: flex-start;
            background: var(--card-bg); margin-bottom: 8px; padding: 10px;
            border-radius: 8px; border: 1px solid var(--border);
            cursor: pointer; transition: 0.2s;
        }
        .talent-item.selected { 
            background: var(--selected); border-color: #ffd700;
        }

        .talent-icon { 
            width: 44px; height: 44px; border-radius: 6px; 
            margin-right: 12px; flex-shrink: 0; border: 1px solid #444;
        }
        .talent-info { flex: 1; }
        .talent-name { font-weight: bold; font-size: 0.9rem; color: #fff; margin-bottom: 2px; }
        .talent-desc { font-size: 0.8rem; color: #bbb; line-height: 1.4; word-break: keep-all; }

        /* 하단 고정 빌드 요약창 */
        #footer {
            position: fixed; bottom: 0; width: 100%; background: rgba(10, 10, 15, 0.98);
            backdrop-filter: blur(10px); border-top: 2px solid var(--primary);
            padding: 12px; box-sizing: border-box; z-index: 1000;
            display: flex; flex-direction: column; align-items: center; gap: 10px;
        }
        
        /* 선택된 이미지 나열 구역 */
        #selected-summary {
            display: flex; gap: 6px; justify-content: center; align-items: center;
            min-height: 40px; width: 100%;
        }
        .summary-slot {
            width: 38px; height: 38px; border: 1px solid #333; border-radius: 4px;
            background: #000; display: flex; align-items: center; justify-content: center;
            overflow: hidden;
        }
        .summary-slot img { width: 100%; height: 100%; object-fit: cover; }
        .summary-slot.empty { font-size: 10px; color: #444; }

        #build-code {
            width: 100%; max-width: 450px; background: #222; color: #ffd700;
            border: 1px dashed #555; padding: 8px; border-radius: 4px;
            font-family: monospace; font-size: 0.95rem; text-align: center; cursor: pointer;
        }
    </style>
</head>
<body>
    <div id="header">
        <select onchange="selectHero(this.value)">
            <option value="">영웅을 선택하세요</option>
            $HERO_OPTIONS
        </select>
    </div>

    <div id="main-content">
        <div id="hero-display">
            <p style="text-align:center; color:#555; margin-top:100px;">영웅을 선택해주세요.</p>
        </div>
    </div>

    <div id="footer">
        <div id="selected-summary">
            <div class="summary-slot empty" id="slot-0">1</div>
            <div class="summary-slot empty" id="slot-1">4</div>
            <div class="summary-slot empty" id="slot-2">7</div>
            <div class="summary-slot empty" id="slot-3">10</div>
            <div class="summary-slot empty" id="slot-4">13</div>
            <div class="summary-slot empty" id="slot-5">16</div>
            <div class="summary-slot empty" id="slot-6">20</div>
        </div>
        <div id="build-code" onclick="copyCode()">[빌드 코드 대기중]</div>
    </div>

    <script>
        const hotsData = $JSON_DATA;
        const imgBase = "$IMG_BASE";
        let currentHeroHyperlink = "None";
        let selectedTalents = [0, 0, 0, 0, 0, 0, 0];

        function selectHero(heroId) {
            if(!heroId) return;
            const hero = hotsData[heroId];
            currentHeroHyperlink = hero.hyperlinkId;
            selectedTalents = [0, 0, 0, 0, 0, 0, 0];
            
            // 요약 슬롯 초기화
            for(let i=0; i<7; i++) {
                const slot = document.getElementById('slot-' + i);
                slot.innerHTML = [1,4,7,10,13,16,20][i];
                slot.classList.add('empty');
            }

            let html = '<div class="hero-name-title">' + hero.name + '</div>';
            const levels = Object.keys(hero.talents).sort((a,b) => {
                return parseInt(a.replace(/[^0-9]/g, "")) - parseInt(b.replace(/[^0-9]/g, ""));
            });
            
            levels.forEach((level, idx) => {
                const displayLv = level.replace(/[^0-9]/g, "");
                html += '<div class="tier-section"><div class="tier-label">Level ' + displayLv + '</div>';
                
                hero.talents[level].forEach((t, tIdx) => {
                    const cleanDesc = t.fullTooltip.replace(/<[^>]*>?/gm, "").replace(/'/g, "\\\\'");
                    const iconUrl = imgBase + t.icon;
                    
                    html += `
                        <div class="talent-item group-` + idx + `" onclick="pickTalent(` + idx + `, ` + (tIdx + 1) + `, '` + iconUrl + `', this)">
                            <img class="talent-icon" src="` + iconUrl + `">
                            <div class="talent-info">
                                <div class="talent-name">` + t.name + `</div>
                                <div class="talent-desc">` + cleanDesc + `</div>
                            </div>
                        </div>`;
                });
                html += '</div>';
            });
            document.getElementById("hero-display").innerHTML = html;
            updateCode();
        }

        function pickTalent(tierIdx, talentNum, iconUrl, el) {
            selectedTalents[tierIdx] = talentNum;
            
            // 리스트 UI 업데이트
            document.querySelectorAll(".group-" + tierIdx).forEach(item => item.classList.remove("selected"));
            el.classList.add("selected");
            
            // 하단 요약 아이콘 업데이트
            const slot = document.getElementById('slot-' + tierIdx);
            slot.innerHTML = '<img src="' + iconUrl + '">';
            slot.classList.remove('empty');
            
            updateCode();
        }

        function updateCode() {
            const code = selectedTalents.join("");
            document.getElementById("build-code").innerText = "[T" + code + "," + currentHeroHyperlink + "]";
        }

        function copyCode() {
            const txt = document.getElementById("build-code").innerText;
            if(txt.includes("대기중")) return;
            const temp = document.createElement("textarea");
            document.body.appendChild(temp);
            temp.value = txt;
            temp.select();
            document.execCommand("copy");
            document.body.removeChild(temp);
            alert("복사 완료!");
        }
    </script>
</body>
</html>"""

    t = Template(html_skeleton)
    final_html = t.substitute(
        HERO_OPTIONS=hero_options_html,
        JSON_DATA=json.dumps(data, ensure_ascii=False),
        IMG_BASE=img_cdn_base
    )

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"🎉 하단 요약 바가 추가된 '{output_file}'이 생성되었습니다.")

if __name__ == "__main__":
    generate_html()