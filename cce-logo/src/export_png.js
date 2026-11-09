const { chromium } = require('playwright'); const fs=require('fs'); const path=require('path');
(async()=>{
  const dir='/home/user/Grafiae/cce-logo/svg', out='/home/user/Grafiae/cce-logo/png'; fs.mkdirSync(out,{recursive:true});
  const b=await chromium.launch();
  for (const f of fs.readdirSync(dir).filter(x=>x.endsWith('.svg'))) {
    const svg=fs.readFileSync(path.join(dir,f),'utf8'); const m=svg.match(/viewBox="0 0 (\d+) (\d+)"/); const W=+m[1],H=+m[2];
    const k=2400/Math.max(W,H); const w=Math.round(W*k), h=Math.round(H*k);
    const wrap=path.join(__dirname,'_wrap.html');
    fs.writeFileSync(wrap,`<html><body style="margin:0;background:transparent"><img src="file://${path.join(dir,f)}" style="width:${w}px;height:${h}px;display:block"></body></html>`);
    const pg=await b.newPage({viewport:{width:w,height:h}});
    await pg.goto('file://'+wrap); await pg.waitForTimeout(120);
    await pg.screenshot({path:path.join(out,f.replace('.svg','.png')),omitBackground:true});
    await pg.close();
  }
  await b.close();
})();
