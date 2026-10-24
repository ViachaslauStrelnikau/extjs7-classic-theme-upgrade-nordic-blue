from pathlib import Path
import json,hashlib,shutil,re
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');O=Path(__file__).parent/'output/task008';D=O/'documents';D.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
policy=read(R/'config/nordic-blue-policy.json');icons=read(R/'config/nordic-blue-icons.json')
for name in ['geometry-comparison.json','lint-report.json','compiler-consumption.json','policy-controls.json']:assert read(O/name)['status']=='PASS'
log=(R/'artifacts/nordic-blue/TASK-008/build-lab-nordic.log').read_text(encoding='utf-8-sig')
assert '[WRN]' not in log and '[ERR]' not in log
protected=read(R/'artifacts/nordic-blue/TASK-008/protected-inputs.json')
assert all(sha(R/p)==h for p,h in protected.items())
baseline=read(R/'artifacts/nordic-blue/TASK-006/input-hashes.json')
changed=[p for p,h in baseline.items() if sha(R/p)!=h]
expected_prior=read(R/'artifacts/nordic-blue/TASK-007/post-install-guards.json')['baselineSourceChanges']
assert changed==expected_prior,(changed,expected_prior)
for version in ['ext-7.7.0.31/version.properties','TestApp/ext/version.properties']:
 assert 'version.full=7.7.0.31' in (R/version).read_text()
manifest=read(R/'artifacts/nordic-blue/TASK-004/icon-manifest.json');inherited=[]
for entry in manifest['entries']:
 if entry['id'].startswith('adapter/'):continue
 p=R/'TestApp/build/theme-lab/nordic/testing/resources'/entry['resource']
 assert p.exists() and sha(p)==entry['sourceSha256'],entry['resource']
 inherited.append({'id':entry['id'],'resource':entry['resource'],'sha256':sha(p),'status':'UNCHANGED_CLASSIC'})
(O/'inherited-icons.json').write_text(json.dumps({'status':'PASS','count':len(inherited),'entries':inherited},indent=2),encoding='utf-8')
(O/'source-guards.json').write_text(json.dumps({'status':'PASS','protectedApplicationInputs':len(protected),'sdkSassFiles':len(policy['sdkSources']),'baselineInputs':len(baseline),'changesComparedWithTask006':changed,'note':'Only documented TASK-007 instructions/profile/readme differences pre-exist. No additional baseline inputs changed during TASK-008; source SDK and original TestApp config/code/common fixture are intact.'},indent=2),encoding='utf-8')
def write(rel,text):
 p=D/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
rows=['# TASK-008 — точная карта цветовых назначений','','Все строки реально потребляются compiled CSS; доказательство: compiler-consumption.json. Метрики и изображения не переопределены.','','| SDK variable | Nordic value | Theme source | SDK declaration |','|---|---|---|---|']
for name,v in policy['allowColorOverrides'].items():
 decl=v['declarations'][-1]
 rows.append('| `$'+name+'` | `'+v['rhs']+'` | `'+v['path']+'` | `'+decl['path']+':'+str(decl['line'])+'` |')
write('artifacts/nordic-blue/TASK-008/variable-allowlist.md','\n'.join(rows)+'\n')
report=f'''# TASK-008 — палитра и проверенный allowlist: DONE

Дата: 2026-10-23. SDK 7.7.0.31 / Cmd 7.7.0.36 / Java 8. Эта задача создаёт цветовую основу, не завершает тему.

## Реализация

- В `TestApp/packages/local/theme-nordic-blue/sass/var/all.scss` заданы все **15 canonical Nordic tokens** из palette.md через `dynamic()`. Короткие aliases таблицы PDF (`nb-header` и подобные) не вводились. Значения из PDF не объявляются результатом точного замера screenshot.
- **52 color-only SDK variables** распределены по 13 реальным Ext namespace files: 50 проверенных в TASK-002 плюс `$button-default-border-color-over = $nb-accent-hover` и `$form-field-empty-color = $nb-muted`. Эти два существующих SDK hook используют последние два токена; не добавлены пустые/imageless/glyph hooks.
- Явные компонентные исключения PDF сохранены: Grid header `#EAF0F8`, Window border `#AFC2D9`, Grid header trigger `transparent`. Они не размножают базовые 15 tokens.
- `package.json` сохранён в штатной Cmd структуре. Единственное необходимое изменение конфигурации: добавить `${{package.dir}}/sass/var/all.scss` первым в `sencha.sass.var`, перед каталогом. В реальном Cmd 7.7 автоподключение package all.scss не сработало; первый build завершился `Reference to undeclared variable: $nb_surface`. Исправлен explicit import для app и slicer; отклонённый build сохранён в `build-missing-token-import.log`.
- Общий `$base-color`, fonts, sizes, padding, radius, positions, image/glyph flags, UI mixins, JS overrides и новые icons не вводились. Classic gradients пока наследуются. `overrides/` и source `resources/images/` пусты.

## Политика и команда

- `config/nordic-blue-policy.json`: точный allowlist имён/значений/файлов, 300 хешей SDK Sass, ссылки на declarations/consumers, защищённый generated package config. Все остальные overrides отклоняются.
- `config/nordic-blue-icons.json`: привязка к одобренному v2 manifest/approval по SHA-256, **648** уникальных runtime path contracts для 1x/2x PNG/GIF, exact bytes/dimensions, CSS sheet size и sprite contracts. 2x не удваивает размер в CSS. Все 182 vector masters также сверяются с одобренными hashes.
- `tools/lint-nordic-blue.py`: read-only, только Python standard library, не запускает сборку и не меняет файлы. SCSS допускает лишь конкретные `dynamic(color/token)` assignments. Произвольный CSS/import/function/mixin, metric/image/position variable, неизвестные имена и runtime JS/font файлы запрещены.
- Image resources распознаются по manifest, но `integrationEnabled=false`: рабочее подключение резервируется до TASK-013 и остальных её зависимостей. Смена bitmap/CSS размеров, density или sprite contract выявляется. Geometry adapters сейчас не разрешены; их точное CSS и данные потребуется проверить на TASK-013, широкого исключения для background-size/position нет.

Из корня проекта:

```powershell
& 'C:\\Users\\Damned\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe' tools/lint-nordic-blue.py --check-icon-candidates
```

Можно использовать `python tools/lint-nordic-blue.py --check-icon-candidates`, если Python доступен на PATH. Флаг `--report <path>` сохраняет JSON отчёт. Проверенный результат: **PASS, exit 0**, 15 tokens, 52 overrides, 300 SDK files, 648 candidate contracts. Никакие новые test suites приложения не добавлялись; контрольные изменения ниже — обязательная проверка policy этой карточки.

## Доказательство использования переменных

Из реального Cmd-generated stylesheet создан отдельный `compiler-probe/consumption-probe.scss`: перед RULE section каждому из 52 hooks назначен уникальный временный цвет. **Все 52** цвета найдены в настоящих compiled CSS declarations с примерами selectors/properties (`compiler-consumption.json`). Marker CSS не добавлялся; theme sources и рабочий compiled CSS sentinel values не получали. Отдельный Fashion probe использует тот же встроенный Node/Fashion, exit 0; imports относительные на диске D (Windows absolute import из внешней копии Fashion интерпретировал неправильно, этот служебный probe исправлен до принятия доказательства).

**33 policy controls: PASS.** Положительные проверки принимают разрешённый color hook и одобренные 1x/2x contracts. Отрицательные выявляют padding/font/radius, global base-color, image/gradient/position change, неизвестную переменную, token alias, неверный namespace/value, новый UI/JS/font, непросмотренный image, изменение bitmap/CSS size, sprite contract, early icon integration, duplicate/missing assignments и изменение package config. Все изменения сделаны в памяти или disposable копии малого child package, не в SDK/приложении. Полный список: `policy-controls.json`.

## Реальная сборка и геометрия

Рабочая папка `TestApp/theme-lab`:

```powershell
..\\..\\node_modules\\@sencha\\cmd-windows\\dist\\sencha.exe app build lab-nordic testing
```

Окончательный build: **exit 0**, без `[WRN]`/`[ERR]`; output `TestApp/build/theme-lab/nordic/testing/app.json`, CSS `resources/NordicThemeLab-all.css` (SHA-256 `{sha(R/'TestApp/build/theme-lab/nordic/testing/resources/NordicThemeLab-all.css')}`). Полный build log сохранён. Java 8 + bundled Node в PATH как TASK-007. Вызов при выполнении использовал эквивалентный `-cwd=.../TestApp/theme-lab` из staging workspace.

Один неизменённый fixture, Edge 155.0.4283.62, Windows, 1280×1600, en-US, Europe/Minsk, фиксированная дата, software raster/sRGB и GIF frame0 policy принятого TASK-006. При DPR1 и DPR2 снято **102 сценария × 2 = 204 raw PNG/JSON pairs**. Сравнены **11 280 elements и 1 926 icon observations**: геометрия/типографика/box model/offsets/focus/data/scroll/opacity совпадают точно, без 1px tolerance; нет пустых выборок, duplicates, runtime errors или 404. В color comparison исключены только перечисленные paint properties и цветовые части gradient/shadow; их структура и все остальные параметры сравниваются. **Pixel equality с Classic не заявляется**: палитра изменилась. Визуальная приёмка состояний/gradients и полный release gate остаются следующим задачам.

Все **180** родительских icon resources, намеченных к будущей замене, пока побайтово совпадают с Classic (`inherited-icons.json`); два adapter resources ещё не подключены. Одобренные masters/candidates не редактировались. Контроль 1474 baseline source inputs показал лишь ранее документированные изменения инструкций TASK-007; оригинальные TestApp app.json/code и обе SDK не менялись (`source-guards.json`).

## Продолжение

TASK-008 DONE. Следующая задача по порядку — **TASK-009**, Panel/Window/Toolbar/Button: полная палитра состояний, отдельное решение по gradients, визуальные/геометрические доказательства. 010–012 также получили выполненную зависимость 008. Новые значки остаются до TASK-013. Готовность всей темы не заявляется.
'''
write('artifacts/nordic-blue/TASK-008/palette-policy-report.md',report)
card=(R/'docs/plans/nordic-blue/tasks/TASK-008.md').read_text(encoding='utf-8-sig').replace('Статус: IN_PROGRESS','Статус: DONE').replace('- [ ]','- [x]')
card=card[:card.index('## Запись исполнителя')]+'''## Запись исполнителя

- Выполнено 2026-10-23. В package sass/var/all.scss — 15 dynamic tokens. В 13 namespace files — 52 проверенных color hooks; все реально потребляются CSS, все токены используются. Единственные добавления к TASK-002: hover border кнопки и placeholder color поля.
- package.json: explicit sass/var/all.scss перед var directory; реальная сборка Cmd показала необходимость для app/slicer. Generated структура сохранена, SDK/application не изменены.
- Policy: config/nordic-blue-policy.json, config/nordic-blue-icons.json; команда `python tools/lint-nordic-blue.py --check-icon-candidates` (проверена bundled Python 3.12.14). PASS/exit 0; 300 SDK files, 648 image contracts, 182 approved masters; source resources/images и overrides пусты.
- 33 policy controls PASS, включая реальные padding/font size, sprite position, 2x CSS size, JS override и manifest geometry mutation. Integration disabled до TASK-013.
- `app build lab-nordic testing` с Cmd 7.7.0.36 / SDK 7.7.0.31: exit 0, без warnings/errors. Первый отказ с отсутствующим token import сохранён отдельно; причина исправлена.
- Geometry: 102 сценария × DPR1/2, 11 280 element и 1 926 icon comparisons; ноль расхождений метрик/типографики/offsets. Цветовые отличия ожидаемы; pixel equality не заявляется. 180 parent icon assets пока unchanged.
- [Отчёт](../../../../artifacts/nordic-blue/TASK-008/palette-policy-report.md), [compiler proof](../../../../artifacts/nordic-blue/TASK-008/compiler-consumption.json), [policy controls](../../../../artifacts/nordic-blue/TASK-008/policy-controls.json), [geometry](../../../../artifacts/nordic-blue/TASK-008/geometry-comparison.json).
- Ограничения: state palette/gradients/компонентная визуальная приёмка — TASK-009–012, icons — TASK-013, release checks — TASK-014–016.
- Следующая задача: TASK-009.
'''
write('docs/plans/nordic-blue/tasks/TASK-008.md',card)
index=(R/'docs/plans/nordic-blue/README.md').read_text(encoding='utf-8-sig')
index=index.replace('Палитра и иконки в тему ещё не интегрированы.','TASK-008 завершена: введены 15 токенов, 52 color hooks и проверенный lint; геометрия DPR1/2 сохранена. Компонентные состояния и новые иконки ещё впереди.')
index=index.replace('| 002, 007 | TODO |','| 002, 007 | DONE |')
write('docs/plans/nordic-blue/README.md',index)
palette=(R/'docs/plans/nordic-blue/palette.md').read_text(encoding='utf-8-sig')
palette=palette.replace('Это значения для реализации; они ещё не применены.','TASK-008: базовые значения применены к теме через dynamic tokens и 52 SDK color hooks; компонентная приёмка состояний/gradients остаётся TASK-009–012.')
palette=palette.replace('Назначения Nordic ещё не применялись.','Назначения Nordic применены и проверены в TASK-008; полная карта находится в config/nordic-blue-policy.json и artifacts/nordic-blue/TASK-008/variable-allowlist.md.')
palette+='''
## TASK-008: активная цветовая основа

Все 15 canonical tokens находятся в package sass/var/all.scss; explicit entry в package.json sencha.sass.var обеспечивает включение в Cmd 7.7 app и slicer. 50 исходных назначений сохранены; дополнительно `$button-default-border-color-over: dynamic($nb-accent-hover)` и `$form-field-empty-color: dynamic($nb-muted)` используют остальные токены. Декларации/consumers подтверждены локальным SDK; изолированный Fashion probe доказал compiled usage всех 52 hooks. Короткие aliases PDF не вводятся. Grid header #EAF0F8, Window border #AFC2D9 и transparent trigger остаются конкретными исключениями из таблицы.

Команда read-only policy: `python tools/lint-nordic-blue.py --check-icon-candidates` из корня. Геометрия и fonts совпали с Classic в 102 сценариях при DPR1/2; цвета изменились намеренно. Подробности — artifacts/nordic-blue/TASK-008/palette-policy-report.md. Gradients, дополнительные state colors и component visual acceptance — следующие задачи; эта запись не означает готовность темы.
'''
write('docs/plans/nordic-blue/palette.md',palette)
agents=(R/'AGENTS.md').read_text(encoding='utf-8-sig')
agents+='''
## Color policy and lint (TASK-008)

The initial palette now uses 15 canonical dynamic tokens and 52 verified SDK color hooks in namespace files. `package.json` must explicitly include `${package.dir}/sass/var/all.scss` before the var directory: installed Cmd 7.7 did not auto-include package all.scss in app/slicer builds. Preserve this reviewed configuration.

Before building any theme change, run from the project root:

```powershell
& 'C:\\Users\\Damned\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe' tools/lint-nordic-blue.py --check-icon-candidates
```

The script is read-only and uses the Python standard library; `python tools/lint-nordic-blue.py --check-icon-candidates` also works with a configured Python. Policies live in config/nordic-blue-policy.json and config/nordic-blue-icons.json. Unlisted variables, geometry/typography/image/position assignments, global base-color, arbitrary CSS/UI mixins, extra runtime JS/fonts, changed protected config and unapproved image bytes/contracts fail. Exact approved 1x/2x bitmap/CSS-size/sprite contracts are recognized; icon integration is still disabled until TASK-013. No broad background-size/position exception is allowed. Any policy expansion needs SDK declarations/actual compiled consumers and the relevant component geometry review; do not weaken the policy to hide a regression. State/gradient refinements remain TASK-009–012. TASK-008 report records 33 controls and strict DPR1/2 geometry evidence; this is not theme release acceptance.
'''
write('AGENTS.md',agents)
write('tools/README.md','''# Nordic Blue source policy

From the project root run `python tools/lint-nordic-blue.py --check-icon-candidates` (standard library only). The verified bundled Python command is in AGENTS.md. Use `--report <path>` to save JSON. The script reads files and returns exit 0 for PASS, 1 for policy violations; it does not build the application.

`config/nordic-blue-policy.json` binds 15 tokens, exact color assignments, Ext namespace paths, SDK hashes and reviewed package configuration. `config/nordic-blue-icons.json` binds approved 1x/2x bytes, original logical sheet size and sprite contracts. Candidate validation checks all known exports and masters; integration remains disabled until TASK-013. Arbitrary stylesheet rules, UI mixins, geometry overrides and runtime JS are rejected. Future component/asset exceptions require explicit evidence and narrow reviewed policy entries.

Evidence and the 33 positive/negative controls are in artifacts/nordic-blue/TASK-008. Do not run preparation/installation helpers from those evidence files as routine checks: they reproduce historical mutations, while this lint command is read-only.
''')
expected={str(p.relative_to(D)).replace('\\','/'):sha(R/p.relative_to(D)) if (R/p.relative_to(D)).exists() else None for p in D.rglob('*') if p.is_file()}
(O/'document-expected.json').write_text(json.dumps(expected,indent=2),encoding='utf-8')
commands={'generateSources':'prepare_task008.py -> guarded install_task008_sources.py; package explicit token import fix recorded separately',
 'build':{'cwd':'TestApp/theme-lab','command':'..\\..\\node_modules\\@sencha\\cmd-windows\\dist\\sencha.exe app build lab-nordic testing','equivalentActualInvocation':'sencha.exe -cwd=D:\\Projects\\Extjs7ClassicThemeUpgradeNordicBlue\\TestApp\\theme-lab app build lab-nordic testing','sdk':'7.7.0.31','cmd':'7.7.0.36','java':'1.8.0_501','exitCode':0,'earlierExitCode':321,'earlierFailure':'Missing explicit package token import; build-missing-token-import.log'},
 'lint':{'command':'python tools/lint-nordic-blue.py --check-icon-candidates','exitCode':0},
 'policyControls':{'command':'python policy-controls.py','controls':33,'exitCode':0},
 'compilerProbe':{'command':'Cmd bundled Node fashion.js compile compiler-probe/consumption-probe.scss compiler-probe/consumption-probe.css','exitCode':0,'actualConsumers':52},
 'captures':{'commands':['NORDIC_CPU_RASTER=1 modern-node capture.cjs 1 1','NORDIC_CPU_RASTER=1 modern-node capture.cjs 2 1'],'exitCodes':[0,0],'browser':'155.0.4283.62'},
 'geometryComparison':{'command':'python compare-geometry.py','exitCode':0}}
(O/'commands.json').write_text(json.dumps(commands,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':'PREPARED','documentFiles':len(expected),'parentIconsUnchanged':len(inherited),'buildWarnings':0}))
