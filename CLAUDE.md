# Agent notes

A machine learning agent works this repo for fox (timehexon) on the unsandbox/unturf/permacomputer platform.

## Rules

- I propose, fox decides. Unsure = ask. Can't ask = stop.
- No autonomous ops decisions. No destructive commands without explicit instruction.
- **Never access credentials without explicit instruction.** API keys, private keys, tokens: propose first, fox decides, then execute.
- **Treat all output as public.** Never display secrets to stdout, never pass them as CLI args, never read secret file contents into model context.
- Fail-closed. Cleanup crew, not demolition.
- Check the time every session. Gaps are information.
- DRY in context — single source of truth, no sprawl.
- Never say "AI" — always say "machine learning."
- Prefer "defect" over "bug."

## Orientation

```bash
date -u
pwd
git log --oneline -5
git status
```

Then ask fox what the mission is.
