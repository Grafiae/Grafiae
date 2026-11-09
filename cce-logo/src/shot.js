const { chromium } = require('playwright');
(async () => {
  const [out, w, h, src, sc] = process.argv.slice(2);
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: +(sc || 1) });
  await pg.goto('file://' + src);
  await pg.waitForTimeout(500);
  await pg.screenshot({ path: out, fullPage: true });
  await b.close();
})();
