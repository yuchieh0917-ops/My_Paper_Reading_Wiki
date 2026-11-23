#!/usr/bin/env python3
"""Executable gate graph: validates data; reports return nodes; can be called by CI."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
steps=[('Wiki 索引同步 / Gate 0',[sys.executable,str(ROOT/'tools/wiki_ops.py'),'index']),('Wiki Markdown Lint / Gate 1',[sys.executable,str(ROOT/'tools/wiki_ops.py'),'lint']),('來源與 LLM Query 映射完整性 / Gate 2',[sys.executable,str(ROOT/'tools/validate_project.py')]),('教學 HTML 與 Wiki 大綱一致性 / Gate 3',[sys.executable,str(ROOT/'tools/build_slides.py'),'--check']),('前端 JavaScript 語法 / Gate 4',['node','--check',str(ROOT/'scripts/wiki.js')]),('投影片控制 JavaScript / Gate 4',['node','--check',str(ROOT/'scripts/slides.js')])]
for title,cmd in steps:
 print('RUN',title,flush=True)
 try: code=subprocess.call(cmd)
 except FileNotFoundError: print('SKIP：缺少 Node.js；請在 GitHub Actions 或本機安裝 Node.js。');continue
 if code:
  print('FAIL：請依錯誤類型回到 ingest／Wiki 建構或 HTML 修正節點，重新測試。');sys.exit(code)
print('PASS：所有可執行檢查節點通過；瀏覽器視覺仍應人工檢查。')
