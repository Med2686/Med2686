/* Atelier SQL Quest : exercices en glisser-déposer (ou clic / clavier), animés.
   Trois mécaniques : "assemblage" (construire une requête avec des blocs),
   "ordre" (remettre dans l'ordre d'exécution), "jointure" (relier deux tables puis voir la jointure se dérouler).
   Dépend de window.SQLQ exposé par app.js. */
(function () {
  "use strict";
  var Q = function () { return window.SQLQ; };
  var RM = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var sleep = function (ms) { return new Promise(function (r) { setTimeout(r, RM ? 0 : ms); }); };
  var esc = function (s) { return Q().esc(s); };
  function shake(node) { if (!node || RM) return; node.classList.remove("shake"); void node.offsetWidth; node.classList.add("shake"); }

  /* ======================= ASSEMBLAGE ======================= */
  function assemblage(ex, root) {
    var placed = {};           // slot.k -> [index de chip]
    var picked = null;         // chip sélectionnée au clic (alternative au glisser)
    ex.slots.forEach(function (s) { placed[s.k] = []; });
    var used = function (i) { return ex.slots.some(function (s) { return placed[s.k].indexOf(i) >= 0; }); };

    root.innerHTML =
      "<p class='meta'>Glisse les blocs dans les bonnes zones (ou clique un bloc, puis clique une zone). Clique un bloc posé pour le retirer.</p>" +
      "<div class='pool' id='pool' aria-label='Blocs disponibles'></div>" +
      "<div class='slots' id='slots'></div>" +
      "<h4 class='mini'>Requête obtenue</h4><pre id='preview'><code></code></pre>" +
      "<div class='actions'><button class='btn' id='at-run'>Voir le résultat</button><button class='btn primary' id='at-submit'>Valider ma requête</button><button class='btn' id='at-clear'>Tout retirer</button></div>" +
      "<div id='result'></div><div id='msg' class='msg' role='status'></div>";

    function sqlText() {
      var parts = [];
      ex.slots.forEach(function (s) {
        var items = placed[s.k]; if (!items.length) return;
        parts.push(s.label + " " + items.map(function (i) { return ex.chips[i].t; }).join(s.sep || ", "));
      });
      return parts.join("\n");
    }
    function setMsg(t, ok) { var m = root.querySelector("#msg"); m.textContent = (t || "").replace(/\*\*/g, ""); m.className = "msg" + (t ? (ok ? " ok" : " ko") : ""); }
    function render() {
      var pool = root.querySelector("#pool");
      pool.innerHTML = ex.chips.map(function (c, i) {
        return used(i) ? "" : "<button class='chip" + (picked === i ? " picked" : "") + "' draggable='true' data-i='" + i + "'>" + esc(c.t) + "</button>";
      }).join("") || "<span class='meta'>Tous les blocs sont posés.</span>";
      root.querySelector("#slots").innerHTML = ex.slots.map(function (s) {
        var its = placed[s.k].map(function (i) { return "<button class='chip placed' data-r='" + i + "' data-k='" + s.k + "' title='Retirer'>" + esc(ex.chips[i].t) + "</button>"; }).join("");
        return "<div class='slot' tabindex='0' role='button' data-k='" + s.k + "' aria-label='Zone " + esc(s.label) + "'><span class='kw'>" + esc(s.label) + "</span><div class='slot-items'>" + (its || "<span class='ph'>dépose ici</span>") + "</div></div>";
      }).join("");
      var sql = sqlText();
      root.querySelector("#preview code").textContent = sql || "-- la requête s'affiche ici au fur et à mesure";
      Array.prototype.forEach.call(root.querySelectorAll(".chip:not(.placed)"), function (b) {
        b.addEventListener("dragstart", function (e) { e.dataTransfer.setData("text/plain", b.getAttribute("data-i")); e.dataTransfer.effectAllowed = "move"; });
        b.addEventListener("click", function () { picked = (picked === +b.getAttribute("data-i")) ? null : +b.getAttribute("data-i"); render(); });
      });
      Array.prototype.forEach.call(root.querySelectorAll(".chip.placed"), function (b) {
        b.addEventListener("click", function (e) { e.stopPropagation(); var k = b.getAttribute("data-k"), i = +b.getAttribute("data-r"); placed[k].splice(placed[k].indexOf(i), 1); setMsg(""); render(); });
      });
      Array.prototype.forEach.call(root.querySelectorAll(".slot"), function (sl) {
        sl.addEventListener("dragover", function (e) { e.preventDefault(); sl.classList.add("over"); });
        sl.addEventListener("dragleave", function () { sl.classList.remove("over"); });
        sl.addEventListener("drop", function (e) { e.preventDefault(); sl.classList.remove("over"); var i = parseInt(e.dataTransfer.getData("text/plain"), 10); if (!isNaN(i)) drop(i, sl); });
        sl.addEventListener("click", function () { if (picked !== null) drop(picked, sl); });
        sl.addEventListener("keydown", function (e) { if ((e.key === "Enter" || e.key === " ") && picked !== null) { e.preventDefault(); drop(picked, sl); } });
      });
    }
    function drop(i, slotNode) {
      var k = slotNode.getAttribute("data-k"), slot = ex.slots.filter(function (s) { return s.k === k; })[0], chip = ex.chips[i];
      picked = null;
      if (chip.s !== k) {
        var twin = ex.chips.some(function (c, j) { return j !== i && c.t === chip.t && c.s === k && !used(j); });
        setMsg(twin ? "Il existe un deuxième bloc « " + chip.t + " » prévu pour " + slot.label + " : prends celui-là." : ((chip.pas && chip.pas[k]) || ("« " + chip.t + " » ne va pas dans " + slot.label + ".")), false);
        shake(slotNode); render(); return;
      }
      if (!slot.multi && placed[k].length) { setMsg(slot.label + " n'accepte qu'un seul bloc : retire l'autre d'abord.", false); shake(slotNode); render(); return; }
      placed[k].push(i); setMsg(""); render();
      var added = root.querySelectorAll(".slot[data-k='" + k + "'] .chip.placed"); if (added.length) added[added.length - 1].classList.add("pop");
    }
    function runLive() {
      var sql = sqlText(), box = root.querySelector("#result");
      if (!placed.select.length || !placed.from.length) { box.innerHTML = ""; setMsg("Il faut au moins un bloc dans SELECT et dans FROM.", false); return null; }
      try {
        var r = Q().run(sql);
        box.innerHTML = "<div class='res-wrap'>" + Q().grid(r.columns, r.values.slice(0, 100)) + "</div><div class='meta'>" + r.values.length + " ligne(s).</div>";
        return r;
      } catch (e) { box.innerHTML = "<div class='err'>Erreur SQL : " + esc(e.message) + "</div>"; return null; }
    }
    root.querySelector("#at-run").addEventListener("click", function () { if (runLive()) setMsg(""); });
    root.querySelector("#at-clear").addEventListener("click", function () { ex.slots.forEach(function (s) { placed[s.k] = []; }); picked = null; root.querySelector("#result").innerHTML = ""; setMsg(""); render(); });
    root.querySelector("#at-submit").addEventListener("click", function () {
      var sql = sqlText(), u = runLive(), verdict;
      if (!u) verdict = { ok: false, msg: "La requête n'a pas pu s'exécuter telle quelle : complète ou corrige les blocs." };
      else verdict = Q().compare(u, Q().run(ex.solution), !!ex.ordered);
      Q().finish(ex, verdict, sql || "(vide)");
    });
    render();
  }

  /* ======================= ORDRE D'EXÉCUTION ======================= */
  function ordre(ex, root) {
    var order = ex.melange.slice();      // indices dans ex.items (ordre correct = 0..n-1)
    var dragFrom = null;
    root.innerHTML = "<p class='meta'>Glisse les cartes (ou utilise ▲ ▼) pour les remettre dans l'ordre où le moteur les exécute, de la première à la dernière.</p><ol class='order' id='order'></ol><div class='actions'><button class='btn primary' id='or-submit'>Vérifier l'ordre</button></div><div id='msg' class='msg' role='status'></div>";
    function render(marks) {
      var ol = root.querySelector("#order");
      ol.innerHTML = order.map(function (idx, pos) {
        var it = ex.items[idx], cls = "ocard" + (marks ? (marks[pos] ? " good" : " bad") : "");
        return "<li class='" + cls + "' draggable='true' data-p='" + pos + "'><span class='n'>" + (pos + 1) + "</span><span class='ot'><b>" + esc(it.t) + "</b><small>" + esc(it.d) + "</small></span><span class='mv'><button class='btn sm' data-up='" + pos + "' aria-label='Monter'>▲</button><button class='btn sm' data-dn='" + pos + "' aria-label='Descendre'>▼</button></span></li>";
      }).join("");
      Array.prototype.forEach.call(ol.querySelectorAll("li"), function (li) {
        li.addEventListener("dragstart", function (e) { dragFrom = +li.getAttribute("data-p"); e.dataTransfer.setData("text/plain", String(dragFrom)); e.dataTransfer.effectAllowed = "move"; li.classList.add("dragging"); });
        li.addEventListener("dragend", function () { li.classList.remove("dragging"); });
        li.addEventListener("dragover", function (e) { e.preventDefault(); li.classList.add("over"); });
        li.addEventListener("dragleave", function () { li.classList.remove("over"); });
        li.addEventListener("drop", function (e) { e.preventDefault(); var to = +li.getAttribute("data-p"); if (dragFrom !== null && dragFrom !== to) { var m = order.splice(dragFrom, 1)[0]; order.splice(to, 0, m); } dragFrom = null; render(); });
      });
      Array.prototype.forEach.call(ol.querySelectorAll("[data-up]"), function (b) { b.addEventListener("click", function () { move(+b.getAttribute("data-up"), -1); }); });
      Array.prototype.forEach.call(ol.querySelectorAll("[data-dn]"), function (b) { b.addEventListener("click", function () { move(+b.getAttribute("data-dn"), 1); }); });
    }
    function move(p, d) { var q = p + d; if (q < 0 || q >= order.length) return; var t = order[p]; order[p] = order[q]; order[q] = t; render(); }
    root.querySelector("#or-submit").addEventListener("click", function () {
      var marks = order.map(function (idx, pos) { return idx === pos; }), good = marks.filter(Boolean).length, ok = good === order.length;
      render(marks);
      var cards = root.querySelectorAll(".ocard"); Array.prototype.forEach.call(cards, function (c, i) { if (!RM) c.style.animationDelay = (i * 70) + "ms"; c.classList.add("reveal"); });
      var m = root.querySelector("#msg"); m.className = "msg " + (ok ? "ok" : "ko");
      m.textContent = ok ? "Ordre exact." : good + " carte(s) sur " + order.length + " bien placée(s). Les cartes en rouge sont mal placées : remets-les et revérifie.";
      Q().finish(ex, ok ? { ok: true } : { ok: false, msg: good + " / " + order.length + " cartes bien placées." }, order.map(function (i) { return ex.items[i].t; }).join(" > "));
    });
    render();
  }

  /* ======================= JOINTURE ANIMÉE ======================= */
  function jointure(ex, root) {
    var L = ex.left, R = ex.right, picked = null, linked = false, running = false, rows = {};
    function sel(side) {
      var S = side === "l" ? L : R;
      var r = Q().run("SELECT " + S.cols.join(", ") + " FROM " + S.table + " WHERE " + S.where + " ORDER BY id");
      return r;
    }
    var left = sel("l"), right = sel("r");
    function tbl(side, data) {
      var S = side === "l" ? L : R;
      return "<div class='jt' data-side='" + side + "'><div class='jt-h'>" + esc(S.label) + "</div><table class='grid'><thead><tr>" +
        data.columns.map(function (c) { return "<th><button class='handle' draggable='true' data-side='" + side + "' data-col='" + c + "'>" + esc(c) + "</button></th>"; }).join("") +
        "</tr></thead><tbody>" + data.values.map(function (r, i) { return "<tr data-side='" + side + "' data-i='" + i + "'>" + r.map(function (v) { return "<td>" + (v === null ? "NULL" : esc(v)) + "</td>"; }).join("") + "</tr>"; }).join("") + "</tbody></table></div>";
    }
    root.innerHTML =
      "<div class='step'><b>Étape 1.</b> Relie les deux tables par leur clé : glisse un en-tête de colonne sur un autre en-tête (ou clique-les l'un après l'autre).</div>" +
      "<div class='jgrid'>" + tbl("l", left) + tbl("r", right) + "</div>" +
      "<div id='linkinfo' class='linkinfo'>Aucun lien pour l'instant.</div>" +
      "<div class='step'><b>Étape 2.</b> " + esc(ex.goal) + "</div>" +
      "<div class='jctl'><label><input type='radio' name='jt' value='INNER'> INNER JOIN</label><label><input type='radio' name='jt' value='LEFT'> LEFT JOIN <small>(" + esc(L.table) + " à gauche)</small></label>" +
      "<label class='pred'>Combien de lignes aura le résultat ? <input id='pred' type='number' min='0' max='99' inputmode='numeric'></label>" +
      "<button class='btn primary' id='jn-run'>Lancer la jointure</button></div>" +
      "<div class='step'><b>Résultat</b> <span id='counts' class='meta'></span></div><div id='jres' class='jres'></div><div id='msg' class='msg' role='status'></div>";

    function setMsg(t, ok) { var m = root.querySelector("#msg"); m.textContent = t || ""; m.className = "msg" + (t ? (ok ? " ok" : " ko") : ""); }
    function tryLink(a, b) {
      if (a.side === b.side) { setMsg("Il faut relier une colonne de chaque table.", false); return; }
      var l = a.side === "l" ? a : b, r = a.side === "l" ? b : a, good = l.col === L.key && r.col === R.key;
      var info = root.querySelector("#linkinfo");
      if (good) {
        linked = true; info.className = "linkinfo ok";
        info.innerHTML = "Lien posé : <code>ON " + esc(R.table) + "." + esc(R.key) + " = " + esc(L.table) + "." + esc(L.key) + "</code>";
        Array.prototype.forEach.call(root.querySelectorAll(".handle"), function (h) { h.classList.remove("picked"); });
        Array.prototype.forEach.call(root.querySelectorAll(".handle"), function (h) { if ((h.getAttribute("data-side") === "l" && h.getAttribute("data-col") === L.key) || (h.getAttribute("data-side") === "r" && h.getAttribute("data-col") === R.key)) h.classList.add("linked"); });
        setMsg("");
      } else { linked = false; info.className = "linkinfo"; info.textContent = "Aucun lien pour l'instant."; setMsg("Ces deux colonnes ne désignent pas la même chose. Cherche la clé étrangère : quelle colonne de " + R.table + " contient un numéro de " + L.table + " ?", false); shake(info); Array.prototype.forEach.call(root.querySelectorAll(".handle"), function (h) { h.classList.remove("picked", "linked"); }); }
    }
    Array.prototype.forEach.call(root.querySelectorAll(".handle"), function (h) {
      var me = function () { return { side: h.getAttribute("data-side"), col: h.getAttribute("data-col") }; };
      h.addEventListener("dragstart", function (e) { e.dataTransfer.setData("text/plain", JSON.stringify(me())); });
      h.addEventListener("dragover", function (e) { e.preventDefault(); h.classList.add("over"); });
      h.addEventListener("dragleave", function () { h.classList.remove("over"); });
      h.addEventListener("drop", function (e) { e.preventDefault(); h.classList.remove("over"); try { tryLink(JSON.parse(e.dataTransfer.getData("text/plain")), me()); } catch (x) {} });
      h.addEventListener("click", function () {
        if (!picked) { picked = me(); h.classList.add("picked"); return; }
        var a = picked; picked = null; Array.prototype.forEach.call(root.querySelectorAll(".handle"), function (x) { x.classList.remove("picked"); }); tryLink(a, me());
      });
    });

    function aliasCols(p, S) { return S.cols.map(function (c) { return p + "." + c + " AS " + p + "_" + c; }).join(", "); }
    function sqlFor(type) {
      return "SELECT " + aliasCols("l", L) + ", " + aliasCols("r", R) + " FROM (SELECT " + L.cols.join(", ") + " FROM " + L.table + " WHERE " + L.where + ") l " + type + " JOIN (SELECT " + R.cols.join(", ") + " FROM " + R.table + " WHERE " + R.where + ") r ON r." + R.key + " = l." + L.key + " ORDER BY l.id, r.id";
    }
    root.querySelector("#jn-run").addEventListener("click", async function () {
      if (running) return;
      var type = (root.querySelector("input[name='jt']:checked") || {}).value, predV = root.querySelector("#pred").value;
      if (!linked) { setMsg("Étape 1 d'abord : relie les deux colonnes clés.", false); return; }
      if (!type) { setMsg("Choisis le type de jointure.", false); return; }
      if (predV === "") { setMsg("Fais d'abord ta prédiction : combien de lignes ?", false); root.querySelector("#pred").focus(); return; }
      running = true; setMsg("");
      var res = Q().run(sqlFor(type)), cols = res.columns, total = res.values.length, jres = root.querySelector("#jres");
      jres.innerHTML = "<table class='grid'><thead><tr>" + cols.map(function (c) { return "<th>" + esc(c) + "</th>"; }).join("") + "</tr></thead><tbody></tbody></table>";
      var tb = jres.querySelector("tbody"), counts = root.querySelector("#counts"), n = 0, lost = 0;
      Array.prototype.forEach.call(root.querySelectorAll(".jt tr"), function (tr) { tr.classList.remove("hl", "lost", "match"); });
      var lKey = cols.indexOf("l_" + L.key), rKey = cols.indexOf("r_" + R.key);
      for (var i = 0; i < left.values.length; i++) {
        var lid = left.values[i][0], lrow = root.querySelector(".jt[data-side='l'] tbody tr[data-i='" + i + "']");
        lrow.classList.add("hl"); await sleep(260);
        var mine = res.values.filter(function (r) { return r[lKey] === lid; });
        var matched = mine.filter(function (r) { return r[cols.indexOf("r_id")] !== null; });
        right.values.forEach(function (rv, j) { if (rv[right.columns.indexOf(R.key)] === lid) root.querySelector(".jt[data-side='r'] tbody tr[data-i='" + j + "']").classList.add("match"); });
        await sleep(matched.length ? 260 : 80);
        if (!mine.length) { lost++; lrow.classList.remove("hl"); lrow.classList.add("lost"); counts.textContent = n + " ligne(s) · " + lost + " cas sans correspondance, éliminé(s)"; await sleep(160); }
        mine.forEach(function (r) {
          var tr = document.createElement("tr"); tr.className = "enter";
          tr.innerHTML = r.map(function (v) { return v === null ? "<td class='null'>NULL</td>" : "<td>" + esc(v) + "</td>"; }).join("");
          tb.appendChild(tr); n++;
        });
        if (mine.length) counts.textContent = n + " ligne(s)" + (lost ? " · " + lost + " cas sans correspondance, éliminé(s)" : "");
        await sleep(120);
        lrow.classList.remove("hl");
        Array.prototype.forEach.call(root.querySelectorAll(".jt[data-side='r'] tr.match"), function (t) { t.classList.remove("match"); });
      }
      counts.textContent = total + " ligne(s) pour " + left.values.length + " " + L.table + (lost ? " · " + lost + " éliminé(s)" : "");
      running = false;
      var pred = parseInt(predV, 10), expect = ex.attendu;
      var okType = type === expect, okPred = pred === total, verdict;
      if (!okType) verdict = { ok: false, msg: "Avec INNER JOIN, " + lost + " cas de test sur " + left.values.length + " disparaissent du résultat : ceux qui n'ont aucune anomalie. Or on veut les voir tous : relance avec LEFT JOIN." };
      else if (!okPred) verdict = { ok: false, msg: "Bon type de jointure, mais ta prédiction (" + pred + ") ne correspond pas : le résultat contient " + total + " lignes pour " + left.values.length + " cas de test. Regarde les cas qui ont deux anomalies : ils apparaissent deux fois. Modifie ta prédiction et relance." };
      else verdict = { ok: true };
      setMsg(verdict.ok ? "Bien vu : prédiction exacte (" + total + " lignes) et bon type de jointure." : verdict.msg, verdict.ok);
      Q().finish(ex, verdict, type + " JOIN, prédiction " + pred + ", résultat " + total);
    });
  }

  window.Atelier = { assemblage: assemblage, ordre: ordre, jointure: jointure };
})();
