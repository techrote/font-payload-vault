"""Assemble the self-contained type tester (all per-size web fonts embedded as data URIs).

Writes ../specimen/specimen.html (opens offline from disk) and ../specimen/tester-artifact.html
(the same page without a document skeleton, for publishing as a claude.ai artifact).
"""
import base64, os
HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(HERE, '..', 'fonts', 'web')
OUT = os.path.join(HERE, '..', 'specimen')

def b64(name):
    with open(os.path.join(WEB, name), 'rb') as f:
        return base64.b64encode(f.read()).decode()

def main():
    t = open(os.path.join(HERE, 'tester.template.html'), encoding='utf-8').read()
    faces = [f'@font-face{{font-family:"BluedSwarf{n}{w}";src:url(data:font/woff2;base64,{b64(f"BluedSwarf{n}px-{w}.woff2")}) format("woff2");}}'
             for n in range(6, 17) for w in ('Regular', 'Bold')]
    t = (t.replace('{{FACES}}', '\n'.join(faces))
          .replace('{{UI11}}', b64('BluedSwarf11px-Regular.woff2'))
          .replace('{{UI11B}}', b64('BluedSwarf11px-Bold.woff2')))
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, 'tester-artifact.html'), 'w', encoding='utf-8') as f:
        f.write(t)
    with open(os.path.join(OUT, 'specimen.html'), 'w', encoding='utf-8') as f:
        f.write('<!doctype html>\n<html lang="en"><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width, initial-scale=1">\n' + t)
    print('ok')

if __name__ == '__main__':
    main()
