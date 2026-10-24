# Nordic Blue: geometry and functional gate (TASK-014)

From `D:\Projects\Extjs7ClassicThemeUpgradeNordicBlue`:

```powershell
& 'C:\Users\Damned\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' tools/nordic-blue-regression/run.py --output artifacts/nordic-blue/regression-new-run
```

Prerequisites: the local Theme Lab server is running; the Nordic testing build exists and is current. This command does not build or start a server. Optional `--url http://127.0.0.1:PORT/theme-lab/` must include the Theme Lab directory. Optional `--node PATH` selects Node 24. Drivers use the installed bundled Playwright and Edge. All project/baseline paths intentionally refer to this Windows project. See AGENTS.md for Sencha Cmd commands and Java environment. Run builds sequentially before the gate when theme sources change.

Output must be a **new directory**. Existing output is rejected; the runner never updates TASK-006, masters, approvals or application/theme sources. It copies its executable sources and frozen frame resources into each run for reproducibility. A missing file, unexpected scenario/action count, duplicate ID, missing element, state/value mismatch, geometry/typography delta, script/network error or nonzero child exit fails the command. `execution.json` and step logs identify failures; `run-status.json` is authoritative completion status. A failed/partial directory is diagnostic evidence, not an accepted run; rerun into another fresh directory after fixing the cause.

## Coverage

- 102 fixture cases/states at each DPR 1 and 2 against the immutable TASK-006 Classic baseline.
- Genuine paired mouse/keyboard checkpoints for forms (24), grid/tree/paging (23), secondary controls (29), core button states (28), window (14) **per theme and DPR**. Plus five core flows per theme/DPR: button menus, Space, toolbar overflow and panel collapse/expand.
- Window header drag inside the constrained host, southeast resize, close tool, Escape, eight forward Tabs, reverse Tab and modal Escape. The drag moves upward by 30 px to avoid the existing Classic bottom constraint. No fixture configuration is changed.
- Twelve resize/move icon adapter state/hit-area/click-dispatch checks. All native icon bounds, offsets and pseudo metrics also participate in full case/action comparisons.
- Real temporary browser controls: +1 px translation and +1 px font size at both DPRs; compare rejects mutations and passes after exact restoration. Five synthetic structural controls per DPR verify missing/count/state/duplicate/empty failures.

## Comparison contract

`extract.js` retains stable semantic IDs, complete captured typography/box model, bounds, transforms, icon and pseudo metadata, focus, data/stores, scroll and state. `metrics.py` compares exactly with no pixel tolerance. Only explicit paint-color properties, colors inside shadows and reviewed gradient-only paint layers are omitted. Shadow geometry, opacity, fonts and dimensions remain exact.

`icon-contracts.py` reads the **active** manifest from config/nordic-blue-icons.json. Each substituted resource must match its approved parent, density and CSS sheet size. Only approved resize/move y-offset adapters map to Classic. Never normalize arbitrary image paths, dimensions or offsets.

Animated GIF captures use declared first composited frames for reproducibility. Source GIF and derived PNG hashes are checked before the run. Nordic substitutions come from the actual approved/built Nordic GIF, never Classic artwork. Runtime GIFs remain intact. This gate checks metrics and behavior; screenshot pixel acceptance is TASK-015, release build/integration matrix TASK-016, delivery TASK-017.

## Results

`regression-results.json`, `review.html`, `icon-contract-observations.json`, `adapter-validation.json`, `negative-controls/`, source guards, raw JSON/PNG captures, execution commands/exit codes and step logs. No final release readiness is implied by PASS.

Sources consolidate the reviewed TASK-009–013 drivers and REV-001 v3 contract binding; previous artifacts stay immutable. Python uses only its standard library. Node drivers use Playwright; browser version is written in capture/action indexes.
