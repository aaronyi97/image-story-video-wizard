# Codex and WorkBuddy host routing

Do not route by product name alone. Route by verified capability in the current session.

## Capability check

At START, determine whether the host can currently:

- read and write the chosen local project folder;
- package and open attachments;
- route to the requested writing model;
- use a logged-in browser within the authorized boundary;
- call the configured TTS service without exposing secrets;
- generate or inspect images;
- run HyperFrames or another confirmed assembly tool;
- render a local video.

Record the result in `PROJECT_STATE.json`. `Logged in` is not proof of the correct account, and an installed tool is not proof it is authorized for this project.

## Codex route

Use Codex as the continuous host when local files, required tools, and render capability are available. It may own the state file, produce project artifacts, coordinate writing-model handoffs, inspect images, build the HyperFrames project, and render after the preview gate.

If a required external model or service is unavailable, do not substitute silently. Create a bounded user action or handoff package.

## WorkBuddy route

WorkBuddy may own early stages when it can analyze benchmarks, build or consume a writing pack, and use Kimi K3. For the tutorial route, select Kimi K3, turn on Max mode, choose the strongest available thinking setting such as `超高`, and use the 1M context window when those controls are actually visible. Confirm the selected model, mode, thinking strength, and context window before claiming Kimi K3 participated; if the product labels or available options have changed, state the nearest verified substitute instead of pretending the original setting is still available.

If WorkBuddy has verified local file and render capabilities, it may continue. Otherwise stop after the last supported stage and create `HANDOFF.md` plus all referenced artifacts for Codex. Tell the user exactly:

- what WorkBuddy completed;
- what remains unconfirmed;
- which folder or archive to give Codex;
- what Codex should do first;
- which gate must be presented to the user next.

## Handoff rules

Use `assets/handoff-template.md`. A handoff is valid only when artifact paths resolve or files are included, current stage/status are explicit, and the pending user request is preserved.

Do not call a handoff complete merely because a summary was written. Validate the state and package contents.
