#!/usr/bin/env python3
"""Exercise each offline type tester against its committed webfont in Chromium.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
Install requirements-original-trio-browser.txt and run playwright install chromium.
"""
from __future__ import annotations
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import importlib.metadata
import json
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright
from build import ROOT, FAMILIES


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def run(executable: str | None = None) -> dict:
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    results = []
    try:
        with sync_playwright() as playwright:
            options = {'headless': True}
            if executable:
                options['executable_path'] = executable
            browser = playwright.chromium.launch(**options)
            try:
                for family in FAMILIES:
                    page = browser.new_page(viewport={'width': 1400, 'height': 1000})
                    errors = []
                    external = []
                    page.on('pageerror', lambda error: errors.append(str(error)))
                    page.on('request', lambda request: external.append(request.url) if not request.url.startswith(f'http://127.0.0.1:{server.server_port}/') else None)
                    url = f'http://127.0.0.1:{server.server_port}/{family}/specimen/index.html'
                    page.goto(url)
                    page.wait_for_function("document.querySelector('#status').textContent.includes('loaded.')")
                    assert page.locator('#coverage .cell').count() == 254
                    sample = 'A0 <script> Ω e\u0301'
                    page.locator('#input').fill(sample)
                    missing = page.locator('#missing').inner_text()
                    assert 'U+03A9' in missing and 'U+0301' in missing
                    assert page.locator('#proof').inner_text() == sample
                    assert page.locator('#proof script').count() == 0
                    page.locator('#size').evaluate("(e)=>{e.value='64';e.dispatchEvent(new Event('input',{bubbles:true}));}")
                    assert page.locator('#proof').evaluate('(e)=>getComputedStyle(e).fontSize') == '64px'
                    page.locator('#line').evaluate("(e)=>{e.value='150';e.dispatchEvent(new Event('input',{bubbles:true}));}")
                    assert page.locator('#proof').evaluate('(e)=>getComputedStyle(e).lineHeight') == '96px'
                    page.locator('#track').evaluate("(e)=>{e.value='5';e.dispatchEvent(new Event('input',{bubbles:true}));}")
                    assert abs(float(page.locator('#proof').evaluate('(e)=>getComputedStyle(e).letterSpacing').removesuffix('px')) - 3.2) < .01
                    page.locator('#kern').uncheck()
                    assert page.locator('#proof').evaluate('(e)=>getComputedStyle(e).fontKerning') == 'none'
                    page.locator('#polarity').click()
                    assert page.locator('body').evaluate("e=>e.classList.contains('dark')")
                    # Both web and desktop fallback URLs must fail visibly, not silently.
                    page.route('**/fonts/*', lambda route: route.abort())
                    page.reload()
                    page.wait_for_function("document.querySelector('#status').textContent.includes('FONT NOT LOADED')")
                    assert not errors, errors
                    assert not external, external
                    results.append({'family': family, 'font_load': True, 'repertoire_cells': 254,
                                    'missing_codepoint_warning': True, 'literal_text_not_html': True,
                                    'size_line_tracking_kerning_controls': True, 'polarity': True,
                                    'load_failure_warning': True, 'external_requests': external,
                                    'script_errors': errors})
                    page.close()
                version = browser.version
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)
    return {'schema': 1, 'successful': True, 'chromium': version,
            'playwright': importlib.metadata.version('playwright'), 'families': results,
            'font_manifest': json.loads((ROOT / 'docs/original-trio-manifest.json').read_text(encoding='utf-8'))}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--executable', help='Optional installed Chromium executable; normally use Playwright Chromium')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = run(args.executable)
    encoded = json.dumps(result, indent=2) + '\n'
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(encoded, encoding='utf-8')
    print(encoded)
