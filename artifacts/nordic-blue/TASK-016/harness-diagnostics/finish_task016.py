from pathlib import Path
import json,hashlib,shutil,html
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');A=R/'artifacts/nordic-blue/TASK-016';T=R/'tools/nordic-blue-acceptance'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
write=lambda p,s:p.write_text(s,encoding='utf-8')
browsers=[]
for name in ['edge','chromium','firefox']:
 b=read(A/f'browsers/{name}/browser-results.json');assert b['status']=='PASS';assert read(A/f'browsers/{name}/run-status.json')['status']=='PASS';browsers.append({k:v for k,v in b.items() if k!='results'})
native=read(A/'native-page-comparison.json');audit=read(A/'source-resource-mode-audit.json');assert native['status']==audit['status']=='PASS';assert read(A/'original-app-testing.json')['status']=='PASS'
commands=read(A/'build-commands.json')+read(A/'development-output-commands.json');assert len(commands)==17 and all(c['exitCode']==0 for c in commands)
matrix={'status':'PASS','sdk':'7.7.0.31','cmd':'7.7.0.36','browsers':browsers,'nativePairs':native['pairs'],'nativeElements':native['elementComparisons'],'buildInvocations':len(commands),'standalonePackageBuild':{'status':'NOT_REQUIRED','reason':'Delivery is source theme package consumed by Sencha Cmd app builds; no precompiled standalone package promised.'},'sdk79':{'status':'NOT_RUN','reason':'Optional TASK-018; not part of target 7.7 acceptance.'},'scope':'Windows, installed browsers, DPR1/2. Fresh Classic/Nordic comparisons within each browser. Exact visual goldens remain Edge-only TASK-015.'}
write(A/'acceptance-matrix.json',json.dumps(matrix,indent=2))
write(T/'README.md','''# Nordic Blue: build and integration acceptance (TASK-016)

These tools target this Windows checkout and its installed SDK 7.7.0.31. Use Java 8, local Cmd 7.7.0.36, its bundled Node 6 for Fashion, and the documented bundled Python/Node24 for browser drivers. The existing fixture server is http://127.0.0.1:51752/. Start `node tools/nordic-blue-acceptance/serve.cjs` from the root for the actual-output console audit at http://127.0.0.1:51753/ (read-only TestApp root plus SDK alias). This server answers the browser-only /favicon.ico request with HTTP204; it does not mask component/resource requests. The original server/app remain unchanged. NORDIC_ACCEPTANCE_URL can select a different actual-output server.

The scripts intentionally name TASK-016 evidence paths. **Do not rerun writers over accepted evidence.** For a new acceptance run, copy the harness to a new work area, change its output root consistently, probe installed browser paths/versions, and retain accepted artifacts. The TASK-014/015 runners already accept fresh --output directories and reject existing outputs.

1. `python build-matrix.py`: sequential Classic/Nordic lab and real TestApp builds for testing/development/production, then the unchanged original TestApp testing build; 13 invocations. The descriptors use one workspace and original app sources. Development local.properties enable page/JS packaging with the installed Cmd's supported skip.page=0/skip.js=0. No CLI -D flags.
2. `node probe-browsers.cjs`: record actually available installed executables; inspect version and successful launch before claiming availability. Playwright must match its patched Firefox. The accepted Firefox is 152.0.4, not the incompatible 157 diagnostic.
3. `python run-browser.py edge` (also chromium/firefox): full fresh Classic/Nordic testing fixture and action captures, exact metrics/contracts comparison. Each output browser folder must not already exist.
4. `node native-pages.cjs edge` (also chromium/firefox): open actual built index.html with microloader/manifest/compiled JS/CSS, reload, exercise the unchanged real app, inject the unchanged lab fixture only after its compiled entry loads. 96 records per browser. `python compare-native.py`: 144 exact pairs.
5. The recorded TASK-016/build-modes.cjs and extract.js perform nine native CSS/resource/catalog probes (three modes × DPR1/native DPR2/forced 1x fallback), including development CSS imports. `python audit.py` checks protected sources, six sets of 648 resource SHA values, 18 overview pairs, build-warning provenance and 36 pairs of actual package manifests/runtime flags.
6. `node original-app.cjs` opens the actual original testing output without changing app.json.

Exact recorded commands/exit codes, browser paths/options, snapshots and network evidence are under artifacts/nordic-blue/TASK-016. A browser-specific fresh Classic baseline does not relax counts/IDs/state/metric comparisons or modify TASK-006. No cross-browser coordinate equivalence is claimed. SDK binaries, dependencies and compiled output are local prerequisites, excluded from Git.
''')
write(R/'TestApp/theme-acceptance/README.md','''# Real TestApp acceptance descriptors

classic/ and nordic/ build the same original TestApp application classes, view Sass, controller/store, app.js and workspace. Only the theme selection, output root and paths rebased to the original workspace differ from TestApp/app.json. index.html/build.xml are byte copies of their original counterparts. Original TestApp source and descriptor remain unchanged.

From either directory, use `..\\..\\..\\node_modules\\@sencha\\cmd-windows\\dist\\sencha.exe app build testing` (or development/production). Use the project Java 8 / Cmd-bundled Node environment. Outputs: TestApp/build/theme-acceptance/{classic,nordic}/{mode}.

local.properties enables skip.page=0 and skip.js=0, because installed Cmd development defaults skip both. This packages real development output pages without altering debug/logger, app behavior or theme rendering. The laboratory uses the same packaging properties. Do not add these validation-only hooks to the original TestApp unless explicitly needed.

TASK-016 captures the actual output pages, responsive navigation, all tabs, selection confirmation and cancellation. Existing app-specific navigation Sass and font-awesome remain intact, including pre-existing missing navigation image build warnings. No theme-specific app fixes were introduced.
''')
report='''# TASK-016 — матрица сборок и интеграция

Статус: **PASS / DONE**, 2026-10-24. SDK **7.7.0.31**, Sencha Cmd **7.7.0.36**, Windows, Java 8. Тема и исходное приложение не менялись.

## Сборки и настоящие output pages

- 12 сборок: laboratory и исходный TestApp через отдельные Classic/Nordic descriptors × development/testing/production; плюс исходная пользовательская `app build testing`: все exit 0.
- Четыре дополнительные development-сборки с поддерживаемыми local.properties: все exit 0. Cmd по умолчанию устанавливает skip.page=1/skip.js=1. Для acceptance включены только упаковка index.html/JS (значения 0); не изменены debug/logger и приложение. Неудачная попытка CLI -D сохранена как диагностика, не считается успешной сборкой.
- Проверены реальные `TestApp/build/{theme-lab,theme-acceptance}/{classic,nordic}/{mode}/index.html`, их microloader/manifest/JS/CSS, cache reload. Ни старый watch, ни замена SDK debug JS не выдаются за output pages. Lab fixture подключается после готовности реального compiled entry; real TestApp работает без инъекции fixture.
- 72 отдельных контекста (24 на браузер), каждый с начальной загрузкой и reload: 144 загрузки, 288 snapshots; **144 пары / 40 230 элементов**, точные размеры, шрифты, offsets, состояния и данные совпали.
- 36 пар manifest: одинаковые родительские packages/inclusion/runtime flags; добавлен только theme-nordic-blue extending theme-classic. Ext.theme.name остаётся Classic: никаких runtime JS overrides не добавлено.
- 648 одобренных resources в каждой из шести Nordic outputs совпали по SHA. Девять каталогов по 182 sheets, DPR1/2 и вынужденный 1x fallback, 18 overview/reload сравнений — PASS. Development CSS imports включены в проверку.
- Console/page errors, HTTP404 и смешение build outputs: 0 в принятой матрице. Исходная пользовательская testing-страница: SDK 7.7.0.31, 4 вкладки / 4 записи, PASS.

## Браузеры и поведение

'''
for b in browsers:
 report+=f"- {b['browser']['name']} **{b['browser']['version']}**: PASS, {b['coveragePairs']} fixture pairs + {b['actionStatePairs']} action/state pairs + {b['additionalCoreFlows']} additional core flows, DPR1/2.\n"
report+='''
Fresh Classic/Nordic baseline сравнивается строго внутри каждого браузера/DPR. Между браузерами равенство координат/шрифтов не заявляется. TASK-006 неизменён. Полный визуальный pixel golden относится к Edge из TASK-015, не переносится автоматически на Firefox/Chromium.

Firefox 157 запускался, но протокол управления прервался при закрытии context; частичные результаты сохранены в browsers/firefox-157-diagnostic и не включены как PASS. С установленным совместимым Firefox152.0.4 повторён весь набор с нуля. Первые output-page пробы остановились на отсутствии development index; они сохранены в native-pages-initial. Оба диагностических препятствия устранены и перепроверены. Дополнительно сохранены timeout-диагностики при конкурентных запусках; повтор проводится без изменения readiness/сравнений. Исходный сервер возвращал 404 на браузерный /favicon.ico; отдельный read-only acceptance server на51753 отвечает на этот служебный запрос204. Компонентные requests не перехватываются. Принятая матрица явно слушает console.error/pageerror/requestfailed; исходный сервер51752 и приложение не изменены.

## Реальное приложение и ограничения

700 защищённых файлов (пакет, исходный TestApp и общая fixture) неизменны по SHA. Проверены home, confirm selection/No, три другие вкладки и responsive wide navigation. Существующие Main.scss/Application.scss, navigation UI и font-awesome сохранены. Старые build warnings о navigation images встречаются и в исходном Classic; новых warnings нет. Не добавлялись app-specific theme fixes.

Поставка — исходный theme package, собираемый потребляющим приложением; отдельный precompiled standalone package не обещан, standalone build — NOT_REQUIRED. Ext JS7.9 — NOT_RUN, отдельная необязательная TASK-018. Это завершение технической матрицы 7.7, не новое одобрение полного дизайна пользователем и не гарантия для всех сторонних приложений/браузеров.

Доказательства: acceptance-matrix.json, build-commands.json, development-output-commands.json, browser-availability.json, browsers/*/browser-results.json, native-page-comparison.json, native-pages-*.json, source-resource-mode-audit.json, build-mode-validation.json, original-app-testing.json. Все команды и exit codes сохранены; скриншоты доступны в review.html. Следующая задача: TASK-017 (поставка и итоговый отчёт).
'''
write(A/'acceptance-report.md',report)
cards=[]
for b in browsers:
 name=b['browser']['name']
 for mode in ['testing','development','production']:
  for theme in ['classic','nordic']:
   p=f'native-pages/{name}/real/{mode}/dpr-1/{theme}/home-tall.png'
   cards.append(f'<figure><figcaption>{name} {b["browser"]["version"]} · {mode} · {theme}</figcaption><a href="{p}"><img loading="lazy" src="{p}"></a></figure>')
write(A/'review.html','<!doctype html><meta charset="utf-8"><title>TASK-016 acceptance</title><style>body{font:14px Arial;background:#f4f7fc;color:#25374d;margin:24px}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}figure{margin:0;background:white;padding:8px;border:1px solid #b7c8dc}img{width:100%}figcaption{margin-bottom:8px}a{color:#32618b}</style><h1>TASK-016 · PASS</h1><p>17 successful build invocations · 3 browsers · 3 modes · DPR1/2 · 144 actual-output pairs / 40,230 elements: exact metrics.</p><p><a href="acceptance-report.md">Report</a> · <a href="acceptance-matrix.json">Matrix</a> · <a href="native-page-comparison.json">Native metrics</a> · <a href="source-resource-mode-audit.json">Source/resource audit</a></p><div class="grid">'+''.join(cards)+'</div>')
p=R/'docs/plans/nordic-blue/tasks/TASK-016.md';s=p.read_text(encoding='utf-8-sig').replace('Статус: IN_PROGRESS','Статус: DONE').replace('- [ ]','- [x]');s=s[:s.index('## Запись исполнителя')]+'''## Запись исполнителя

- Изменения: отдельные theme-acceptance descriptors, local.properties для упаковки development pages, tools/nordic-blue-acceptance и отчёты. SDK/theme/app sources не менялись (700 SHA).
- 17 сборок exit0; SDK7.7.0.31/Cmd7.7.0.36, Edge155/Chromium156/Firefox152. Полные версии/команды в acceptance-matrix/build-commands.
- Каждый браузер: 204 fixture +236 action/state pairs, 20 core flows. Реальные output pages:144pairs/40230elements, PASS. Все648resources×6outputs, manifest flags и cache reload — PASS.
- Старые navigation warnings сохранены; standalone precompiled package NOT_REQUIRED; SDK7.9 NOT_RUN. Диагностика Firefox157 и development CLI сохранена отдельно и не считается PASS.
- [Отчёт](../../../../artifacts/nordic-blue/TASK-016/acceptance-report.md), [галерея](../../../../artifacts/nordic-blue/TASK-016/review.html).
- Следующая задача: TASK-017.
''';write(p,s)
p=R/'docs/plans/nordic-blue/README.md';s=p.read_text(encoding='utf-8-sig');start=s.index('Статус:');end=s.index('\n\n',start);s=s[:start]+'Статус: IN_PROGRESS. TASK-001–016 выполнены; обязательная матрица SDK7.7.0.31 пройдена. Следующий этап — TASK-017: поставка и итоговый отчёт. TASK-018 (7.9) необязательна и не выполнена.'+s[end:];s=s.replace('| 014, 015 | IN_PROGRESS |','| 014, 015 | DONE |');write(p,s)
p=R/'AGENTS.md';write(p,p.read_text(encoding='utf-8-sig')+'''
## Build/browser integration acceptance (TASK-016)

Completed2026-10-24: SDK7.7.0.31/Cmd7.7.0.36, 17 successful invocations. development/testing/production actual output pages passed in Edge155.0.4283.62, Chromium156.0.8078.4 and Firefox152.0.4 at DPR1/2. Per browser:204 fixture+236action/state pairs+20core flows; actual outputs144pairs/40230elements total, no exact metric/state drift. All648resources×6Nordic outputs SHA-verified; 36manifest pairs/runtime flags match except added Nordic package. 700 protected sources unchanged. Existing app-specific navigation image warnings remain baseline warnings, not a new regression.

TestApp/theme-acceptance/{classic,nordic} descriptors rebase original app paths and theme/output only. local.properties in these two directories and theme-lab enables skip.page=0/skip.js=0 because installed Cmd development defaults skip both; packaging only. Original TestApp descriptor/classes/Sass unchanged. Do not use unsupported CLI -Dskip flags. Tools/evidence are fixed to this Windows acceptance run; do not overwrite accepted outputs. Read tools/nordic-blue-acceptance/README.md.

Firefox157 diagnostic failed browser-context cleanup; partial data is not PASS. Compatible152 full retry is accepted. Standalone precompiled theme package not promised: NOT_REQUIRED; source package app builds validated. SDK7.9 NOT_RUN/optional018. Report artifacts/nordic-blue/TASK-016/acceptance-report.md. Next017; full-theme final user approval is not implied by technical matrix.
''')
p=R/'README.md';s=p.read_text(encoding='utf-8-sig');s=s.replace('TASK-001–015','TASK-001–016').replace('TASK-001 through TASK-015','TASK-001 through TASK-016');s=s.replace('окончательная матрица сборок/интеграции и поставка остаются **TASK-016/017**','матрица сборок/интеграции TASK-016 пройдена; поставка остаётся **TASK-017**');s+='\n## Build/browser acceptance\n\nTASK-016 passed actual development/testing/production pages in Edge155, Chromium156 and Firefox152 at DPR1/2, including unchanged real TestApp views and app Sass. [Report](artifacts/nordic-blue/TASK-016/acceptance-report.md), [review](artifacts/nordic-blue/TASK-016/review.html), [harness](tools/nordic-blue-acceptance/README.md). Delivery documentation remains TASK-017; SDK7.9 is not tested.\n';write(p,s)
diagnostics=A/'harness-diagnostics';diagnostics.mkdir()
for name in ['prepare_task016.py','build_task016.py','build_task016_development_pages.py','enable_task016_development.py','restart_task016_final.py','run_task016_browser.py','resume_task016_firefox.py','console_task016.py','server_task016.py','retry_native_task016.py','audit_task016.py','finish_task016.py']:
 shutil.copy2(Path(__file__).parent/name,diagnostics/name)
files=[p for p in A.rglob('*') if p.is_file() and p.name!='artifact-manifest.json']
manifest={'status':'PASS','scope':'All TASK-016 local evidence, including clearly labelled failed diagnostics; compiled outputs/dependencies are excluded from Git, not from local build inputs.','files':[{'path':p.relative_to(A).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)]}
write(A/'artifact-manifest.json',json.dumps(manifest,indent=2));print('TASK-016 DONE;',len(files),'evidence files hashed')
