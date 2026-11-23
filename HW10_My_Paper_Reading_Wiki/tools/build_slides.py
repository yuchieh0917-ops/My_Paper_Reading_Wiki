#!/usr/bin/env python3
"""Rebuild static teaching slides FROM wiki source IDs and approved slide plan.
Run: python tools/build_slides.py --check  OR --write
"""
import json,html,argparse,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser()
p.add_argument('--write',action='store_true')
p.add_argument('--check',action='store_true')
a=p.parse_args()
if not (a.write or a.check):p.error('Specify --write or --check')
src=json.loads((ROOT/'data/wiki-sources.json').read_text(encoding='utf-8'))
slides=json.loads((ROOT/'data/slide-plan.json').read_text(encoding='utf-8'))
source_map={s['id']:s for s in src}
parts=[]
for i,s in enumerate(slides):
 for sid in s['refs']:
  if sid not in source_map:sys.exit(f'FAIL: Slide {i+1} unknown source {sid}; return to Wiki/slide-plan validation')
 refs=''.join(f'<a href="./wiki.html?source={rid}#wiki-detail" title="{html.escape(source_map[rid]["author"])} DOI {html.escape(source_map[rid]["doi"])}">{rid}</a>' for rid in s['refs'])
 bullets=''.join('<li>'+html.escape(q)+'</li>' for q in s['points'])
 quizhtml='''<div class="quiz-box"><button type="button" class="mini-button" id="quiz-answer">檢查我的答案</button><p id="quiz-feedback" class="quiz-feedback" role="status" aria-live="polite"></p></div>''' if s.get('quiz') else ''
 parts.append(f'<section class="teaching-slide" data-slide="{i}" aria-label="第 {i+1} 張：{html.escape(s["t"])}"><p class="slide-label">{html.escape(s["k"])}</p><h2>{html.escape(s["t"])}</h2><p class="slide-lead">{html.escape(s["lead"])}</p><ul class="slide-points">{bullets}</ul>{quizhtml}<div class="slide-bottom"><p class="slide-tip">✦ {html.escape(s["tip"])}</p><div class="slide-cites" aria-label="Wiki 來源">{refs}</div></div></section>')
start='<div class="slide-stage" id="slide-stage">'
end='</div><div class="slide-toolbar">'
path=ROOT/'slides.html';old=path.read_text(encoding='utf-8')
if old.count(start)!=1 or old.count(end)!=1:sys.exit('FAIL: no unique slide template container')
head,tail=old.split(start,1)
_,rest=tail.split(end,1)
new=head+start+''.join(parts)+end+rest
if a.write:
 path.write_text(new,encoding='utf-8');print(f'PASS: regenerated {len(slides)} teaching slides with validated wiki links')
else:
 if new != old:sys.exit('FAIL: slide plan and HTML out of sync; run --write then validate')
 print(f'PASS: generated HTML matches {len(slides)} approved slide-plan entries')
