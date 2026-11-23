# My Paper Reading Wiki｜知識總目錄

> 這是 AI 查詢 Wiki 時首先閱讀的目錄。來源 PDF 屬私人原始資料，不包含在公開專案。
> 自動維護：`python3 tools/wiki_ops.py index --write`；改動後請執行 `lint`。

## 知識規範與操作紀錄

- [SCHEMA：Ingest／Query／Lint 工作規範](SCHEMA.md)
- [維護時間線](log.md)
- [Wiki 知識庫操作規範](SCHEMA.md)

## 來源文獻（Sources）

- [S01 · Exhausted Heart Rate Responses to Repeated Psychological Stress in Women With Major Depressive Disorder](sources/S01.md) — 兩組皆有首次壓力反應；憂鬱症組在第二次壓力暴露時未呈現相同的心率反應，主觀壓力也較難恢復到基線。
- [S02 · Individual differences in parasympathetic nervous system reactivity in response to everyday stress are associated with momentary emotional exhaustion](sources/S02.md) — 日常時間壓力增加時，HRV 傾向降低；HRV 對壓力反應較明顯的個體，也較常出現情緒耗竭。
- [S03 · Psychophysiological stress response after a 6-week Mindful Self-Compassion training in psychiatric rehabilitation inpatients: a randomized post-test only study](sources/S03.md) — 校正多重檢定後，MSC 與 PMR 兩組在壓力反應和心理測量指標上的差異未達顯著。
- [S04 · Psychophysiological fidelity: A comparative study of stress responses to real and simulated clinical emergencies](sources/S04.md) — 模擬情境引發較多威脅評估和較高焦慮；兩類事件的高頻 HRV 都比基線低，但模擬事件後恢復更接近基線。
- [S05 · Demand-resource evaluations and post-performance thoughts in classical music students: how they are linked and influenced by music performance anxiety, audience, and time](sources/S05.md) — DRES 隨表演焦慮增加而降低，在公開情境低於私人情境，且從表演前到表演中下降。
- [S06 · Multilayer Perceptron-Based Wearable Exercise-Related Heart Rate Variability Predicts Anxiety and Depression in College Students](sources/S06.md) — 模型預測焦慮／憂鬱等級呈現不同程度的分類準確率，論文指出預測連續量表分數仍有改進空間。
- [S07 · Using 24-h Heart Rate Variability to Investigate the Sleep Quality and Depression Symptoms of Medical Students](sources/S07.md) — 整體 PSQI 與 HRV、憂鬱分數與 HRV 的關聯未達顯著；但睡眠干擾子向度與部分日夜 HRV 指標有負相關。
- [S08 · Stress Responses and Recovery in Student Athletes: Heart Rate Variability and Skin Conductance Patterns Across Cognitive Challenges: A Pilot Study](sources/S08.md) — 壓力作業時 HR 與 SCL 升高；RMSSD 與高頻 HRV 也升高，與「壓力下 HRV 一律下降」的簡化預期不同。
- [S09 · The cumulative effect of chronic stress and depressive symptoms affects heart rate in a working population](sources/S09.md) — 極高慢性壓力合併憂鬱症狀時，心率晝夜節律較平坦；壓力反應減弱較與憂鬱症狀而非慢性壓力單獨相關。夜間 RMSSD 未顯示相同關聯。
- [S10 · Self-regulation, stress appraisal, and esport action performance](sources/S10.md) — 較高自我調節與較偏向挑戰的評估、較好的操作表現呈關聯；作者亦報告自我調節的中介分析。

## 知識概念（Concepts）

- [研究問題（Research Question）](concepts/question.md) — 研究要回答的具體疑問，是判斷方法與結果有沒有對題的起點。
- [研究設計（Study Design）](concepts/study-design.md) — 橫斷、受試者內比較、重複量數、隨機分組等設計，會決定能支持的結論強度。
- [操作型定義（Operationalization）](concepts/operationalization.md) — 抽象概念如何以可觀察指標測量。例如壓力可以是自陳時間壓力、DRES 評估或生理反應。
- [心率變異性（HRV）](concepts/hrv.md) — 相鄰心跳間隔的變動程度。RMSSD 與高頻功率等是不同指標；需注意量測長度、呼吸與情境。
- [需求—資源評估（DRES）](concepts/dres.md) — Demand Resource Evaluation Score 反映個人評估情境需求與自身資源的差異，可協助理解挑戰與威脅的主觀評估。
- [壓力反應（Stress Reactivity）](concepts/stress-reactivity.md) — 面臨壓力時生理或心理指標相對於基線的變化；也要區分恢復速度與反覆暴露的反應。
- [生態效度（Ecological Validity）](concepts/ecological-validity.md) — 研究情境與日常現實有多接近。實驗室與真實情境各有控制力及外推性的優缺點。
- [統計顯著與解讀（Statistical Inference）](concepts/statistics.md) — 統計顯著不等於效果大、實務有意義或存在因果；未達顯著也不是「完全沒有差異」。
- [模型預測（Prediction）](concepts/machine-learning.md) — 利用資料預測未知案例，不等於診斷或因果機制。要看交叉驗證、類別比例與外部效度。
- [研究限制與因果（Limitations & Causality）](concepts/limitation.md) — 樣本、設計、混淆變項、情境與測量誤差都會限制結論。橫斷相關通常不足以證明因果。

## 跨來源整合（Synthesis）

- [HRV 在不同壓力情境中的結果為何不同？](syntheses/hrv-across-contexts.md) — 用多份來源進行比較，列出推論界線

## 已完成的 LLM 查詢紀錄（Query artifacts）

- [2026-11-23 · LLM 查詢：HRV 與壓力結果方向為何不同？](queries/2026-11-23-hrv-reading.md) — 問題、閱讀路徑、回答與簡報對應
