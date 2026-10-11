# The Harness Is Part of the Model (short film)

## Overview
- **Topic**: What the groundwork for agent-team RL actually showed
- **Hook**: "Can one model learn to work as a team?" Then the twist: before a team can learn anything, the harness decides more than the agents do.
- **Target audience**: ML researchers and engineers
- **Length**: narrated with an AI-generated voice (OpenAI TTS "ash" for part 2; ElevenLabs "George" for part 1)
- **Key insight**: what the model is shown (a clock, a file instead of a question, its own tokens) moved results more than teammates did. So the harness is part of the model.

## Narrative arc
Pose the team question with a single dot that splits into many. Show that untrained teammates collapse back onto the solo line. Show RL working in the simplest setting, then failing inside a harness for a reason you can see (thinking shrinks). Show that the expensive part is infrastructure, and that the dangerous part is silent. Resolve on the title line.

---

## Scene 1: The question (≈9 s)
**Purpose**: open quietly and set the question.
- One clay dot at centre. It forks into 5 dots connected by thin slate lines (a small team graph), which breathe slightly.
- Text fades in above: *Can one model learn to work as a team?* (serif, italic)
- Below in small mono: "collective intelligence · part 1"

## Scene 2: Teammates didn't help (≈14 s)
**Purpose**: Result 1.
- The team graph collapses into a horizontal axis with a single vertical clay line labelled "solo".
- Six short slate bars per family (subagents, team, collective…) rise around the line and settle near it. Use one compact row of 6 families; family names in small mono.
- Caption: "Untrained, every harness arm landed within noise of solo."
- Second caption replaces it: "Collaboration appeared only where the work split. A visible clock changed behaviour more than teammates did."

## Scene 3: RL works when the setting is simple (≈14 s)
**Purpose**: Result 2.
- Axes: training step 0–80, score 0–16. Curve draws through 6.22, 7.42, 8.82, 11.48, 11.85, 12.22, in clay, with a faint CI band.
- Number ticker: 6.22 → 12.22.
- Caption: "Single-call GRPO, 9B model: FrontierCS 6.22 → 12.22." Then a small line: "+6.00 [4.00, 8.33] paired · flattening after step 40."

## Scene 4: The same recipe inside a harness (≈14 s)
**Purpose**: Result 3, the turn.
- Two horizontal bars on a log scale: "thinking per call". Single call ≈ 30,000 tokens is a long clay bar. In the harness, 27 tokens is a sliver.
- Caption: "Same model, same recipe, inside a general coding harness: no gain (−0.02 at step 10)."
- Then: "Inside the harness, it thought 27 tokens per call."

## Scene 5: The cost is infrastructure (≈14 s)
**Purpose**: Result 4.
- Two stacked GPU-hour blocks: single call 1.2 vs agentic 9.3, captioned "≈ 8× per step".
- Three lever chips slide in, each with its number:
  - admission control ≈ 10×
  - token-in / token-out: 2.71× → 1.05× trained tokens
  - speculative decoding 1.9×
- Caption: "Most of the gap was fixable."

## Scene 6: Silent failures (≈8 s)
**Purpose**: Result 5.
- A small "judge" box outputs a green-ish ✓ that is actually wrong: the score flips to 0 with no error mark. A clay "canary" dot pulses beside it and catches it.
- Caption: "The dangerous failures were silent. Canaries caught them."

## Scene 7: Resolution (≈8 s)
- Everything fades. The title draws in serif: **The harness is part of the model.**
- Small mono line beneath: "collective intelligence · part 1 · preliminary results"

---

## Transitions & flow
- Recurring motif: the clay dot (the model). It splits into a team (S1), becomes the solo reference line (S2), rides the learning curve (S3), and becomes the canary (S6).
- Cross-fades only; no flashy transforms. 0.6–1.0 s fades, 1.5–2.5 s holds after each caption.

## Color palette
- Background: ivory `#F4F1EA`
- Ink: slate `#1F2328`; secondary ink `#5B6168`; rules `#D9D4C7`
- Accent: clay `#C8643B` (the model, the key number)
- Neutral data: `#9AA0A6`

## Typography
- Serif titles and captions: Charter
- Numbers and labels: Menlo

## Mathematical content
None beyond numbers. Use `Text` (Pango), not `MathTex`.

## Implementation order
One `Scene` class with sub-methods per scene (simpler timing and continuity), rendered at 1080p30 with `-qh`.
