# HW10 — 真實執行、檢查及修正紀錄

**檢查日期：** 2026-11-23（Asia/Taipei）  
**檢查範圍：** 使用者提供的 10 篇 PDF、HW9 三篇既有論文與其投影片、10 個 Wiki 概念、14 張 HTML 教學投影片。  
**原則：** 僅列實際執行過的測試；公開 GitHub Pages 的正式網址尚未提供，所以未宣稱線上部署成功。

## 1. 驗證結果摘要

| Gate / 測試 | 執行方式 | 實際結果 | 狀態 |
|---|---|---|---|
| 來源 PDF 讀取與一致性 | `python tools/ingest_local.py /private/papers --check` | S01–S10 全部符合 SHA256、頁數與可擷取字數；總計 **122 頁** | PASS |
| Wiki 出處與雙向連結 | `python tools/validate_project.py` | 10 篇來源、10 個概念、14 張投影片、3 筆 HW9 論文及既有投影片檔案皆通過 | PASS |
| 簡報生成一致性 | `python tools/build_slides.py --check` | `slides.html` 與 `slide-plan.json` 一致 | PASS |
| JS 語法檢查 | `python tools/run_workflow.py`（包含 `node --check`） | 未回報語法錯誤 | PASS |
| 故障注入：未知來源 | `python tools/validate_project.py --inject-bad-source` | 人為加入 `S99`，檢查器成功拒絕 | PASS（預期攔截） |
| 離線 Chromium DOM 互動測試 | `python tools/browser_smoke.py` | **15 項均通過**：Wiki 來源與概念渲染／查詢、簡報上下一頁／方向鍵／測驗、手機橫向溢出等 | PASS |
| GitHub Pages 正式 HTTP 站台 | 尚未部署至使用者 Repository | 需要使用者上傳後，於真實網址測試 | 待確認 |
| 真實手機 Safari / Android | 未在實體裝置測試 | 需使用者開站確認 | 待確認 |

**瀏覽器測試方法限制：** 此環境的 Chromium 拒絕直接開啟 `http://127.0.0.1` 和 `file://`（`ERR_BLOCKED_BY_ADMINISTRATOR`）。為了仍能檢查 UI，改為 `page.set_content` 注入**本專案實際 HTML / CSS / JS**，Wiki 的兩份 JSON 以本機原始內容模擬 `fetch()`。這證明程式的部分 DOM 與互動行為，但**不等於**端對端 HTTP 部署測試。瀏覽器測試腳本保留於完整開發封存版 ZIP；GitHub 100 檔精簡版不包含該非部署必要腳本；此處保留真實結果紀錄。

## 2. 一次可追溯的失敗 → 修改 → 重新測試

| 問題編號 | 起初在哪個節點發現 | 實際錯誤 | 修正前結果 | 檢查提前到 | 修正內容 | 重新測試 |
|---|---|---|---|---|---|---|
| F01 | HTML 前端 / 手機版版面檢查 | 原 HW9 `.slide-stage` 保留 `aspect-ratio:16/9`，與 HW10 600px 最小高度交互作用，導致 **390px 手機視窗的網頁寬度達 1086px** | FAIL | 新舊 CSS 樣式整合時就測 390px 視窗，不等完成所有內容 | 只在 `.slides-root .slide-stage` 覆寫 `aspect-ratio:auto; width:100%; min-width:0`，避免破壞 HW9 原投影片縮圖 | PASS；390px 視窗不再整頁橫向溢出 |
| F02 | 教學簡報 / 教學設計檢視 | 測驗投影片的提示先寫「正確答案：B」，學習者未點按查看答案前就看到解答 | FAIL | 移至 `slide-plan.json` 的教學大綱驗證，在生成 HTML 前檢查 | 更新 `slide-plan.json` 的提示，重新執行 `python tools/build_slides.py --write`；驗證器增加不得含「正確答案」的測驗提示規則 | PASS；只在按下「檢查我的答案」後顯示答案 |
| F03 | 文件驗證 / README 證據 | 初次整體結構檢查尚未要求 `docs/test-report.md`，可能在沒有真實測試紀錄時也得到通過 | 缺口被發現 | 在 `tools/validate_project.py` 的驗收項目加入 README、測試紀錄及 Wiki Markdown 頁面的存在性檢查 | 補齊本紀錄並強化驗證器 | PASS；故意移除時將無法通過 |

## 3. 三個 Loop 如何執行

**Loop 1 — 來源檢查。** PDF 若與 manifest 的雜湊、頁數或文字量不符，就回到私有來源資料夾重新取得／解析，不把不一致版本標成 ingest 成功。實際的十篇來源比較均通過。

**Loop 2 — Wiki／引用檢查。** 在 HTML 生成之前檢查 DOI 格式、來源 ID、PDF 證據頁碼、概念雙向關聯，避免簡報引用不存在的研究。曾以 S99 故障注入驗證攔截成功。

**Loop 3 — 教學輸出檢查。** 手機溢出返回 CSS 節點；測驗提示錯誤返回 `slide-plan.json` 節點，而非只在 HTML 改文字。修正後重新生成並重跑測試。

以上為「自動驗證關卡 + 依錯誤類型返回修正 + 再次執行」的 Loop；**不是已實作一個能自己讀 PDF、自己修正學術論述的全天候雲端 LLM Agent**。內容的學術正確性仍以原始文獻為最後依據。

## 4. 反思草稿：可以依自己的體驗調整

**哪一個節點最常出錯？** 在這一輪實測中，觀察到的前端／教學輸出問題比來源資料格式問題更具體：兩項需要修正的問題都出現在「簡報產生／呈現」相關環節。因為目前只是一次專案執行，不能聲稱這代表長期故障頻率。

**把檢查往前移到哪裡？** 針對內容設計，先在 `slide-plan.json` 檢查「測驗不得提前透露答案」；針對網站樣式，先在沿用 HW9 CSS 時加入手機寬度與溢出檢查。資料面則將來源、DOI、證據頁碼與引用 ID 的檢查提前到產生 HTML 之前。

**修改了 Workflow / Graph 嗎？為什麼？** 有。在最初的資料收集 → 簡報生成 → 一次驗收之外，新增來源 Gate、知識 Gate、呈現 Gate，以及各自失敗返回節點；同時對呈現節點細分為「教學大綱檢查」和「手機版 CSS 檢查」。理由是排版錯誤和資料引用錯誤不應重新執行相同一大段工作，應定位原因後回到真正出錯的節點。

## 5. 上傳後仍需填入的紀錄

- GitHub Repository URL：`（待使用者填入）`
- GitHub Pages URL：`（待使用者填入）`
- Pages 首頁、Wiki 切頁、簡報 1–14 張、S01 來源連結：`（待使用者實測）`
- 真實手機瀏覽器與寬度：`（待使用者實測）`
- 上傳日期、執行者：`（待使用者填入）`

只需在正式部署後補上這些實測項目；不要把待確認項目改成已通過而未實際測試。


## 6. 2026-11-23 Karpathy Wiki 維護補強與一次 LLM Query

此次加強工作**並非在網站中安裝即時聊天 AI**，而是將原先一次批次整理的 Wiki 改成可累積的 Markdown 知識庫規範：`wiki/SCHEMA.md`、`wiki/index.md`、`wiki/log.md`，搭配 `tools/wiki_ops.py` 的 index、query、lint、ingest-verify 指令。

LLM 在本次製作階段依 **index → S02／S08 → HRV／壓力反應／操作型定義／限制** 的路徑讀取 Wiki，分析兩種壓力情境的 HRV 結果差異，寫成 `wiki/syntheses/hrv-across-contexts.md`、`wiki/queries/2026-11-23-hrv-reading.md`，更新 `slide-plan.json` 第 7、10 張，並由生成腳本重建 `slides.html`。詳細 Query／Source → Slide 的證據見 `docs/llm-query-trace.md`、`data/llm-query-trace.json` 與 `wiki/log.md`。

新增檢查前移：**每次 Query 前驗證 Index 與 Wiki Markdown 連結；每次生成 HTML 前驗證 Query → Slide 映射**。本次實際重新執行結果請見下一節（會在執行後填入，不把預計的檢查寫成 PASS）。


## 7. 強化後實際檢查結果（2026-11-23）

| 檢查 | 實際執行方式 | 結果 |
|---|---|---|
| 私有 PDF 來源一致性 | 重新從使用者的 `papers.zip` 解壓到**專案外的私有測試資料夾**，執行 `tools/ingest_local.py ... --check` | **PASS 10／10**：頁數、SHA256、文字字數對上原始 Manifest；原始 PDF 不包含在 GitHub ZIP |
| 真正 Query Wiki | `tools/wiki_ops.py query` 讀 `wiki/index.md`、S02、S08 與 4 個概念頁；ChatGPT 依結果綜合 | 已寫回 Query 與跨來源整合頁，並更新第 7、10 張投影片；見 `docs/llm-query-trace.md` |
| Index／Wiki Markdown Lint | `python3 tools/wiki_ops.py index`、`python3 tools/wiki_ops.py lint` | **PASS**，共 26 個 Markdown 頁面 |
| Lint 失敗路徑故障注入 | 在 `wiki/syntheses/_lint-injection.md` 暫時新增不存在的概念連結 `../concepts/does-not-exist.md` | **預期 FAIL，退出碼 1**：檢出壞連結與過期索引；刪除測試檔後重測 **PASS** |
| 來源故障注入 | `python3 tools/validate_project.py --inject-bad-source` | **預期攔截成功**：虛構來源 `S99` 無法通過 |
| Query → Slide 引用映射 | `python3 tools/validate_project.py`、`python3 tools/build_slides.py --check` | **PASS**：來源頁、LLM Query 路徑、第 7／10 張引用、生成 HTML 一致 |
| GitHub Pages 所需程式流程 | `python3 tools/run_workflow.py` | **PASS**：索引、Lint、知識／來源、生成 HTML 與前端 JS 語法檢查 |
| 離線 Chromium UI 測試 | `python3 tools/browser_smoke.py` | **PASS 15／15**：桌機／手機版翻頁、測驗、Wiki 搜尋及連結；仍非線上 HTTP E2E |
| GitHub Pages 真實網域 | 尚未由使用者部署 | **待確認**，不能填 PASS |

**本次新增的反思：** 之前的重點在「生成完才檢查 HTML」，這次透過故障注入具體驗證了新節點 **Wiki Index／Lint Gate** 的價值：如果索引未同步或 Markdown 連結壞掉，在 Query 前就會被擋下，而不需要等到簡報引用失敗才追查 Wiki。此為一次測試證據，不代表長期錯誤率統計。


## 8. 14 張投影片全頁面檢查（新補強）

新增 `tools/slide_layout_audit.py` 對 14 張教學頁面逐張檢查 1365px 桌機與 390px 手機視窗，共 **28／28 項通過**。項目包括整頁水平溢出、投影片容器溢出與頁尾引用區是否被容器裁切。保存第 7、10 張更新後畫面至 `docs/previews/query_{desktop,mobile}_slide{07,10}.png`。測試一樣是本機注入 HTML／CSS／JS，而非已部署 GitHub Pages 的網路端到端測試。


### GitHub 100 檔精簡版備註

為符合網頁上傳的單批檔案數限制，本次精簡版移除開發預覽 PNG、重複說明、部分離線輔助測試腳本；保留完整 Wiki、HTML 頁面、HW9 投影片素材、來源映射、Graph 與測試紀錄。離線瀏覽器測試、PDF SHA256/擷取字數核對的結果為**精簡前已執行**，不能將此視為精簡 ZIP 內所有測試腳本皆可重現。精簡後仍可執行 `python3 tools/run_workflow.py`、`python3 tools/wiki_ops.py lint`、`python3 tools/build_slides.py --check`。
