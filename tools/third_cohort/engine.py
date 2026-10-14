"""Geometry and character-composition engine for the third original-font cohort.
Only this project's four handwritten alphabets contribute letter outlines.
Copyright (c) 2026 techrote. Released with the font source under SIL OFL 1.1.
"""
from __future__ import annotations
import hashlib,math,unicodedata
from shapely.geometry import Point, LineString, Polygon, GeometryCollection, box as shapely_box
from shapely.ops import unary_union
from shapely.affinity import translate,scale,skew
from masters import TRACE,BUSHING,MICRO,GRID

ASCII={chr(i) for i in range(32,127)}
CP1252=set('€‚ƒ„…†‡ˆ‰Š‹ŒŽ‘’“”•–—˜™š›œžŸ')
SYMBOLS=set('←↑→↓▲►▼◄✓✗■□●○─│┌┐└┘├┤┬┴┼█▀▄▌▐░▒▓≠≤≥±')
COVERAGE=ASCII|{chr(i) for i in range(160,256)}|CP1252|SYMBOLS
BLANK={' ','\u00a0','\u00ad'}
BOUNDS=(-250,1000)

def rect(x0,y0,x1,y1):return shapely_box(x0,y0,x1,y1)
def disc(x,y,r):return Point(x,y).buffer(r,quad_segs=9)
def union(*geom):
    xs=[g for g in geom if g is not None and not g.is_empty]
    if not xs:return GeometryCollection()
    return unary_union(xs)
def path_points(spec):
    out=[]
    for section in spec.split('|'):
        pts=[]
        for item in section.split():
            x,y=item.split(',');pts.append((float(x),float(y)))
        if pts:out.append(pts)
    return out

def paths_geom(spec,stem,quad_segs=4,cap=2,join=2,scale_x=74,scale_y=86,ox=111):
    pieces=[]
    for section in path_points(spec):
        pts=[(ox+x*scale_x,y*scale_y) for x,y in section]
        if len(pts)==1:pieces.append(disc(*pts[0],stem/2))
        elif len(pts)==2 and pts[0]==pts[1]:pieces.append(disc(*pts[0],stem/2))
        else:pieces.append(LineString(pts).buffer(stem/2,cap_style=cap,join_style=join,quad_segs=quad_segs,mitre_limit=2.5))
    return union(*pieces)

def grid_geom(rows,mode):
    pix=[]
    if len(rows)!=9 or any(len(row)!=7 or set(row)-set('.#') for row in rows):
        raise ValueError('Expected authored nine-row, seven-column grid')
    for y,row in enumerate(rows):
        cy=705-y*86
        for x,v in enumerate(row):
            if v!='#':continue
            cx=111+x*75
            if mode=='pixel':pix.append(rect(cx-30,cy-32,cx+30,cy+33))
            elif mode=='forge':
                # Thickening toward the output edge produces stepped internal mass.
                pix.append(Polygon([(cx-40,cy-45),(cx+36,cy-45),(cx+44,cy-37),(cx+44,cy+43),(cx-40,cy+43)]))
                if x<6 and row[x+1]!='#':pix.append(rect(cx+20,cy-11,cx+46,cy+6))
            elif mode=='haze':
                pix.append(rect(cx-22,cy-20,cx+22,cy+22))
                digest=hashlib.sha256(f'checksum-haze-v1:{x}:{y}:{row}'.encode()).digest()
                if digest[0]%3!=0:
                    dx=31+digest[1]%15
                    pix.append(rect(cx+dx-6,cy-10,cx+dx+6,cy+2))
                if digest[2]%5==0:pix.append(rect(cx-14,cy-42,cx+1,cy-31))
    return union(*pix)

def snap(g):
    if g.is_empty:return GeometryCollection()
    # Boolean resolution is performed before integer serialization by the font pen.
    # `buffer(0)` repairs self-touching strokes; no simplification alters features.
    return g.buffer(0)

def fit(g,advance,margin=32):
    if g.is_empty:return g
    x0,_,x1,_=g.bounds
    fac=min(1.0,(advance-2*margin)/max(1.0,x1-x0))
    if fac<1:g=scale(g,xfact=fac,yfact=1,origin=(0,0))
    x0,_,x1,_=g.bounds
    return translate(g,xoff=(advance-(x0+x1))/2)

def bounds_clip(g,adv):
    return snap(g.intersection(rect(0,-250,adv,1000))) if not g.is_empty else g

def mod_plate(g,adv,code):
    # Hollow weld seam around an unusually massive bridge; retain the core.
    bulky=g.buffer(32,join_style=2).buffer(0)
    inset=bulky.buffer(-42,join_style=2)
    return bulky.difference(inset)

def mod_ghost(g,adv,code):
    # A real separated echo, not OpenType shadow color or time-dependent noise.
    a=translate(g,xoff=-40,yoff=0)
    b=translate(g,xoff=62,yoff=34)
    a=a.difference(rect(0,265,adv,278)) if ord(code)%3==0 else a
    return union(a,b)

def mod_sling(g,adv,code):
    return skew(g,xs=12,origin=(adv/2,0))

def mod_eddy(g,adv,code):
    # Deterministic drilled-out interruption; never applied to neutral symbols.
    h=hashlib.sha256(('eddy-notch-v1:'+code).encode()).digest()
    cuts=[]
    for j in range(2):
        x=adv*(.30+.36*(h[2*j]/255));y=135+510*(h[2*j+1]/255)
        cuts.append(disc(x,y,21))
    return g.difference(union(*cuts))

def mod_torque(g,adv,code):
    # Original angular stock gets one small fastening hole in select wide glyphs.
    if code in 'BDOPQR0689':
        hole=disc(adv*.12,535,13)
        return g.difference(hole)
    return g

def mod_carbon(g,adv,code):
    # Chatter-gouges inclined to the stroke: bounded, stable subtractive texture.
    if code in ' ,.;:':return g
    holes=[]
    d=hashlib.sha256(('carbon-check-v1:'+code).encode()).digest()
    for j in range(3):
        yy=148+j*217+(d[j]%29)
        # A diagonal milling-chatter stripe spans the full current silhouette.
        holes.append(LineString([(adv*.09,yy-35),(adv*.91,yy+52)]).buffer(13,cap_style=2))
    return g.difference(union(*holes))

def cap_specific(c,g,style,adv):
    if style=='bridge':return mod_plate(g,adv,c)
    if style=='ghost':return mod_ghost(g,adv,c)
    if style=='sling':return mod_sling(g,adv,c)
    if style=='eddy':return mod_eddy(g,adv,c)
    if style=='torque':return mod_torque(g,adv,c)
    if style=='carbon':return mod_carbon(g,adv,c)
    return g

def drawn_ascii(mod):
    lineage=mod.LINEAGE
    outlines={'trace':TRACE,'bushing':BUSHING,'micro':MICRO,'grid':GRID}[lineage]
    assert len(outlines)==62
    originals={**outlines,**getattr(mod,'PATCHES',{})}
    out={}
    for c in sorted(ASCII):
        if c==' ':
            out[c]=(GeometryCollection(),mod.ADVANCE if mod.MONO else 310)
            continue
        if c in originals:
            if lineage=='grid':
                # Only this lineage uses a source bitmap. The grid is still a font outline,
                # not imported bitmap strikes.
                rows=originals[c].split('/')
                g=grid_geom(rows,mod.MODE)
            else:
                g=paths_geom(originals[c],mod.STEM,cap=1 if mod.MODE in ('bush','sling','eddy') else 2,join=1 if mod.MODE in ('bush','sling','eddy') else 2)
                if lineage=='micro' and mod.MODE=='slab':
                    # Bracketless, deliberately selective feet, not slabs on all corners.
                    terminals=[]
                    for seg in path_points(originals[c]):
                        for x,y in (seg[0],seg[-1]):
                            if y in (0,8) and c not in 'OSQ0oabcdegsuwvxz':
                                cx=111+x*74;cy=y*86
                                terminals.append(rect(cx-75,cy-24,cx+75,cy+24))
                    g=union(g,*terminals)
                g=cap_specific(c,g,mod.MODE,mod.ADVANCE)
            if mod.MODE=='ghost' and c in '0O':
                g=union(g,LineString([(230,140),(490,650)]).buffer(21,cap_style=2))
            # Variable width follows drawn geometry, with an explicit tabular digit contract.
            if mod.MONO:adv=mod.ADVANCE
            elif c.isdigit():adv=mod.DIGIT_ADVANCE
            else:
                gw=g.bounds[2]-g.bounds[0] if not g.is_empty else 300
                adv=max(380,min(mod.ADVANCE,round(gw+mod.TRACK)))
            g=fit(g,adv,mod.MARGIN)
            out[c]=(bounds_clip(g,adv),adv)
        else:
            adv=mod.ADVANCE if mod.MONO else (mod.DIGIT_ADVANCE if c.isdigit() else 500)
            g=punctuation_shape(c,adv,mod.STEM,mod.LINEAGE)
            out[c]=(bounds_clip(g,adv),adv)
    return out

def punctuation_shape(c,adv,stem,lineage):
    # A shared *newly authored* ASCII punctuation set, visually adapted by stem.
    cx=adv/2; b=stem*.76
    L=lambda points:LineString(points).buffer(b/2,cap_style=2,join_style=2)
    D=lambda x,y:disc(x,y,stem*.48)
    parts=[]
    p=rect
    if c in '.·':parts=[D(cx,55)]
    elif c==',':parts=[L([(cx+15,75),(cx-16,-72)])]
    elif c==':':parts=[D(cx,65),D(cx,440)]
    elif c==';':parts=[D(cx,435),L([(cx+15,80),(cx-12,-65)])]
    elif c=='!':parts=[L([(cx,715),(cx,218)]),D(cx,40)]
    elif c=='?':parts=[L([(adv*.22,540),(adv*.28,710),(adv*.68,710),(adv*.78,560),(cx,390),(cx,225)]),D(cx,39)]
    elif c in "'’‘`":parts=[L([(cx+11,715),(cx-12,550)])]
    elif c=='"':parts=[L([(cx-70,715),(cx-78,553)]),L([(cx+70,715),(cx+60,553)])]
    elif c in '-−–—_':parts=[L([(adv*.16,340 if c!='_' else 0),(adv*.84,340 if c!='_' else 0)])]
    elif c=='+':parts=[L([(adv*.16,352),(adv*.84,352)]),L([(cx,125),(cx,580)])]
    elif c=='=':parts=[L([(adv*.17,250),(adv*.83,250)]),L([(adv*.17,460),(adv*.83,460)])]
    elif c in '/\\':parts=[L([(adv*(.15 if c=='/' else .85),-90),(adv*(.85 if c=='/' else .15),765)])]
    elif c=='|':parts=[L([(cx,-160),(cx,825)])]
    elif c=='#':parts=[L([(cx-102,740),(cx-151,0)]),L([(cx+110,740),(cx+62,0)]),L([(adv*.12,240),(adv*.88,240)]),L([(adv*.12,510),(adv*.88,510)])]
    elif c=='$':parts=[L([(adv*.76,650),(adv*.33,720),(adv*.16,570),(adv*.78,220),(adv*.63,0),(adv*.18,100)]),L([(cx,-110),(cx,810)])]
    elif c=='%':parts=[D(adv*.27,610).difference(D(adv*.27,610).buffer(-stem*.24)),D(adv*.72,125).difference(D(adv*.72,125).buffer(-stem*.24)),L([(adv*.23,20),(adv*.78,705)])]
    elif c=='&':parts=[L([(adv*.79,100),(adv*.49,410),(adv*.25,655),(adv*.52,755),(adv*.61,590),(adv*.20,330),(adv*.20,40),(adv*.73,40),(adv*.82,260)])]
    elif c in '()':
        x0=adv*(.66 if c=='(' else .34);x1=adv*(.25 if c=='(' else .75)
        parts=[L([(x0,815),(x1,680),(x1,80),(x0,-130)])]
    elif c in '[]':
        x=adv*(.24 if c=='[' else .76);sgn=1 if c=='[' else -1
        parts=[L([(x+sgn*adv*.29,810),(x,810),(x,-100),(x+sgn*adv*.29,-100)])]
    elif c in '{}':
        x=adv*(.65 if c=='{' else .35);d= -1 if c=='{' else 1
        parts=[L([(x,790),(x+d*adv*.19,750),(x+d*adv*.19,470),(x,360),(x+d*adv*.19,240),(x+d*adv*.19,-50),(x,-100)])]
    elif c in '<>':parts=[L([(adv*(.75 if c=='<' else .25),685),(adv*(.2 if c=='<' else .8),360),(adv*(.75 if c=='<' else .25),35)])]
    elif c=='@':
        outer=Point(cx,350).buffer(289,quad_segs=24).difference(Point(cx,350).buffer(246,quad_segs=24))
        parts=[outer,L([(adv*.71,275),(adv*.71,540),(adv*.44,550),(adv*.35,430),(adv*.45,272),(adv*.7,270),(adv*.84,365)])]
    elif c=='^':parts=[L([(adv*.17,430),(cx,756),(adv*.83,430)])]
    elif c=='~':parts=[L([(adv*.16,390),(adv*.35,455),(adv*.64,335),(adv*.84,405)])]
    elif c=='*':parts=[L([(cx,215),(cx,665)]),L([(adv*.25,300),(adv*.75,590)]),L([(adv*.25,590),(adv*.75,300)])]
    else:parts=[p(adv*.31,232,adv*.69,452)]
    return union(*parts)

def mark(accent,mid,y):
    line=lambda pts:LineString(pts).buffer(28,cap_style=2,join_style=2)
    if accent=='\u0300':return line([(mid+15,y+50),(mid-47,y+128)])
    if accent=='\u0301':return line([(mid-15,y+50),(mid+47,y+128)])
    if accent=='\u0302':return line([(mid-87,y+40),(mid,y+123),(mid+87,y+40)])
    if accent=='\u0303':return line([(mid-80,y+65),(mid-36,y+95),(mid+18,y+62),(mid+80,y+95)])
    if accent=='\u0308':return union(disc(mid-67,y+79,28),disc(mid+67,y+79,28))
    if accent=='\u030a':return disc(mid,y+76,66).difference(disc(mid,y+76,37))
    if accent=='\u0304':return line([(mid-83,y+79),(mid+83,y+79)])
    if accent=='\u0306':return line([(mid-65,y+112),(mid,y+60),(mid+65,y+112)])
    if accent=='\u030c':return line([(mid-80,y+124),(mid,y+43),(mid+80,y+124)])
    if accent=='\u0307':return disc(mid,y+80,28)
    return line([(mid-83,y+44),(mid+83,y+44)])

def compose(base,acc,sh,stem):
    g,a=sh[base]
    if base=='i':
        g=g.intersection(rect(0,-250,a,510))
    mid=a*.5
    if acc in ('\u0327','\u0328'):
        low=LineString([(mid-13,-30),(mid+22,-109),(mid-44,-185)]).buffer(stem*.35,cap_style=2)
        return bounds_clip(union(g,low),a),a
    y=min(815,g.bounds[3]+42)
    overlay=mark(acc,mid,y)
    if overlay.bounds[3]>985:overlay=translate(overlay,yoff=985-overlay.bounds[3])
    return bounds_clip(union(g,overlay),a),a

def shape_compose(c,sh,mod):
    # Derived auxiliary contours are openly shared recipes; original drawn Latin stays per-lineage.
    a=mod.ADVANCE if mod.MONO else 585
    d=unicodedata.normalize('NFD',c)
    if len(d)==2 and d[0] in sh and unicodedata.combining(d[1]):return compose(d[0],d[1],sh,mod.STEM)
    if c in ('\u00a0','\u00ad'):return GeometryCollection(),sh[' '][1]
    if c in 'ÆæŒœ':
        pair={'Æ':'AE','æ':'ae','Œ':'OE','œ':'oe'}[c]
        g=union(translate(scale(sh[pair[0]][0],xfact=.64,yfact=1,origin=(0,0)),xoff=-12),translate(scale(sh[pair[1]][0],xfact=.62,yfact=1,origin=(0,0)),xoff=a*.37))
        return bounds_clip(fit(g,a,22),a),a
    if c in 'Øø':
        pair='O' if c=='Ø' else 'o';g,b=sh[pair]
        return bounds_clip(union(fit(g,a,42),LineString([(a*.26,60),(a*.75,670 if c=='Ø' else 440)]).buffer(mod.STEM*.30,cap_style=2)),a),a
    if c in 'Ðð':
        g,b=sh['D' if c=='Ð' else 'd'];return bounds_clip(union(fit(g,a),rect(a*.10,360,a*.88,398)),a),a
    if c in 'Þþ':
        g,b=sh['P' if c=='Þ' else 'p'];return bounds_clip(fit(g,a),a),a
    if c=='ß':return bounds_clip(fit(union(sh['B'][0],translate(scale(sh['s'][0],xfact=.5,yfact=.6,origin=(0,0)),xoff=a*.34)),a),a),a
    if c in 'Łł':
        g,_=sh['L' if c=='Ł' else 'l'];return bounds_clip(union(fit(g,a),LineString([(a*.16,300),(a*.78,460)]).buffer(23,cap_style=2)),a),a
    if c=='ı':
        g,_=sh['i'];return bounds_clip(g.intersection(rect(0,-250,a,515)),a),a
    if c in '¡¿':
        g,_=sh['!' if c=='¡' else '?'];return bounds_clip(scale(g,xfact=-1,yfact=-1,origin=(a/2,350)),a),a
    if c in 'ªº':
        g,_=sh['a' if c=='ª' else 'o'];return bounds_clip(translate(scale(g,xfact=.65,yfact=.66,origin=(0,0)),xoff=55,yoff=230),a),a
    if c in '¹²³':
        g,_=sh[{'¹':'1','²':'2','³':'3'}[c]];return bounds_clip(translate(scale(g,xfact=.54,yfact=.54,origin=(0,0)),xoff=150,yoff=400),a),a
    if c in '¼½¾':
        first,last={'¼':('1','4'),'½':('1','2'),'¾':('3','4')}[c]
        g=union(translate(scale(sh[first][0],xfact=.43,yfact=.4,origin=(0,0)),xoff=5,yoff=350),translate(scale(sh[last][0],xfact=.43,yfact=.4,origin=(0,0)),xoff=a*.52),LineString([(a*.37,85),(a*.64,630)]).buffer(21,cap_style=2))
        return bounds_clip(g,a),a
    if c in '§¶':return bounds_clip(punctuation_shape('&' if c=='§' else '#',a,mod.STEM,mod.LINEAGE),a),a
    if c in '¢£¥€':
        base={'¢':'c','£':'E','¥':'Y','€':'C'}[c]
        g,_=sh[base];g=fit(g,a)
        extra=(rect(a*.13,240,a*.86,275) if c in '£€' else LineString([(a*.5,85),(a*.5,690)]).buffer(22,cap_style=2))
        if c=='¥':extra=union(rect(a*.14,230,a*.84,266),rect(a*.14,340,a*.84,376))
        return bounds_clip(union(g,extra),a),a
    if c in '©®':
        outer=disc(a*.5,370,295).difference(disc(a*.5,370,264))
        g,_=sh['C' if c=='©' else 'R'];return bounds_clip(union(outer,translate(scale(g,xfact=.58,yfact=.64,origin=(0,0)),xoff=a*.23,yoff=170)),a),a
    if c in '°º':return disc(a*.5,625,103).difference(disc(a*.5,625,64)),a
    if c in 'µ':
        g,_=sh['u'];return bounds_clip(union(g,rect(a*.12,-172,a*.20,145)),a),a
    if c in '×÷':
        if c=='×':return punctuation_shape('*',a,mod.STEM,mod.LINEAGE),a
        return union(rect(a*.2,320,a*.8,356),disc(a*.5,510,33),disc(a*.5,165,33)),a
    if c in '±≠≤≥':
        if c=='±':return union(punctuation_shape('+',a,mod.STEM,mod.LINEAGE),rect(a*.18,80,a*.82,110)),a
        if c=='≠':return union(punctuation_shape('=',a,mod.STEM,mod.LINEAGE),punctuation_shape('/',a,mod.STEM*.50,mod.LINEAGE)),a
        s='<' if c=='≤' else '>';return union(punctuation_shape(s,a,mod.STEM,mod.LINEAGE),rect(a*.17,35,a*.83,65)),a
    if c in '←↑→↓':
        if c in '←→':
            s=-1 if c=='←' else 1;mid=a*.50
            return union(rect(a*.18,327,a*.82,372),LineString([(mid+s*a*.25,545),(mid+s*a*.39,350),(mid+s*a*.25,160)]).buffer(37,cap_style=2,join_style=2)),a
        sign=1 if c=='↑' else -1
        return union(rect(a*.47,140,a*.53,750),LineString([(a*.25,405+sign*130),(a*.50,405+sign*310),(a*.75,405+sign*130)]).buffer(38,cap_style=2)),a
    if c in '▲►▼◄':
        points={'▲':[(a*.5,775),(a*.1,70),(a*.9,70)],'▼':[(a*.1,710),(a*.9,710),(a*.5,0)],
                '►':[(a*.2,730),(a*.87,370),(a*.2,20)],'◄':[(a*.8,730),(a*.13,370),(a*.8,20)]}[c]
        return Polygon(points),a
    if c=='✓':return LineString([(a*.16,370),(a*.40,150),(a*.87,690)]).buffer(43,cap_style=2),a
    if c=='✗':return punctuation_shape('*',a,mod.STEM,mod.LINEAGE),a
    if c in '■□●○•':
        if c=='■':return rect(a*.16,95,a*.84,675),a
        if c=='□':return rect(a*.16,95,a*.84,675).difference(rect(a*.23,165,a*.77,606)),a
        if c in '●•':return disc(a*.5,385,270 if c=='●' else 82),a
        return disc(a*.5,385,270).difference(disc(a*.5,385,206)),a
    if c in '─│┌┐└┘├┤┬┴┼█▀▄▌▐░▒▓':
        w=mod.ADVANCE if mod.MONO else a
        return tile(c,w),w
    if c in '–—':return punctuation_shape('-',a,mod.STEM,mod.LINEAGE),a
    if c in '‘’‚':return punctuation_shape("'",a,mod.STEM,mod.LINEAGE),a
    if c in '“”„':return punctuation_shape('"',a,mod.STEM,mod.LINEAGE),a
    if c in '‹›':return punctuation_shape('<' if c=='‹' else '>',a,mod.STEM,mod.LINEAGE),a
    if c=='…':return union(disc(a*.17,75,26),disc(a*.5,75,26),disc(a*.83,75,26)),a
    if c in '†‡':return union(rect(a*.48,0,a*.54,740),rect(a*.16,470,a*.85,530),rect(a*.16,270,a*.85,320) if c=='‡' else GeometryCollection()),a
    if c=='™':
        g=union(scale(sh['T'][0],xfact=.48,yfact=.48,origin=(0,0)),translate(scale(sh['M'][0],xfact=.45,yfact=.48,origin=(0,0)),xoff=a*.48))
        return bounds_clip(translate(g,yoff=375),a),a
    if c=='‰':
        g=punctuation_shape('%',a,mod.STEM,mod.LINEAGE)
        return bounds_clip(union(g,disc(a*.84,75,39)),a),a
    if c in '˜ˆ':return mark('\u0303' if c=='˜' else '\u0302',a*.5,420),a
    if c=='ƒ':return bounds_clip(fit(sh['f'][0],a),a),a
    if c=='¤':return union(disc(a*.5,360,215).difference(disc(a*.5,360,130)),punctuation_shape('*',a,35,mod.LINEAGE)),a
    if c in '¨´¸¯':return mark({'¨':'\u0308','´':'\u0301','¸':'\u0327','¯':'\u0304'}[c],a*.5,370),a
    if c in '«»':return union(punctuation_shape('<' if c=='«' else '>',a,mod.STEM*.7,mod.LINEAGE),translate(punctuation_shape('<' if c=='«' else '>',a,mod.STEM*.6,mod.LINEAGE),xoff=75)),a
    if c=='¬':return union(rect(a*.12,365,a*.87,405),rect(a*.82,250,a*.87,405)),a
    if c=='¦':return union(rect(a*.47,500,a*.53,780),rect(a*.47,0,a*.53,260)),a
    if c=='±':return punctuation_shape('+',a,mod.STEM,mod.LINEAGE),a
    if c in 'ŠŽšžŸ':
        base={'Š':'S','Ž':'Z','š':'s','ž':'z','Ÿ':'Y'}[c]
        accent='\u030c' if c!='Ÿ' else '\u0308'
        return compose(base,accent,sh,mod.STEM)
    # Explicit low-priority auxiliary geometric symbols. Never copy existing fonts.
    if c=='¤':return disc(a/2,360,150),a
    return punctuation_shape('*',a,mod.STEM*.75,mod.LINEAGE),a

def tile(c,a):
    # Functional cells fill the exact advance and 1250-unit line cell.
    h=42;cx=a/2;cy=375
    H=rect(0,cy-h/2,a,cy+h/2);V=rect(cx-h/2,-250,cx+h/2,1000)
    if c=='─':return H
    if c=='│':return V
    segs={'┌':(0,1,0,1),'┐':(1,0,0,1),'└':(0,1,1,0),'┘':(1,0,1,0),
          '├':(0,1,1,1),'┤':(1,0,1,1),'┬':(1,1,0,1),'┴':(1,1,1,0),'┼':(1,1,1,1)}
    if c in segs:
        # tuple (left, right, up, down)
        left,right,up,down=segs[c];bits=[]
        if left:bits.append(rect(0,cy-h/2,cx,cy+h/2))
        if right:bits.append(rect(cx,cy-h/2,a,cy+h/2))
        if up:bits.append(rect(cx-h/2,cy,cx+h/2,1000))
        if down:bits.append(rect(cx-h/2,-250,cx+h/2,cy))
        return union(*bits)
    if c=='█':return rect(0,-250,a,1000)
    if c=='▀':return rect(0,375,a,1000)
    if c=='▄':return rect(0,-250,a,375)
    if c=='▌':return rect(0,-250,a/2,1000)
    if c=='▐':return rect(a/2,-250,a,1000)
    cells=[];step=32
    for y in range(-250,1000,step):
        for x in range(0,int(a),step):
            d=(x//step*7+y//step*11)%8
            if d<(2 if c=='░' else 4 if c=='▒' else 6):cells.append(rect(x,y,min(x+step,a),min(y+step,1000)))
    return union(*cells)

def extend(core,mod):
    sh=dict(core)
    for c in sorted(COVERAGE-set(sh)):
        sh[c]=shape_compose(c,sh,mod)
        g,a=sh[c]
        if not g.is_empty:
            sh[c]=(bounds_clip(g if c in '─│┌┐└┘├┤┬┴┼█▀▄▌▐░▒▓' else fit(g,a,20),a),a)
    assert len(sh)==len(COVERAGE)
    return sh
