# 7 · App Demo (Claude UI)  — "watch the AI do it"

Preview: `previews/07-app-demo.jpg`. Reference reels: DfnvsSwMsTk (Claude desktop on cyan curtain, "OPUS 5.5 JUST DID IT"),
DfnK5SBtupw (desktop app, "CLAUDE DID THIS"), DffgwLZD3Gh / Dff405ZEynK / DffsyTYj9Pi (Claude chat card), DfZnxlXtzO_ (chat "Here is your reel ✓"),
DfUkTLOt_82 (Claude search bar + chips), DfmHCwID7n3 / Dfe8r86DxTk (terminal + chrome), DfUPOTmthsX (prompt panel + result + "Step 4 of 8").

## Look
A faithful dark **Claude app UI** floating on a **vertical curtain** of glowing stripes, with a chrome headline on top.
The UI types the prompt, "thinks", ticks a checklist, then the finished vertical video plays inside the chat. Proof-by-demo.

## Backgrounds
- **Cyan curtain**: vertical stripes 22–30 px, `#04121a` → `#0d5466` → `#38c6e0` highlights with a bright vertical light band that drifts sideways; deep black edges.
- **Violet/blue curtain**: same with `#1a1240 → #4a3aa8 → #8a7cff` (DffUrynD-Sp "ALL OF IT").
- **Grey curtain**: `#1a1c1e → #6f7477` (DfhteR9D2xG "EDITS VIDEOS NOW").

## UI pieces (dark mode, faithful)
- **Desktop window** 1000×1180, radius 22, `#262624` body, `#1f1e1d` sidebar 190 px (✻ Claude, New chat, Search, Chats, Projects, Artifacts, Code; Recents list),
  title bar with traffic lights, project name ("Cap guy reel", "My funnel reel").
- **Attachments row**: video thumbnail + "brief.md · Markdown · 2 KB" + "video-editing.skill" cards (`#30302e`, radius 12).
- **User message**: Inter 400 22 px `#e8e6e1`, the real prompt (e.g. "Edit raw.mp4 with my video-editing skill and brief.md. Behind his head, a big silver word on each thought…").
- "✻ Thought for 14s ›" (muted) → "✻ Done. Here is your reel." 
- **Result**: vertical video player 360×640 inside the chat ("FINAL · CLAUDE") + right column checklist with **orange dot bullets** filling in one by one:
  "Cut the pauses", "Word behind the head", "Waves + gauge", "Icon cards on words", "Plates by his head", "Captions on words";
  file card "final.mp4 · 1080×1920 · 30 fps · 10 s" + orange **Download** button → "✓ Saved".
- Reply box at the bottom ("Reply to Claude…", model chip "Opus 5.5", orange send).
- **Chat-card variant** (compact): "Claude · Edit my reel" header, user card with raw.mp4 thumbnail + "✻ motion-story" chip + "Edit this in my style.",
  "✻ Here is your reel ✓", reel.mp4 card + checklist "✓ Cut the pauses · ✓ Room graded · ✓ Word behind the head · ✓ Captions on words · ✓ Glass ribbon · ✓ Sound" + Download.
- **Terminal variant**: see style 5 (Claude Code), JetBrains Mono, orange ✻, green "Done".

## Motion
Window rises with a 6° tilt → 0 (14 f). Typing 2 chars/frame, caret blink 15 f. "Thinking" shimmer on the text (gradient sweep). Checklist ticks every 8 f (blip).
Video fades in, plays. Download button: hover → click (cursor glides, click sound) → "Saved". Slow camera push 1.00→1.06 on the whole UI.

## Sound
Keys, soft UI ticks, click, a positive chime on "Done", the result video's audio once it plays. Music optional (low ambient).

## Use it for
Any "AI did my work" story: his Claude workflows, n8n automations (swap the UI for n8n's canvas, same logic), DevOps tools.

## Voice & music (measured on the references)
No narrator: the result video's own voice plays once it appears; ≈1.8 hits/s (keys, ticks, whooshes).

## Opening (measured at 10 fps on 5 wrappers: W06, W10, C09, D08, L06)
**There is no intro build.** Frame 0 already shows the full layout: comment bubble, tag, chrome headline + subline, both phones, prompt
bar. The first frame IS the cover (feed thumbnail) — it must read instantly. Only these move: the AFTER clip plays from its first beat
(already mid-sentence), the BEFORE clip plays raw, the CTA pill fades in at 0.4–0.7 s, a carousel keeps turning. Ignore my older
"0–1 s build-up" timings in this file: build-ups lose the scroll.
