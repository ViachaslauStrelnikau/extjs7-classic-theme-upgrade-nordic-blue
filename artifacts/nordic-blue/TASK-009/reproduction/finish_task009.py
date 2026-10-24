from pathlib import Path
import json,hashlib,shutil
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent/'output/task009';D=O/'documents';D.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['phase-a-geometry.json','flat-geometry.json','core-state-comparison.json','compiler-consumption.json','policy-controls.json','lint-report.json']:
 assert read(O/name)['status']=='PASS',name
policy=read(R/'config/nordic-blue-policy.json');assert len(policy['allowColorOverrides'])==104 and len(policy['allowGradientOverrides'])==14
assert read(O/'core-state-comparison.json')['pairComparisons']==56
assert len(read(O/'core-state-comparison.json')['paintChecks'])==168
assert all(sha(R/p)==h for p,h in read(R/'artifacts/nordic-blue/TASK-009/protected-inputs.json').items())
assert all(sha(R/p)==h for p,h in policy['sdkSources'].items())
for name in ['build-phase-a.log','build-flat.log']:
 text=(R/'artifacts/nordic-blue/TASK-009'/name).read_text(encoding='utf-8-sig');assert '[ERR]' not in text and '[WRN]' not in text
manifest=read(R/'artifacts/nordic-blue/TASK-004/icon-manifest.json');unchanged=[]
for entry in manifest['entries']:
 if entry['id'].startswith('adapter/'):continue
 p=R/'TestApp/build/theme-lab/nordic/testing/resources'/entry['resource'];assert sha(p)==entry['sourceSha256']
 unchanged.append({'resource':entry['resource'],'sha256':sha(p)})
(O/'inherited-icons.json').write_text(json.dumps({'status':'PASS','count':len(unchanged),'resources':unchanged},indent=2),encoding='utf-8')
baseline=read(R/'artifacts/nordic-blue/TASK-006/input-hashes.json');changes=[p for p,h in baseline.items() if sha(R/p)!=h]
assert not [p for p in changes if p.startswith(('TestApp/ext/','ext-7.7.0.31/','TestApp/app/')) or p=='TestApp/theme-lab/fixture.js'],changes
(O/'source-guards.json').write_text(json.dumps({'status':'PASS','sdkSassFiles':300,'originalApplicationInputs':18,'baselineInputsCompared':len(baseline),'baselineDifferences':changes,'note':'Only existing project instruction/readme/profile changes; SDK, application sources/config and common fixture unchanged. Source overrides/images empty.'},indent=2),encoding='utf-8')
for name in ['focus-palette-decision.json','focus-pressed-decision.json']:
 data=read(O/name);data['status']='PASS';data['validation']='Final core-state-comparison.json: all 168 state paint pairs distinct, all 56 Classic/Nordic geometry pairs match.'
 (O/name).write_text(json.dumps(data,indent=2),encoding='utf-8')
def write(rel,text):
 p=D/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
css=R/'TestApp/build/theme-lab/nordic/testing/resources/NordicThemeLab-all.css'
report=f'''# TASK-009 — Panel, Window, Toolbar, Button: DONE

Завершено 2026-10-24 (Europe/Minsk). Рабочий SDK 7.7.0.31 / Cmd 7.7.0.36 / Java 8. Это промежуточный этап темы; release acceptance остаётся впереди.

## Изменения

- `sass/var/panel/Panel.scss`: цвет текста body, framed background, inner header border и focus outlines, дополнительно к цветам TASK-008. Normal/framed/collapsed/disabled используют неизменённую конструкцию Classic.
- `sass/var/window/Window.scss`: body/background/inner border в Nordic palette, body text; сохранены Classic radius, header padding, border widths, modal mask, drag/resize behavior и существующая тень. Новые тени не добавлялись.
- `sass/var/toolbar/Toolbar.scss`: text, footer, separators и surfaces; normal/overflow/open/disabled покрыты.
- `sass/var/button/Button.scss`: все семь normal/hover/focus/pressed/focus-over/focus-pressed/disabled состояний default и toolbar family. Цвет текста остаётся Nordic text; disabled использует унаследованное ослабление opacity Classic. Split/menu arrow boxes, hit areas и images не менялись.
- Всего активно **104 color hooks**: 52 из TASK-008 + 52 новых. Все подтверждены installed SDK и фактическим compiled consumption. Проверка сначала выявила 14 неиспользуемых inner-border hooks; они удалены вместо включения внутренних рамок. Удаление дало byte-identical CSS/resources, доказательство `prune-output-identity.json` относится к этому этапу до последующих state-color fixes.

## Градиенты и особенности SDK

Сначала собрана полная state palette с наследуемыми gradients (phase A): **22 сценария × DPR1/2**, **2738 element comparisons**, zero drift. Только после этого разрешены **14** конкретных `dynamic('none')` assignments: Panel header, Toolbar background, 7 default button gradients, 5 toolbar button interaction gradients. Window header уже flat в родительском SDK. Radius/frame padding/widths и shadow geometry унаследованы.

Lint допускает эти 14 hooks только по точным имени/пути/value и SHA-связанному `gradient-review.json`, который ссылается на принятый phase-A geometry report. Остальные gradients и любой произвольный CSS/selector/UI mixin/JS override остаются запрещены. Политика была расширена проверенными toolbar gradient declarations, отсутствовавшими в первоначальном общем списке TASK-002.

Попарная проверка обнаружила особенность `theme-neutral/sass/var/button/Button.scss`: комбинированные backgrounds не выводятся, когда равны соответствующим over/pressed значениям. Из-за specificity keyboard focus мог скрыть hover или pressed. Исправлено только штатными цветами:

| State | Background | Border / indicator |
|---|---|---|
| normal | nb-control-bg (toolbar transparent) | nb-border (toolbar transparent) |
| hover | nb-control-hover | nb-accent-hover |
| focus | nb-control-bg | nb-accent + inherited dotted outline |
| pressed | nb-control-pressed | nb-accent |
| focus-over | nb-accent-soft | nb-accent + inherited dotted outline |
| focus-pressed | #C7DCF6 | nb-accent + inherited dotted outline |
| disabled | nb-control-bg (toolbar transparent) | inherited disabled opacity |

`#C7DCF6` — узкий компонентный state value: rounded RGB mix 90% `#D8E7FA` + 10% `#3275D6` = (199,220,246). 15 публичных tokens не изменились. Этот оттенок достаточно светлый для унаследованных тёмных стрелок. Причины/исправления и отклонённые comparisons сохранены в focus decision/diagnostic JSON; CSS overrides и metric changes не потребовались.

## Реальная сборка и policy

Из `TestApp/theme-lab`:

```powershell
..\\..\\node_modules\\@sencha\\cmd-windows\\dist\\sencha.exe app build lab-nordic testing
```

Фактические вызовы использовали эквивалентный `-cwd=.../TestApp/theme-lab`, Java 8 и bundled Node на PATH. Phase A и окончательный flat build: **exit 0**, без warnings/errors. Полные build logs сохранены. CSS SHA-256: `{sha(css)}`. SDK, production TestApp app.json/app.js/config и общий fixture.js не изменялись.

Read-only `python tools/lint-nordic-blue.py --check-icon-candidates`: **PASS/exit 0**, 15 tokens, 104 colors, 14 reviewed gradients, 300 SDK Sass hashes, 648 approved icon path contracts. Python 3.12.14. **39 положительных/отрицательных controls PASS**; добавлены exact reviewed gradient, неверный enum/path/color и altered-review checks. SDK declarations и consumers перечислены в policy; `compiler-consumption.json` доказывает **104** фактических CSS consumers через уникальные временные цвета в изолированном Fashion probe. Marker rules не добавлялись, рабочий CSS sentinel colors не получал.

## Итоговые сравнения

Edge 155.0.4283.62, Windows, 1280×1600, DPR1 и DPR2, en-US, Europe/Minsk. Детерминированная дата fixture остаётся 2026-10-23 как в принятом baseline; дата завершения работы и дата fixture различаются намеренно. Software raster/sRGB и first-frame GIF routing соответствуют TASK-006.

- **102 сценария × 2 DPR** окончательной сборки: raw PNG/JSON в `nordic/captures/pass-3/dpr-1` и `dpr-2`. **11 280 element comparisons, 1926 icon observations: zero geometry/typography/box/scroll/visibility/opacity/offset drift**. Нового text overflow нет: client/scroll bounds и typography сравнивались точно. Сохраняется исходное Classic clipping.
- Дополнительные **4 targets × 7 states × 2 DPR**: 56 пар Classic↔Nordic, 112 raw screenshots/JSON в `core-states-v3`. **1710 element comparisons** без отличий метрик; **168 попарных paint comparisons** подтверждают различимость всех семи состояний каждого target. Background gradients на этих кнопках отсутствуют. Hover/pressed вводятся реальной мышью, focus — стандартным API, disabled — API; фактические классы и state flags проверяются. `pressed` property не использовался как единственное доказательство: он отражает enableToggle, а pointer press проверяется по штатному x-btn-pressed.
- **20 mouse/keyboard checks PASS** (Classic/Nordic × DPR1/2): click menu/split arrow, focus on real menu item + Escape, focused normal button + Space, overflow menu + Escape, panel collapse/expand mouse. Focus menu item является явным предусловием Escape; не заявляется, что нажатие Escape с произвольным фокусом проверяет menu navigation.
- Normal/framed/collapsed panels, modal/moved/resized windows, split/menu buttons, narrow/open/disabled toolbar также вошли в общий fixture. Полная drag/resize/keyboard release matrix — TASK-014–016.
- Цвета, разрешённые gradient layers и данные профиля исключаются только из geometry comparison; image URLs/sizes/offsets и все прочие метрики сравниваются. **Pixel equality с Classic не заявляется**: оформление изменено. Raw captures сохранены; это не новые release golden snapshots.
- Все **180** parent icon resources, намеченных к замене, пока byte-identical Classic. Source images/overrides пусты, artwork approved v2 не редактировался и не интегрирован. Generated slicer frame surfaces изменены штатной компиляцией colors/gradients, не правкой SDK/resources.

Подробности: [геометрия](flat-geometry.json), [состояния и действия](core-state-comparison.json), [policy controls](policy-controls.json), [consumers](compiler-consumption.json). [Визуальное сравнение](review.html) показывает исходные raw кадры. Итоговыми являются pass-3 и core-states-v3.

### Хранение кадров при заполненном D:

Во время копирования дубликатов промежуточных кадров диск D: заполнился. Удалены только частично скопированные собственные диагностические каталоги TASK-009; оригиналы остались на C:. **Итоговые raw PNG/JSON, phase-A кадры, compiled stylesheet и source snapshots хранятся в `evidence.zip`** внутри TASK-009. Указанные выше пути — имена entries этого архива. `evidence-index.json` содержит SHA-256 архива и исходных кадров. Gallery server читает ZIP в память и показывает PNG без распаковки на D.

Предыдущие raw диагностические проходы дополнительно сохранены в `C:/Users/Damned/.codex/.chatgpt-projects/g-p-6909aeed3f508191801b816a6bd2b338/output/task009/diagnostics.zip`; их summary JSON находятся в проекте. Это локальное ограничение поставки диагностики, не изменение SDK/приложения или критериев приёмки. Полные распакованные копии всех кадров также остались в C staging. Не распаковывать архивы на D до освобождения места. Запуск просмотра: bundled Node `artifacts/nordic-blue/TASK-009/review-server.cjs` из корня проекта, открыть напечатанный loopback URL.

## Продолжение

TASK-009 DONE. Следующая задача — **TASK-010**, fields/triggers/fieldsets. TASK-011/012 ещё TODO; новые icons — TASK-013, после её зависимостей. Готовность всей темы не заявляется.
'''
write('artifacts/nordic-blue/TASK-009/core-component-report.md',report)
card=(R/'docs/plans/nordic-blue/tasks/TASK-009.md').read_text(encoding='utf-8-sig').replace('Статус: IN_PROGRESS','Статус: DONE').replace('- [ ]','- [x]')
card=card[:card.index('## Запись исполнителя')]+'''## Запись исполнителя

- Завершено 2026-10-24. SCSS Panel/Window/Toolbar/Button: core surfaces, all 7 default/toolbar button states, focus outlines и disabled colors с унаследованной opacity. Активно 104 verified color hooks (52 новых); 14 неиспользуемых inner-border hooks удалены по compiler proof.
- Gradients убраны только после phase-A comparison: 22 сценария × DPR1/2, 2738 comparisons, zero drift. Разрешены 14 конкретных dynamic('none') hooks, SHA-связанных с review evidence. Frame radius/padding/widths и тени не менялись.
- SDK combined-state omission/specificity исправлена через color variables: focus control-bg, focus-over accent-soft, focus-pressed #C7DCF6 (90% control-pressed + 10% accent, RGB rounded). Публичные 15 tokens сохранены, нет CSS/JS overrides.
- Cmd 7.7.0.36 / SDK 7.7.0.31, `app build lab-nordic testing` из theme-lab: exit 0, без warnings/errors. Lint PASS, 39 controls PASS; реальный Fashion probe подтверждает 104 compiled color consumers.
- Финальная geometry: 102 сценария × DPR1/2, 11 280 elements и 1926 icon observations без отклонений; client/scroll bounds и шрифты совпадают, нового overflow нет. Extra core states: 56 Classic/Nordic pairs / 1710 elements, 168 paint pairs distinct, 20 mouse/keyboard checks PASS.
- Все 180 parent icons пока unchanged; approved v2 не подключён. SDK/application/fixture неизменны. Full drag/resize/keyboard release gate ещё впереди.
- Диск D заполнился при копировании diagnostics. Итоговые raw кадры/JSON и snapshots сохранены losslessly в artifacts/nordic-blue/TASK-009/evidence.zip; gallery читает архив без распаковки. Предыдущие диагностические кадры дополнительно сохранены на C (storage-decision.json); SDK и исходники не удалялись.
- [Отчёт](../../../../artifacts/nordic-blue/TASK-009/core-component-report.md), [визуальный просмотр](../../../../artifacts/nordic-blue/TASK-009/review.html), [geometry](../../../../artifacts/nordic-blue/TASK-009/flat-geometry.json), [states](../../../../artifacts/nordic-blue/TASK-009/core-state-comparison.json).
- Следующая задача: TASK-010. Готовность всей темы не заявляется.
'''
write('docs/plans/nordic-blue/tasks/TASK-009.md',card)
index=(R/'docs/plans/nordic-blue/README.md').read_text(encoding='utf-8-sig').replace('| 008 | TODO |','| 008 | DONE |',1)
index=index.replace('Компонентные состояния и новые иконки ещё впереди.','TASK-009 завершена: основные Panel/Window/Toolbar/Button оформлены и проверены. Следующий этап — TASK-010; остальные группы и новые иконки ещё впереди.')
write('docs/plans/nordic-blue/README.md',index)
agents=(R/'AGENTS.md').read_text(encoding='utf-8-sig')
agents+='''
## Core component refinement (TASK-009)

The active policy now contains 104 verified color hooks and 14 exact reviewed `dynamic('none')` gradient hooks. Gradient exceptions require the exact SDK name/path/value and SHA-linked artifacts/nordic-blue/TASK-009/gradient-review.json plus its phase-A geometry report. Unlisted gradients, arbitrary CSS, geometry changes and JS/UI overrides still fail lint. Do not expand these exceptions globally.

Classic's button mixin conditionally omits combined-state declarations when their values equal ordinary hover/pressed. Keyboard focus specificity can then obscure hover/pressed. Preserve the reviewed focus color choices: focus uses control-bg, focus-over uses accent-soft, focus-pressed uses #C7DCF6 (RGB 90% control-pressed + 10% accent). The latter is a component state value; the fifteen canonical tokens remain unchanged. Validate all seven states pairwise using genuine pointer focus/pressed flags, not just button.pressed (which represents enableToggle).

TASK-009 evidence: final full fixture pass-3, core-states-v3, 168 distinct paint pairs, zero metric drift, real Cmd testing build. Raw captures and snapshots are losslessly packed in artifacts/nordic-blue/TASK-009/evidence.zip because D filled during diagnostic copying; gallery server reads the archive in memory. Earlier diagnostic raw frames also remain in the C staging diagnostics.zip recorded in storage-decision.json; summary reports are in the project. Do not extract archives or run another build on D until enough space is available. Source images and overrides remain empty. Next task: TASK-010; full release acceptance and icons integration are pending.
'''
write('AGENTS.md',agents)
palette=(R/'docs/plans/nordic-blue/palette.md').read_text(encoding='utf-8-sig')
palette+='''
## TASK-009: основные компоненты

Завершено 2026-10-24: активны 104 verified color hooks и 14 отдельно проверенных flat-gradient hooks. Политика обновлена без metric overrides. Для default/toolbar buttons: normal control-bg (toolbar transparent), hover control-hover, focus control-bg + accent border/inherited outline, pressed control-pressed, focus-over accent-soft, focus-pressed #C7DCF6, disabled сохраняет Classic opacity. #C7DCF6 — компонентный state color, RGB 90% control-pressed + 10% accent, rounded; это не новый публичный token. Отличающиеся combined-state значения необходимы для реального вывода правил button mixin в SDK 7.7.

Frames/radius/padding и все шрифты наследуются. 14 unused inner-border color assignments удалены по compiler proof. Следующий этап — TASK-010; новые icon assets по-прежнему не интегрированы. Подробности: artifacts/nordic-blue/TASK-009/core-component-report.md.
'''
write('docs/plans/nordic-blue/palette.md',palette)
expected={str(p.relative_to(D)).replace('\\','/'):sha(R/p.relative_to(D)) if (R/p.relative_to(D)).exists() else None for p in D.rglob('*') if p.is_file()}
(O/'document-expected.json').write_text(json.dumps(expected,indent=2),encoding='utf-8')
commands={'completionDate':'2026-10-24','sdk':'7.7.0.31','cmd':'7.7.0.36','java':'1.8.0_501','python':'3.12.14',
 'buildCommand':'sencha.exe -cwd=D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue/TestApp/theme-lab app build lab-nordic testing','finalBuildExitCode':0,
 'lintCommand':'python tools/lint-nordic-blue.py --check-icon-candidates','lintExitCode':0,'controls':39,
 'finalCaptureCommands':['NORDIC_CPU_RASTER=1 modern-node capture.cjs 1 3','NORDIC_CPU_RASTER=1 modern-node capture.cjs 2 3'],'captureExitCodes':[0,0],
 'coreCommands':['modern-node core-review.cjs 1','modern-node core-review.cjs 2'],'coreExitCodes':[0,0],
 'finalGeometryExitCode':0,'finalCoreComparisonExitCode':0,'compilerConsumerCount':104,
 'diagnostics':'Earlier checker syntax/driver corrections and two valid detected state paint failures were resolved. Rejected comparisons and prior captures retained; only final pass-3/core-states-v3 accepted.'}
(O/'commands.json').write_text(json.dumps(commands,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':'READY_TO_INSTALL','documents':len(expected),'sourceIconsUnchanged':len(unchanged)}))
