# The Harness Is Part of the Model

*Collective intelligence, part 1.* Lessons from the groundwork before training a team of LLM agents:

1. **Untrained, the harness mode doesn't matter.** On up to 96 tasks, Qwen3.8-27B solo, with built-in subagents, in team mode, and in three versions of a collective harness are all within noise (one attempt per task). Collaboration appears only where the work splits by module.
2. **Single-call GRPO nearly doubled FrontierCS.** Qwen3.5-9B went from 6.22 to 12.22 on 172 problems by step 70 (paired +6.00 [+4.00, +8.33]), then flattened.
3. **Trained as an agent in a general coding harness, the same model showed no sign of learning by step 10**, thinking a median of 27 tokens per call.
4. **Agentic RL used about 8× the GPU-hours per step; only ~1.4× of that is extra work.** The rest is idle or underfilled GPUs. Problem → fix → effect tables cover serving, rollout/training, and evaluation.
5. **The dangerous failures are silent.**

No team has been trained yet.

**→ Read the essay: [macoredroid.github.io/collective-intelligence](https://macoredroid.github.io/collective-intelligence/)**

The page is a single static file in [`docs/index.html`](docs/index.html), served by GitHub Pages from `/docs`. A 97-second narrated summary is embedded on the page ([MP4](docs/media/the-harness-is-part-of-the-model.mp4)); its Manim source and narration script are in [`video/`](video/). Narration voice: ElevenLabs.

## The series

- [Part 1 · The Harness Is Part of the Model](https://macoredroid.github.io/collective-intelligence/)
- [Part 2 · The Wall, the Compile Tax, and the Oracle](https://macoredroid.github.io/collective-intelligence/part-2/)
- [Part 3 · Climbing From Zero Without a Teacher](https://macoredroid.github.io/collective-intelligence/part-3/)
- [Part 4 · Borrowing a Foothold: Distilling Simulated Annealing into a 9B Agent](https://macoredroid.github.io/collective-intelligence/part-4/)
