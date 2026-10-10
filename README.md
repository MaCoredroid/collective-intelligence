# Collective Intelligence: Preliminary Results

Preliminary results toward on-policy team RL for LLM agents:

1. **The mechanics emerge untrained; the judgment doesn't.** An untrained team forked in 15 of 116 trials, almost all on tasks that split by module, rebuilt a lead-and-workers tree, and gained about nothing over solo.
2. **Single collaboration decisions carry a large, measurable signal.** Re-running one frozen fork decision gave 0.009 / 0.005 / 0.716, so decision-level credit for team RL is feasible.
3. **The RL stack learns the task.** Solo GRPO on Qwen3.5-9B: FrontierCS 6.22 → 11.48 by step 40 (paired +5.26 [+3.50, +7.30]).
4. **The harness is a first-order variable.** The same recipe inside a general coding harness learned nothing in 10 steps.

No team has been trained yet.

**→ Read the essay: [macoredroid.github.io/collective-intelligence](https://macoredroid.github.io/collective-intelligence/)**

The page is a single static file in [`docs/index.html`](docs/index.html), served by GitHub Pages from `/docs`.
