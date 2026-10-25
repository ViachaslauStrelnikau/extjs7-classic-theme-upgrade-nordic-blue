from pathlib import Path
import json,hashlib,shutil
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');A=R/'artifacts/nordic-blue/TASK-021';C=Path(__file__).parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));write=lambda p,s:p.write_text(s,encoding='utf-8');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for f in ['acceptance-matrix.json','final-parent-lint.json','final-soft-lint.json','source-integrity.json']:assert read(A/f)['status']=='PASS'
one,two=[read(A/d/'release-manifest.json') for d in ['source-release','source-release-repeat']];assert one['sha256']==two['sha256'] and one['status']==two['status']=='PASS'
write(A/'reproducibility-check.json',json.dumps({'status':'PASS','sha256':one['sha256'],'bytes':one['bytes'],'payloadFiles':one['payloadFiles'],'runs':['source-release','source-release-repeat'],'verification':'Both ZIPs and every entry/CRC match exact current source bytes; fixed timestamps/order/permissions/compression. ZIPs are local/gitignored; recipe and input files are versioned.'},indent=2))
write(A/'FINAL-RECEIPT.md',f'''# Nordic Soft — интеграция завершена

TASK-021: DONE. SDK7.7.0.31/Cmd7.7.0.36, Windows. Полные geometry/function проверки: Edge/Chromium/Firefox,DPR1/2. Actual pages:3build modes/3browsers/DPR1/2,144pairs/40230elements. 18motion contexts,9catalog runs по182sheets,648resources×6outputs,5negative controls и700unchanged source files. Точные версии/ограничения — acceptance-matrix.json/integration-report.md.

Source archive: [nordic-soft-extjs-classic-7.7-source.zip](source-release/{one['archive']}), {one['bytes']}bytes, {one['payloadFiles']}payload files; SHA256 `{one['sha256']}`. Две упаковки совпали байт в байт.

Включены оба source theme packages и opt-in module, masters/approvals/manifests/policies/notices/reports. SDK/Classic reference bitmaps/compiled apps/dependencies не входят. Воспроизведение: `python tools/nordic-soft-release.py --output artifacts/nordic-blue/soft-release-new-run` (новая папка). Архивы локальные; исходники/recipe/manifest опубликованы в Git.

Просмотр: http://127.0.0.1:51754/soft-preview/index.html . Реальный TestApp: http://127.0.0.1:51754/build/theme-acceptance/soft/testing/index.html . Установка/откат/API — docs/nordic-soft-installation.md. Дополнительные анимации подключаются явно, исходное приложение не переписано. Старые approvals/goldens сохранены; новая полная Soft pixel-golden калибровка отдельно не выполнена, прежний pixel PASS ей не присваивается. Совместимость7.9 не заявляется.
''')
p=R/'docs/plans/nordic-blue/tasks/TASK-021.md';s=p.read_text(encoding='utf-8-sig').replace('Статус: IN_PROGRESS','Статус: DONE');s+='''
## Запись исполнителя

- Cmd-generated child theme,24approved tree files,624inherited resources; no runtime Ext overrides. Separate optional public-listener motion module, authored opacity/reduced motion/manual off/detach preserved.
- 12successful build invocations (6initial+6final), byte-identical final CSS. Every browser:204fixture+236action-state pairs+20core flows,21614element comparisons, DPR1/2. Actual output pages144pairs/40230elements;18motion contexts,9catalog/density/fallback runs. All PASS in recorded scope.
- 5negative controls rejected,700original source files unchanged. Parent and child lint PASS; source archive reproducible in2runs. No original app-specific fixes.
- Evidence: artifacts/nordic-blue/TASK-021/FINAL-RECEIPT.md, acceptance-matrix.json and integration-report.md. Parent pixel golden unchanged; no new full Soft pixel golden claimed. SDK7.9 NOT_RUN.
- Commit/push this completed integration separately. No renewed style/artwork approval needed: user has approved Soft and v2 folders.
''';write(p,s)
p=R/'docs/plans/nordic-blue/README.md';write(p,p.read_text(encoding='utf-8-sig')+'''
[TASK-021](tasks/TASK-021.md) — DONE: отдельный подключаемый пакет Nordic Soft с одобренными папкамиv2 и opt-in motion.3browser versions×DPR1/2 geometry/function,3build modes/actual pages, reduced/manual motion и source handoff проверены. Исходная тема и её golden сохранены. Новая полная pixel-golden Soft отдельно не фиксировалась; SDK7.9 не проверен.
''')
p=R/'AGENTS.md';write(p,p.read_text(encoding='utf-8-sig')+'''
## Nordic Soft integration accepted (TASK-021, 2026-10-25)

User approved shown squarer folder v2 by “хорошо. продолжай” in reply to the explicit integration approval question. Approval/hash now recorded in artifacts/nordic-blue/TASK-021/artwork-approval.json. Earlier WAITING records describe historical candidates; do not re-ask style or artwork approval for unchanged Soft/v2. Active parent icon config/golden remains v3; Soft has separate config/nordic-soft-icons.json and exact config/nordic-soft-policy.json. Child package is TestApp/packages/local/theme-nordic-blue-soft, Cmd-generated, extends theme-nordic-blue.24PNG/GIF1x/2x overrides,624inherited resources;16×16CSS boxes unchanged. No Ext class overrides.

Optional resources/soft-motion.js is not auto-included in application JS. Public attach/enable/disable API only; explicit shadow:false opts into CSS elevation; never call private SDK shadow APIs. Appearance150ms from35% of authored opacity to authored opacity; hide immediate, native animateTarget priority;120ms color/border/background transitions. System/manual reduction, repeat show, Escape, authored opacity.6, detach/destroy verified. Doc: docs/nordic-soft-installation.md. Original TestApp/classes/Sass/theme-lab/parent package unchanged700SHA; Soft has separate soft-lab and theme-acceptance/soft descriptors/outputs.

All3installed browsers (versions in TASK-021/acceptance-matrix.json):204fixture+236action/state pairs+20flows each at DPR1/2. Exact layout/font/state checks retained; only selected3/4px radius paint normalized by selector ownership/exact value, plus approved image contracts. Final actual output pages144pairs/40230elements,18motion contexts,9catalog/density/fallback probes,5negative controls,6outputs×648resources all PASS.12realCmd invocations exit0; finalCSS byte-identical to geometry captures. Parent/Soft lint separate; do not expand parent policy to accommodate child paint.

Source delivery: tools/nordic-soft-release.py --output NEW_DIR, includes both packages/masters/approval/policy/notices/report, noSDK/Classic reference bitmaps/compiled app/dependencies. Two byte-identical archives checked, ZIPs local/gitignored. See TASK-021/FINAL-RECEIPT.md. Parent pixel golden immutable; do not claim its PASS for Soft or auto-refresh it. No new full Soft pixel-golden calibration here;7.9/otherOS/arbitrarycustomUI/fullRTLlayout remain outside recorded scope. Any future visual-golden adoption requires its own calibration/source/environment binding and review. Preserve separate commit+push after each completed task.
''')
p=R/'README.md';write(p,p.read_text(encoding='utf-8-sig')+'''
## Nordic Soft — подключаемая версия

Выбранная Nordic Soft интегрирована отдельным пакетом `TestApp/packages/local/theme-nordic-blue-soft` поверх прежней темы: мягкие скругления, более квадратные жёлтые папки/синие документы, опциональные анимации. [Установка, API и откат](docs/nordic-soft-installation.md), [итоговый receipt/архив](artifacts/nordic-blue/TASK-021/FINAL-RECEIPT.md), [матрица](artifacts/nordic-blue/TASK-021/acceptance-matrix.json). Прежняя тема остаётся доступной.

Просмотр собранной Soft: http://127.0.0.1:51754/soft-preview/index.html (тот же preview server). Actual TestApp: /build/theme-acceptance/soft/testing/index.html.3browser versions/DPR1/2 geometry/function и3build modes проверены; новая полная pixel-golden Soft отдельно не фиксировалась. Анимации включаются явным API, SDK/app prototypes не патчатся. Source-пакет включает обе зависимости; `python tools/nordic-soft-release.py --output artifacts/nordic-blue/soft-release-new-run` создаёт новый воспроизводимый архив.7.9непроверена.
''')
H=A/'harness';H.mkdir()
for name in ['integrate_soft.py','build_soft.py','soft-motion.js','prepare_soft_gate.py','run_soft_gate.py','prepare_soft_preview.py','soft_modes_motion.cjs','soft_modes_motion_multi.cjs','prepare_soft_real.py','prepare_soft_native.py','prepare_soft_catalog.py','compare_soft_native.py','compare_soft_native_all.py','run_soft_other_browser.py','soft-policy-stage.py','soft-docs.py','final_soft_builds.py','soft_controls.py','report_soft.py','finish_soft.py']:
 shutil.copy2(C/name,H/name)
write(H/'README.md','''# Executed integration harness

Scripts and copied gate sources document the actual TASK-021 run on this Windows checkout. They intentionally use fixed evidence roots. Do not rerun writers over accepted evidence; prepare a fresh directory/copy and redirect all output paths. Parent tools and historical baselines remain immutable. Geometry drivers use a copied extract.js with selector-owned radius metadata; comparison exception checks exact3/4px values only. Source/reduced-motion/API/native/catalog evidence are independent checks. Missing-browser-metadata and Firefox fixture-boot race diagnostics remain recorded, not counted as successful initial steps. For future changes rerun parent/child lint and real builds before a new gate; never update source/approval/golden SHA to hide a regression.
''')
files=[p for p in A.rglob('*') if p.is_file() and p.name!='artifact-manifest.json'];write(A/'artifact-manifest.json',json.dumps({'status':'PASS','scope':'All retained TASK-021 evidence and clearly labelled diagnostics. Local ZIPs are intentionally gitignored.','files':[{'path':p.relative_to(A).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p),'localOnly':p.suffix=='.zip'} for p in sorted(files)]},indent=2))
print('TASK-021 DONE;',len(files),'evidence files; Soft integration and source delivery complete')
