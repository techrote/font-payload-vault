#!/usr/bin/env python3
"""Test twelve local type testers in Chromium over HTTP and file:// URLs.
Copyright (c) 2026 techrote. SIL OFL 1.1; see OFL.txt.
"""
from __future__ import annotations
import argparse,http.server,json,threading,contextlib
from pathlib import Path
from build import ROOT,FAMILIES,master

class SilentHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*args,**kw):super().__init__(*args,directory=str(ROOT),**kw)
    def log_message(self,*a):pass

def main(report=None):
    from playwright.sync_api import sync_playwright
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),SilentHandler)
    thr=threading.Thread(target=server.serve_forever,daemon=True);thr.start()
    output={'schema':1,'successful':False,'browser':None,'families':[],'font_manifest':json.loads((ROOT/'docs/third-cohort-manifest.json').read_text())}
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
            output['browser']=browser.version
            try:
                for rel in FAMILIES:
                    m=master(rel);found={'family':m.FAMILY,'style':m.STYLE,'http_font_load':False,'file_font_load':False,
                        'repertoire_cells':0,'missing_codepoint_warning':False,'literal_text_not_html':False,'controls':False,
                        'polarity_and_reset':False,'visible_font_failure':False,'external_requests':[],'script_errors':[]}
                    path=(ROOT/rel/'specimen/index.html').resolve()
                    for kind,url in [('http',f'http://127.0.0.1:{server.server_port}/{rel}/specimen/index.html'),('file',path.as_uri())]:
                        page=browser.new_page();errors=[];external=[]
                        page.on('pageerror',lambda e:errors.append(str(e)))
                        page.on('request',lambda req:external.append(req.url) if not(req.url.startswith('file:') or req.url.startswith(f'http://127.0.0.1:{server.server_port}/')) else None)
                        page.goto(url,wait_until='load')
                        page.wait_for_function("document.querySelector('#status').dataset.loaded !== undefined",timeout=15000)
                        assert page.locator('#status').get_attribute('data-loaded')=='true',(rel,kind,page.locator('#status').inner_text())
                        found[kind+'_font_load']=True
                        if kind=='http':
                            found['repertoire_cells']=page.locator('.cell').count()
                            assert found['repertoire_cells']==254
                            page.locator('#input').fill('ABC🛰')
                            found['missing_codepoint_warning']='U+1F6F0' in page.locator('#missing').inner_text()
                            assert found['missing_codepoint_warning']
                            unsafe='<img src=x onerror=alert(1)> &'
                            page.locator('#input').fill(unsafe)
                            found['literal_text_not_html']=page.locator('#preview').inner_text()==unsafe and page.locator('#preview img').count()==0
                            assert found['literal_text_not_html']
                            page.evaluate("() => { for (const [id,value] of [['size','71'],['leading','1.5'],['tracking','2']]) {const input=document.getElementById(id); input.value=value;input.dispatchEvent(new Event('input',{bubbles:true}));}}")
                            found['controls']=page.locator('#sizeValue').inner_text()=='71px' and page.locator('#preview').evaluate("el=>getComputedStyle(el).fontSize")=='71px'
                            assert found['controls']
                            page.locator('#dark').check()
                            assert 'dark' in page.locator('body').get_attribute('class')
                            page.locator('#reset').click()
                            found['polarity_and_reset']=('dark' not in (page.locator('body').get_attribute('class') or '') and m.SAMPLES[0] in page.locator('#preview').inner_text())
                            assert found['polarity_and_reset']
                        found['external_requests'].extend(external);found['script_errors'].extend(errors)
                        page.close()
                    # Deliberately prevent the WOFF2 load once to check visible fallback warning.
                    page=browser.new_page()
                    page.route('**/*.woff2',lambda route:route.abort())
                    page.goto(f'http://127.0.0.1:{server.server_port}/{rel}/specimen/index.html')
                    page.wait_for_function("document.querySelector('#status').dataset.loaded !== undefined",timeout=15000)
                    found['visible_font_failure']=(page.locator('#status').get_attribute('data-loaded')=='false' and 'FONT LOAD FAILED' in page.locator('#status').inner_text())
                    assert found['visible_font_failure']
                    page.close()
                    assert not found['external_requests'] and not found['script_errors'],found
                    output['families'].append(found)
                    print(m.FAMILY+': local HTTP/file/browser checks passed',flush=True)
            finally:browser.close()
        output['successful']=True
    finally:
        server.shutdown();server.server_close()
        if report:
            report.parent.mkdir(parents=True,exist_ok=True)
            report.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    assert output['successful'] and len(output['families'])==12
    return output

if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--report',type=Path)
    opts=a.parse_args();main(opts.report)
