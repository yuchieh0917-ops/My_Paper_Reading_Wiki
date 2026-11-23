# My Paper Reading Wiki — 生成式 AI 課程 HW10

**主題：** 如何讀懂心理學研究？——以壓力、心率變異性（HRV）與自我調節研究為例。

延續第九週 **My Paper Reading List** 的 HTML / CSS / JavaScript / JSON 架構及 Academic Garden 視覺風格，擴充為 Wiki 知識庫、教學型 HTML 簡報和有回饋迴圈的 Graph。

## 直接觀看網站（GitHub Pages）

上傳並啟用 GitHub Pages 後開啟：

- `index.html`：保留 HW9 原閱讀清單與簡報典藏。
- `wiki.html`：10 篇真實論文（S01–S10）、10 個概念節點、搜尋與雙向引用。
- `slides.html`：14 張適合初學者的教學 HTML 投影片，可用鍵盤方向鍵、按鈕、測驗。
- `workflow.html`：三個 Loop（來源、知識、呈現）、Graph 與執行關卡。
- `evaluation.html`：實際檢查、修正與反思。
- `paper.html?id=...`：HW9 原有論文詳細頁與原投影片播放器。

## 作業要求對應

| 要求 | 交付位置 |
|---|---|
| LLM Wiki 主題與簡介 | 本 README、`wiki.html` |
| Wiki 連結或成果 | `wiki.html`、`wiki/sources/`、`wiki/concepts/` |
| 至少 ingest 五篇來源 | 本次 10 篇 PDF，`data/wiki-sources.json`、`docs/ingest-log.md` |
| 可瀏覽教學 HTML 簡報 | `slides.html`、`data/slide-plan.json` |
| Loop / Graph 說明 | `workflow.html`、`docs/workflow.mmd`、`assets/workflow.svg` |
| 一次真實執行與驗證 | `docs/test-report.md`、`tools/` |
| 哪個節點出錯，如何提前檢查 | `evaluation.html`、`docs/test-report.md` |
| 先討論、後生成 | `docs/decision-log.md`、`docs/llm-query-trace.md` |

## 在自己電腦啟動（注意不要直接雙擊 Wiki HTML）

此網站使用 JavaScript `fetch()` 讀取本地 JSON，請在解壓縮資料夾內啟動 HTTP 伺服器：

```bash
python3 -m http.server 8000
```

然後使用瀏覽器開啟 `http://localhost:8000`。舊 HTML 與圖片多可直接雙擊，但 Wiki 查詢必須有 HTTP 服務。**不需要後端伺服器、API Key 或 Node.js** 才能展示網站。

## 直接上傳 GitHub 並啟用 Pages

1. 在 GitHub 建立新的 **Public Repository**，例如 `hw10-paper-reading-wiki`（若要使用 GitHub Pages 免費公開網站，可依自己的方案與權限設定）。
2. **先解壓 ZIP**：上傳裡面的 `index.html`、`wiki.html`、`slides.html`、`data/`、`assets/`、`.github/` 等檔案到 Repository 根目錄；**不要只把 ZIP 當成單一檔案上傳**。如果使用 GitHub 網頁上傳，隱藏的 `.github/` 與 `.nojekyll` 應確保有包含；也可用 Git 提交整個專案。
3. GitHub 專案的 **Settings → Pages → Build and deployment** 選擇 **Deploy from a branch**，分支 `main`，資料夾 `/ (root)`，然後 Save。
4. GitHub Pages 網址通常為 `https://你的帳號.github.io/儲存庫名稱/`；請以 Pages 顯示的實際網址為準。
5. 開啟首頁、Wiki、教學簡報及 Workflow，實際點擊引用與翻頁；確認手機尺寸與 Pages 路徑。把真實網址貼到作業繳交欄位。

**另一種上傳方式（已安裝 Git）：** 在本資料夾執行 `git init`、`git add .`、`git commit -m "HW10 LLM Wiki"`，連接新遠端後 `git push -u origin main`。請先設定帳號與遠端。


## Karpathy 式 LLM Wiki 維護（本次 HW10 強化版）

這個專案參考 [Karpathy 的 LLM Wiki 方法](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 的 **Raw Sources → Wiki → Schema** 三層設計，並加入 **Ingest、Query、Lint**，不是官方程式碼的複製。公共 GitHub 不收錄私有 PDF；使用者於本機保留原始來源。

- [維護規範（Schema）](wiki/SCHEMA.md)：AI 應如何先討論、逐篇整合、維護雙向連結、檢索、檢查。
- [知識索引（Index）](wiki/index.md)：AI Query 之前先讀，包含來源、概念、跨研究整合及 Query 成果頁。
- [操作日誌（Log）](wiki/log.md)：append-only 方式記錄 index、query、lint 及實際修正。
- [跨來源整合頁](wiki/syntheses/hrv-across-contexts.md)：對比 S02 與 S08 的 HRV 壓力反應，不把兩個結果誤認為必然互相推翻。
- [一次實際 LLM Query 追溯記錄](docs/llm-query-trace.md)：列出查詢問題、實際閱讀的 Wiki 頁、LLM 綜合、投影片第 7／10 張改動，以及生成／驗證方式；[機器可讀映射](data/llm-query-trace.json)。

**可重現操作：**

```bash
python3 tools/wiki_ops.py index --write
python3 tools/wiki_ops.py lint --record
python3 tools/wiki_ops.py query --question 'HRV 為什麼在不同壓力研究方向不同？' --sources S02,S08 --concepts hrv,operationalization,limitation --log
python3 tools/wiki_ops.py ingest-verify --id S02
python3 tools/build_slides.py --check
python3 tools/run_workflow.py
## 28 項瀏覽器版面檢查已在精簡前開發階段執行，紀錄見 docs/test-report.md
```

其中 `wiki_ops.py query` 是**檔案檢索／證據列印工具，不是 AI 模型**。真正的 LLM 知識綜合與更新頁面是依 Schema 由 ChatGPT / GPT Work 執行，並保留於本次 Query 成果頁。每次新增來源時，AI 應更新 JSON、來源頁、相關概念頁、跨文獻整合、Index、Log，並重跑 Lint。網站仍是靜態 GitHub Pages 展示，不需公開 API Key。

## 檢查與重建

```bash
python3 tools/run_workflow.py
python3 tools/validate_project.py --inject-bad-source
python3 tools/build_slides.py --check
```

若有自己的原始 PDF 私有資料夾：

```bash
python3 -m pip install pymupdf
## 私有 PDF 的完整稽核腳本保留於非公開的完整開發封存版；此 ZIP 包含 Wiki 記錄與 SHA256
```

`tools/build_slides.py --write` 會從 `data/slide-plan.json` 重新產生簡報 HTML；請先確認 Wiki 來源 ID 與教學內容，再執行，避免覆寫手工修訂。`.github/workflows/validate.yml` 在推送時執行靜態 Gate；無法取代瀏覽器／科學內容人工檢查。

## 著作權與真實性界線

- 使用者提供的 10 篇 PDF **不在公開 ZIP**。Wiki 保存自製學習摘要、DOI、PDF 頁碼與檔案 SHA256。
- 此 Wiki 為已由本地來源處理並輸出成靜態網站的知識成果；**網頁本身沒有即時呼叫 LLM，也沒有自動發現並修復學術錯誤的代理程式**。自動化 Gate 可攔截資料／引用／程式錯誤，需要依 Graph 人工或 GPT Work 回到對應節點修正再測。
- 本地原始 PDF 的檔案雜湊、文字擷取、資料一致性可程式驗證；科學解讀需回查原文。
- GitHub Pages 的正式部署與不同實體設備的檢查須由上傳者完成並保留結果。

重要證據：`docs/decision-log.md`、`docs/ingest-log.md`、`docs/llm-query-trace.md`、`docs/test-report.md`。


## GitHub 網頁上傳精簡版（100 個檔案）

本 ZIP 已移除 7 張開發用預覽截圖、重複文件及非部署必要的離線輔助檢查腳本，保留網站、42 張 HW9 圖片、10 個 Wiki 來源頁、10 個概念頁、教學簡報、Graph、實際測試紀錄、Wiki Lint 與簡報生成腳本。網站檔案總數為 **100**。

因 GitHub 網頁上傳會計算所選取檔案數，請解壓後進入 `HW10_My_Paper_Reading_Wiki`，全選**內部**檔案／資料夾再上傳，保留原有資料夾結構。若網頁限制或隱藏檔處理導致失敗，也可分兩批提交（例如先上傳 `assets/`，再上傳其餘內容）；GitHub Repository 本身不是只能放 100 個檔案。

`docs/test-report.md` 中的 Chromium 測試與 PDF 本機 ingest 檢查是在精簡前、具有完整工具與私有來源的開發環境進行；本公開版保留測試結果，但**沒有聲稱能從這個精簡 ZIP 單獨重跑全部私有 PDF 與瀏覽器腳本**。若需要保留完整原始輔助測試程式，請另存完整封存版 ZIP。
