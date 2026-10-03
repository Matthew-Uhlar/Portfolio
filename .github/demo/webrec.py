import asyncio, os, tempfile, subprocess, json
from playwright.async_api import async_playwright
OVERLAY = r"""
(() => {
  const css = '#__cap{position:fixed;left:0;right:0;bottom:0;z-index:2147483647;background:rgba(31,111,235,.96);color:#fff;font:600 20px/1.35 \'DejaVu Sans\',Arial,sans-serif;padding:13px 22px;pointer-events:none;box-shadow:0 -2px 12px rgba(0,0,0,.25)}  #__cur{position:fixed;z-index:2147483647;width:22px;height:22px;border-radius:50%;background:rgba(255,196,0,.55);border:2px solid #ffb300;pointer-events:none;transform:translate(-50%,-50%);transition:left .35s ease,top .35s ease;left:-50px;top:-50px}  #__cur.click{background:rgba(255,120,0,.85);width:30px;height:30px}';
  function ensure(){ if(!document.body) return;
    if(!document.getElementById('__cap')){const s=document.createElement('style');s.textContent=css;document.head.appendChild(s);
      const c=document.createElement('div');c.id='__cap';document.body.appendChild(c);
      const k=document.createElement('div');k.id='__cur';document.body.appendChild(k);}
    const t=sessionStorage.getItem('__cap')||'';const c=document.getElementById('__cap');if(c.textContent!==t)c.textContent=t;c.style.display=t?'block':'none';
    const p=JSON.parse(sessionStorage.getItem('__cur')||'null');const k=document.getElementById('__cur');if(p&&k&&!k.dataset.init){k.style.transition='none';k.style.left=p[0]+'px';k.style.top=p[1]+'px';k.dataset.init=1;setTimeout(()=>k.style.transition='',50)}}
  window.__setCap=t=>{sessionStorage.setItem('__cap',t);ensure()};
  window.__move=(x,y,click)=>{ensure();const k=document.getElementById('__cur');k.style.left=x+'px';k.style.top=y+'px';sessionStorage.setItem('__cur',JSON.stringify([x,y]));if(click){k.classList.add('click');setTimeout(()=>k.classList.remove('click'),300)}};
  setInterval(ensure,200); document.addEventListener('DOMContentLoaded',ensure);
})();
"""
class Rec:
    def __init__(self, page): self.p = page
    async def cap(self, text, wait=0):
        await self.p.evaluate("t=>window.__setCap&&window.__setCap(t)", text)
        if wait: await self.p.wait_for_timeout(wait)
    async def point(self, loc, click=True):
        await loc.scroll_into_view_if_needed(timeout=5000)
        b = await loc.bounding_box()
        if b:
            x, y = b['x']+b['width']/2, b['y']+b['height']/2
            await self.p.evaluate("([x,y])=>window.__move&&window.__move(x,y,false)", [x, y])
            await self.p.wait_for_timeout(450)
            if click: await self.p.evaluate("([x,y])=>window.__move&&window.__move(x,y,true)", [x, y])
    async def click(self, loc, wait=900):
        await self.point(loc); await loc.click(); await self.p.wait_for_timeout(wait)
    async def type(self, loc, text, delay=45):
        await self.point(loc); await loc.click(); await loc.fill('')
        await loc.press_sequentially(text, delay=delay)
    async def scroll(self, dy=400, steps=4, pause=250):
        for _ in range(steps):
            await self.p.mouse.wheel(0, dy/steps); await self.p.wait_for_timeout(pause)

async def record(base, scenario, w=1280, h=720):
    d = tempfile.mkdtemp()
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        ctx = await b.new_context(viewport={'width':w,'height':h}, record_video_dir=d, record_video_size={'width':w,'height':h}, bypass_csp=True)
        await ctx.add_init_script(OVERLAY)
        page = await ctx.new_page(); page.set_default_timeout(15000)
        try:
            await scenario(page, Rec(page))
        finally:
            v = await page.video.path(); await ctx.close(); await b.close()
    encode(v, base)

def encode(v, base, trim_start=0.0):
    pre = ['-ss', str(trim_start)] if trim_start else []
    subprocess.run(['ffmpeg','-y','-loglevel','error',*pre,'-i',v,'-c:v','libx264','-pix_fmt','yuv420p','-crf','26','-preset','slow','-movflags','+faststart',base+'.mp4'],check=True)
    subprocess.run(['ffmpeg','-y','-loglevel','error',*pre,'-i',v,'-vf','fps=8,scale=880:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer:bayer_scale=4','-loop','0',base+'.gif'],check=True)
    for ext in ('mp4','gif'): print(base+'.'+ext, os.path.getsize(base+'.'+ext)//1024, 'KB')

async def step(page, name, coro):
    """Run one demo step; on failure log it and keep recording so one flaky selector doesn't kill the video."""
    try:
        await coro
        print(f"[ok] {name}", flush=True)
    except Exception as e:  # noqa: BLE001
        print(f"[FAILED] {name}: {e}".splitlines()[0], flush=True)
        try:
            await page.screenshot(path=f"/tmp/demo-fail-{name.replace(' ','_')}.png")
        except Exception:
            pass

async def wait_for_http(url, timeout=240):
    import urllib.request, time
    end = time.time() + timeout
    while time.time() < end:
        try:
            urllib.request.urlopen(url, timeout=3); return True
        except Exception:
            await asyncio.sleep(2)
    raise RuntimeError(f"{url} did not come up")
