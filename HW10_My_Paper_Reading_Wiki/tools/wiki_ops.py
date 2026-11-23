#!/usr/bin/env python3
"""Transparent, local helper for Karpathy-style Markdown Wiki operations.
Does not call an LLM: agent reads returned pages and writes human-reviewed synthesis.
Commands:
  python tools/wiki_ops.py index --write
  python tools/wiki_ops.py query --question '...' --sources S02,S08 --concepts hrv,limitation --log
  python tools/wiki_ops.py lint
  python tools/wiki_ops.py ingest-verify --id S01 --record
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[1]
WIKI=ROOT/'wiki'
LOG=WIKI/'log.md'

def read(name): return json.loads((ROOT/name).read_text(encoding='utf-8'))
def timestamp(): return datetime.now(ZoneInfo('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S +08:00')
def log(op,title,lines):
    if not LOG.exists():
        raise RuntimeError('wiki/log.md 不存在；請先建立不可覆寫的操作紀錄檔')
    stamp=timestamp()
    with LOG.open('a',encoding='utf-8') as f:
        f.write(f'\n## [{stamp}] {op} | {title}\n\n')
        f.write('\n'.join('- '+line for line in lines).rstrip()+'\n')
    print(f'LOGGED {op} {stamp}')

def page_index():
    sources=read('data/wiki-sources.json'); concepts=read('data/wiki-concepts.json')
    o=['# My Paper Reading Wiki｜知識總目錄','',
       '> 這是 AI 查詢 Wiki 時首先閱讀的目錄。來源 PDF 屬私人原始資料，不包含在公開專案。',
       '> 自動維護：`python3 tools/wiki_ops.py index --write`；改動後請執行 `lint`。','',
       '## 知識規範與操作紀錄','',
       '- [SCHEMA：Ingest／Query／Lint 工作規範](SCHEMA.md)',
       '- [維護時間線](log.md)',
       '- [Wiki 知識庫操作規範](SCHEMA.md)','',
       '## 來源文獻（Sources）','']
    for s in sources:
        finding=s.get('finding','').strip()
        if len(finding)>85:finding=finding[:85]+'…'
        o.append(f'- [{s["id"]} · {s["title"]}](sources/{s["id"]}.md) — {finding}')
    o+=['','## 知識概念（Concepts）','']
    for c in concepts:
        o.append(f'- [{c["name"]}](concepts/{c["id"]}.md) — {c["desc"]}')
    synth=sorted((WIKI/'syntheses').glob('*.md'))
    if synth:
        o+=['','## 跨來源整合（Synthesis）','']
        for p in synth:
            h=p.read_text(encoding='utf-8').splitlines()[0].lstrip('# ').strip()
            o.append(f'- [{h}](syntheses/{p.name}) — 用多份來源進行比較，列出推論界線')
    queries=sorted((WIKI/'queries').glob('*.md'))
    if queries:
        o+=['','## 已完成的 LLM 查詢紀錄（Query artifacts）','']
        for p in queries:
            h=p.read_text(encoding='utf-8').splitlines()[0].lstrip('# ').strip()
            o.append(f'- [{h}](queries/{p.name}) — 問題、閱讀路徑、回答與簡報對應')
    return '\n'.join(o)+'\n'

def lint():
    errors=[]; warnings=[]
    all_md=sorted(WIKI.rglob('*.md'))
    if len(all_md)<10:errors.append('Wiki 頁數異常少')
    for p in all_md:
        t=p.read_text(encoding='utf-8')
        if not t.strip():errors.append(f'空白頁：{p.relative_to(ROOT)}')
        for match in re.finditer(r'\[[^\]]+\]\(([^)]+)\)',t):
            target=match.group(1).split('#')[0].strip()
            if not target or target.startswith(('https://','http://','mailto:')):continue
            if not (p.parent/target).resolve().is_file():errors.append(f'壞連結：{p.relative_to(ROOT)} -> {target}')
    sources=read('data/wiki-sources.json'); concepts=read('data/wiki-concepts.json')
    cids={c['id'] for c in concepts}; sids={s['id'] for s in sources}
    for s in sources:
        sp=WIKI/'sources'/f'{s["id"]}.md'
        if not sp.is_file():errors.append(f'來源頁不存在 {s["id"]}');continue
        st=sp.read_text(encoding='utf-8')
        for c in s.get('concepts',[]):
            if c not in cids:errors.append(f'{s["id"]} 未知概念 {c}')
            elif f'../concepts/{c}.md' not in st:errors.append(f'來源頁連結缺失 {s["id"]}->{c}')
    for c in concepts:
        cp=WIKI/'concepts'/f'{c["id"]}.md'
        if not cp.is_file():errors.append(f'概念頁不存在 {c["id"]}');continue
        ct=cp.read_text(encoding='utf-8')
        if not c.get('sources'):warnings.append(f'沒有來源支撐的概念 {c["id"]}')
        for sid in c.get('sources',[]):
            if sid not in sids:errors.append(f'{c["id"]} -> 未知來源 {sid}')
            elif f'../sources/{sid}.md' not in ct:errors.append(f'概念頁連結缺失 {c["id"]}->{sid}')
            elif c['id'] not in next(s for s in sources if s['id']==sid).get('concepts',[]):errors.append(f'概念雙向 JSON 關聯缺失 {c["id"]}->{sid}')
    if (WIKI/'index.md').read_text(encoding='utf-8') != page_index():errors.append('index.md 過期；請執行 index --write')
    if not LOG.is_file():errors.append('缺少 wiki/log.md')
    # Structural checks cannot assess factual contradictions or whether a question is actually solved.
    warnings.append('科學性矛盾／文獻過時／推論強度須由 LLM 與使用者依來源人工評估')
    return errors,warnings

def main():
    parser=argparse.ArgumentParser(description='LLM Wiki 可重現操作；本程式不冒充 LLM')
    sp=parser.add_subparsers(dest='command',required=True)
    i=sp.add_parser('index');i.add_argument('--write',action='store_true');i.add_argument('--record',action='store_true')
    q=sp.add_parser('query');q.add_argument('--question',required=True);q.add_argument('--sources',default='');q.add_argument('--concepts',default='');q.add_argument('--log',action='store_true')
    l=sp.add_parser('lint');l.add_argument('--record',action='store_true')
    ig=sp.add_parser('ingest-verify');ig.add_argument('--id',required=True);ig.add_argument('--record',action='store_true')
    args=parser.parse_args()
    if args.command=='index':
        new=page_index();path=WIKI/'index.md'
        if args.write:
            was=path.read_text(encoding='utf-8') if path.exists() else ''
            path.write_text(new,encoding='utf-8')
            print(f'PASS：索引已更新；來源 {len(read("data/wiki-sources.json"))}、概念 {len(read("data/wiki-concepts.json"))}。變更：{was!=new}')
            if args.record:log('index','重建 Markdown Wiki index', [f'變更：{was!=new}','輸出：wiki/index.md'])
        elif path.read_text(encoding='utf-8')==new:print('PASS：index.md 與現有知識頁一致')
        else:sys.exit('FAIL：index.md 過期，請 index --write')
    elif args.command=='query':
        sids=[x.strip() for x in args.sources.split(',') if x.strip()]
        cids=[x.strip() for x in args.concepts.split(',') if x.strip()]
        ps=[WIKI/'index.md']+[WIKI/'sources'/f'{x}.md' for x in sids]+[WIKI/'concepts'/f'{x}.md' for x in cids]
        bad=[p for p in ps if not p.is_file()]
        if bad:sys.exit('FAIL：查詢頁面缺失 '+', '.join(str(p) for p in bad))
        print('QUESTION: '+args.question)
        print('READ ORDER: '+', '.join(str(p.relative_to(ROOT)) for p in ps))
        for p in ps[1:]:
            print('\n===== '+str(p.relative_to(ROOT))+' =====\n'+p.read_text(encoding='utf-8'))
        print('\n注意：以上為本地文件檢索結果，不是 LLM 自動生成之答案。請交由 LLM 綜合、人工審核、再寫回 Wiki。')
        if args.log:log('query','Wiki 文件檢索（供 LLM 綜合）', ['問題：'+args.question,'讀取頁面：'+', '.join(str(p.relative_to(ROOT)) for p in ps),'此步驟只取得來源，綜合答案另記於 wiki/queries/'])
    elif args.command=='lint':
        errors,warnings=lint()
        for msg in errors:print('FAIL '+msg)
        for msg in warnings:print('NOTE '+msg)
        if args.record:log('lint','Wiki Markdown 連結、索引與關聯檢查',[f'Errors: {len(errors)}',f'Warnings: {len(warnings)}','科學性內容需另行人工／LLM 查核'])
        if errors:sys.exit(1)
        print(f'PASS：Wiki lint 通過；{len(list(WIKI.rglob("*.md")))} 個 Markdown 頁面。')
    elif args.command=='ingest-verify':
        s=next((x for x in read('data/wiki-sources.json') if x['id']==args.id),None)
        if not s:sys.exit('FAIL：JSON 中找不到 '+args.id)
        p=WIKI/'sources'/f'{args.id}.md'
        if not p.exists():sys.exit('FAIL：缺少 '+str(p))
        errors,warnings=lint()
        if errors:sys.exit('FAIL：請先修正 lint 錯誤，不能宣稱 ingest 完成。\n'+'\n'.join(errors))
        print(f'PASS：{args.id} 的結構、DOI、概念關聯已驗證；內容是否忠於 PDF 仍須由 LLM／使用者審核。')
        if args.record:log('ingest','來源結構檢查 '+args.id,['來源：'+s['title'],'DOI：'+s['doi'],'Wiki 頁：'+str(p.relative_to(ROOT)),'注意：這是既有來源的結構檢查，不代表現在重新解析了 PDF'])

if __name__=='__main__':main()
