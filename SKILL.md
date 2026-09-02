---
name: image-story-video-wizard
description: Use when a user wants step-by-step help making an audio-first image-story, AI narration, slideshow, illustrated story, AI 讲书, 图片联播, 有声故事, or 静态图叙事视频 with Codex or WorkBuddy; not for a standalone script, single image, or ordinary video editing.
---

# Image Story Video Wizard

Own the process. The user supplies the current decision or material; the Skill decides what must happen next, explains it, performs everything it can, and stops at the next confirmation gate.

## Guided interaction contract

Never dump the whole workflow and ask the user to drive it. At every turn, say:

1. `现在进行到：` current stage and purpose.
2. `我现在会做：` the action the Skill will take.
3. `你现在只需要：` one to three current inputs or decisions.
4. `完成后我会交付：` the concrete artifact or preview.
5. `确认后下一步：` the next stage, without starting it early.

Ask only what blocks the current stage. Do not ask the user to choose the next workflow step. Avoid generic questions such as “接下来想做什么？” Instead state the next step and request its minimum input.

Use these stage statuses exactly: `未开始`, `进行中`, `待确认`, `已确认`, `需要返工`, `已跳过`. A reply such as “继续” or “可以” approves only the current gate, not all later gates.

## Start or resume

On first use, detect whether this is a new project or a resumed one. Look for `PROJECT_STATE.json` in the supplied project folder. If none exists, initialize one with `scripts/project_state.py init`. If a state file exists, validate it, summarize the latest confirmed artifact, and resume at `pending_request`; do not restart from the beginning.

At stage 0, identify the actual host and capabilities. Read [references/host-routing.md](references/host-routing.md) when choosing between Codex, WorkBuddy, or a handoff. Never claim a host can access local files, call a model, use a logged-in browser, synthesize audio, or render unless that capability is available now.

Read [references/workflow.md](references/workflow.md) before starting a project and whenever entering a new stage. Read [references/state-schema.md](references/state-schema.md) before creating or changing project state.

## Stage order and hard gates

Follow this state machine:

`START → BRIEF → BENCHMARKS → WRITING_PACK → SCRIPT → VOICE → STORYBOARD → VISUAL_STYLE → CHARACTER_ANCHORS → IMAGE_PROMPTS → IMAGE_GENERATION → ASSET_QC → MUSIC → PREVIEW → FINAL_RENDER → FEEDBACK`

Hard gates:

- Do not generate a writing pack before product direction and benchmark roles are confirmed.
- Do not synthesize full narration before the final script is confirmed.
- Do not write the complete image-prompt manifest before image cadence and visual style are confirmed.
- Do not batch-generate images before a three-to-five-image pilot and any required character anchors are confirmed.
- Do not render a final video before the user accepts the preview.
- Do not publish, upload, post, or change a live channel unless the user separately authorizes that action.

If a gate fails, mark `需要返工`, return only to the earliest affected stage, and preserve later artifacts as untrusted rather than deleting them.

## Production invariants

### Script

- Learn a benchmark's topic logic, structure, pace, hooks, transitions, and audience need; never copy its original wording or finished assets.
- Build a self-contained writing pack. Prefer complete benchmark samples over adjective-only style instructions.
- Require one complete first draft. If it is too short or hollow, repair the writing pack and start a fresh writing conversation; do not ask the writer model to pad the same draft.
- After draft generation, use one focused repair pass. Large rewrites require a clear reason and user confirmation.

### Voice

- Ask whether TTS credentials are locally configured; never ask the user to paste a secret into chat. If absent, guide local secret storage and verify only availability.
- Compare five to ten voices with the same approximately twenty-second sample. Confirm voice first, then test speaking rate.
- Prefer narration output with sentence- or word-level timestamps when available.

### Storyboard and images

- Calculate image count from narration duration. A dynamic 6–8 second cadence means about 75–100 images per ten minutes; an economical 10–12 second cadence means about 50–60.
- Lock image style and text treatment with a three-to-five-image pilot before producing the full prompt manifest.
- Detect recurring characters. When identity continuity matters, confirm face and full-body anchors before batch generation.
- In manual mode, guide a pilot first, then batches. Do not dump dozens of prompts in the first image turn.
- Keep prompt IDs, storyboard IDs, generated filenames, and narration ranges aligned.

### Assembly and review

- Prefer HyperFrames for programmable assembly when available, but follow the confirmed project format and host capability.
- When actual assembly or rendering begins in an environment that provides the HyperFrames skills, load the `hyperframes` mandatory entry point and follow the routed core, media, animation, audio, and CLI instructions that apply to the confirmed project.
- Align images, subtitles, text cards, and optional music to narration timing.
- Produce a reviewable preview before final render. Machine checks do not replace visual inspection and one full human watch.
- Keep delivery status `已做待验` until the user accepts the final master.

## Secrets and external actions

Do not store API keys, session URLs, redemption codes, cookies, or tokens in prompts, project files, logs, screenshots, or repositories. Ask whether access is configured, not for the plaintext secret.

Model calls that spend money, browser actions using logged-in sessions, final rendering, uploads, and publishing must stay within the user's current authorization. Explain cost or account impact before the action when material.

## Project artifacts

Use stable filenames so the project can resume across hosts:

- `PROJECT_STATE.json`
- `BRIEF.md`
- `BENCHMARKS.md`
- `writing-pack/`
- `SCRIPT.md`
- `audio/`
- `STORYBOARD.csv`
- `VISUAL_STYLE.md`
- `characters/`
- `IMAGE_PROMPTS.md`
- `images/`
- `review/`
- `renders/`
- `HANDOFF.md` when another host must continue

Use the templates in `assets/` when creating these artifacts. Validate `PROJECT_STATE.json` before claiming a stage is complete.

## Completion

Completion means the confirmed master and its resumable project files exist and pass the proportional checks in the workflow. Report the current state as `未做`, `已做待验`, or `已验收`. Do not call a workflow “automated” merely because one sample rendered; record manual intervention and real production time after several episodes.
