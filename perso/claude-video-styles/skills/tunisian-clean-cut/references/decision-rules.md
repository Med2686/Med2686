# Decision rules and the worked example (ref-edit reel, 2026-11-11)

## The rules, in the order to apply them

1. **Understand the video first.** Read the whole reading pack and write the topic in one line and the
   outline (hook → points → ending). Every later decision is "does this phrase belong to the sentence he
   meant?". You cannot judge a retake without knowing the intended sentence.
2. **Reconstruct the intended sentence in Derja (arabizi)**, per phrase, from the three passes + the strip.
   Write it like the keep list: « w houni exactement win tetla9a la différence bin les users el 3adiyin ».
3. **Last take wins, at every scale.** Syllable, word, phrase, whole sentence: keep the LAST complete take.
   - « so don't… so don't just learn AI » → keep the second (the first was wrongly kept on 2026-11-11).
   - « el kol ye7taj, el kol ye7taj el créativité » → keep only the last.
   - Takes joined by « wala » or « w » are still takes.
4. **A false start glued to its retake is still a false start.** « ou la cap|ou la capacité de juger »:
   a 20-30 ms notch, one speech region. Cut from the start of the false start to the notch.
5. **A restart of the same sentence keeps the second**, even if the first went further: « khater l'AI tnajjem
   ta3tik kol chay » → « khater l'AI tnajjem ta3tik réponse t'ban parfaite ».
6. **A correction keeps the correction**: « les visuals… les effets visuels » → « les effets visuels ».
7. **Cut tics and throat-clearing** (`derja-fillers.md`): « ena personnellement, donc ena, ki nchouf » →
   keep from « ki nchouf »; d'accord, ok, fhemt, ya3ni (filler), euh, mmm, et cetera, trailing wala,
   « donc » as an empty starter, a repeated filler « par exemple » in an enumeration.
8. **Cut a reformulated duplicate idea (keep the last)**, but **never lose a real moment**: if the second
   version drops something the first said (a number, a name, a joke, a strong word), it is not a duplicate.
   Keep the first, or flag it. A rephrase that adds meaning stays.
9. **Unclear = flag, never silent cut.** « w … kif hedhi el kol (mot pas clair) » went to the user as an
   open question.
10. **Zero pauses.** The build removes every quiet run > 0.06 s inside kept lines (20 ms pads). He spots
    0.3 s. No silent gesture insert, ever: a visual idea goes on the spoken words.
11. **Never clip a word.** Bounds in dips; proof.py's END check; French nasal endings.
12. **Script reading while talking is covered, not cut** (a full-screen graphic over the look-away); the
    words stay. Thinking looks are fine.

## The findings list (send BEFORE the final cut)

One line per decision that is not an obvious pause removal, with mic times, so he can say "restore 7":

Example (line numbers illustrative):
```
Findings, clean cut v2 (mic = Recording (52), times in s):
 1. #34 · mic 237.9  CUT 238.20-238.59 false start « ou la cap… » → keeps « ou la capacité de juger le résultat »
 2. #42 · mic 267.5  CUT ≈267.98-269.6 opener « ena personnellement, donc ena » → keeps « ki nchouf produit masna3 bel IA »
 3. #51 · mic 321.25 CUT 321.25-322.25 first take « so don't » → keeps « donc ma tet3allemch l'AI bark »
 4. #53 · mic 324.4  CUT 324.40-325.16 « learn » said twice → keeps « t3allem kifech tkoun smart around AI »
 5. #49 · mic 309.0  ? « ça reflète enti… » said 3 times: keep the 3rd only? (FLAG, needs your ear)
Open: #6 · mic 46.8 « w … kif hedhi el kol » unclear word — keep or cut?
```

Then the Studio labels (`#n · mic t s`) let him point at any moment.

## Worked example: what the user had to correct on 2026-11-11, and what now catches it

| Correction | What happened | Caught by |
|---|---|---|
| (a) « ou la cap… ou la capacité de juger » (mic 237.92-238.58 then 238.60) | one speech region; whole-line passes all heard « ou la capacité de juger le résultat » | bursts.py: notch 238.45 score 5 and 238.59 score 2 (ECHO z+2.5, TIDY, SOUNDS-LIKE fr « oulika »~« oulacapa »); CLUSTER 238.45..238.59 → keep from 238.59 (the last), proved by `listen.py 238.59-241.0` |
| (b) « ena personnellement, donc ena, ki nchouf » (mic 267.5-270.7) | kept as the line opening | scan.py: REOPEN « ena personnellement donc ena » + OPENER (en+fr); bursts.py « ! » at 269.54 (ECHO z+4.0, acoustic only) |
| (c) « so don't… so don't just learn AI » (mic 321.25-321.92, then 322.30) | I kept the FIRST take as its own line « Donc ma » | scan.py REPEAT « so don t » (en plain); bursts.py CLUSTER 321.65..322.25 → keep from 322.25; qa_clean DOUBLED « so don t »; rule 3. Note: the region transcript alone said « So don't just learn AI » (tidied) |
| (d) « learn, learn how to be smart » (mic 324.75-325.16 then 325.16) | whole-line en/fr said « Learn how to… » | bursts.py notch 325.16 score 10 (PAIR-REPEAT en « learn learn how to be smart », PREFIX, ECHO z+3.9); scan.py en-verb « Learn, learn »; qa_clean.py DOUBLED « learn » |
| (e1) « kol hedha yotlob créativité… el kol ye7taj, el kol ye7taj el créativité » (mic ~155.7-165.4) | three takes | find_repeats « el kol ye7taj » x2; rule 3 → keep 163.76-165.50 |
| (e2) « les visuals… les effets visuels » (mic ~147-151) | correction | rule 6 → keep 150.30-151.50 |
| (e3) « khater l'AI tnajjem ta3tik kol chay » → « … réponse t'ban parfaite » | sentence restart | find_repeats RESTART (6-gram); rule 5 → keep 222.50-225.80 |
| (e4) second « par exemple » inside the enumeration (mic ~126.5 and ~131) | filler repeat | rule 7 |
| open | « ça reflète ce que tu fais, ça reflète ce que tu fais, ça reflète si tu es créatif » (mic 309-318.75) | scan.py REPEAT « ce que tu fais » / « it reflects what you do »: decide from meaning (two takes then the full one: keep the last complete) |

Things that were right and must stay right:
- The camera is 4K HLG + Dolby Vision, rotated, 29.997 fps → fps=30 grid, mobius tone map, 4K kept.
- Mic offset 20.666 s, drift 6 ms (sync.py reproduces it on 20 s slices: 20.663 / 20.669).
- He reads in the pauses; the one look-away while talking (mic 187.37-188.27, « bech tefhem un problème »)
  gets a COVER (gaze_cover.py finds exactly that one).
