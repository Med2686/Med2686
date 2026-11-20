#!/usr/bin/env python3
"""Génère artifact/index.html : version « page publiable » de index.html (contenu sans doctype/head,
thèmes clair/sombre/explicite, marges de sécurité téléphone). Les scripts restent des fichiers à côté.
Usage : python3 build_artifact.py"""
import pathlib, re
here = pathlib.Path(__file__).resolve().parent
src = (here / "index.html").read_text(encoding="utf-8")
css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
body = re.search(r"<body>(.*?)</body>", src, re.S).group(1)

# 1) thèmes : le bloc sombre devient « système sombre sauf choix clair explicite » + « choix sombre explicite »
m = re.search(r"@media \(prefers-color-scheme: dark\) \{\s*:root \{(.*?)\n  \}\n\}", css, re.S)
assert m, "bloc sombre introuvable"
inner = m.group(1)
css = css.replace(m.group(0),
    "@media (prefers-color-scheme: dark) {\n  :root:not([data-theme=\"light\"]) {" + inner + "\n  }\n}\n:root[data-theme=\"dark\"] {" + inner + "\n}")

# 2) en-tête collant : marges latérales des deux côtés, bande de sécurité en haut
old = ".top { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 14px; padding: 10px max(16px, env(safe-area-inset-left, 0px)); background: var(--panel); border-bottom: 1px solid var(--line); position: sticky; top: 0; z-index: 5; }"
assert old in css, "règle .top introuvable"
css = css.replace(old,
    ".top { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 14px; padding-block: 10px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); background: var(--panel); border-bottom: 1px solid var(--line); position: sticky; top: env(safe-area-inset-top, 0px); z-index: 11; }\n"
    "body::before { content: \"\"; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: var(--panel); }")
css = css.replace(".data { position: sticky; top: 64px;", ".data { position: sticky; top: calc(64px + env(safe-area-inset-top, 0px));")

out = ("<title>SQL Quest</title>\n<meta name=\"claude:viewport-fit-sides\" content=\"cover\">\n<style>" + css + "</style>\n" + body.strip() + "\n")
(here / "artifact").mkdir(exist_ok=True)
(here / "artifact" / "index.html").write_text(out, encoding="utf-8")
print("artifact/index.html généré,", len(out) // 1024, "Ko")
