# Nordic Blue visual gate — TASK-015

From `D:\Projects\Extjs7ClassicThemeUpgradeNordicBlue`:

```powershell
& 'C:\Users\Damned\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' tools/nordic-blue-visual/run.py --output artifacts/nordic-blue/visual-new-run
```

Needs the running Theme Lab server and a current **testing** build. Run the documented Sencha Cmd build first after theme changes; this gate does not build. Optional `--url http://127.0.0.1:PORT/theme-lab/` and `--node PATH`. Python dependencies: Pillow, NumPy; bundled Node 24, Playwright and installed Edge. Use a fresh output directory; the runner rejects any existing directory and never updates a golden or earlier evidence. All project paths intentionally refer to this Windows project.

## Three independent checks

1. **Geometry:** the TASK-014 comparator and exact approved icon contracts compare Classic/Nordic per DPR, plus before/after normalization. No geometry/typography tolerance.
2. **Structure:** normalize paint in the browser, preserving every URL image layer, its size, repeat and offset. Compare exact RGB pixels outside the frozen support of approved artwork. Missing cases, DOM correspondence mismatch, escaped support pixels and any unmasked pixel change fail.
3. **Nordic artwork and appearance:** exact raw/normalized Nordic snapshots, frozen support masks and decoded frames from **all 648 approved runtime files**. An image defect inside an excluded structural region still fails its own golden comparison. Check encoded resource SHA as well as decoded frame pixels. No unreviewed artwork is accepted by refreshing the baseline.

Goldens are bound by `config/nordic-blue-visual.json`. Their manifest records the active v3 approval/manifest hashes, browser/SDK and every snapshot/frame hash. Initial `golden-v1` is a technical baseline of the checked implementation, **not a claim of final user approval or completed release acceptance**. User approval of v2 plus the folder v3 revision authorizes the icon artwork represented here.

## Capture and normalization

- Edge, software raster, sRGB, 1280×1600, DPR1/2 separately, en-US, Europe/Minsk; wait for Theme Lab readiness, fonts/data/layout and actual requested pointer state. Source GIF and frame0 PNG hashes must match. Use actual Nordic GIF frames; never substitute Classic art into Nordic.
- Raw captures retain real theme paint. Capture clipping removes only the laboratory header above `#lab-stage`, preserving all component/floating content below it; it is not a component mask. The overview includes the full stage.
- For normalization, match the complete body tree and iframe bodies by recorded traversal key/tag, alongside stable semantic geometry IDs. Canonical paint uses Classic's transparent/solid decisions on both themes. Neutralize explicit colors/shadow colors; remove only gradient layers from the comma-separated background-image list. **Keep URL layers.** Do not change fonts, geometry, opacity, pointer behavior, background sheet size/offset or hit areas. The iframe designMode caret requires explicit capture-only `caret-color:transparent` during normalization; raw paint stays intact.
- Support is observed from **two auxiliary opaque planes**, black and white, with all other paint transparent and only the paired approved bitmap owners retained. Any differing channel contributes support. These planes are not normalized output. Transparent-alpha screenshots alone can round faint edge contributions to zero and are intentionally not used. No dilation or padding is applied.
- Check each support pixel against an actual approved owner bound. The SDK's static inline checkcolumn `::after` can paint below its host span; use its recorded containing cell-inner only as a leak guard. The legacy Classic tab-close raster at DPR2 has an observed device-pixel fringe beyond the fractional close-element border; use its recorded containing tab as the guard. Neither guard adds pixels to the support. Do not fabricate a pseudo DOMRect or turn the cell/tab into a mask. The exclusion itself still contains only observed icon ink. Raw golden comparison covers that ink without a mask.

## Threshold and controls

`maxChannelDelta=0`, `allowedChangedPixels=0`, `maskDilation=0`. Calibrate using exact repeated raw images and independent repeat captures of every component group plus framed/invalid/focus/menu/modal/open/pressed/hover states at both DPRs. No `0.001` ratio or broad antialias allowance. Any future browser/font/rendering change needs recalibration and review, not a silent threshold increase.

Real browser negative controls shift the folder icon and adjacent tree text by **1 CSS px** while keeping dimensions; a third control changes icon artwork through a filter without a geometry delta. Pixel/golden checks must fail; adjacent text must fail outside the frozen mask. Restore exact original inline style and require exact pixels/metrics again. Diagnostic browser pages are discarded; no control reaches production.

## Golden review/update procedure

1. Preserve the failing run and old manifest. Diagnose source changes before considering a new golden.
2. For artwork changes, show changed real-size/2x states and obtain explicit user approval of that version/hash. Existing v3 approval must not be reused for new drawings.
3. Require geometry/functional gate, actual build, icon contracts, repeated visual captures and negative controls to pass. Explain every intended visual change with old/new/diff images; never accept unexplained structure drift.
4. Create a **new versioned** golden directory, record approval/review evidence, source/environment hashes and rationale, then deliberately update the visual config binding. Never overwrite v1 or automatically accept the current screenshot. The initial `goldens.py` refuses an existing target; it is not called by the normal runner.
5. Re-run the normal visual gate against the new binding. Retain old goldens and history. Full release/build integration acceptance remains TASK-016/017.

Outputs: raw/normalized/support images, pixel diffs, metrics, `visual-results.json`, `golden-results.json`, negative controls, step logs and `run-status.json`. A failed/partial run is diagnostic evidence, not a new baseline. Initial gallery/report: artifacts/nordic-blue/TASK-015/review.html and visual-policy.md.
