"""Explicit, fail-closed repertoire and original symbol/accent construction.
Copyright (c) 2026 techrote. SIL Open Font License 1.1.
All components come from the current family's own master or these primitives.
"""
from __future__ import annotations
import unicodedata
from geometry import (box, disc, stroke, path, polygon, chamfer, merge, scale,
                      translate, Polygon, clean)

ASCII = {chr(i) for i in range(32,127)}
LATIN1 = {chr(i) for i in range(160,256)}
CP1252 = set(bytes(range(128,256)).decode('cp1252',errors='ignore'))
EXTRA = set('←↑→↓↔−≠≤≥│─┌┐└┘├┤┬┴┼█▀▄▌▐░▒▓■□▲▶▼◀✓✕')
COVERAGE = ASCII | LATIN1 | CP1252 | EXTRA
BLANKS = {' ', '\u00a0'}
BOX_ARMS = {
    '─':'lr', '│':'ud', '┌':'rd', '┐':'ld', '└':'ru', '┘':'lu',
    '├':'urd', '┤':'uld', '┬':'lrd', '┴':'lru', '┼':'lrud'
}


def extend(core, stem=72, default_advance=640):
    result = dict(core)
    w = min(stem,110)
    center = default_advance/2
    def s(points, width=w):
        return stroke(points,width,join='bevel')
    def own(c):
        return core[c][0]
    def shrink(c, x=.55,y=.55,dx=0,dy=0):
        return translate(scale(own(c),xfact=x,yfact=y,origin=(0,0)),xoff=dx,yoff=dy)
    def put(c,g,advance=None):
        a = default_advance if advance is None else advance
        result[c] = (g,a)
    def fit(g,a=default_advance,margin=55):
        if g.is_empty:
            return g
        x0,y0,x1,y1 = g.bounds
        factor = min(1,(a-2*margin)/(x1-x0))
        g = scale(g,xfact=factor,yfact=1,origin=(0,0))
        x0,_,x1,_ = g.bounds
        return translate(g,xoff=(a-(x1-x0))/2-x0)
    def paired(left,right):
        return fit(merge(shrink(left,.52,1),shrink(right,.52,1,default_advance*.43)))

    put('\u00a0',Polygon(),core[' '][1])
    # Soft hyphen has a real hyphen outline when a layout engine exposes it.
    put('\u00ad',own('-'),core['-'][1])
    for c,base in [('Æ','A'),('æ','a'),('Œ','O'),('œ','o')]:
        put(c,paired(base,'E' if c.isupper() else 'e'))
    for c,b in [('Ø','O'),('ø','o')]:
        g = own(b); x0,y0,x1,y1 = g.bounds
        put(c,merge(g,s([(x0+50,y0+20),(x1-50,y1-20)],w*.72)),core[b][1])
    put('Ð',merge(own('D'),s([(60,340),(360,340)])),core['D'][1])
    put('ð',merge(shrink('o',1,.9),s([(center+130,390),(center-80,710)]),s([(center-160,560),(center+115,667)])))
    for c,b in [('Þ','P'),('þ','p')]:
        g = shrink(b,1,.72,0,120 if c=='Þ' else 35)
        put(c,merge(g,s([(125,-190 if c=='þ' else 0),(125,700)])))
    put('ß',merge(path('M 133 0 L 133 507 C 133 731 462 739 463 542 C 463 429 341 429 341 330 C 341 252 522 281 522 145 C 522 30 416 -1 321 49',w),Polygon()))
    put('ƒ',merge(shrink('f',.86,1,25,-60),s([(220,110),(183,-147)])))
    put('µ',merge(shrink('u',1,.95),s([(125,-210),(125,360)])))
    put('ı',shrink('l',1,.72))

    marks = {
        '\u0300': s([(center-91,113),(center+55,15)],w*.70),
        '\u0301': s([(center-55,15),(center+91,113)],w*.70),
        '\u0302': s([(center-135,10),(center,110),(center+135,10)],w*.70),
        '\u0303': path(f'M {center-145} 30 C {center-60} 160 {center+52} -64 {center+145} 66',w*.64),
        '\u0308': merge(box(center-138,22,center-58,102),box(center+58,22,center+138,102)),
        '\u030a': disc(center,75,78).difference(disc(center,75,34)),
        '\u030c': s([(center-135,110),(center,10),(center+135,110)],w*.70),
    }
    for c in sorted(COVERAGE):
        if c in result:
            continue
        decomp = unicodedata.normalize('NFD',c)
        if len(decomp)==2 and decomp[0] in core and decomp[0].isalpha():
            base,accent = decomp
            g,a = core[base]
            # Accented lowercase i replaces its dot, never stacks over it.
            if base == 'i' and g.bounds[3] > 600:
                g = g.intersection(box(-1000,-1000,2000,600))
            x0,y0,x1,y1 = g.bounds
            if accent=='\u0327':
                mark = path('M 335 0 L 299 -71 C 433 -69 411 -195 261 -167',w*.67)
                mark = translate(mark,xoff=(x0+x1)/2-320,yoff=y0)
            elif accent in marks:
                mark=marks[accent]
                mark=translate(mark,xoff=(x0+x1)/2-center,yoff=y1+47-mark.bounds[1])
            else:
                raise ValueError(f'Unsupported diacritic {ord(accent):04X}')
            put(c,merge(g,mark),a)

    put('¡',translate(scale(own('!'),xfact=1,yfact=-1,origin=(0,0)),yoff=520))
    put('¿',translate(scale(own('?'),xfact=-1,yfact=-1,origin=(center,260)),yoff=0))
    put('¢',merge(shrink('c',1,1,0,100),s([(center,-15),(center,695)],w*.68)))
    pound=path('M 130 36 L 515 36 M 196 36 L 244 483 C 264 681 450 714 520 580 M 111 338 L 429 338',w)
    put('£',pound)
    put('¤',merge(disc(center,340,162).difference(disc(center,340,162-w)),s([(137,522),(center-125,465)]),s([(center+125,465),(center+183,522)]),s([(137,158),(center-125,215)]),s([(center+125,215),(center+183,158)])))
    put('¥',merge(own('Y'),s([(133,270),(default_advance-133,270)]),s([(133,145),(default_advance-133,145)])))
    put('€',merge(own('C'),s([(64,271),(424,271)],w*.8),s([(64,425),(424,425)],w*.8)))
    put('¦',merge(box(center-w/2,405,center+w/2,740),box(center-w/2,-90,center+w/2,250)))
    sec=path('M 491 591 C 400 743 172 681 172 535 C 172 365 484 424 484 235 C 484 47 168 33 168 227 C 168 404 489 336 489 144 C 489 -67 235 -100 150 48',w*.85)
    put('§',sec)
    put('¨',translate(marks['\u0308'],yoff=580))
    put('´',translate(marks['\u0301'],yoff=575))
    put('¸',path('M 352 13 L 290 -63 C 451 -60 414 -203 253 -171',w*.7))
    put('¯',box(136,640,default_advance-136,640+w*.7))
    put('°',disc(center,550,123).difference(disc(center,550,123-w*.75)))
    for c,base in [('©','C'),('®','R')]:
        ring=disc(center,351,293).difference(disc(center,351,257))
        put(c,merge(ring,shrink(base,.55,.57,center*.45,150)))
    for c,b in [('ª','a'),('º','o')]:
        put(c,merge(shrink(b,.59,.65,center*.4,345),box(165,269,default_advance-165,269+w*.55)))
    for c,b in [('¹','1'),('²','2'),('³','3')]:
        put(c,shrink(b,.59,.57,center*.4,327))
    for c,top,bot in [('¼','1','4'),('½','1','2'),('¾','3','4')]:
        put(c,merge(shrink(top,.43,.48,0,372),shrink(bot,.43,.48,default_advance*.54,0),s([(155,0),(default_advance-140,700)],w*.65)))
    put('±',merge(translate(own('+'),yoff=122),s([(112,18),(default_advance-112,18)])))
    put('¬',merge(s([(95,383),(default_advance-95,383)]),s([(default_advance-95,383),(default_advance-95,162)])))
    pilcrow=merge(disc(264,482,191).intersection(box(0,200,390,720)),box(264,291,390,673),box(354,-54,354+w,700),box(490,-54,490+w,700))
    put('¶',pilcrow)
    put('·',disc(center,290,w*.62))
    put('•',disc(center,328,w*1.16))
    put('×',merge(s([(140,118),(default_advance-140,522)]),s([(140,522),(default_advance-140,118)])))
    put('÷',merge(s([(130,320),(default_advance-130,320)]),disc(center,115,w*.65),disc(center,525,w*.65)))
    put('−',s([(112,300),(default_advance-112,300)]))
    put('≠',merge(own('='),s([(201,24),(default_advance-201,613)],w*.72)))
    for c,b in [('≤','<'),('≥','>')]:
        put(c,merge(translate(scale(own(b),xfact=1,yfact=.76,origin=(0,0)),yoff=133),s([(128,25),(default_advance-128,25)])))
    for c,b in [('‘',"'"),('’',"'"),('‚',','),('“','"'),('”','"'),('„','"')]:
        # Explicit wedge-shaped quote direction, independent of apostrophe style.
        g=polygon([(center-28,700),(center+65,700),(center+15,565),(center-80,530)])
        if c in '‘“': g=translate(scale(g,xfact=-1,yfact=-1,origin=(center,615)),yoff=0)
        if c in '“”„': g=merge(translate(g,xoff=-99),translate(g,xoff=99))
        if c in '‚„': g=translate(g,yoff=-579)
        put(c,g)
    for c,left,double in [('‹',True,False),('›',False,False),('«',True,True),('»',False,True)]:
        pts=[(130,93),(275,275),(130,457)]
        g=s(pts,w*.8)
        if double:g=merge(g,translate(g,xoff=212))
        if left:g=scale(g,xfact=-1,yfact=1,origin=(center,0))
        put(c,fit(g))
    put('–',box(86,270,default_advance-86,270+w))
    put('—',box(20,270,default_advance-20,270+w))
    put('…',merge(*(box(x-w*.40,0,x+w*.40,w*.82) for x in [130,center,default_advance-130])))
    put('†',merge(s([(center,-80),(center,736)],w*.8),s([(128,483),(default_advance-128,483)],w*.8)))
    put('‡',merge(result['†'][0],s([(128,182),(default_advance-128,182)],w*.8)))
    put('ˆ',translate(marks['\u0302'],yoff=580))
    put('˜',translate(marks['\u0303'],yoff=580))
    put('™',merge(shrink('T',.48,.45,0,360),shrink('M',.48,.45,default_advance*.48,360)))
    put('‰',merge(shrink('%',.71,.92,0,20),disc(default_advance-96,112,78).difference(disc(default_advance-96,112,37))))

    # Functional cell geometry is intentionally NOT glitched or stencil-cut.
    # Line boxes span the declared 1000/-250 metrics (1250-unit line height).
    mid=350; half=36
    for c,arms in BOX_ARMS.items():
        ink=[]
        if 'l' in arms: ink.append(box(0,mid-half,center+half,mid+half))
        if 'r' in arms: ink.append(box(center-half,mid-half,default_advance,mid+half))
        if 'u' in arms: ink.append(box(center-half,mid-half,center+half,1000))
        if 'd' in arms: ink.append(box(center-half,-250,center+half,mid+half))
        put(c,merge(*ink))
    for c,b in {'█':(0,-250,default_advance,1000),'▀':(0,375,default_advance,1000),'▄':(0,-250,default_advance,375),
                '▌':(0,-250,center,1000),'▐':(center,-250,default_advance,1000)}.items():
        put(c,box(*b))
    for c,n in [('░',1),('▒',2),('▓',3)]:
        ink=[]
        for row in range(20):
            for col in range(10):
                if (row+col*3)%4<n:
                    ink.append(box(col*default_advance/10,-250+row*62.5,(col+1)*default_advance/10,-250+(row+1)*62.5))
        put(c,merge(*ink))
    for c in '←→↔':
        p=[s([(80,350),(default_advance-80,350)],w*.8)]
        if c in '←↔':p.append(s([(245,545),(80,350),(245,155)],w*.8))
        if c in '→↔':p.append(s([(default_advance-245,545),(default_advance-80,350),(default_advance-245,155)],w*.8))
        put(c,merge(*p))
    for c,flip in [('↑',False),('↓',True)]:
        g=merge(s([(center,84),(center,616)],w*.8),s([(center-190,430),(center,616),(center+190,430)],w*.8))
        if flip:g=scale(g,xfact=1,yfact=-1,origin=(center,350))
        put(c,g)
    put('✓',s([(119,301),(265,125),(533,610)],w*.95))
    put('✕',merge(s([(155,100),(default_advance-155,600)]),s([(155,600),(default_advance-155,100)])))
    put('■',box(111,102,default_advance-111,598))
    put('□',box(111,102,default_advance-111,598).difference(box(111+w,102+w,default_advance-111-w,598-w)))
    for c,pts in {'▲':[(center,640),(80,60),(default_advance-80,60)],'▼':[(center,60),(80,640),(default_advance-80,640)],
                  '▶':[(default_advance-60,350),(100,80),(100,620)],'◀':[(60,350),(default_advance-100,80),(default_advance-100,620)]}.items():
        put(c,polygon(pts))
    # Do not encode unsupported extras just because a recipe is available.
    result={c:result[c] for c in sorted(COVERAGE)}
    assert set(result)==COVERAGE
    for c,(g,a) in list(result.items()):
        if c not in core and c not in BOX_ARMS and c not in '█▀▄▌▐░▒▓' and c not in BLANKS:
            result[c]=(fit(g,a),a)
    return {c:(clean(g),a) for c,(g,a) in result.items()}
