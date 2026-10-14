#!/usr/bin/env python3
"""Exercise all twelve actual offline testers over HTTP and file URLs.
Copyright (c) 2026 techrote. SIL OFL 1.1; see OFL.txt.
"""
from __future__ import annotations
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from importlib.metadata import version
import json
from pathlib import Path
import threading
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
from build import ROOT, FAMILIES, config

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass


def run(report_path=None,executable=None):
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    origin=f'http://127.0.0.1:{server.server_address[1]}'
    records=[]
    try:
        with sync_playwright() as pw:
            options=dict(headless=True,args=['--no-sandbox'])
            if executable:options['executable_path']=str(executable)
            browser=pw.chromium.launch(**options)
            for rel in FAMILIES:
                cfg=config(rel);context=browser.new_context();page=context.new_page()
                external=[];errors=[]
                def request_seen(request):
                    u=urlparse(request.url)
                    if u.scheme in ('http','https') and not request.url.startswith(origin+'/'):external.append(request.url)
                page.on('request',request_seen);page.on('pageerror',lambda error:errors.append(str(error)))
                page.goto(origin+'/'+rel+'/specimen/index.html',wait_until='load')
                page.wait_for_function("document.getElementById('status').dataset.loaded==='true'")
                css_style='oblique' if cfg['style']=='Oblique' else 'normal'
                assert page.evaluate('(s)=>document.fonts.check(s)',f'{css_style} 52px "{cfg["family"]}"')
                assert page.locator('#grid .cell').count()==254
                assert page.locator('#preview').evaluate('(el)=>getComputedStyle(el).fontFamily').split(',')[0].replace('"','')==cfg['family']
                literal='<img src=x onerror="window.badInput=1"> & <b>literal</b>'
                page.locator('#input').fill(literal)
                assert page.locator('#preview').text_content()==literal
                assert page.locator('#preview img, #preview b').count()==0
                assert page.evaluate('typeof window.badInput')=='undefined'
                page.locator('#input').fill('a\u0301 \U0001F600')
                warning=page.locator('#missing').text_content()
                assert 'U+0301' in warning and 'U+1F600' in warning
                page.evaluate("""()=>{for(const [id,v] of [['size','83'],['line','1.7'],['tracking','2.5']]){const e=document.getElementById(id);e.value=v;e.dispatchEvent(new Event('input'));}}""")
                assert page.locator('#preview').evaluate('(e)=>e.style.fontSize')=='83px'
                assert page.locator('#preview').evaluate('(e)=>e.style.lineHeight')=='1.7'
                assert page.locator('#preview').evaluate('(e)=>e.style.letterSpacing')=='2.5px'
                page.locator('#polarity').check();assert page.locator('body').evaluate("e=>e.classList.contains('dark')")
                page.locator('#reset').click()
                assert page.locator('#size').input_value()=='52'
                assert page.locator('#line').input_value()=='1.25'
                assert page.locator('#tracking').input_value()=='0'
                assert not page.locator('#polarity').is_checked()
                assert page.locator('#input').input_value().startswith(cfg['family']+'\n')
                assert not page.locator('#missing').text_content()
                page.goto((ROOT/rel/'specimen/index.html').as_uri(),wait_until='load')
                page.wait_for_function("document.getElementById('status').dataset.loaded==='true'")
                assert page.locator('#grid .cell').count()==254
                assert not errors,(rel,errors)
                assert not external,(rel,external)
                context.close()
                # A fresh context prevents a previous font cache from concealing failure.
                failure_context=browser.new_context();failure=failure_context.new_page()
                failure.route('**/*.woff2',lambda route:route.abort())
                failure.goto(origin+'/'+rel+'/specimen/index.html',wait_until='load')
                failure.wait_for_function("document.getElementById('status').dataset.loaded==='false'")
                assert failure.locator('#status').is_visible()
                assert 'FONT LOAD FAILED' in failure.locator('#status').text_content()
                failure_context.close()
                records.append(dict(family=cfg['family'],http_font_load=True,file_font_load=True,repertoire_cells=254,
                  actual_family_selected=True,literal_text_not_html=True,missing_unicode_warning=True,
                  controls=True,polarity=True,full_reset=True,visible_font_failure=True,external_requests=external,script_errors=errors))
                print(cfg['family']+': HTTP, file URL, controls, Unicode and failure checks passed',flush=True)
            chromium=browser.version;browser.close()
    finally:
        server.shutdown();server.server_close();thread.join(timeout=5)
    report=dict(schema=1,successful=True,chromium=chromium,playwright=version('playwright'),families=records,
      font_manifest=json.loads((ROOT/'docs/fourth-cohort-manifest.json').read_text(encoding='utf-8')))
    if report_path:
        report_path.parent.mkdir(parents=True,exist_ok=True);report_path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--report',type=Path)
    parser.add_argument('--executable',type=Path,help='Optional local Chromium; hosted acceptance uses pinned Playwright Chromium')
    args=parser.parse_args();run(args.report,args.executable)
