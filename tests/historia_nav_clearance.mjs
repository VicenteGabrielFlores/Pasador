import { createRequire } from 'node:module';

const require = createRequire('/tmp/shot/package.json');
const puppeteer = require('puppeteer-core');
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';

const root = new URL('..', import.meta.url).pathname;
const types = { '.html': 'text/html', '.png': 'image/png', '.svg': 'image/svg+xml', '.jpg': 'image/jpeg', '.css': 'text/css', '.js': 'text/javascript', '.webp': 'image/webp', '.ico': 'image/x-icon' };

function startServer() {
  return new Promise((resolve) => {
    const server = createServer(async (req, res) => {
      const url = new URL(req.url, 'http://127.0.0.1');
      const rel = normalize(decodeURIComponent(url.pathname)).replace(/^(\.\.[/\\])+/, '');
      const path = join(root, rel === '/' ? '/index.html' : rel);
      try {
        const body = await readFile(path);
        res.writeHead(200, { 'content-type': types[extname(path)] || 'application/octet-stream' });
        res.end(body);
      } catch {
        res.writeHead(404);
        res.end('missing');
      }
    });
    server.listen(0, '127.0.0.1', () => resolve(server));
  });
}

function assert(cond, message) {
  if (!cond) throw new Error(message);
}

const views = [
  { name: 'phone 390', w: 390, h: 844, fixed: false },
  { name: 'phone 320', w: 320, h: 568, fixed: false },
  { name: 'landscape', w: 844, h: 390, fixed: false },
  { name: 'short landscape', w: 932, h: 430, fixed: false },
  { name: 'desktop', w: 1280, h: 800, fixed: true },
];

const server = await startServer();
const base = `http://127.0.0.1:${server.address().port}`;
const browser = await puppeteer.launch({
  executablePath: '/usr/bin/google-chrome-stable',
  headless: 'new',
  args: ['--no-sandbox', '--disable-dev-shm-usage'],
});

try {
  for (const view of views) {
    const page = await browser.newPage();
    await page.setViewport({ width: view.w, height: view.h });
    await page.goto(`${base}/historia.html`, { waitUntil: 'networkidle0' });
    await page.evaluate(() => document.fonts.ready);
    const top = await page.evaluate(() => {
      const nav = document.getElementById('navbar');
      const nb = nav.getBoundingClientRect();
      const title = nav.querySelector('.nav-title').getBoundingClientRect();
      const links = [...nav.querySelectorAll('.nav-links a')].map((a) => {
        const r = a.getBoundingClientRect();
        return { text: a.textContent.trim(), left: r.left, right: r.right, top: r.top, bottom: r.bottom };
      });
      const hitsTitle = links.filter((l) => l.left < title.right - 1 && l.right > title.left + 1 && l.top < title.bottom && l.bottom > title.top).map((l) => l.text);
      const root = document.getElementById('page-scroll');
      let textHits = 0;
      const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
      let node;
      while ((node = walker.nextNode())) {
        if (!node.textContent.trim()) continue;
        const range = document.createRange();
        range.selectNodeContents(node);
        for (const r of range.getClientRects()) {
          if (r.width < 1 || r.height < 1) continue;
          if (r.top < nb.bottom - 0.5 && r.bottom > nb.top + 0.5 && r.right > nb.left && r.left < nb.right) textHits += 1;
        }
      }
      return {
        navPos: getComputedStyle(nav).position,
        heroPad: getComputedStyle(document.getElementById('hero')).paddingTop,
        hitsTitle,
        novel: links.find((l) => l.text === 'The Novel'),
        navLeft: nb.left,
        navRight: nb.right,
        textHits,
      };
    });
    assert(top.navPos === (view.fixed ? 'fixed' : 'relative'), `${view.name}: nav is ${top.navPos}`);
    assert(top.textHits === 0, `${view.name}: ${top.textHits} text lines sit under the nav`);
    assert(top.hitsTitle.length === 0, `${view.name}: title overlaps ${top.hitsTitle.join(', ')}`);
    assert(top.novel.left >= top.navLeft - 1 && top.novel.right <= top.navRight + 1, `${view.name}: The Novel is clipped`);
    if (view.fixed) assert(top.heroPad === '128px', `${view.name}: hero padding changed to ${top.heroPad}`);

    await page.evaluate(() => {
      const scroller = document.getElementById('page-scroll');
      const inner = ['auto', 'scroll'].includes(getComputedStyle(scroller).overflowY);
      if (inner) scroller.scrollTop = 1600;
      else window.scrollTo(0, 1600);
    });
    if (!view.fixed) {
      const midHits = await page.evaluate(() => {
        const nb = document.getElementById('navbar').getBoundingClientRect();
        const root = document.getElementById('page-scroll');
        let textHits = 0;
        const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
        let node;
        while ((node = walker.nextNode())) {
          if (!node.textContent.trim()) continue;
          const range = document.createRange();
          range.selectNodeContents(node);
          for (const r of range.getClientRects()) {
            if (r.width < 1 || r.height < 1) continue;
            if (r.top < nb.bottom - 0.5 && r.bottom > nb.top + 0.5 && r.right > nb.left && r.left < nb.right) textHits += 1;
          }
        }
        return textHits;
      });
      assert(midHits === 0, `${view.name}: scrolled text sits under the nav (${midHits})`);
    }

    await page.goto(`${base}/historia.html#part-vi`, { waitUntil: 'networkidle0' });
    await page.evaluate(() => document.fonts.ready);
    let anchor = null;
    for (let i = 0; i < 20; i += 1) {
      anchor = await page.evaluate(() => {
        const nav = document.getElementById('navbar').getBoundingClientRect();
        const eye = document.querySelector('#part-vi .part-eyebrow').getBoundingClientRect();
        return { eyeTop: eye.top, eyeBottom: eye.bottom, navBottom: nav.bottom, viewH: window.innerHeight };
      });
      if (anchor.eyeTop >= anchor.navBottom - 1 && anchor.eyeBottom < anchor.viewH) break;
      await new Promise((r) => setTimeout(r, 150));
    }
    assert(anchor.eyeTop >= anchor.navBottom - 1, `${view.name}: part eyebrow starts at ${anchor.eyeTop}, under nav ${anchor.navBottom}`);
    assert(anchor.eyeBottom < anchor.viewH, `${view.name}: part eyebrow is below the viewport`);

    const poems = await page.evaluate(async () => {
      const ul = document.querySelector('.nav-links');
      ul.scrollLeft = ul.scrollWidth;
      await new Promise((r) => requestAnimationFrame(r));
      const link = [...ul.querySelectorAll('a')].find((a) => a.textContent.includes('Poems'));
      const r = link.getBoundingClientRect();
      const nav = document.getElementById('navbar').getBoundingClientRect();
      return r.left >= nav.left - 1 && r.right <= nav.right + 1;
    });
    assert(poems, `${view.name}: Poems cannot be scrolled into the nav`);
    await page.close();
    console.log('ok', view.name);
  }
} finally {
  await browser.close();
  server.close();
}
