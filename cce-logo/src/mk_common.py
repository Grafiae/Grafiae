import random, math
SV="file:///home/user/Grafiae/cce-logo/svg/"
FONTS="file:///tmp/claude-0/-home-user-Grafiae/505c24ee-2e35-5947-935f-cfc53e082e9e/scratchpad/build/fonts2/"
FONTCSS=f"""
@font-face{{font-family:'Cormorant';src:url('{FONTS}Cormorant.ttf');font-weight:300 700}}
@font-face{{font-family:'Cormorant';src:url('{FONTS}CormorantItalic.ttf');font-weight:300 700;font-style:italic}}
@font-face{{font-family:'Jost';src:url('{FONTS}Jost.ttf');font-weight:100 900}}
@font-face{{font-family:'Pinyon';src:url('{FONTS}Pinyon.ttf')}}
"""
def bokeh(W,H,n=26,seed=3,col="#E3C77A",amin=.05,amax=.22,rmin=6,rmax=46):
    r=random.Random(seed); o=[]
    for i in range(n):
        x=r.uniform(0,W); y=r.uniform(0,H); rad=r.uniform(rmin,rmax)
        a=r.uniform(amin,amax)
        if r.random()<.5: o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rad:.0f}" fill="{col}" opacity="{a:.2f}"/>')
        else: o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rad:.0f}" fill="none" stroke="{col}" stroke-width="1.4" opacity="{a*3:.2f}"/>')
    return "".join(o)
def arches(x,base,scale=1,col="#C9A24B",op=.5,sw=1.3):
    out=[]
    for (dx,w,h) in [(0,190,330),(214,252,430),(490,190,330)]:
        w*=scale;h*=scale;X=x+dx*scale;r=w/2
        out.append(f'<path d="M{X} {base}V{base-h+r}A{r} {r} 0 0 1 {X+w} {base-h+r}V{base}" fill="none" stroke="{col}" stroke-width="{sw}" opacity="{op}"/>')
    return "".join(out)
