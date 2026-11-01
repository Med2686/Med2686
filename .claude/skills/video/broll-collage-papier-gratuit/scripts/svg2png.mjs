// Rastérise des SVG (fond transparent) en PNG via Chromium (Playwright déjà installé).
// Usage : node svg2png.mjs <dossier_svg> <dossier_png> [largeur_px=1200]
import { readdirSync, readFileSync, mkdirSync } from "node:fs";
import { createRequire } from "node:module";
import { join, basename } from "node:path";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const [, , inDir, outDir, w = "1200"] = process.argv;
if (!inDir || !outDir) { console.error("Usage: node svg2png.mjs <svg_dir> <png_dir> [width]"); process.exit(1); }
mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ deviceScaleFactor: 1 });
for (const f of readdirSync(inDir).filter((f) => f.endsWith(".svg"))) {
  const svg = readFileSync(join(inDir, f), "utf8");
  await page.setViewportSize({ width: +w, height: +w });
  await page.setContent(`<html><body style="margin:0;background:transparent">
    <div id="s" style="display:inline-block;width:${w}px">${svg}</div></body></html>`);
  await page.evaluate((w) => { const e = document.querySelector("#s svg"); e.setAttribute("width", w); e.removeAttribute("height"); }, +w);
  const el = await page.$("#s svg");
  await el.screenshot({ path: join(outDir, basename(f, ".svg") + ".png"), omitBackground: true });
  console.log("ok", f);
}
await browser.close();
