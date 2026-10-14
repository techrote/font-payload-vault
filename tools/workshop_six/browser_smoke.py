#!/usr/bin/env python3
"""Test the six specimens over loopback HTTP and directly from local files.
Copyright (c) 2026 techrote. SIL OFL 1.1; see OFL.txt.
"""
from __future__ import annotations
import argparse,json
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from importlib.metadata import version
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright
from build import ROOT,FAMILIES,master
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

def run():
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
    thread=Thread(target=server.serve_forever,daemon=True);thread.start();results=[]
    origin=f'http://127.0.0.1:{server.server_port}/'
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            try:
                for rel in FAMILIES:
                    m=master(rel);page=browser.new_page(viewport={'width':1400,'height':1000});errors=[];external=[]
                    page.on('pageerror',lambda e:errors.append(str(e)))
                    page.on('request',lambda r:external.append(r.url) if not r.url.startswith(origin) else None)
                    page.goto(origin+rel+'/specimen/index.html')
                    page.wait_for_function("document.querySelector('#status').dataset.loaded==='true'")
                    assert page.locator('#grid .cell').count()==254
                    assert m.FAMILY in page.locator('#status').inner_text()
                    sample='A0 <script>window.__injected=1</script> Ω e\u0301 🔧'
                    page.locator('#input').fill(sample)
                    assert page.locator('#preview').inner_text()==sample
                    assert page.locator('#preview script').count()==0
                    assert page.evaluate('window.__injected===undefined')
                    warning=page.locator('#missing').inner_text()
                    assert all(s in warning for s in ('U+03A9','U+0301','U+1F527'))
                    for id,value in [('size','64'),('line','1.5'),('tracking','2')]:
                        page.locator('#'+id).evaluate('(e,v)=>{e.value=v;e.dispatchEvent(new Event("input",{bubbles:true}));}',value)
                    assert page.locator('#preview').evaluate('e=>getComputedStyle(e).fontSize')=='64px'
                    assert page.locator('#preview').evaluate('e=>getComputedStyle(e).lineHeight')=='96px'
                    assert page.locator('#preview').evaluate('e=>getComputedStyle(e).letterSpacing')=='2px'
                    assert page.locator('#preview').evaluate('e=>getComputedStyle(e).fontSynthesis')=='none'
                    page.locator('#polarity').check();assert page.locator('body').evaluate('e=>e.classList.contains("dark")')
                    page.locator('#reset').click();assert page.locator('#input').input_value()=='\n'.join(m.SAMPLES)
                    page.route('**/fonts/*',lambda route:route.abort());page.reload()
                    page.wait_for_function("document.querySelector('#status').dataset.loaded==='false'")
                    assert 'fallback' in page.locator('#status').inner_text()
                    assert not errors,errors
                    assert not external,external
                    page.close()
                    # Verify the documented double-click/local-file route too.
                    local=browser.new_page();local_errors=[];local_network=[]
                    local.on('pageerror',lambda e:local_errors.append(str(e)))
                    local.on('request',lambda r:local_network.append(r.url) if not r.url.startswith('file:') else None)
                    local.goto((ROOT/rel/'specimen/index.html').as_uri())
                    local.wait_for_function("document.querySelector('#status').dataset.loaded==='true'")
                    assert local.locator('#grid .cell').count()==254
                    assert not local_errors,local_errors
                    assert not local_network,local_network
                    local.close()
                    results.append({'family':m.FAMILY,'http_font_load':True,'file_font_load':True,'repertoire_cells':254,
                        'missing_unicode_warning':True,'literal_text_not_html':True,'controls':True,'polarity':True,'reset':True,
                        'visible_font_failure':True,'external_requests':[],'script_errors':[]})
                chromium=browser.version
            finally:browser.close()
    finally:
        server.shutdown();server.server_close();thread.join(timeout=5)
    return {'schema':1,'successful':True,'chromium':chromium,'playwright':version('playwright'),'families':results,
        'font_manifest':json.loads((ROOT/'docs/workshop-six-manifest.json').read_text(encoding='utf-8'))}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',type=Path);args=p.parse_args();result=run()
    text=json.dumps(result,indent=2)+'\n'
    if args.report:args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(text,encoding='utf-8')
    print(text)
