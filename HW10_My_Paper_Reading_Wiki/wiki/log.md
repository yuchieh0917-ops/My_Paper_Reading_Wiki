# LLM Wiki 操作紀錄（append-only）

> 以下是從 **2026-11-23** 開始建立的新操作日誌。舊版十篇文獻的解析與先前檢查，請參閱 `docs/ingest-log.md` 與 `docs/test-report.md`。不追溯捏造先前每個步驟的精確時間。

## [2026-11-23] migration | 補強 Karpathy 式維護架構

- 來源：既有 HW10 ZIP（包含 10 篇來源頁、10 個概念頁、14 張 HTML 投影片）。
- 新增：Schema、知識索引、時間線、Query 紀錄與跨文獻整合頁。
- 注意：這是既有資料的整理及擴充，不代表 10 篇 PDF 在這個時間點重新 ingest。

## [2026-11-23 23:13:18 +08:00] index | 重建 Markdown Wiki index

- 變更：True
- 輸出：wiki/index.md

## [2026-11-23 23:13:32 +08:00] query | Wiki 文件檢索（供 LLM 綜合）

- 問題：為什麼日常時間壓力研究與認知挑戰研究的 HRV 結果方向不同？這能教初學者什麼？
- 讀取頁面：wiki/index.md, wiki/sources/S02.md, wiki/sources/S08.md, wiki/concepts/hrv.md, wiki/concepts/stress-reactivity.md, wiki/concepts/operationalization.md, wiki/concepts/limitation.md
- 此步驟只取得來源，綜合答案另記於 wiki/queries/

## [2026-11-23] synthesize | LLM 以 S02 與 S08 比較 HRV 壓力結果

- 查詢問題：日常時間壓力與認知挑戰兩篇研究的 HRV 為何可能方向不同？
- 證據：`wiki/sources/S02.md`、`wiki/sources/S08.md`、HRV／操作型定義／壓力反應／研究限制概念頁。
- LLM 輸出：`wiki/syntheses/hrv-across-contexts.md`、`wiki/queries/2026-11-23-hrv-reading.md`。
- 更新教學大綱：`data/slide-plan.json` 的第 7、10 張；保留來源 S02、S08；執行 HTML 重建與驗證。
- 注意：上述為一次新 Query 的知識整合，不宣稱這次重新解析原始 PDF。

## [2026-11-23 23:15:41 +08:00] lint | Wiki Markdown 連結、索引與關聯檢查

- Errors: 0
- Warnings: 1
- 科學性內容需另行人工／LLM 查核

## [2026-11-23 23:19:01 +08:00] lint | Wiki Markdown 連結、索引與關聯檢查

- Errors: 0
- Warnings: 1
- 科學性內容需另行人工／LLM 查核

## [2026-11-23 23:23:03 +08:00] test | 故障注入與回歸驗證

- Lint 負向測試：暫放不存在的 `../concepts/does-not-exist.md`，確認偵測到壞連結與索引過期並以 exit 1 阻擋；刪除後 lint PASS。
- 引用負向測試：注入未知來源 `S99`，驗證程式成功阻擋；回復原始內容後重新驗證 PASS。
- 來源 PDF 復核：10/10 份 SHA256、頁數與可擷取字數相符，PDF 僅在非公開測試資料夾。
- 14 張投影片各跑 1365px 桌機與 390px 手機：28/28 項版面無溢出；另原始 15/15 項互動測試 PASS。
- 已保存對照、執行範圍與限制於 `docs/test-report.md`；GitHub Pages HTTP 部署尚待上傳者驗證。
