const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const pg=await b.newPage();await pg.goto('file://'+process.argv[2]);await pg.waitForTimeout(1200);
await pg.pdf({path:process.argv[3],width:'297mm',height:'210mm',printBackground:true,preferCSSPageSize:true});await b.close();})();
