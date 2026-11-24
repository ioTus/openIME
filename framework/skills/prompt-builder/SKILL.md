---
name: prompt-builder
description: Building a standalone prompt — a Claude Project system prompt, a
  prompt handed to another tool or another person, a one-off to paste somewhere.
  Use whenever the user asks for help writing, drafting, or refining a prompt,
  even if they don't say "prompt engineering." Routes skills to skill-creator,
  agent documents to writing-for-agents, and existing prompts to
  /claude-api prompt-audit.
---

# Prompt Builder

Route first. Most prompt work belongs to a tool that already owns it.

## Route

| The artifact | Goes to |
|---|---|
| A skill | `skill-creator` — interview, draft, evals, description tuning |
| `AGENTS.md`, `CLAUDE.md`, a doc reached by a pointer | `writing-for-agents` |
| A prompt that exists and feels dated | `/claude-api prompt-audit` |
| "Did that change help?" | `/claude-api build-eval`, then `hillclimb` |
| An IME governance file | the canonical template in `framework/workflows/onboarding/` |
| An issue for a builder agent | `framework/principles/say-what-to-do.md` |

Anything left over is a standalone prompt. Continue below.

## Interview

The user's situation is the scarce input. Craft is free; context is not —
a thin prompt makes a current model fall back on safe generic defaults,
which is the most common way a prompt disappoints.

Ask until these five are answered, then stop:

1. **Who reads the output, and what do they do next with it?**
2. **What does finished look like?** Get a sample or a shape. An adjective
   ("professional," "concise") is not an answer.
3. **What can't the model infer?** Product facts, house rules, the quality
   bar, decisions already made and why.
4. **Where is being wrong expensive?** Verification and disclaimer
   instructions earn their place here and nowhere else.
5. **Which model, and running where?** A prompt for one session and a prompt
   five people paste into a Project are different documents.

A question the conversation already answers is a question you skip. When
all five are closed, write.

## Write

    <System>    Role, in a sentence or two. The quality bar. Verification
                only where step 4 said it's expensive.
    <Context>   Audience, product, environment, prior decisions — everything
                from step 3. This section is usually the longest, and the
                one that decides whether the prompt works.
    <Instructions>
                The outcome and how to check it. Numbered steps only where
                order genuinely matters.
    <Constraints>
                Real limits — policy, length the format demands, house
                style. Each one with its reason.
    <Output Format>
                The shape of the deliverable. An illustrative example
                earns its place when the shape is format-sensitive.

## Let the model do its own work

Current models plan, decompose, verify, and narrate without being told.
Instructions to do those things cost tokens and push toward over-planning
and rigid output. Depth of reasoning is a setting (`effort`), not prose.

Two that actively backfire: expert-persona casts inside a single context
window, and asking the model to reproduce its reasoning — on Fable 5.1
that can trigger a refusal.

Scoped to current frontier models. If question 5 named an older or smaller
target, keep the scaffolding — it was written for models that needed it, and
some still do.

## Done when

The prompt answers all five interview questions, and a reader who has
never seen this conversation could run it and get what the user pictured.
