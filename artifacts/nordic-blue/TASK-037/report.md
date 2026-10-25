# TASK-037: Nordic Soft Contrast1.2.0

2026-10-25. DONE: final approved state-study paint integrated, built, bounded Classic geometry/function checks and source delivery completed. User design approval is design-approval.json; final1px header separator /1px selection edges /2px left accent follow TASK-035/036. No new icon approval required: artwork unchanged.

## Source and architecture

Same package theme-nordic-blue-soft-contrast now1.2.0, extends Soft1.0.0 -> Nordic Blue1.0.1 -> installed Classic7.7.0.31. Approved groups#d7e4f3 / leaf#e6eef8, blue selection#bfd7f5 / hover#e3eefc, quiet vertical lines,1px header stripe and fine selection. Source :root specificity preserves the preview cascade; no app class required. Exact decorative blocks and SHA-linked policy reviewed in decorative-review.json; no general positioning/size allowance added. Header stripe is absolute pointer-transparent paint with1px height, no flow box. Own JS/Ext overrides/images/fonts remain absent. Inherited opt-in motion unchanged.

All648approved runtime files unchanged in all6builds; parents and original app/common fixture hashes unchanged. WGR not modified/built. Custom-icon parent fix retained. Main contrast-preview loads current compiled CSS. state-preview shows retained local1.1.1 vs compiled1.2.0, without candidate.css. Old compiled reference is local ignored output; reproducibility condition in state-preview/README.md.

## Actual validation

SDK7.7.0.31 / Cmd7.7.0.36 / Java8 / bundled Node6.6builds lab+TestApp contrast descriptors x testing/development/production exit0; inputs hashes stable during build.3source lints PASS; embedded manifests1.2.0,648resource SHA per output PASS. Existing TestApp navigation-image warnings retained in logs.

Fresh final regression-2: Edge156.0.4314.42, DPR1/2, viewport1280x1600; 204 fixture pairs, 236 paired action/state checkpoints, 20 additional flows, 21614 element comparisons PASS. Native geometry/fonts/positions/state exact; declaration-owned shadows/radii,1px inset outlines and exact header stripe validated separately as approved paint. Four actual temporary browser1px position/font mutations rejected and exact restores PASS. See acceptance-summary.json, regression-2/browser-results.json and negative-results.json. No historical baseline/golden updated.

First regression is diagnostic FAIL: Classic form/text-bg.gif caused the old extractor to catalog an otherwise unregistered input only in Classic; flat fields remove that decorative texture. Final extractor records unique-owned native input independently of paint. Both DOM nodes and complete metrics remain measured. Only validated native non-invalid INPUT/TEXTAREA with exact installed text-bg.gif -> none may normalize decorative image removal; no arbitrary icon/resource masking. Details flat-texture-review.json. Fresh run2 recaptured all states/actions; failed evidence preserved.

Actual IAB compiled paint readback confirms header fill, selection inset and1px stripe with no candidate stylesheet (compiled-paint.json); compiled comparison screenshot compiled-comparison.png. This is not full pixel-golden,3browser,full RTL,SDK7.9 or motion release acceptance of1.2.0. Those were not run. Arbitrary third-party UI/app CSS not universally covered.

## Source delivery and update

Current source-only ZIP under source-delivery/ includes all3packages. Install all3, especially Nordic Blue1.0.1, and rebuild consuming application. No SDK/node_modules/compiled output included; no new artwork license grant. Repeated source-delivery-repeat/ archive is checked byte-identical by source-reproducibility.json. Recipe tools/nordic-soft-light-release.py and docs/nordic-soft-light-installation.md. Separate commit/push follows per user instruction.
