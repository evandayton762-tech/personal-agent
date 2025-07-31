# Cost Management Rules

The agent minimizes cost by controlling language model usage and third‑party expenses. The following rules apply:

1. **Prefer recipes and deterministic tools**: Use pre‑defined recipes and deterministic tool adapters whenever possible to avoid additional language model calls. Only call the language model when necessary for planning, summarization, or dynamic reasoning.

2. **Single validation pass**: Perform only one validation pass per step. Avoid extended internal dialogue or multiple reasoning rounds that consume extra tokens.

3. **Semantic cache**: Reuse prior answers for identical prompts and previously executed recipe flows. The agent should maintain a cache keyed on prompt and context so that repeated tasks don’t require new model calls.

4. **Tripwires**: When cumulative token usage reaches 80% of the per‑task or daily limit, the agent warns the user or itself. At 90%, the agent halts enqueueing new steps and splits remaining work into the next available window.

5. **Conservative defaults**: Start with conservative token caps (e.g., 8k per task, 25k per day) and adjust upward only with explicit user approval.
