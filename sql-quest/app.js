(function () {
  "use strict";
  var $ = function (s) { return document.querySelector(s); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var KEY = "sqlquest-v1";
  var state = { answers: {}, submitted: {}, status: {}, hints: {}, xp: {} };
  var RM = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var FREE = { id: "free", type: "libre", titre: "Bac à sable libre", niveau: "libre", tables: [] };
  var TABLES = ["anomalies", "cas_test", "exigences", "campagnes", "clients", "comptes", "transactions", "batchs"];
  var FK = { cas_test_id: "cas_test", exigence_id: "exigences", campagne_id: "campagnes", client_id: "clients", compte_id: "comptes", batch_id: "batchs" };
  var ROW_LIMIT = 200;
  var db, current, currentTable;

  /* ---------- stockage (jamais bloquant) ---------- */
  function load() { try { var s = JSON.parse(localStorage.getItem(KEY) || "null"); if (s) { Object.keys(state).forEach(function (k) { state[k] = s[k] || {}; }); } } catch (e) {} }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} }

  /* ---------- texte léger ---------- */
  function inline(t) { return esc(t).replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>"); }
  function md(src) {
    var parts = String(src).split(/```sql\n([\s\S]*?)```/g), out = "";
    parts.forEach(function (p, i) {
      if (i % 2) { out += "<pre><code>" + esc(p.replace(/\n$/, "")) + "</code></pre>"; return; }
      p.split(/\n\s*\n/).forEach(function (b) {
        b = b.trim(); if (!b) return;
        var lines = b.split("\n");
        if (lines.every(function (l) { return /^- /.test(l); })) {
          out += "<ul>" + lines.map(function (l) { return "<li>" + inline(l.slice(2)) + "</li>"; }).join("") + "</ul>";
        } else { out += "<p>" + inline(b).replace(/\n/g, "<br>") + "</p>"; }
      });
    });
    return out;
  }
  function toast(msg) { var t = $("#toast"); t.textContent = msg; t.classList.add("show"); clearTimeout(toast.h); toast.h = setTimeout(function () { t.classList.remove("show"); }, 2200); }

  /* ---------- SQL ---------- */
  function b64bytes(b64) { var bin = atob(b64), n = bin.length, u = new Uint8Array(n); for (var i = 0; i < n; i++) u[i] = bin.charCodeAt(i); return u; }
  function runQuery(sql) {
    var clean = sql.replace(/--[^\n]*/g, "").replace(/\/\*[\s\S]*?\*\//g, "").trim();
    if (!clean) throw new Error("Écris une requête avant de l'exécuter.");
    if (!/^(select|with|pragma|explain)\b/i.test(clean)) {
      var first = (clean.split(/\s+/)[0] || "").toUpperCase();
      if (/^(insert|update|delete|drop|create|alter|replace|truncate|attach|vacuum)$/i.test(first)) throw new Error("Lecture seule : " + first + " est interdit ici. Seules les requêtes SELECT (ou WITH) sont autorisées.");
      throw new Error("Requête non reconnue : elle doit commencer par SELECT (ou WITH). Vérifie l'orthographe du premier mot : « " + first + " ».");
    }
    var stmt = db.prepare(sql);
    try {
      var columns = stmt.getColumnNames(), values = [];
      while (stmt.step()) values.push(stmt.get());
      return { columns: columns, values: values };
    } finally { stmt.free(); }
  }
  function norm(v) { if (v === null) return "NULL"; if (typeof v === "number") return String(Math.round(v * 100) / 100); return String(v); }
  function rowKey(r) { return JSON.stringify(r.map(norm)); }
  function compare(u, ref, ordered) {
    if (u.columns.length !== ref.columns.length) return { ok: false, msg: "Nombre de colonnes : attendu " + ref.columns.length + ", obtenu " + u.columns.length + "." };
    if (u.values.length !== ref.values.length) return { ok: false, msg: "Nombre de lignes : attendu " + ref.values.length + ", obtenu " + u.values.length + "." };
    var a = u.values.map(rowKey), b = ref.values.map(rowKey);
    if (a.join("\n") === b.join("\n")) return { ok: true };
    a.sort(); b.sort();
    var sameSet = a.join("\n") === b.join("\n");
    if (sameSet && !ordered) return { ok: true };
    if (sameSet && ordered) return { ok: false, msg: "Les lignes sont les bonnes, mais l'ordre demandé n'est pas respecté (vérifie ORDER BY et les égalités)." };
    return { ok: false, msg: "Même nombre de lignes et de colonnes, mais des valeurs diffèrent (filtre, arrondi, colonne choisie ?)." };
  }
  function gridHTML(cols, rows, opt) {
    opt = opt || {};
    var h = "<table class='grid'><thead><tr>" + cols.map(function (c) { return "<th>" + esc(c) + "</th>"; }).join("") + "</tr></thead><tbody>";
    rows.forEach(function (r) {
      h += "<tr" + (opt.rowIds ? " data-id='" + esc(r[0]) + "'" : "") + ">";
      r.forEach(function (v, i) {
        var c = cols[i];
        if (v === null) h += "<td class='null'>NULL</td>";
        else if (opt.fk && FK[c]) h += "<td class='fk' data-t='" + FK[c] + "' data-v='" + esc(v) + "' title='Aller à " + FK[c] + " n°" + esc(v) + "'>" + esc(v) + " ↗</td>";
        else h += "<td>" + esc(v) + "</td>";
      });
      h += "</tr>";
    });
    return h + "</tbody></table>";
  }

  /* ---------- panneau de données ---------- */
  function renderTabs() {
    var rel = (current && current.tables) || [];
    $("#tabs").innerHTML = TABLES.map(function (t) {
      return "<button class='tab" + (rel.indexOf(t) >= 0 ? " rel" : "") + "' role='tab' data-t='" + t + "' aria-selected='" + (t === currentTable) + "'>" + t + "</button>";
    }).join("");
  }
  function showTable(t, rowId) {
    currentTable = t; renderTabs();
    var total = db.exec("SELECT COUNT(*) FROM " + t)[0].values[0][0];
    var r = runQuery("SELECT * FROM " + t + " LIMIT " + ROW_LIMIT);
    $("#datagrid").innerHTML = gridHTML(r.columns, r.values, { fk: true, rowIds: true });
    $("#datameta").textContent = total + " ligne(s)" + (total > ROW_LIMIT ? " · " + ROW_LIMIT + " premières affichées" : "") + (r.columns.some(function (c) { return FK[c]; }) ? " · les valeurs bleues (↗) sont cliquables : elles mènent à la ligne visée." : "");
    if (rowId != null) {
      var tr = $("#datagrid tr[data-id='" + String(rowId).replace(/'/g, "") + "']");
      if (tr) { tr.scrollIntoView({ block: "center", behavior: "auto" }); tr.classList.add("flash"); setTimeout(function () { tr.classList.remove("flash"); }, 2500); }
      else toast("Ligne " + rowId + " non affichée (au-delà des " + ROW_LIMIT + " premières).");
    }
  }

  /* ---------- exercices ---------- */
  function statusOf(id) { return state.status[id] || (state.submitted[id] ? "repondu" : "todo"); }
  var PILL = { todo: "À FAIRE", repondu: "RÉPONDU", pass: "PASS", partiel: "PARTIEL", fail: "FAIL" };
  function pill(id) { var s = statusOf(id); return "<span class='pill " + s + "'>" + PILL[s] + "</span>"; }
  function validated() { return window.EXERCICES.filter(function (e) { return state.status[e.id] === "pass"; }).length; }
  function renderMeter() { $("#meter").innerHTML = "<b>" + validated() + "</b> / " + window.EXERCICES.length + " validés"; renderXp(); }
  var BASE = { 0: 5, 1: 10, 2: 15, 3: 20 };
  var LEVELS = [["Stagiaire de recette", 0], ["Lecteur de tables", 0.15], ["Enquêteur de données", 0.4], ["Analyste SQL", 0.7], ["Référent data", 0.95]];
  function xpTotal() { return window.EXERCICES.reduce(function (a, e) { return a + (BASE[e.niveau] || 10); }, 0); }
  function xpNow() { return Object.keys(state.xp).reduce(function (a, k) { return a + state.xp[k]; }, 0); }
  function renderXp() {
    var T = xpTotal(), x = xpNow(), lv = 0;
    LEVELS.forEach(function (l, i) { if (x >= Math.round(l[1] * T)) lv = i; });
    var lo = Math.round(LEVELS[lv][1] * T), hi = lv + 1 < LEVELS.length ? Math.round(LEVELS[lv + 1][1] * T) : T;
    var pct = hi > lo ? Math.min(100, Math.round(100 * (x - lo) / (hi - lo))) : 100;
    $("#lvl").textContent = "Rang " + (lv + 1) + " · " + LEVELS[lv][0];
    $("#xpfill").style.width = pct + "%";
    $("#xpnum").textContent = x + " XP" + (lv + 1 < LEVELS.length ? " · prochain rang à " + hi : "");
    if (renderXp.lv !== undefined && lv > renderXp.lv) toast("Nouveau rang : " + LEVELS[lv][0]);
    renderXp.lv = lv;
  }
  function award(ex) {
    if (state.xp[ex.id]) return;
    var v = Math.round((BASE[ex.niveau] || 10) * (state.hints[ex.id] ? 0.7 : 1));
    state.xp[ex.id] = v; save(); toast("+" + v + " XP" + (state.hints[ex.id] ? " (indice utilisé)" : "")); renderXp();
  }
  function burst() {
    if (RM) return;
    var box = document.createElement("div"); box.className = "burst";
    for (var i = 0; i < 18; i++) { var p = document.createElement("i"), a = (i / 18) * Math.PI * 2, d = 60 + Math.random() * 90; p.style.setProperty("--dx", Math.cos(a) * d + "px"); p.style.setProperty("--dy", Math.sin(a) * d + "px"); p.style.background = ["var(--accent)", "var(--pass)", "var(--warn)", "var(--info)"][i % 4]; box.appendChild(p); }
    document.body.appendChild(box); setTimeout(function () { box.remove(); }, 1100);
  }
  function renderNav() {
    var h = "", last = null;
    window.EXERCICES.forEach(function (e) {
      if (e.niveau !== last) { h += "<h4>" + esc(window.NIVEAUX[e.niveau]) + "</h4>"; last = e.niveau; }
      h += "<a href='#" + e.id + "' data-id='" + e.id + "' aria-current='" + (current && current.id === e.id) + "'><span class='t'>" + esc(e.titre) + "<br><span class='id'>" + e.id + (e.atelier ? " · <span class='tag'>glisser-déposer</span>" : "") + "</span></span>" + pill(e.id) + "</a>";
    });
    h += "<h4>Libre</h4><a href='#free' data-id='free' aria-current='" + (current && current.id === "free") + "'><span class='t'>Bac à sable libre<br><span class='id'>requêtes de ton choix</span></span></a>";
    $("#nav").innerHTML = h; renderMeter();
  }
  function find(id) { return id === "free" ? FREE : window.EXERCICES.filter(function (e) { return e.id === id; })[0]; }

  function renderExercise(ex, keepTable) {
    current = ex; renderNav();
    var idx = window.EXERCICES.indexOf(ex), isSql = ex.type === "sql" || ex.type === "libre";
    var h = "<article class='card'><div class='ticket'><span>" + ex.id + "</span><span>" + esc(window.NIVEAUX[ex.niveau] || "Libre") + "</span><span id='pillbox'>" + (ex.type === "libre" ? "" : pill(ex.id)) + "</span></div><h2>" + esc(ex.titre) + "</h2></article>";
    if (ex.type === "libre") {
      h += "<section class='card situation'><h3>Mode libre</h3><p>Pose tes propres questions aux tables (panneau Données). Seules les requêtes <code>SELECT</code> sont autorisées. Raccourci : <code>Ctrl+Entrée</code> pour exécuter.</p></section>";
    } else {
      h += "<section class='card situation'><h3>Situation</h3>" + md(ex.situation) + "</section>";
      if (ex.cours) h += "<section class='card'><details class='cours'><summary>Rappel de cours</summary><div>" + md(ex.cours) + "</div></details></section>";
      h += "<section class='card'><h3>Question</h3>" + md(ex.question) + "</section>";
    }
    var atel = ["assemblage", "ordre", "jointure"].indexOf(ex.type) >= 0;
    if (atel) {
      h += "<section class='card atelier'><h3>Atelier</h3><div id='atelier'></div>" + (ex.indices ? "<div class='actions'><button class='btn' id='btn-hint'></button></div><div id='hints'></div>" : "") + "</section>";
    } else {
      h += "<section class='card'><h3>" + (isSql ? "Ta requête" : "Ta réponse") + "</h3><textarea id='answer' class='" + (isSql ? "sql" : "") + "' spellcheck='false' placeholder='" + (isSql ? "SELECT ..." : "Écris ta réponse ici, avec tes mots.") + "'></textarea>";
      h += "<div class='actions'>";
      if (isSql) h += "<button class='btn' id='btn-run'>Exécuter</button>";
      if (ex.type !== "libre") h += "<button class='btn primary' id='btn-submit'>Valider ma réponse</button>";
      if (ex.indices) h += "<button class='btn' id='btn-hint'></button>";
      h += "</div><div id='hints'></div><div id='result'></div></section>";
    }
    h += "<div id='correction'></div>";
    if (ex.type !== "libre") h += "<div class='pager'><button class='btn' id='btn-prev'" + (idx <= 0 ? " disabled" : "") + ">← Précédent</button><button class='btn' id='btn-next'" + (idx >= window.EXERCICES.length - 1 ? " disabled" : "") + ">Suivant →</button></div>";
    $("#main").innerHTML = h;

    if (atel) { window.Atelier[ex.type](ex, $("#atelier")); } else {
      var ta = $("#answer"); ta.value = state.answers[ex.id] || "";
      ta.addEventListener("input", function () { state.answers[ex.id] = ta.value; save(); });
      if (isSql) {
        $("#btn-run").addEventListener("click", function () { execute(ta.value); });
        ta.addEventListener("keydown", function (e) { if ((e.ctrlKey || e.metaKey) && e.key === "Enter") { e.preventDefault(); execute(ta.value); } });
      }
      if (ex.type !== "libre") $("#btn-submit").addEventListener("click", function () { submit(ex); });
}
    if (ex.indices) { renderHints(ex); $("#btn-hint").addEventListener("click", function () { var n = (state.hints[ex.id] || 0); if (n < ex.indices.length) { state.hints[ex.id] = n + 1; save(); renderHints(ex); } }); }
    if ($("#btn-prev")) $("#btn-prev").addEventListener("click", function () { go(window.EXERCICES[idx - 1].id); });
    if ($("#btn-next")) $("#btn-next").addEventListener("click", function () { go(window.EXERCICES[idx + 1].id); });
    if (state.submitted[ex.id]) renderCorrection(ex, null);
    if (!keepTable && ex.tables && ex.tables.length) showTable(ex.tables[0]);
    else if (!currentTable) showTable("anomalies");
    else renderTabs();
    window.scrollTo(0, 0);
  }
  function renderHints(ex) {
    var n = state.hints[ex.id] || 0;
    $("#hints").innerHTML = ex.indices.slice(0, n).map(function (t, i) { return "<div class='hint'><b>Indice " + (i + 1) + ".</b> " + inline(t) + "</div>"; }).join("");
    var b = $("#btn-hint"); b.textContent = n >= ex.indices.length ? "Plus d'indice" : "Indice " + (n + 1) + " / " + ex.indices.length; b.disabled = n >= ex.indices.length;
  }
  function execute(sql) {
    var box = $("#result");
    try {
      var r = runQuery(sql);
      box.innerHTML = "<div class='res-wrap'>" + gridHTML(r.columns, r.values.slice(0, 100)) + "</div><div class='meta'>" + r.values.length + " ligne(s)" + (r.values.length > 100 ? " · 100 premières affichées" : "") + ".</div>";
      return r;
    } catch (e) { box.innerHTML = "<div class='err'>Erreur SQL : " + esc(e.message) + "</div>"; return null; }
  }

  function submit(ex) {
    var ans = ($("#answer").value || "").trim();
    if (!ans) { toast("Écris d'abord ta réponse : la correction s'affiche après."); $("#answer").focus(); return; }
    var verdict = null;
    if (ex.type === "sql") {
      var u = execute(ans);
      if (!u) verdict = { ok: false, msg: "Ta requête a produit une erreur (voir ci-dessus). Corrige-la et valide à nouveau." };
      else verdict = compare(u, runQuery(ex.solution), !!ex.ordered);
    }
    finish(ex, verdict, ans);
  }
  /* Enregistre un résultat (appelé aussi par l'atelier) : statut, XP, correction, animation. */
  function finish(ex, verdict, answerText) {
    state.answers[ex.id] = answerText; state.submitted[ex.id] = true;
    var first = false;
    if (verdict) {
      if (verdict.ok) { first = state.status[ex.id] !== "pass"; state.status[ex.id] = "pass"; award(ex); }
      else if (state.status[ex.id] !== "pass") state.status[ex.id] = "fail";
    }
    save(); renderCorrection(ex, verdict); renderNav();
    var pb = $("#pillbox"); if (pb) pb.innerHTML = pill(ex.id);
    if (first) burst();
    var c = $("#correction"); if (c) c.scrollIntoView({ block: "start", behavior: RM ? "auto" : "smooth" });
  }
  window.SQLQ = { run: runQuery, compare: compare, grid: gridHTML, esc: esc, finish: finish };
  function renderCorrection(ex, verdict) {
    var h = "<section class='card correction'>";
    if (ex.type === "sql" || ex.type === "assemblage") {
      var s = state.status[ex.id];
      if (!verdict) verdict = s === "pass" ? { ok: true } : { ok: false, msg: "Dernière validation : résultat différent de l'attendu. Tu peux corriger et valider à nouveau." };
      h += verdict.ok ? "<div class='verdict ok'>Résultat conforme à l'attendu.<small>Ta requête renvoie les mêmes colonnes et les mêmes lignes que la correction. Compare quand même ton écriture avec celle ci-dessous.</small></div>"
                      : "<div class='verdict ko'>Résultat différent de l'attendu.<small>" + esc(verdict.msg) + "</small></div>";
      h += "<h4>Correction</h4><pre><code>" + esc(ex.solution) + "</code></pre>";
      var ref = runQuery(ex.solution);
      h += "<h4>Résultat attendu (" + ref.values.length + " ligne" + (ref.values.length > 1 ? "s" : "") + ")</h4><div class='res-wrap'>" + gridHTML(ref.columns, ref.values.slice(0, 30)) + "</div>";
      h += "<h4>Explication</h4>" + md(ex.explication);
    } else if (ex.type === "ordre" || ex.type === "jointure") {
      var s2 = state.status[ex.id];
      if (!verdict) verdict = s2 === "pass" ? { ok: true } : { ok: false, msg: "Pas encore réussi : tu peux réessayer ci-dessus." };
      h += verdict.ok ? "<div class='verdict ok'>Réussi.</div>" : "<div class='verdict ko'>Pas encore.<small>" + esc(verdict.msg) + "</small></div>";
      h += "<h4>Correction</h4>" + md(ex.correction) + "<h4>Explication</h4>" + md(ex.explication);
    } else {
      h += "<h4>Correction</h4>" + md(ex.correction) + "<h4>Explication</h4>" + md(ex.explication);
      var st = state.status[ex.id];
      h += "<div class='selfeval'><span>Ta réponse était :</span>" + [["pass", "Juste"], ["partiel", "Partielle"], ["fail", "À revoir"]].map(function (o) { return "<button class='btn" + (st === o[0] ? " on" : "") + "' data-ev='" + o[0] + "'>" + o[1] + "</button>"; }).join("") + "</div>";
      h += "<div class='meta'>Auto-évaluation honnête : c'est elle qui compte dans ta progression. Tu peux aussi me coller tes réponses (bouton « Copier mes réponses ») pour une correction détaillée.</div>";
    }
    $("#correction").innerHTML = h + "</section>";
    Array.prototype.forEach.call(document.querySelectorAll("[data-ev]"), function (b) {
      b.addEventListener("click", function () { var ev = b.getAttribute("data-ev"), first = ev === "pass" && !state.xp[ex.id]; state.status[ex.id] = ev; if (ev === "pass") award(ex); save(); renderCorrection(ex, null); renderNav(); $("#pillbox").innerHTML = pill(ex.id); if (first) burst(); });
    });
  }

  /* ---------- navigation, export ---------- */
  function go(id) { location.hash = id; }
  function route() {
    var id = (location.hash || "").replace("#", "") || (window.EXERCICES.filter(function (e) { return statusOf(e.id) === "todo"; })[0] || window.EXERCICES[0]).id;
    var ex = find(id) || window.EXERCICES[0];
    if (window.matchMedia("(max-width: 1000px)").matches) $("#navdet").removeAttribute("open");
    renderExercise(ex, false);
  }
  function exportText() {
    var out = "# Mes réponses SQL Quest\n\n";
    window.EXERCICES.forEach(function (e) {
      if (!state.answers[e.id]) return;
      out += "## " + e.id + " — " + e.titre + "\nStatut : " + PILL[statusOf(e.id)] + " · indices utilisés : " + (state.hints[e.id] || 0) + "\n```" + (e.type === "sql" ? "sql" : "") + "\n" + state.answers[e.id] + "\n```\n\n";
    });
    return out;
  }
  function copy(text) {
    function fallback() { var t = document.createElement("textarea"); t.value = text; t.style.position = "fixed"; t.style.opacity = "0"; document.body.appendChild(t); t.select(); var ok = false; try { ok = document.execCommand("copy"); } catch (e) {} document.body.removeChild(t); toast(ok ? "Réponses copiées : colle-les dans la conversation." : "Copie impossible : sélectionne et copie manuellement."); }
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(function () { toast("Réponses copiées : colle-les dans la conversation."); }, fallback); else fallback();
  }

  /* ---------- démarrage ---------- */
  function start() {
    load();
    window.initSqlJs({ wasmBinary: b64bytes(window.SQLJS_WASM_B64) }).then(function (SQL) {
      db = new SQL.Database(); db.exec(window.SEED_SQL);
      $("#nav").addEventListener("click", function (e) { var a = e.target.closest("a"); if (a && window.matchMedia("(max-width: 1000px)").matches) setTimeout(function () { $("#navdet").removeAttribute("open"); }, 0); });
      $("#tabs").addEventListener("click", function (e) { var b = e.target.closest(".tab"); if (b) showTable(b.getAttribute("data-t")); });
      $("#datagrid").addEventListener("click", function (e) { var c = e.target.closest("td.fk"); if (c) showTable(c.getAttribute("data-t"), c.getAttribute("data-v")); });
      $("#btn-export").addEventListener("click", function () { var t = exportText(); if (t.indexOf("##") < 0) toast("Aucune réponse à copier pour l'instant."); else copy(t); });
      $("#btn-reset").addEventListener("click", function () {
        var b = $("#btn-reset");
        if (b.getAttribute("data-armed") !== "1") { b.setAttribute("data-armed", "1"); b.textContent = "Confirmer l'effacement"; setTimeout(function () { b.removeAttribute("data-armed"); b.textContent = "Effacer ma progression"; }, 4000); return; }
        state = { answers: {}, submitted: {}, status: {}, hints: {}, xp: {} }; save(); b.removeAttribute("data-armed"); b.textContent = "Effacer ma progression"; route(); toast("Progression effacée.");
      });
      window.addEventListener("hashchange", route);
      route();
    }, function (err) { $("#main").innerHTML = "<div class='boot'>Impossible de démarrer le moteur SQL : " + esc(err && err.message || err) + "</div>"; });
  }
  start();
})();
