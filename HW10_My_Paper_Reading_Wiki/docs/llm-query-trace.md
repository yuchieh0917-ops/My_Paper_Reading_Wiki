# 一次真實 LLM Query → 整合 Wiki → 更新 HTML 的紀錄

**日期：** 2026-11-23（Asia/Taipei）  
**問題：** 為什麼日常時間壓力研究與認知挑戰研究的 HRV 結果方向不同？這能教初學者什麼？  
**執行方式：** ChatGPT 在此製作階段實際讀取專案內 Wiki Markdown 頁面，進行跨文獻知識綜合並改寫簡報大綱；`tools/wiki_ops.py` 負責可重現的本地檔案檢索、日誌與 Lint，**不呼叫模型、不冒充模型答案**。

## 1. 知識檢索（實際執行）

```bash
python3 tools/wiki_ops.py query \
  --question '為什麼日常時間壓力研究與認知挑戰研究的 HRV 結果方向不同？這能教初學者什麼？' \
  --sources S02,S08 \
  --concepts hrv,stress-reactivity,operationalization,limitation \
  --log
```

由 index 開始，實際讀取：`wiki/index.md` → `wiki/sources/S02.md` → `wiki/sources/S08.md` → `wiki/concepts/hrv.md` → `wiki/concepts/stress-reactivity.md` → `wiki/concepts/operationalization.md` → `wiki/concepts/limitation.md`。

## 2. 兩篇來源的可追溯主張

| Wiki 頁 | 讀到的資料 | 教學上不可跳過的限制 |
|---|---|---|
| [S02](../wiki/sources/S02.md) | EMA 研究日常時間壓力；來源摘要指出壓力增加時 HRV 傾向下降 | 觀察性資料，不足以推論壓力造成長期情緒耗竭 |
| [S08](../wiki/sources/S08.md) | 認知挑戰先導研究；來源摘要指出 HR 與 SCL 上升，RMSSD 和高頻 HRV 也上升 | 大學運動員樣本與短時段測量，不足以一般化為所有壓力情境 |
| [HRV 概念](../wiki/concepts/hrv.md) | HRV 不是單一萬用壓力分數 | 不同指標與情境不應直接合併 |
| [操作型定義](../wiki/concepts/operationalization.md) | 相同名稱的抽象概念可能用不同指標測量 | 先比 Methods，再比 Results |

## 3. LLM 整合回答

兩篇研究都談 HRV 和壓力，但研究情境、樣本、時間尺度和指標不同，因此方向不一致**不能直接解讀成研究互相推翻**。初學者應先核對研究設計、操作型定義與測量情境，再判斷是否為真正衝突；也不能宣稱此比較已證明某種特定生理機制。

已將此綜合結果寫回 [HRV 跨情境整合頁](../wiki/syntheses/hrv-across-contexts.md) 和 [Wiki Query 成果頁](../wiki/queries/2026-11-23-hrv-reading.md)，使這次問答成為**可再用的 Wiki 知識**。

## 4. 從 Query 到 HTML 的實際變更

| 步驟 | 輸出 | 檢查 |
|---|---|---|
| LLM 知識綜合 | `wiki/syntheses/hrv-across-contexts.md` | S02／S08 各有來源頁及研究限制 |
| LLM 調整教學設計 | `data/slide-plan.json` 的第 7、10 張 | 每張 `refs` 對應來源 ID；沒有把相關誤寫成因果 |
| 程式生成 HTML | `python3 tools/build_slides.py --write` | `--check` 比對生成結果與 JSON 大綱 |
| Wiki 管理 | `wiki/index.md`、`wiki/log.md` | `tools/wiki_ops.py lint` 驗證內容索引與 Markdown 連結 |
| 整體回歸 | `python3 tools/run_workflow.py` | 網站資料與 JS 語法關卡，待下方實際重跑結果 |

完整機器可讀映射：`data/llm-query-trace.json`。此檔讓每一張修改過的簡報都能追到此次 Query 所讀的 Wiki 路徑及來源 ID。

## 5. 誠實界線

- 這是**一個**在當前 ChatGPT 工作階段執行並記錄的 Wiki 查詢與更新，不代表網站內建即時 LLM、持續背景代理或 GPT Work 曾執行這筆查詢。
- 檢查腳本能比對引用 ID、頁面存在與結構，不能獨立保證學術解讀完全正確；重要主張仍須回查使用者提供的論文 PDF。
- GitHub Pages 需使用者完成部署並在公開網址實測。
