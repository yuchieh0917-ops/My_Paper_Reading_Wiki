# 2026-11-23 · LLM 查詢：HRV 與壓力結果方向為何不同？

## 查詢問題

「為什麼日常時間壓力的研究與認知挑戰研究中，HRV 的變化方向不同？這能教初學者怎麼批判閱讀？」

## Wiki 讀取路徑

1. [知識總目錄](../index.md)
2. [S02：日常時間壓力](../sources/S02.md)
3. [S08：認知挑戰先導研究](../sources/S08.md)
4. [HRV 概念](../concepts/hrv.md)
5. [壓力反應概念](../concepts/stress-reactivity.md)
6. [操作型定義](../concepts/operationalization.md)
7. [研究限制](../concepts/limitation.md)

## 本次由 LLM 依 Wiki 整合的回答

S02 的來源頁記載：在生態瞬時評估（EMA）日常情境，時間壓力增加與 HRV 降低相連；S08 則記載：學生運動員在 Stroop 與心算等短期認知作業期間，RMSSD 與高頻 HRV 升高。因為對象、時間尺度、指標與測試情境不同，這兩個方向不能直接當成同一研究問題的互相否定。教學時應引導學生先查 Methods 的**操作型定義、設計、時間點及樣本**，再比較 Results，而不是先挑一篇當作普遍定律。

此答案的依據是 Wiki 既有摘要與概念頁；**並未在本次查詢重新解讀 PDF 全部數據，也不能證明確切生理機制**。

## Query → Slide 的實際修改

- 第 7 張（`06 / HRV`）：加入「在比較 HRV 前先核對指標、樣本和壓力作業」的檢查提示。
- 第 10 張（`09 / CONTRADICTIONS`）：明確將「結果不同」改寫為「先檢查操作型定義、時間尺度與情境，再判斷是否矛盾」。
- 新增跨來源整合頁：[HRV 跨情境比較](../syntheses/hrv-across-contexts.md)。

## 檢查範圍

- 來源引用：S02、S08 都存在於 `wiki/sources/` 且包含 DOI、研究設計、發現與限制。
- 不支持的推論：沒有宣稱壓力「必然」使 HRV 上升／下降。
- 機械測試：重建 HTML 後執行 `build_slides.py --check`、`validate_project.py` 與 Wiki Lint。

## 執行真實性說明

此回答由本次 ChatGPT（LLM）讀取上述 Wiki 頁面後重新整理並寫入專案，不是 `wiki_ops.py query` 的純字串檢索程式自動生成。程式檢索只是讓「先讀 Wiki」的步驟可重現；實際的 LLM 綜合文字位於本檔案與整合頁。
