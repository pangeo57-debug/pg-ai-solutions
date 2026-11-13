# PG AI Solutions: design system

**Direction: "Από το χάος, η βέλτιστη λύση" (From chaos, the optimal solution).**
A dark, quiet site that shows it knows AI and algorithms by what it *does*, not by what it claims.
The hero runs a real 2-opt solver on screen. The stops start out scattered, the solver arranges them into the PG monogram,
and then they settle into a day's optimal route. Everything else stays calm so that moment carries the page.

We do **not** sell AI agents. AI is how we build, so it shows in how the site behaves: live computation,
text that types itself, numbers that converge. It does not show up as chatbots or stock photos.

Chosen from three rounds of directions (see `.inhabited/sampling.md`, which is local and ignored by git). No UXKIN reference sites were used,
because the connection failed. The decisions come from the existing brand (PG monogram, sky→pink route) and the owner's feedback:
no "neighbourhood shop" photography, keep the logo and colours, keep the route animation, and make the AI feel native.

Code tokens live in `assets/site.css` `:root`. Pages use the names, never raw values.

---

## Color (dark only)

There is one theme on purpose: the route glow only works on a dark ground. `theme-color` is `#06080F`.

| Token | Value | Role |
|---|---|---|
| `--bg` | `#06080F` | Page background |
| `--bg2` | `#0B0F1B` | Raised surfaces: cards, form, prompt box, HUD |
| `--bg3` | `#111727` | Hover on surfaces, inputs |
| `--line` | `#1A2031` | Hairlines, card borders |
| `--line2` | `#2A3247` | Stronger borders (inputs, language switch) |
| `--ink` | `#EEF1F7` | Headings and body text (17.8:1 on `--bg`) |
| `--mute` | `#9AA3B8` | Secondary text and labels (7.9:1) |
| `--sky` | `#0593C6` | Brand blue: logo, route start, focus ring |
| `--sky-ink` | `#3FB8EA` | Blue for *text* on dark: links, numbers, eyebrow (8.6:1) |
| `--pink` | `#D83995` | Brand pink: route end, live markers |
| `--pink-ink` | `#EE6DB5` | Pink for *text* on dark: section numbers, error notes (6.9:1) |
| `--ok` | `#2FD27A` | "Live" dot, success state |
| `--grad` | `#0593C6 → #D83995` | **The route.** Logo, solver lines, progress bars, one emphasised phrase per heading (`<em>`) |
| `--grad-text` | `#3FB8EA → #EE6DB5` | The same gradient lifted for legibility when used on text |

Rules:
- The gradient is the brand route, not decoration. Use at most one gradient element per viewport besides the hero canvas.
- Primary action = white button (`--ink` background, `--bg` text). It is the brightest thing after the route.
- No glassmorphism and no coloured section backgrounds. Depth comes from `--bg2` surfaces and hairlines only.

## Typography

| Token | Value |
|---|---|
| `--font` | **Manrope** 400–800, variable, self-hosted (`manrope-latin-var`, `manrope-greek-var`). Covers headings and body in both languages. |
| `--mono` | `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`. Used for labels, the HUD, the typed prompt and step numbers. |

| Style | Size / line-height | Weight | Tracking |
|---|---|---|---|
| `.h1` | `clamp(2.9rem, 6.6vw, 5.8rem)` / 1.0 | 800 | −0.045em |
| `.h2` | `clamp(2rem, 4.2vw, 3.5rem)` / 1.05 | 800 | −0.035em |
| `.h3` | `clamp(1.25rem, 1.8vw, 1.5rem)` / 1.2 | 700 | −0.02em |
| `.lead` | `clamp(1.05rem, 1.4vw, 1.2rem)` / 1.6 | 400 | 0 |
| body | 17px / 1.65 | 400 | 0 |
| small | 14–15px / 1.5 | 400–500 | 0 |
| label (mono) | 12px / 1.4, uppercase | 500 | 0.08em |

Body text is never below 16px in inputs, and lines are capped at about 60ch (`.lead { max-width: 56ch }`).

## Spacing and layout

- 4px base scale: `4 8 12 16 20 24 32 48 64 96 128`.
- Content width `--max: 1200px`, side gutter `20px` (plus the safe area on iOS).
- Section rhythm: `--sec: clamp(88px, 11vw, 140px)` top and bottom, and `64px` on mobile.
- Headings are left-aligned. Nothing is centred except single buttons inside cards.

## Shape and depth

| Token | Value | Use |
|---|---|---|
| `--r-s` | 10px | Inputs, tags, language switch |
| `--r` | 12px | Buttons |
| `--r-l` | 18px | Cards, prompt box, project shots, form |
| pill | 999px | Prompt chips |

There are no drop shadows. The only shadow-like effect is the route's own blurred glow on the hero canvas.

## Motion

| Token | Value | Use |
|---|---|---|
| `--ease-out` | `cubic-bezier(.23,1,.32,1)` | Every entrance, press and reveal |
| `--ease-io` | `cubic-bezier(.77,0,.175,1)` | On-screen movement: stops travelling, clip-path reveals |

1. **Hero sequence** (once per load, about 6s): stops ease in from random points (1s, ease-out). A greedy tour is drawn, then 2-opt improves it **one move per frame**, which makes it legible. The tour reaches the PG monogram, glows and holds for 2.6s. The stops then move (1.3s, ease-in-out) to a day's random stops, are solved again, and **rest on the route**: no loop, and a soft light keeps travelling along it. The HUD counts stops, iterations and km, with a gradient progress bar.
2. **Headline**: the words appear from `blur(10px)`, `translateY(12px)`, opacity 0 over 900ms ease-out, with a 70ms stagger. The lead text and buttons fade up 8px after it.
3. **Prompt box** (on scroll into view): the request types itself at about 22ms per character, then the chips stagger in 60ms apart and the plan lines follow 180ms apart.
4. **Cards** (`.rv`): reveal with `clip-path: inset(0 0 100% 0)` → `inset(0)`, 900ms ease-in-out, staggered 70ms by column. Counters (`data-count`) count up over 1.2s.
5. **Press**: `.btn:active { transform: scale(.97) }` over 160ms. Hover effects only under `(hover:hover) and (pointer:fine)`.
6. **Reduced motion**: no travel, blur or clip. Text and cards fade only, and the hero shows the PG frame and then the finished route straight away.

Only `transform`, `opacity`, `filter` (on the headline only) and `clip-path` are animated. The canvas pauses when it is off-screen.

## Components

- **Header**: sticky, `--bg` at 80% with a 12px blur and a hairline below. Logo (the PG mark) and wordmark on the left. Nav in `--mute`, with a 1px gradient underline for the current page. The language switch is a mono pill.
- **Buttons**:
  - `.btn` is primary: white, 12px radius, Manrope 700 at 15px, with an arrow that moves 4px on hover.
  - `.btn.line` is secondary: transparent with a `--line2` border, which brightens to `--ink` on hover.
  - `.txtlink` is quiet: `--mute` with an underline that turns pink on hover.
  - Every button and link has a 2px `--sky` focus ring, offset 3px. Disabled buttons sit at 50% opacity.
- **Eyebrow**: 12px mono uppercase in `--sky-ink`. The hero eyebrow adds a pulsing `--ok` dot.
- **Cards** (`.scard`, `.wcard`, bento): `--bg2`, a 1px `--line` border and 18px radius. On hover the border becomes `--line2` and the background `--bg3`.
- **HUD**: mono 12px on `--bg2` at 85% with a hairline border. It holds the value columns and a 3px gradient progress bar.
- **Prompt box**: a `--bg2` panel with mono typed text and a pink caret, pill chips and a plan list.
- **Steps**: four columns with a 2px gradient rule on top, mono numbers in `--pink-ink` and hairline dividers.
- **Forms**: `--bg3` inputs with a `--line2` border that turns `--sky` on focus. Labels are mono. The project/partnership radio is a segmented control, with the selected option in white.
- **Footer**: a hairline above it and `--mute` text that turns `--ink` on hover.

## Imagery and icons

- **No stock photography.** The visuals are the live solver and real screenshots of our own projects (`assets/work/*.webp`), shown in `--bg2` frames.
- Icons are text arrows (→, ↗) only. No emoji and no icon font.
- The PG monogram (`logo/pg-mark.svg`) is the only logo artwork. Its path is also the hero's target shape.

## Do not

Do not use purple-to-blue gradients, glass cards, centred hero layouts, three identical feature cards with icons on top, stock photos of "business owners", chatbot mock-ups, or gradient text on more than one phrase per heading.
