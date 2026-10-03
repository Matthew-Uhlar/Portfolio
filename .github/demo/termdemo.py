"""Record an animated terminal session (real captured output) to MP4 + GIF.
usage: python termdemo.py spec.json out_basename
spec: {"title": str, "caption": str, "cwd": str, "steps":[{"note":str?, "cmd":str, "out":str}]}
"""
import json, sys, html, subprocess, os, tempfile, asyncio
from playwright.async_api import async_playwright

spec = json.load(open(sys.argv[1])); base = sys.argv[2]
page_html = """<!doctype html><html><head><meta charset=utf-8><style>
body{margin:0;background:#0d1117;font-family:'DejaVu Sans Mono',monospace;color:#c9d1d9}
.bar{height:44px;background:#161b22;display:flex;align-items:center;padding:0 16px;gap:8px;border-bottom:1px solid #30363d}
.dot{width:12px;height:12px;border-radius:50%}.t{margin-left:14px;font-family:'DejaVu Sans',sans-serif;font-size:15px;color:#8b949e}
#term{padding:18px 22px;font-size:17px;line-height:1.45;white-space:pre-wrap;height:560px;overflow:hidden}
.p{color:#3fb950}.c{color:#e6edf3}.o{color:#c9d1d9}.n{color:#d2a8ff;font-style:italic}
.cap{position:fixed;left:0;right:0;bottom:0;background:#1f6feb;color:#fff;font-family:'DejaVu Sans',sans-serif;font-size:20px;padding:14px 22px;min-height:40px}
.hl{color:#f0883e}.gr{color:#3fb950}.rd{color:#f85149}
</style></head><body><div class=bar><span class=dot style="background:#f85149"></span><span class=dot style="background:#d29922"></span><span class=dot style="background:#3fb950"></span><span class=t>TITLE</span></div><div id=term></div><div class=cap id=cap>CAPTION</div>
<script>
const steps=STEPS;const term=document.getElementById('term');const cap=document.getElementById('cap');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;')}
function color(s){return esc(s).replace(/^(\\s*)(ADDED.*|Added:.*)$/gm,'$1<span class=gr>$2</span>').replace(/^(\\s*)(MODIFIED.*|Modified:.*)$/gm,'$1<span class=hl>$2</span>').replace(/^(\\s*)(DELETED.*|Deleted:.*|FAIL.*|error.*)$/gm,'$1<span class=rd>$2</span>').replace(/(ok|passed|PASS)/g,'<span class=gr>$1</span>')}
(async()=>{await sleep(1200);
for(const s of steps){ if(s.note){cap.textContent=s.note;}
 if(s.cmd!==null){const line=document.createElement('div');line.innerHTML='<span class=p>matt@dev</span>:<span style="color:#58a6ff">'+(s.cwd||'~/project')+'</span>$ <span class=c></span>';term.appendChild(line);
 const c=line.querySelector('.c');for(const ch of s.cmd){c.textContent+=ch;await sleep(38);}
 await sleep(500);}const o=document.createElement('div');o.className='o';term.appendChild(o);
 const lines=s.out.replace(/\\s+$/,'').split('\\n');for(const l of lines){o.innerHTML+=color(l)+'\\n';term.scrollTop=term.scrollHeight;await sleep(s.fast?25:70);}
 term.scrollTop=term.scrollHeight;await sleep(s.pause||2600);
 if(s.clear){term.innerHTML='';}
}
cap.textContent=FINAL;await sleep(3000);window.DONE=true;})();
</script></body></html>"""
page_html = (page_html.replace('TITLE', html.escape(spec['title'])).replace('CAPTION', html.escape(spec['caption']))
  .replace('STEPS', json.dumps(spec['steps'])).replace('FINAL', json.dumps(spec.get('final', spec['caption']))))

async def main():
    d = tempfile.mkdtemp(); hp = os.path.join(d, 'p.html'); open(hp, 'w').write(page_html)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width':1280,'height':720}, record_video_dir=d, record_video_size={'width':1280,'height':720})
        pg = await ctx.new_page(); await pg.goto('file://'+hp)
        await pg.wait_for_function('window.DONE===true', timeout=600000)
        v = await pg.video.path(); await ctx.close(); await b.close()
    encode(v, base)

def encode(v, base):
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',v,'-c:v','libx264','-pix_fmt','yuv420p','-crf','26','-preset','slow','-movflags','+faststart',base+'.mp4'],check=True)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',v,'-vf','fps=8,scale=880:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=bayer:bayer_scale=4','-loop','0',base+'.gif'],check=True)
    for ext in ('mp4','gif'): print(base+'.'+ext, os.path.getsize(base+'.'+ext)//1024, 'KB')

if __name__ == '__main__': asyncio.run(main())
