# LLM Wiki 維護規範（Schema）｜My Paper Reading Wiki

> 靈感：Andrej Karpathy 的 [LLM Wiki 概念](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。本專案是依需求自行實作的版本，**不宣稱是原作者的程式碼或官方產品**。閱讀本頁後再操作 Wiki。

## 0. 分層與責任

1. **Raw sources（不可變）**：使用者提供的 PDF 原始檔，儲存於本機 `private/raw/` 或其他不公開的位置。只讀、記錄檔案雜湊，不改寫、不進 GitHub；原始文獻是最終證據。
2. **Wiki（由 LLM 協助維護）**：`wiki/sources/` 是各篇有來源的摘要；`wiki/concepts/` 是跨篇共同概念；`wiki/syntheses/` 是比較、衝突與整合；`wiki/queries/` 保存有用的查詢答案。AI 可以提出修改，但需使用者核准才公開。
3. **Schema**：本文件定義標準操作，`AGENTS.md` 定義整體專案規範。`data/wiki-sources.json`、`data/wiki-concepts.json` 是可被網站呈現的對應資料，須保持一致。

## 1. Ingest（新來源匯入）

**先討論再生成**：使用者指定來源、範圍和教學關注點，AI 先回報來源的真實書目資訊、PDF 可讀性、應該加入的概念與既有知識的可能差異，待使用者確認才更動。

檢查與更新順序：

1. 對原始 PDF 計算 SHA256、頁數、文字可擷取數、DOI（不代表學術真實性已完成交叉審核）。如檔案只有掃描影像，請人工確認後另處理。
2. 先讀 `wiki/index.md`，尋找相同 DOI、同義概念、相近研究與需要更新的既有頁面，避免重複建立。
3. 在 `data/wiki-sources.json` 登錄唯一的 `S##`、DOI、來源頁碼與重要發現、研究限制；更新 `wiki/sources/S##.md`。
4. **增量整合**：修改受影響的 `wiki/concepts/*.md`、`data/wiki-concepts.json`，新增／修正雙向連結。必要時更新 `wiki/syntheses/` 中既有比較與衝突說明。
5. 執行 `python3 tools/wiki_ops.py index --write`、`python3 tools/wiki_ops.py lint`、`python3 tools/wiki_ops.py ingest-verify --id S## --record`、`python3 tools/validate_project.py`，並檢查 DOI、來源頁碼與結論是否忠於原文。
6. 將結果、失敗原因及修正記入 `wiki/log.md`（由 `--record` 或手動新增真實操作）。不可把既有 PDF 檔案直接視為已成功 ingest。

**回退**：PDF／DOI 失敗回原始來源；概念雙向連結失敗回 Wiki 整合；學術主張查不到證據時不得進到 Query 或簡報。

## 2. Query（查詢與再利用）

1. LLM **先讀 `wiki/index.md`**，再選擇相關 `wiki/sources/`、`wiki/concepts/`、`wiki/syntheses/`；只用已有資料答題，不足就註明缺漏。
2. 使用 `python3 tools/wiki_ops.py query --question '問題' --sources S02,S08 --concepts hrv,limitation --log` 留下**實際檢索記錄**。此 Python 工具不會呼叫 LLM，不可把它輸出的文件當成 LLM 答案。
3. LLM 以繁體中文綜合回答，至少列出來源頁面、PDF 頁碼（若已有明確記錄）、推論限制與相異證據。若多篇研究方向不同，不能擅自合併成一致結論。
4. 對可長期使用的回答建立 `wiki/queries/*.md` 或整合到 `wiki/syntheses/*.md`，重建 index；必要時更新 `data/slide-plan.json`，由 `tools/build_slides.py --write` 重建 HTML。
5. 簡報各張 `refs` 須對應 Wiki 已登錄來源。引用連結完整 ≠ 科學主張已被驗證，仍須人工比對。

## 3. Lint（品質維護）

- **可自動驗證**：`python3 tools/wiki_ops.py lint --record` 檢查 Markdown 連結、頁面存在、索引同步、來源與概念雙向關聯；`tools/validate_project.py` 檢查來源 ID、簡報引用及 HW9 回歸測試。
- **不能自動證明**：論文結論是否正確、是否有過時研究、是否遺漏非顯著發現、兩篇研究是否真正矛盾。必須由 LLM 提出待核對問題，並由使用者回到 PDF／DOI 人工審核。
- **檢查前移**：在 Wiki Query 之前跑 Lint；在生成 HTML 之前跑來源－大綱對照；在發布之前跑瀏覽器及手機版檢查。
- **失敗迴圈**：來源問題回 Ingest、跨文獻衝突回 Wiki 合成、引用問題回 Query／教學大綱、排版／互動問題回 HTML／CSS。

## 4. Wiki 頁面與引用規範

- `wiki/sources/Sxx.md`：原文標題、作者與年份、DOI、檔案雜湊、PDF 證據頁碼、研究設計、測量、發現、限制、概念連結。
- `wiki/concepts/*.md`：定義、讀論文時的警告、支持的來源、相關概念。
- `wiki/syntheses/*.md`：比較問題、共同點、分歧點、可能解釋、**無法推定的事**、雙向鏈結。
- `wiki/queries/*.md`：查詢問題、讀取路徑、LLM 答案、引用與簡報的實際變動，禁止虛構執行。
- `wiki/index.md`：以內容為主的導航，所有知識頁一律列入；每次 Wiki 修改後重建。
- `wiki/log.md`：按時間附加操作記錄，不回填不存在的過往活動，也不竄改舊紀錄。

## 5. 發布權限與保密

- 不將 PDF、未核准草稿、API Key、私人來源資料放入 GitHub Pages。
- GitHub Pages 僅靜態展示，不即時呼叫 LLM；若需再次 AI 維護，請由 GPT Work 或其他 LLM Agent 讀取本專案依本 Schema 執行。
- 不能自動完成的檢查，應註記待確認，而不是標示 PASS。
