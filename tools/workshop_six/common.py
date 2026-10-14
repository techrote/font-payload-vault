"""Shared drawing tools and original ASCII punctuation, not a shared alphabet.
Copyright (c) 2026 techrote. SIL OFL 1.1; see OFL.txt.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'original_trio'))
from geometry import *
ASCII=set(map(chr,range(32,127)))

def ellipse(x0,y0,x1,y1):
    return translate(scale(disc(0,0,1),xfact=(x1-x0)/2,yfact=(y1-y0)/2,origin=(0,0)),xoff=(x1+x0)/2,yoff=(y1+y0)/2)

def oval(x0,y0,x1,y1,wx=80,wy=70):
    return ellipse(x0,y0,x1,y1).difference(ellipse(x0+wx,y0+wy,x1-wx,y1-wy))

def fitted(g,advance,margin=48):
    if g.is_empty:return g
    x0,_,x1,_=g.bounds
    factor=min(1,(advance-2*margin)/(x1-x0))
    g=scale(g,xfact=factor,yfact=1,origin=(0,0));x0,_,x1,_=g.bounds
    return clean(translate(g,xoff=(advance-x1+x0)/2-x0))

def punctuation(width=72):
    """Nominal 600-unit common symbol drawings; each face fits/decorates them."""
    s=lambda spec:path(spec,width,cap='round',join='round')
    d=lambda x,y:disc(x,y,width*.60)
    p={
    ' ':Polygon(),'.':d(300,42),',':s('M 325 80 L 282 -65'),':':merge(d(300,85),d(300,422)),
    ';':merge(d(300,422),s('M 321 95 L 276 -64')),
    '!':merge(s('M 300 710 L 300 244'),d(300,45)),
    '?':merge(s('M 134 551 C 152 783 501 749 480 548 C 477 443 306 431 300 260'),d(300,45)),
    '"':merge(s('M 222 721 L 222 550'),s('M 378 721 L 378 550')),
    "'":s('M 300 721 L 300 550'),
    '`':s('M 243 730 L 357 603'),
    '#':s('M 218 705 L 143 -5 M 452 705 L 377 -5 M 92 234 L 503 234 M 116 473 L 527 473'),
    '$':merge(s('M 486 590 C 414 753 125 739 121 558 C 115 390 477 408 479 197 C 480 -4 194 -25 108 115'),s('M 300 -110 L 300 799')),
    '%':merge(oval(66,399,273,720,54,54),oval(327,-5,534,316,54,54),s('M 122 -1 L 478 714')),
    '&':s('M 506 29 L 157 435 C 25 614 320 818 413 613 C 480 459 112 365 123 169 C 135 -74 464 -32 502 316'),
    '(':s('M 387 761 C 111 586 111 133 387 -71'),
    ')':s('M 213 761 C 489 586 489 133 213 -71'),
    '*':s('M 300 676 L 300 300 M 124 579 L 476 387 M 124 387 L 476 579'),
    '+':s('M 100 310 L 500 310 M 300 110 L 300 510'),
    '-':s('M 121 308 L 479 308'),
    '/':s('M 109 -48 L 491 755'),
    '\\':s('M 109 755 L 491 -48'),
    '=':s('M 105 195 L 495 195 M 105 415 L 495 415'),
    '<':s('M 460 553 L 141 310 L 460 67'),
    '>':s('M 140 553 L 459 310 L 140 67'),
    '@':s('M 427 168 L 445 541 C 216 675 120 148 356 191 C 403 201 427 271 437 394 M 427 190 C 547 27 661 408 510 631 C 357 876 24 684 52 320 C 63 82 196 -107 429 -43'),
    '[':s('M 399 755 L 210 755 L 210 -69 L 399 -69'),
    ']':s('M 201 755 L 390 755 L 390 -69 L 201 -69'),
    '^':s('M 137 525 L 300 716 L 463 525'),
    '_':s('M 62 -109 L 538 -109'),
    '{':s('M 428 754 C 241 788 261 612 266 537 C 272 403 229 363 127 344 C 229 323 273 281 267 145 C 262 56 241 -116 428 -77'),
    '}':s('M 172 754 C 359 788 339 612 334 537 C 328 403 371 363 473 344 C 371 323 327 281 333 145 C 338 56 359 -116 172 -77'),
    '|':s('M 300 -109 L 300 781'),
    '~':s('M 106 272 C 224 463 376 147 494 338'),
    }
    return p

def finish(letters,digits,advance=650,mono=False,width=72,decorator=None):
    """Source dictionaries use character: (geometry, advance). No silent fallback."""
    expected=set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
    if set(letters)!=expected or set(digits)!=set('0123456789'):
        raise ValueError('Incomplete independently drawn alphabet/digit master')
    out={**letters,**digits}
    punct=punctuation(width)
    for c,g in punct.items():
        a=advance if mono else (300 if c==' ' else 290 if c in ".,:;!'`|" else 440 if c in '()[]{}"' else 620)
        out[c]=(fitted(g,a,48),a)
    assert set(out)==ASCII
    if decorator:
        out={c:(decorator(c,g,a),a) for c,(g,a) in out.items()}
    return {c:(clean(g),a) for c,(g,a) in out.items()}
