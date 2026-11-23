#!/usr/bin/env python3
"""Static Wiki provenance checks + regression tests for original HW9."""
from pathlib import Path
import json,re,sys,copy
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def validate(sources,concepts,slides,papers):
 errs=[]
 add=lambda cond,message:errs.append(message) if not cond else None
 ids=[s.get('id') for s in sources]; add(len(sources)>=5,'不足 5 篇已 ingest 文獻')
 add(len(ids)==len(set(ids)),'重複來源 ID')
 concepts_ids=[c.get('id') for c in concepts]
 add(len(concepts_ids)==len(set(concepts_ids)),'重複概念 ID')
 doi_set=[]
 for s in sources:
  sid=s.get('id','?');doi=s.get('doi','')
  doi_set.append(doi)
  add(bool(re.fullmatch(r'10\.\d{4,9}/\S+',doi)),f'{sid} DOI 無效')
  add(s.get('source')=='https://doi.org/'+doi,f'{sid} DOI URL 對不上')
  add(s.get('ingested') and s.get('extractedChars',0)>1200 and s.get('pages',0)>=2,f'{sid} PDF ingest 未確認')
  add(1 <= s.get('evidence',{}).get('pdfPage',0)<=s.get('pages',0),f'{sid} 證據頁碼超界')
  add(len(s.get('sha256',''))==64,f'{sid} 雜湊不完整')
  add(bool(s.get('finding')) and bool(s.get('caution')),f'{sid} 缺少發現或限制')
  md=ROOT/'wiki/sources'/(sid+'.md');add(md.is_file(),f'{sid} 缺少可讀來源 Wiki 頁')
  if md.is_file():add(doi in md.read_text(encoding='utf-8'),f'{sid} Wiki 頁 DOI 不一致')
  for cid in s.get('concepts',[]):add(cid in concepts_ids,f'{sid} 連到不存在概念 {cid}')
 add(len(doi_set)==len(set(doi_set)),'重複 DOI')
 for c in concepts:
  add((ROOT/'wiki/concepts'/(c['id']+'.md')).is_file(),f'缺少可讀概念 Wiki 頁：{c["id"]}')
  for sid in c.get('sources',[]):
   add(sid in ids,f'概念 {c.get("id")} 引用不存在來源 {sid}')
   if sid in ids:
    add(c['id'] in next(s for s in sources if s['id']==sid)['concepts'],f'概念與來源非雙向：{c["id"]} / {sid}')
  for rid in c.get('related',[]):add(rid in concepts_ids,f'概念 {c["id"]} 關聯不存在概念 {rid}')
 for i,s in enumerate(slides,1):
  for sid in s.get('refs',[]):add(sid in ids,f'投影片 {i} 引用不存在來源 {sid}')
  add(bool(s.get('points')) and bool(s.get('t')),f'投影片 {i} 缺內容')
  if s.get('quiz'):add('正確答案' not in s.get('tip',''),f'投影片 {i} 測驗未作答就提示正確答案')
 add(len(slides)>=8,'教學投影片不足')
 for p in papers:
  add((ROOT/'paper.html').is_file(),'HW9 論文詳細頁遺失')
  for path in p.get('slides',[]):add((ROOT/path).is_file(),f'HW9 投影片檔案遺失：{path}')
 for name in ['README.md','docs/decision-log.md','docs/ingest-log.md','docs/test-report.md','docs/workflow.mmd','docs/llm-query-trace.md','wiki/SCHEMA.md','wiki/index.md','wiki/log.md','wiki/syntheses/hrv-across-contexts.md','wiki/queries/2026-11-23-hrv-reading.md','data/llm-query-trace.json','tools/wiki_ops.py','index.html','paper.html','wiki.html','slides.html','workflow.html','evaluation.html','styles/main.css','styles/hw10.css','scripts/app.js','scripts/paper.js','scripts/wiki.js','scripts/slides.js','assets/workflow.svg']:
  add((ROOT/name).is_file(),f'缺少網站資產或證據文件 {name}')
 ev=(ROOT/'evaluation.html').read_text(encoding='utf-8')
 # 追溯真正的 Wiki Query -> LLM 整合 -> 簡報變更（檔案一致性；不等於模型答案真實性驗證）
 trace_path=ROOT/'data/llm-query-trace.json'
 if trace_path.is_file():
  trace=json.loads(trace_path.read_text(encoding='utf-8'))
  add(bool(trace.get('question')) and bool(trace.get('wikiAnswer')),'Query 紀錄沒有問題或 LLM 綜合回答')
  for wp in trace.get('readOrder',[]):add((ROOT/wp).is_file(),f'Query 實際引用的 Wiki 頁不存在 {wp}')
  for op in trace.get('outputs',[]):add((ROOT/op).is_file(),f'Query 輸出檔不存在 {op}')
  for ch in trace.get('slideChanges',[]):
   ix=ch.get('zeroBasedIndex',-1)
   if not isinstance(ix,int) or not 0<=ix<len(slides):errs.append('Query 所列簡報張數超界');continue
   add(ch.get('title')==slides[ix].get('t'),f'Query 映射簡報標題不一致 {ix}')
   for sid in ch.get('refs',[]):add(sid in slides[ix].get('refs',[]),f'Query 映射來源 {sid} 未出現於第 {ix+1} 張投影片')
   for wp in ch.get('wikiPaths',[]):add((ROOT/wp).is_file(),f'Query 映射知識頁不存在 {wp}')
  add(len(trace.get('slideChanges',[]))>=1,'Query 沒有留下至少一張簡報變更映射')
 add('測試結果準備中' not in ev,'Evaluation 頁仍包含測試占位內容')
 html=(ROOT/'slides.html').read_text(encoding='utf-8')
 for i,s in enumerate(slides,1):
  add(f'data-slide="{i-1}"' in html,f'教學頁缺投影片 {i}')
  for sid in s.get('refs',[]):add(f'?source={sid}#wiki-detail' in html, f'教學簡報缺少 {sid} 引用連結')
 return errs
if __name__=='__main__':
 sources=read('data/wiki-sources.json');concepts=read('data/wiki-concepts.json');slides=read('data/slide-plan.json');papers=read('data/papers.json')
 errs=validate(sources,concepts,slides,papers)
 if '--inject-bad-source' in sys.argv:
  broken=copy.deepcopy(slides);broken[0]['refs'].append('S99')
  injected=validate(sources,concepts,broken,papers)
  detected=any('S99' in e for e in injected)
  print(('PASS' if detected else 'FAIL')+' 故障注入：故意引用不存在的 S99，檢查器'+('成功攔截' if detected else '未攔截'))
  sys.exit(0 if detected else 1)
 if errs:
  print('FAIL：',len(errs),'個問題')
  for e in errs:print(' -',e)
  sys.exit(1)
 print(f'PASS：{len(sources)} 篇來源、{len(concepts)} 個概念、{len(slides)} 張教學投影片、{len(papers)} 筆原有論文及其投影片全部通過靜態資料檢查。')
