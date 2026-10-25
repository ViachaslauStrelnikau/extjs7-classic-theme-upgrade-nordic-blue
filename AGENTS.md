# Instructions for Codex

## Project goal

Build a Sencha Cmd theme package named **Nordic Blue** for the Ext JS **Classic** toolkit. The intended framework target is Ext JS **7.7.0**, using the added SDK build **7.7.0.31**. The Ext JS 7.9 themes example is a visual reference only: https://examples.sencha.com/extjs/7.9.0/examples/classic/themes/

Read [the requirements](docs/nordic-blue-requirements.md) before making changes. The Classic screenshot captured from the original conversation is in [docs/reference/classic-baseline.png](docs/reference/classic-baseline.png).

## Environment checks before implementation

- The added SDK is at ext-7.7.0.31. Its version.properties reports version.full 7.7.0.31 and version.release 7.7.0. The TestApp/ext/version.properties copy reports the same. Recheck both if the SDK changes.
- The SDK package at ext-7.7.0.31/classic/theme-classic/package.json identifies sencha.name as theme-classic, toolkit as classic, and ext-theme-classic as an alternate name. TestApp/app.json selects toolkit classic and theme ext-theme-classic.
- The project package.json declares @sencha/cmd-windows ^7.7.0; installed package metadata reports version 7.7.0 and version_full 7.7.0.36. A local binary invocation with -v did not return during the check; verify that Cmd runs before building.
- PATH also resolves to C:\Users\Damned\bin\Sencha\Cmd\4.0.5.87\sencha.exe; sencha version did not return before interruption. Prefer the project-local Cmd only after confirming its runtime works.
- Inspect existing project files before modifying them. Never edit the installed SDK. Preserve the existing TestApp, package.json, package-lock.json, and node_modules unless a documented setup step requires a change.
- Never edit the installed SDK. Keep the theme in its own package and use Sencha Cmd's generated package structure.

## Architecture and compatibility

- Create a theme package with Sencha Cmd for toolkit classic, extending the installed theme-classic package. Verify the generated package.json and inheritance chain against the SDK actually in use.
- Keep application code, component configs, data, and event behavior unchanged. The theme must be selectable in the same Classic applications that use theme-classic.
- Preserve Classic component geometry and typography exactly: rendered bounds, positions, dimensions, spacing, line height, font family, size, weight, and letter spacing. Nordic Blue changes colors and visual treatment only unless a separately documented design decision is approved by the user.
- The user requires updated standard icons. Inventory Classic assets and create the Nordic icon set early (TASK-003/004), then integrate it (TASK-013). Preserve image/display dimensions, sprite cell grid/offsets, hit targets, states and behavior. Retain the original Classic baseline and inherit resources not explicitly replaced. Follow docs/nordic-blue-agent-guide.md; the PDF recommendation to retain all original icons is superseded by this user instruction.
- Keep fixes for clipped text and misaligned arrows within the geometry and behavior requirements. Check the relevant font metrics, padding, line height, sprite/glyph, and alignment rules; do not hide a defect by changing component size.

## Work and completion gate

Follow the roadmap and acceptance checks in the requirements document. Compare Classic and Nordic Blue using the same Ext JS 7.7 SDK, application, data, browser, viewport, zoom, and device scale. Record component bounds and compare screenshots; inspect interactions, keyboard navigation, and component states.

Do not report the theme as ready until a real Sencha Cmd build succeeds and the built theme has been exercised in a Classic test application. Report the exact SDK/Cmd versions, build command, browser and scenarios checked, and any remaining visual differences.


## Implementation plan from the complete research PDF

Read [the agent guide](docs/nordic-blue-agent-guide.md) and [the task index](docs/plans/nordic-blue/README.md). These documents incorporate all 32 PDF pages, the Nordic screenshot and subsequent user instructions. Target 7.7.0.31; 7.9 is optional. Require unchanged geometry, not automatic acceptance of the PDF diagnostic 1 px threshold. Complete tasks by dependencies and record evidence; preparation of this plan does not complete implementation tasks.

## Icon density and user approval

Increase icon pixel density where the SDK/Cmd pipeline safely supports it (e.g. 2x bitmap for the same CSS size). Keep rendered/physical interface size, CSS rects, hit targets, spacing and logical sprite offsets unchanged; preserve a working 1x fallback. Validate DPR 1 and 2 separately. After generating the complete icon set, show all states and real-size/HiDPI previews to the user. TASK-004 enters WAITING_USER_APPROVAL; obtain explicit approval of its version/hash before TASK-013 integration or adopting icon golden snapshots. No response is not approval. Follow the detailed guide for density handling and renewed approval of changed artwork.

## Project build and development commands

Working directory for both commands: D:\Projects\Extjs7ClassicThemeUpgradeNordicBlue\TestApp (the folder containing app.json).

Testing build (user-provided and successfully verified with Cmd 7.7.0.36):

```powershell
..\node_modules\@sencha\cmd-windows\dist\sencha.exe app build testing
```

Start the development server and watcher:

```powershell
..\node_modules\@sencha\cmd-windows\dist\sencha.exe app watch
```

Use the project-local executable above rather than the old global sencha on PATH. The verified build environment uses Java 8 from C:\Program Files\Java\jdk1.8.0_501 and Node.js on PATH. The testing build passed; it reported pre-existing missing tab-navigation image warnings from TestApp's navigation UI. Keep those warnings in the baseline audit. The watch command is the user-provided development command; report its actual server URL after launch rather than assuming a port. Watch is a long-running process and does not replace testing/production acceptance builds.

## Generated Nordic package and laboratory builds (TASK-007)

The Cmd-generated theme is at `TestApp/packages/local/theme-nordic-blue`. Cmd 7.7.0.36 generated the modern `package.json` (`sencha` metadata) and a build.xml importing installed Cmd package build logic; it did **not** generate `.sencha/package`. Preserve this actual scaffold and any `.sencha/package` produced by a future supported migration; do not fabricate old configuration. The original generated files, including the archived identity-only overrides/init.js, are in artifacts/nordic-blue/TASK-007/generated-scaffold. Active overrides/ and resources/images/ are empty after TASK-007.

Lab builds use the separate `TestApp/theme-lab/app.json` descriptor in the same TestApp workspace, with the common fixture and build-requires.js. From `TestApp/theme-lab`, run `..\..\node_modules\@sencha\cmd-windows\dist\sencha.exe app build lab-classic testing` and `..\..\node_modules\@sencha\cmd-windows\dist\sencha.exe app build lab-nordic testing` sequentially. Outputs: `TestApp/build/theme-lab/{classic,nordic}/testing`. The original TestApp commands above and production source/config remain unchanged. Empty child inheritance passed DPR1/2 comparisons; palette/icons and release acceptance remain future tasks.

## Color policy and lint (TASK-008)

The initial palette now uses 15 canonical dynamic tokens and 52 verified SDK color hooks in namespace files. `package.json` must explicitly include `${package.dir}/sass/var/all.scss` before the var directory: installed Cmd 7.7 did not auto-include package all.scss in app/slicer builds. Preserve this reviewed configuration.

Before building any theme change, run from the project root:

```powershell
& 'C:\Users\Damned\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' tools/lint-nordic-blue.py --check-icon-candidates
```

The script is read-only and uses the Python standard library; `python tools/lint-nordic-blue.py --check-icon-candidates` also works with a configured Python. Policies live in config/nordic-blue-policy.json and config/nordic-blue-icons.json. Unlisted variables, geometry/typography/image/position assignments, global base-color, arbitrary CSS/UI mixins, extra runtime JS/fonts, changed protected config and unapproved image bytes/contracts fail. Exact approved 1x/2x bitmap/CSS-size/sprite contracts are recognized; icon integration is still disabled until TASK-013. No broad background-size/position exception is allowed. Any policy expansion needs SDK declarations/actual compiled consumers and the relevant component geometry review; do not weaken the policy to hide a regression. State/gradient refinements remain TASK-009–012. TASK-008 report records 33 controls and strict DPR1/2 geometry evidence; this is not theme release acceptance.

## Core component refinement (TASK-009)

The active policy now contains 104 verified color hooks and 14 exact reviewed `dynamic('none')` gradient hooks. Gradient exceptions require the exact SDK name/path/value and SHA-linked artifacts/nordic-blue/TASK-009/gradient-review.json plus its phase-A geometry report. Unlisted gradients, arbitrary CSS, geometry changes and JS/UI overrides still fail lint. Do not expand these exceptions globally.

Classic's button mixin conditionally omits combined-state declarations when their values equal ordinary hover/pressed. Keyboard focus specificity can then obscure hover/pressed. Preserve the reviewed focus color choices: focus uses control-bg, focus-over uses accent-soft, focus-pressed uses #C7DCF6 (RGB 90% control-pressed + 10% accent). The latter is a component state value; the fifteen canonical tokens remain unchanged. Validate all seven states pairwise using genuine pointer focus/pressed flags, not just button.pressed (which represents enableToggle).

TASK-009 evidence: final full fixture pass-3, core-states-v3, 168 distinct paint pairs, zero metric drift, real Cmd testing build. Raw captures and snapshots are losslessly packed in artifacts/nordic-blue/TASK-009/evidence.zip because D filled during diagnostic copying; gallery server reads the archive in memory. Earlier diagnostic raw frames also remain in the C staging diagnostics.zip recorded in storage-decision.json; summary reports are in the project. Do not extract archives or run another build on D until enough space is available. Source images and overrides remain empty. Next task: TASK-010; full release acceptance and icons integration are pending.

## Form refinement (TASK-010)

Completed 2026-10-24: 117 verified color hooks (13 new form/trigger/fieldset hooks), 15 tokens and the unchanged 14 reviewed gradient hooks. Keep Classic error colors, disabled opacity, readonly behavior and font/box metrics. Do not add inactive glyph hooks when font icons are disabled, or unused form-toolbar-trigger-border-color-focus. Checkbox/Radio share the checked-label mixin. Text/Combo/Date/Time/Number/TextArea derive colors through shared form-field hooks.

Real Nordic lab testing build passed. 102 states at DPR1/2 show zero exact metric drift; 96 real form input/actions and 48 paired comparisons passed. Full evidence and limitations: artifacts/nordic-blue/TASK-010/form-component-report.md and review.html. Source images/overrides remain empty; all 180 inherited standard icon resources remain unchanged until TASK-013. Original application/common fixture and SDK are unchanged. Next task: TASK-011.

The user freed disk space on 2026-10-24; more than 4 GiB was verified before TASK-010. The historical TASK-009 storage block above is resolved. Its evidence.zip remains the accepted archive; avoid unnecessary extraction. Recheck free space before future large builds/capture copies.

## Grid, Tree and paging refinement (TASK-011)

Completed 2026-10-24: 130 verified color hooks, 15 tokens and 17 reviewed gradient hooks. Three header gradients use the same narrow policy with SHA-linked artifacts/nordic-blue/TASK-011/gradient-review.json and phase-a-geometry.json; preserve these expanded files. Tree row styling derives from grid/view; paging derives from existing toolbar/form styles. No inactive glyph hooks, metric flags, typography/indent changes or SDK/JS overrides.

Two real lab testing builds passed. Final 102 states at DPR1/2 match Classic exactly on metrics; 92 real action checkpoints / 46 paired comparisons passed (sort, selection, header menu, column drag, both-axis scroll, tree mouse/keyboard, paging/boundaries). A diagnostic compact viewport uses the same existing setSize/scroll APIs on both themes; fixture configs remain unchanged. Classic resize from 2 px inside a 260 px header with +50 px pointer movement yields 308 px, identically Nordic. Full evidence and remaining limits: artifacts/nordic-blue/TASK-011/grid-component-report.md. Source images/overrides remain empty and approved icons integration remains TASK-013. Next task: TASK-012.

## Secondary components (TASK-012)

Completed 2026-10-24: 177 actual compiled color hooks, 15 tokens, 31 narrowly reviewed flat gradients. New secondary gradients require artifacts/nordic-blue/TASK-012/gradient-review.json and SHA-linked phase-a-geometry.json to remain available. Slider remains bitmap-based (slider-imageless=false); do not enable a new renderer or unused glyph/color rules. Slider artwork, arrows, close/check/loading images integrate in TASK-013 using already approved v2 contracts.

Compiler consumption must recognize both hex and equivalent rgb/rgba: SDK background-opacity converts mask colors to RGBA. Keep both mask background/page color hooks. Only tab-outline-color-focus and menu-scroller-border-color were actually unused and removed; do not change widths/flags to activate them. Diagnostic correction is recorded, and no byte identity claim across gradient changes is made.

Final real lab testing build passed; full102 states at DPR1/2 match metrics/fonts/state/offsets exactly;116 secondary action checkpoints /58 paired comparisons passed. Coverage/status and intentional design differences are in artifacts/nordic-blue/TASK-012/. Source images/overrides remain empty, SDK/application/common fixture unchanged. Next task: TASK-013, integrate the approved v2 icon set (approval already recorded; ask again only if artwork/contracts change). Release acceptance remains TASK-014–017.

## Approved runtime icons (TASK-013)

Completed2026-10-24: resources/images now intentionally contains648 exact approved v2 runtime files; integrationEnabled=true. Approval/manifest/masters/candidates remain immutable. Historic empty-images/integration-pending notes above describe earlier tasks. Keep overrides/ empty and preserve177 color hooks/15tokens/31 reviewed gradients.

sass/src/Component.scss is an exact SHA-bound reviewed image stylesheet, not general CSS permission:294 installed Classic LTR/RTL selector mappings plus the approved resize/move adapters. It changes only approved background-image/whole-sheet background-size and two y=0 mappings. Retain1x preferred/fallbacks and automatic2x at `@media (min-resolution: 192dpi)` (space is required by the verified compiler). Do not scale CSS boxes or sprite offsets. Slider tracks/toast fader explicitly inherit; thumbs replace. Do not switch imageless/font renderer. Five unused legacy aliases retain approved original paths; do not invent selectors.

Geometry checks must map only approved image/density contracts, including nested pseudo metadata; enforce exact sheet size/density before comparison, with only resize/move old-y→0 approved exceptions. Preserve the original component hit box even when lab layout stretches it (140×15); the icon graphic is15×15. Never substitute Classic GIF frames for Nordic artwork; QA frame0 comes from the actual approved/built GIF at its density. Runtime animation bytes remain unchanged.

Testing/development/production real lab builds passed. Development CSS is split into imported _1/_2 files; fallback/density checks must inspect imports too. All648 approved files verified in all modes;182sheets×9 mode/DPR/fallback runs, zero404, native HTTP SHA and cache reload passed. Full102states×DPR1/2 exact metric comparison,304 genuine action executions and45+7 negative controls passed. TASK-013 reports state the actual52 logical native replacement paths/full-catalog scope. Do not turn this into a claim of final visual/functional release readiness. Evidence: artifacts/nordic-blue/TASK-013/icon-integration-report.md. Next: TASK-014.

## Approved folder revision v3 (2026-10-24)

The user approved the shown folder revision with “хорошо. продолжай”. Active icons are now nordic-icons-v3-folders: only folder-open/folder-rtl/folder-open-rtl changed (12PNG/GIF files at1x/2x). Ordinary folder and all636other runtime assets unchanged, same16×16 CSS boxes. CSS bytes, sprite offsets and geometry unchanged. Testing/development/production, full102states×DPR1/2,92 Grid/Tree/paging actions and9 mode/density/fallback probes passed.

Read active manifest/approval paths from config/nordic-blue-icons.json. Current approved files are under artifacts/nordic-blue/REV-001-folders-v3/. The original v2 artifacts remain immutable historical evidence. Lint canonical_images supports only the original TASK-004 source root and the explicit artifacts/nordic-blue root used to combine approved revisions; all SHA/approval/metric checks remain enforced. Report: artifacts/nordic-blue/REV-001-folders-v3/integration-report.md. Next task remains TASK-014.

## Reproducible geometry/functional gate (TASK-014)

Completed2026-10-24. From project root run `python tools/nordic-blue-regression/run.py --output artifacts/nordic-blue/regression-new-run` (configured Python runtime also works). Existing output is rejected. Requires running Theme Lab and current testing build; optional --url and --node documented in tools/nordic-blue-regression/README.md. Never refresh TASK-006 to hide regressions. Run the gate after future theme changes and a real build.

204 fixture pairs and236 action/state pairs at DPR1/2 passed exact metrics;360 functional checkpoints,112 core-state checkpoints,20 additional core flows,12 icon adapter checks. Window pointer drag/resize/close and modal keyboard traversal included. Four real temporary 1px/font mutations plus10 structural controls all failed as expected, restored metrics passed. No geometry tolerance, arbitrary URL normalization or blanket icon masks. Read active icon paths from config; retain approved density/sheet/offset contracts and actual Nordic GIF frame0 policy. Evidence: artifacts/nordic-blue/TASK-014/regression-report.md and run-1/review.html. Theme/package/fixture/SDK unchanged. This is not visual golden or release acceptance; next TASK-015, then016/017.

## Visual structure and Nordic goldens (TASK-015)

Completed2026-10-24. Run `python tools/nordic-blue-visual/run.py --output artifacts/nordic-blue/visual-new-run` from root with current testing build/running lab; --url/--node available. Use bundled Python with Pillow/NumPy. Existing output rejected; no automatic golden update. Instructions: tools/nordic-blue-visual/README.md.

Active technical visual baseline: artifacts/nordic-blue/TASK-015/golden-v1/, bound by config/nordic-blue-visual.json and exact guard/source/environment hashes. Initial full-theme baseline is not final user/release approval. Active artwork remains approved v3. Any new artwork needs explicit user approval; preserve old versions and review old/new/diff before changing the binding. Changed source with stale compiled output must fail.

204 Classic/Nordic cases passed exact metrics and0 unmasked structural pixels;408 raw repeat comparisons and464 independent calibration images had0 drift. Use RGBdelta0/pixels0/dilation0. Keep URL image layers in normalization; neutralize only colors/gradient paint. Exact icon support comes from black/white auxiliary planes and is frozen, not blanket element masks. Pseudo checkbox/legacy fractional tab-close bounds use actual containing cell/tab only as safety guards, never as exclusions. Six real icon/text1px/artwork controls failed, exact restore passed. All648 runtime resources and all decoded frames checked against unmasked artwork golden; native raw/normalized snapshots also unmasked. See artifacts/nordic-blue/TASK-015/visual-policy.md for caret/GIF/clipping rules and limitations. SDK/theme/fixture unchanged. Next TASK-016, then017; do not claim final readiness yet.

## Commit and push each completed task

The user explicitly requests a separate commit and push after every completed task. Finish the task's required evidence and documentation, mark its card/index accurately, inspect staged files for dependencies/generated SDK output/secrets, then commit and push to origin/main. Do not wait for another permission request. Do not mark unfinished work DONE merely to commit. Preserve exact bytes through .gitattributes; keep SDK/node_modules/compiled outputs excluded. Verify the remote commit and clean working tree after each push.

## Build/browser integration acceptance (TASK-016)

Completed2026-10-24: SDK7.7.0.31/Cmd7.7.0.36, 17 successful invocations. development/testing/production actual output pages passed in Edge155.0.4283.62, Chromium156.0.8078.4 and Firefox152.0.4 at DPR1/2. Per browser:204 fixture+236action/state pairs+20core flows; actual outputs144pairs/40230elements total, no exact metric/state drift. All648resources×6Nordic outputs SHA-verified; 36manifest pairs/runtime flags match except added Nordic package. 700 protected sources unchanged. Existing app-specific navigation image warnings remain baseline warnings, not a new regression.

TestApp/theme-acceptance/{classic,nordic} descriptors rebase original app paths and theme/output only. local.properties in these two directories and theme-lab enables skip.page=0/skip.js=0 because installed Cmd development defaults skip both; packaging only. Original TestApp descriptor/classes/Sass unchanged. Do not use unsupported CLI -Dskip flags. Tools/evidence are fixed to this Windows acceptance run; do not overwrite accepted outputs. Read tools/nordic-blue-acceptance/README.md.

Firefox157 diagnostic failed browser-context cleanup; partial data is not PASS. Compatible152 full retry is accepted. Standalone precompiled theme package not promised: NOT_REQUIRED; source package app builds validated. SDK7.9 NOT_RUN/optional018. Report artifacts/nordic-blue/TASK-016/acceptance-report.md. Next017; full-theme final user approval is not implied by technical matrix.

## Source delivery and final technical report (TASK-017)

Completed2026-10-24: required001–017 finished for7.7.0.31. Read docs/nordic-blue-installation.md (install/rollback/build/watch/gates), docs/nordic-blue-release-notes.md and artifacts/nordic-blue/TASK-017/FINAL-RECEIPT.md. Deterministic source-only handoff: `python tools/nordic-blue-release.py --output artifacts/nordic-blue/release-new-run`; output must not exist. Two independent archives matched exactly; each entry/source SHA/CRC checked. Includes approved SVG masters/approval/notices/config/palette/report summaries; no SDK/Classic reference bitmaps/compiled app/dependencies/debug patches. ZIPs remain local/gitignored; recipe, inputs and manifest are versioned. No new artwork license grant is invented.

Previous014/015/016 evidence SHA and700protected inputs checked again. Keep those immutable. Technical acceptance and user approval of icons do not imply final user visual approval of every screen, complete RTL app testing, all custom ui, otherOS/browser versions or animation smoothness. Optional018/SDK7.9 NOT_RUN; do not claim7.9 compatibility. Any future task must retain explicit scope/evidence and get a separate commit+push after DONE.

## Modernization prototype and warm tree artwork (TASK-019, 2026-10-25)

User authorized a comparison stand for Refined/Motion/Soft and prefers warm folders/blue leaves like the attached initial sketch. Implemented only in TestApp/modern-preview, served by its own read-only server on51754. Existing theme/Theme Lab/active approval/policy/goldens remain unchanged. Preview paint CSS and show listeners belong only to demo components; no Ext overrides, no layout/font/hit-box changes intended. Motion is paint-only120ms transitions/150ms opacity on opening; hide remains immediate, system/manual reduction supported. Prototype render is not geometry/function/release acceptance; see TASK-019 report. Do not fold unreviewed preview CSS into the approved package.

REV-002-tree-warm candidate nordic-tree-warm-v1 is WAITING_USER_APPROVAL, not runtime-integrated. SVG masters/PNG1x/2x at unchanged16×16CSSpx and version/SHA are recorded. Obtain explicit approval of actual shown artwork/hash and variant choice before production integration. Prepare production GIF fallback/contracts and new compatibility gates after selection; never silently replace v3 or refresh old goldens. Future completed tasks require separate commit and push as already authorized.

## Soft selected; folder proportions v2 (TASK-020)

User explicitly selected Nordic Soft and requested squarer folders. Selected style is now soft; do not ask for style selection again. Updated only the preview candidate under TestApp/modern-preview/icons-v2: narrower/taller folder silhouette, same16x16 CSS canvas, SVG and1x/2x PNG. Document unchanged. REV-002-tree-warm-v2/nordic-tree-warm-v2 is WAITING_USER_APPROVAL; obtain approval for revised artwork before production integration. Previous candidate/approved production theme/goldens remain unchanged. TASK-020 completes only this prototype revision, not deployment of Soft. Continue separate commit/push for completed tasks.

## Nordic Soft integration accepted (TASK-021, 2026-10-25)

User approved shown squarer folder v2 by “хорошо. продолжай” in reply to the explicit integration approval question. Approval/hash now recorded in artifacts/nordic-blue/TASK-021/artwork-approval.json. Earlier WAITING records describe historical candidates; do not re-ask style or artwork approval for unchanged Soft/v2. Active parent icon config/golden remains v3; Soft has separate config/nordic-soft-icons.json and exact config/nordic-soft-policy.json. Child package is TestApp/packages/local/theme-nordic-blue-soft, Cmd-generated, extends theme-nordic-blue.24PNG/GIF1x/2x overrides,624inherited resources;16×16CSS boxes unchanged. No Ext class overrides.

Optional resources/soft-motion.js is not auto-included in application JS. Public attach/enable/disable API only; explicit shadow:false opts into CSS elevation; never call private SDK shadow APIs. Appearance150ms from35% of authored opacity to authored opacity; hide immediate, native animateTarget priority;120ms color/border/background transitions. System/manual reduction, repeat show, Escape, authored opacity.6, detach/destroy verified. Doc: docs/nordic-soft-installation.md. Original TestApp/classes/Sass/theme-lab/parent package unchanged700SHA; Soft has separate soft-lab and theme-acceptance/soft descriptors/outputs.

All3installed browsers (versions in TASK-021/acceptance-matrix.json):204fixture+236action/state pairs+20flows each at DPR1/2. Exact layout/font/state checks retained; only selected3/4px radius paint normalized by selector ownership/exact value, plus approved image contracts. Final actual output pages144pairs/40230elements,18motion contexts,9catalog/density/fallback probes,5negative controls,6outputs×648resources all PASS.12realCmd invocations exit0; finalCSS byte-identical to geometry captures. Parent/Soft lint separate; do not expand parent policy to accommodate child paint.

Source delivery: tools/nordic-soft-release.py --output NEW_DIR, includes both packages/masters/approval/policy/notices/report, noSDK/Classic reference bitmaps/compiled app/dependencies. Two byte-identical archives checked, ZIPs local/gitignored. See TASK-021/FINAL-RECEIPT.md. Parent pixel golden immutable; do not claim its PASS for Soft or auto-refresh it. No new full Soft pixel-golden calibration here;7.9/otherOS/arbitrarycustomUI/fullRTLlayout remain outside recorded scope. Any future visual-golden adoption requires its own calibration/source/environment binding and review. Preserve separate commit+push after each completed task.

## Design comparison after WGR reference (TASK-022, 2026-10-25)

User authorized preparation of a visual comparison, not final adoption of the resulting artwork/paint. TestApp/design-preview compares current built Soft with a demo-only CSS candidate using one identical sample.js. Preview URL51754/design-preview/index.html. No package/SDK/application/policies/goldens changed and no new Cmd build. Existing approved icons remain. Four observed states/579element pairs have equal recorded rect/font/box metrics; not full Classic/DPR/browser acceptance. Read artifacts/nordic-blue/TASK-022/report.md, including unresolved IAB console MutationObserver diagnostics. Do not copy arbitrary preview CSS into the package. Await feedback on actual result, then map paint to installed Sass consumers, design explicit optional primary UI, preserve normal UI/config/behavior/metrics, build and run strict regression in a separate task. Parent goldens remain immutable.

## Expressive preview v2 (TASK-023)

User found TASK-022 too subtle and authorized a stronger preview. Current design-preview/reference.css is v2: white headers/toolbars, neutral grid, flat decorative field texture, inset selection accents and underlined tabs. Shared sample and package unchanged; no new icons/build.579observed pairs in4states show equal recorded metrics; raw DOM observations in TASK-023, not Classic release acceptance. Keep TASK-022 historical evidence. Await review of the actual v2 before production integration; retain all prior compatibility and approval gates.

## Preview identity persistence fix (TASK-024)

User reproduced candidate styles disappearing after initial display. reference.css stayed loaded but body.design-reference was lost because Ext maintains cached class maps and rewrites className. Design preview now scopes paint to owned html[data-nordic-preview="reference"], assigned before SDK load. Never reintroduce direct body classList writes for variant identity. No observers/polling/SDK overrides.5observed paint checkpoints across mouse/keyboard/window/reloads/motion-toggle retain actual differing colors/field texture/tab paint;253normal metric pairs equal. TASK-022/023 equal geometry alone did not establish stable candidate paint. See TASK-024 report for corrected scope; historical evidence unchanged. Package and motion API acceptance are not part of this fix.

## Preview column headers (TASK-025)

User requested stronger distinction between column headings and data rows. Preview reference.css now uses #deebfa header fill, #ccdef5 hover and a narrow inset lower separator with unchanged typography/boxes. Actual2column rect/font pairs equal current Soft; evidence TASK-025. Demo-only, not package integration; keep html attribute scope from TASK-024.

## Header design refinement (TASK-026)

Latest user direction supersedes TASK-025 blue fill: column headings use tab-bar #f4f6f9 with a3px blue inset on actual .x-column-header-first, matching panel accent. Narrow preview-only change; no font/box changes. TASK-026 records actual matching computed fills and screenshot. Keep owned html scope and prior production gates.
