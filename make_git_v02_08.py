import json
import os

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

    html_skeleton = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>HOTS Pro Build Maker</title>
    <style>
        :root { 
            --primary: #6441a5; --accent: #00d4ff; --bg: #0f0f12;
            --card-bg: #1a1a20; --selected: #2d2d3d; --border: #333;
        }
        body { margin: 0; background: var(--bg); color: #ececec; font-family: 'Pretendard', sans-serif; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        #header { background: #16161a; padding: 10px; border-bottom: 2px solid var(--primary); flex-shrink: 0; }
        .search-container { position: relative; width: 100%; }
        #hero-search { width: 100%; padding: 10px; background: #25252b; color: white; border: 1px solid var(--primary); border-radius: 6px; font-size: 15px; box-sizing: border-box; outline: none; }
        #search-results { position: absolute; top: 45px; left: 0; width: 100%; background: #25252b; border: 1px solid var(--primary); max-height: 300px; overflow-y: auto; display: none; z-index: 110; }
        .result-item { padding: 10px; cursor: pointer; border-bottom: 1px solid #333; display: flex; justify-content: space-between; }
        .result-item:hover { background: var(--primary); }
        #main-content { flex: 1; overflow-y: auto; padding: 10px; padding-bottom: 160px; }
        .tier-row { display: flex; align-items: stretch; background: var(--card-bg); margin-bottom: 6px; border-radius: 6px; border: 1px solid var(--border); height: 90px; }
        .tier-label { width: 35px; background: #222; display: flex; align-items: center; justify-content: center; font-weight: bold; color: var(--accent); font-size: 0.75rem; border-right: 1px solid var(--border); flex-shrink: 0; }
        .tier-icons-area { display: flex; align-items: center; gap: 4px; padding: 8px; background: #1a1a20; flex-shrink: 0; border-right: 1px solid var(--border); }
        .talent-icon { width: 40px; height: 40px; border-radius: 4px; border: 2px solid #444; cursor: pointer; transition: 0.1s; background: #000; }
        .talent-icon.selected { border-color: #ffd700; box-shadow: 0 0 8px rgba(255, 215, 0, 0.4); transform: scale(1.05); }
        .tier-desc-area { flex: 1; padding: 10px; font-size: 0.8rem; color: #ddd; line-height: 1.5; background: #141418; overflow-y: auto; word-break: keep-all; }
        .talent-title-in-desc { color: var(--accent); font-weight: bold; margin-bottom: 4px; font-size: 0.85rem; border-bottom: 1px solid #333; display: inline-block; padding-bottom: 2px; }
        .growth-text { color: #00ff00; font-weight: bold; font-size: 0.75rem; } /* 성장 수치 강조용 스타일 */
        #footer { position: fixed; bottom: 0; width: 100%; background: rgba(10, 10, 15, 0.98); border-top: 2px solid var(--primary); padding: 10px; box-sizing: border-box; display: flex; flex-direction: column; align-items: center; gap: 8px; }
        #selected-summary { display: flex; gap: 5px; }
        .summary-slot { width: 34px; height: 34px; border: 1px solid #333; border-radius: 4px; background: #000; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #444; overflow: hidden; }
        .summary-slot img { width: 100%; height: 100%; object-fit: cover; }
        #build-code { width: 100%; max-width: 400px; background: #222; color: #ffd700; border: 1px dashed #555; padding: 6px; border-radius: 4px; font-family: monospace; font-size: 0.9rem; text-align: center; cursor: pointer; }
    </style>
</head>
<body>
    <div id="header">
        <div class="search-container">
            <input type="text" id="hero-search" placeholder="영웅 검색 또는 리스트 보기" oninput="filterHeroes()" onfocus="filterHeroes()" onclick="this.select()">
            <div id="search-results"></div>
        </div>
    </div>
    <div id="main-content"><div id="hero-display"></div></div>
    <div id="footer">
        <div id="selected-summary"><div class="summary-slot empty" id="slot-0">1</div><div class="summary-slot empty" id="slot-1">4</div><div class="summary-slot empty" id="slot-2">7</div><div class="summary-slot empty" id="slot-3">10</div><div class="summary-slot empty" id="slot-4">13</div><div class="summary-slot empty" id="slot-5">16</div><div class="summary-slot empty" id="slot-6">20</div></div>
        <div id="build-code" onclick="copyCode()">[영웅 선택 대기중]</div>
    </div>

    <script>
        const hotsData = __JSON_DATA__;
        const imgBase = "__IMG_BASE__";
        let currentHeroHyperlink = "None";
        let selectedTalents = [0, 0, 0, 0, 0, 0, 0];

        // 초성 분리 및 영웅 리스트업 로직 (기존과 동일)
        function getChoseong(str) {
            const choseong = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"];
            let result = "";
            for(let i=0; i<str.length; i++) {
                const code = str.charCodeAt(i) - 44032;
                if(code > -1 && code < 11172) result += choseong[Math.floor(code / 588)];
                else result += str.charAt(i);
            }
            return result;
        }

        const heroList = Object.keys(hotsData).map(id => ({
            id: id, name: hotsData[id].name, choseong: getChoseong(hotsData[id].name)
        })).sort((a, b) => a.name.localeCompare(b.name, 'ko'));

        function filterHeroes() {
            const query = document.getElementById("hero-search").value.toLowerCase();
            const resultsDiv = document.getElementById("search-results");
            const filtered = query ? heroList.filter(h => h.name.toLowerCase().includes(query) || h.choseong.includes(query)) : heroList;
            if(filtered.length > 0) {
                let html = "";
                for(let i=0; i<filtered.length; i++) {
                    const h = filtered[i];
                    html += '<div class="result-item" onclick="selectHero(\\'' + h.id + '\\')"><span>' + h.name + '</span><span style="color:#666; font-size:0.75rem;">' + h.choseong + '</span></div>';
                }
                resultsDiv.innerHTML = html;
                resultsDiv.style.display = "block";
            } else { resultsDiv.style.display = "none"; }
        }

        // ★ [핵심] 성장 수치 변환 함수 ★
        function formatDescription(desc) {
            // ~~0.04~~ 패턴을 찾아서 (+4%) 형태로 변환
            return desc.replace(/~~([0-9.]+)~~/g, function(match, p1) {
                const percent = Math.round(parseFloat(p1) * 100);
                return '<span class="growth-text">(+' + percent + '%)</span>';
            });
        }

        function selectHero(heroId) {
            const hero = hotsData[heroId];
            document.getElementById("hero-search").value = hero.name;
            document.getElementById("search-results").style.display = "none";
            currentHeroHyperlink = hero.hyperlinkId;
            selectedTalents = [0, 0, 0, 0, 0, 0, 0];
            for(let i=0; i<7; i++) {
                const slot = document.getElementById('slot-' + i);
                slot.innerHTML = [1,4,7,10,13,16,20][i];
                slot.classList.add('empty');
            }
            let html = '<div style="color:var(--accent); font-weight:bold; margin: 5px 0 10px 5px; font-size:1.1rem;">' + hero.name + '</div>';
            const levels = Object.keys(hero.talents).sort((a,b) => parseInt(a.replace(/[^0-9]/g, "")) - parseInt(b.replace(/[^0-9]/g, "")));
            levels.forEach((level, idx) => {
                const lvNum = level.replace(/[^0-9]/g, "");
                html += '<div class="tier-row">' +
                        '  <div class="tier-label">' + lvNum + '</div>' +
                        '  <div class="tier-icons-area">';
                hero.talents[level].forEach((t, tIdx) => {
                    const cleanDesc = t.fullTooltip.replace(/<[^>]*>?/gm, "").replace(/'/g, "\\\\'");
                    const iconUrl = imgBase + t.icon;
                    html += '<img class="talent-icon t-icon-' + idx + '" src="' + iconUrl + '" onclick="pickCompact(' + idx + ', ' + (tIdx + 1) + ', \\'' + t.name + '\\', \\'' + cleanDesc + '\\', \\'' + iconUrl + '\\', this)">';
                });
                html += '  </div>' +
                        '  <div class="tier-desc-area" id="desc-line-' + idx + '"><span style="color:#444">...</span></div>' +
                        '</div>';
            });
            document.getElementById("hero-display").innerHTML = html;
            updateCode();
        }

        function pickCompact(tierIdx, talentNum, name, desc, iconUrl, el) {
            selectedTalents[tierIdx] = talentNum;
            const descArea = document.getElementById('desc-line-' + tierIdx);
            
            // 변환 함수 적용 후 출력
            const formattedDesc = formatDescription(desc);
            descArea.innerHTML = '<div class="talent-title-in-desc">' + name + '</div><div class="talent-body">' + formattedDesc + '</div>';
            
            descArea.scrollTop = 0;
            document.querySelectorAll(".t-icon-" + tierIdx).forEach(img => img.classList.remove("selected"));
            el.classList.add("selected");
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
            alert("빌드 코드가 복사되었습니다!");
        }

        document.addEventListener("click", (e) => {
            if(!e.target.closest(".search-container")) {
                document.getElementById("search-results").style.display = "none";
            }
        });
    </script>
</body>
</html>"""

    final_html = html_skeleton.replace("__JSON_DATA__", json.dumps(data, ensure_ascii=False))
    final_html = final_html.replace("__IMG_BASE__", img_cdn_base)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print(f"🎉 성장 수치 변환 기능이 적용된 '{output_file}'이 생성되었습니다.")

if __name__ == "__main__":
    generate_html()