# The Harness Is Part of the Model

*Collective intelligence, part 1.* Lessons from the groundwork before training a team of LLM agents:

1. **Untrained, the harness mode doesn't matter.** On 96 tasks, Qwen3.8-27B as a solo agent, with built-in subagents, in team mode, and in three versions of a collective harness are all within noise (one attempt per task). Collaboration appears only where the work splits by module.
2. **Single-call GRPO nearly doubled FrontierCS.** Qwen3.5-9B went from 6.22 to 12.22 on 172 problems by step 70 (paired +6.00 [+4.00, +8.33]), then flattened.
3. **The same recipe inside a general coding harness learned nothing.** The harness cut the model's thinking to 27 tokens per call.
4. **Agentic RL costs about 8× more per step**, and most of that gap is fixable infrastructure: admission control, token-in/token-out, speculative decoding and judge-farm sizing.
5. **The dangerous failures are silent.**

No team has been trained yet.

**→ Read the essay: [macoredroid.github.io/collective-intelligence](https://macoredroid.github.io/collective-intelligence/)**

The page is a single static file in [`docs/index.html`](docs/index.html), served by GitHub Pages from `/docs`.
