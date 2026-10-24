from pathlib import Path
import json,hashlib,shutil
ROOT=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue')
OUT=Path(__file__).parent/'output/task007'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
comparison=read(OUT/'inheritance-comparison.json');assert comparison['status']=='PASS'
before=read(ROOT/'artifacts/nordic-blue/TASK-007/protected-inputs.json')
assert all(sha(ROOT/p)==h for p,h in before.items())
baseline=read(ROOT/'artifacts/nordic-blue/TASK-006/input-hashes.json')
source_changes=[p for p,h in baseline.items() if not (ROOT/p).exists() or sha(ROOT/p)!=h]
assert source_changes==[],source_changes
a=ROOT/'TestApp/build/theme-lab/classic/testing'
b=ROOT/'TestApp/build/theme-lab/nordic/testing'
ma,mb=read(a/'app.json'),read(b/'app.json')
assert mb['packages']['theme-nordic-blue']['extend']=='theme-classic'
assert mb['packages']['theme-nordic-blue']['included']
assert (a/'resources/NordicThemeLab-all.css').read_bytes()==(b/'resources/NordicThemeLab-all.css').read_bytes()
resource_comparisons=[];documentation_differences=[]
for p in sorted((a/'resources').rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(a/'resources');q=b/'resources'/rel
 assert q.is_file(),str(rel)
 if sha(p)!=sha(q):
  assert str(rel)=='Readme.md',str(rel)
  documentation_differences.append({'path':str(rel),'classicSha256':sha(p),'nordicSha256':sha(q),'reason':'Generated package resource-directory heading, not a loaded runtime asset.'})
  continue
 resource_comparisons.append({'path':str(rel).replace('\\','/'),'sha256':sha(p)})
assert {str(p.relative_to(a/'resources')) for p in (a/'resources').rglob('*') if p.is_file()}=={str(p.relative_to(b/'resources')) for p in (b/'resources').rglob('*') if p.is_file()}
loaded={};frozen=[]
for dpr in [1,2]:
 folder=OUT/f'nordic/captures/pass-1/dpr-{dpr}'
 for record in read(folder/'index.json')['records']:
  metric=read(folder/record['metrics'])
  assert not metric['network']['errors'] and not metric['network']['badResponses']
  assert not metric['errors'] and not metric['duplicates'] and not metric['unownedGraphics']
  for r in metric['network']['resources']:
   if '/build/theme-lab/nordic/testing/resources/' in r['url']:
    rel=r['url'].split('/build/theme-lab/nordic/testing/resources/')[1].split('?')[0]
    loaded[rel]={'status':r['status'],'sha256':sha(b/'resources'/rel)}
  frozen.extend(metric['network']['frame0Substitutions'])
proof={'status':'PASS','sdk':'7.7.0.31','cmd':'7.7.0.36',
 'package':mb['packages']['theme-nordic-blue'],
 'inheritance':['theme-nordic-blue','theme-classic','theme-neutral','theme-base'],
 'cssByteIdentical':True,'cssSha256':sha(b/'resources/NordicThemeLab-all.css'),
 'resourceFileCount':len(resource_comparisons),'resourceFiles':resource_comparisons,'documentationDifferences':documentation_differences,
 'loadedBuiltResourceCount':len(loaded),'loadedBuiltResources':loaded,
 'frozenResourceKeys':sorted({x['resource'] for x in frozen}),
 'protectedInputCount':len(before),'baselineInputCount':len(baseline),'sourceChangesBeforeDocumentation':source_changes,
 'themeSourceOverrides':list((ROOT/'TestApp/packages/local/theme-nordic-blue/overrides').iterdir()),
 'themeSourceImages':list((ROOT/'TestApp/packages/local/theme-nordic-blue/resources/images').iterdir()),
 'buildManifests':{'classic':sha(a/'app.json'),'nordic':sha(b/'app.json')}}
assert not proof['themeSourceOverrides'] and not proof['themeSourceImages']
(OUT/'inheritance-proof.json').write_text(json.dumps(proof,indent=2),encoding='utf-8')
doc=OUT/'delivery';doc.mkdir(exist_ok=True)
def write(rel,text):
 p=doc/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
commands={
 'cwdGenerate':'TestApp','generate':'..\\node_modules\\@sencha\\cmd-windows\\dist\\sencha.exe generate theme --extend=theme-classic --toolkit=classic theme-nordic-blue','generateExitCode':0,
 'cwdBuild':'TestApp/theme-lab','builds':[
  {'command':'..\\..\\node_modules\\@sencha\\cmd-windows\\dist\\sencha.exe app build lab-classic testing','exitCode':0},
  {'command':'..\\..\\node_modules\\@sencha\\cmd-windows\\dist\\sencha.exe app build lab-nordic testing','exitCode':0}],
 'environment':{'JAVA_HOME':'C:/Program Files/Java/jdk1.8.0_501','PATHprepend':'JAVA_HOME/bin;project/node_modules/@sencha/cmd-windows/dist/bin/windows/node'},
 'capture':{'node':'C:/Users/Damned/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe','commands':['NORDIC_CPU_RASTER=1 node capture.cjs 1 1','NORDIC_CPU_RASTER=1 node capture.cjs 2 1'],'exitCodes':[0,0],'browser':'155.0.4283.62','args':['--disable-gpu','--force-color-profile=srgb']},
 'rejectedAttempts':[{'command':'generate theme --extend theme-classic --toolkit classic theme-nordic-blue','exitCode':1,'reason':'Cmd consumes spaced option values incorrectly; use equals syntax.'},{'command':'app build lab-classic testing (initial new lab descriptor)','exitCode':321,'reason':'New laboratory id was not a UUID; corrected before both successful builds. Original TestApp id untouched.','log':'build-lab-classic-invalid-uuid.log'}]
}
(OUT/'commands.json').write_text(json.dumps(commands,ensure_ascii=False,indent=2),encoding='utf-8')
report=f'''# TASK-007 — пустой child theme: PASS

Дата: 2026-10-23. Это завершение основы пакета, не готовая тема Nordic Blue.

## Пакет и конфигурация

- Cmd 7.7.0.36 с Java 8 создал `TestApp/packages/local/theme-nordic-blue` в существующем workspace `TestApp/workspace.json`. Обе SDK-копии — Ext JS 7.7.0.31.
- В generated `package.json`: `name=theme-nordic-blue`, `sencha.type=theme`, `sencha.toolkit=classic`, `sencha.extend=theme-classic`. Цепочка: Nordic → Classic → Neutral → Base.
- Данный Cmd генерирует современный JSON scaffold **без `.sencha/package`**. Исходная сгенерированная структура полностью сохранена в `generated-scaffold/`; конфигурация не заменена устаревшими шаблонами. `build.xml` импортирует package build logic установленного Cmd. Если `.sencha/package` появится при будущей штатной генерации/миграции, сохранить его. Это проверенное уточнение пункта 007.1 для реальной версии Cmd.
- Сгенерированный `overrides/init.js` содержит только theme identity flags; он архивирован вместе с scaffold и исключён из активного пакета, чтобы выполнить требование пустого `overrides/`. Других JS, Ext.define overrides, новых UI, Sass правил или переменных нет. `resources/images/` пуст.
- Все default UI наследуются. Утверждённый icon set v2 не интегрирован (TASK-013).

## Реальные сборки

Команды и exit codes: [commands.json](commands.json). Успешные `lab-classic testing` и `lab-nordic testing`: exit 0, без `[WRN]` и `[ERR]`; полные журналы сохранены рядом. Неудачная первоначальная конфигурация с неправильным UUID также сохранена отдельно и исправлена до успешных builds.

Сборочный descriptor `TestApp/theme-lab/app.json` использует тот же workspace/SDK и `build-requires.js` с полным набором fixture классов. Отдельные профили располагаются здесь, а не в production `TestApp/app.json`: обычные пользовательские `app build testing` / `app watch` остаются без изменений. Нет копии SDK или новых component configs. Один `fixture.js` обслуживает Classic и Nordic; лабораторный loader использует скомпилированный CSS реального manifest и полный неизменённый SDK JS, не запускает production Main.

Outputs:
- `TestApp/build/theme-lab/classic/testing/app.json`
- `TestApp/build/theme-lab/nordic/testing/app.json`
- соответствующие `resources/NordicThemeLab-all.css`

CSS обоих builds **побайтово одинаков**: SHA-256 `{proof['cssSha256']}`. Все {len(resource_comparisons)} runtime файлов resources обоих builds также побайтово совпадают, включая созданные Cmd slicer assets. Единственное отличие каталога resources — generated `Readme.md` с названием пакета; этот Markdown не загружается приложением. {len(loaded)} различных built resources реально загружены стендом без 404/ошибок. Новые иконки и цвета в теме отсутствуют.

## Сравнение с зафиксированным Classic TASK-006

- Edge 155.0.4283.62 / Windows, 1280×1600, DPR 1 и 2, en-US, Europe/Minsk, фиксированная дата, software raster + sRGB как в принятом baseline.
- 102 сценария при каждом DPR: всего 204 raw PNG и 204 JSON измерений.
- **11 280 сравнений элементов и 1 926 icon observations: ноль отличий** геометрии, шрифтов, box model, paint, offsets, scroll, data и focus state. Пустые выборки, duplicates, unowned graphics и runtime errors отсутствуют.
- Адреса ресурсов приведены к одному логическому корню только для сравнения строк URL; имена, offsets, размеры и bytes не менялись. Сведения о выбранном профиле проверены отдельно от остального окружения.
- Пиксели Ext fixture совпадают без допуска. В raw PNG отличается имя темы в нативном HTML select и служебной подписи стенда. Исключены только прямоугольник этого select и измеренный DOM Range суффикса подписи для каждого сценария; весь остальной кадр сравнивается. Никакие triggers/tools/текст компонентов не маскируются. Raw PNG и raw diff с различиями подписи сохранены. Точные области: `lab-chrome.json`.
- Семь анимированных Classic GIF стабилизированы тем же first-frame browser routing, что в baseline; перед снимками реальные bytes в обоих builds проверены по исходным Classic SHA-256. SDK и build файлы не переписывались. Это политика только данного сравнения пустого child; после замены значков нужно выводить кадр из фактического нового asset.
- Принятый TASK-006 baseline не перезаписан. Все {len(baseline)} его source inputs и {len(before)} дополнительно защищённых файлов совпали с исходными SHA до обновления документации. `TestApp/app.json`, app.js, build.xml, workspace.json, index.html, application sources и fixture.js не изменены.

Подробности: [inheritance-comparison.json](inheritance-comparison.json), [inheritance-proof.json](inheritance-proof.json), raw captures `nordic/captures/pass-1/dpr-1` и `dpr-2`. Это не полная функциональная/release matrix: расширенные проверки TASK-014–016 ещё впереди.

## Продолжение

TASK-007 DONE. Следующая задача — TASK-008: разрешённая палитра и проверенный Sass allowlist. Не подключать значки до TASK-013 и не заявлять готовность темы по этому отчёту.
'''
write('artifacts/nordic-blue/TASK-007/inheritance-report.md',report)
card=(ROOT/'docs/plans/nordic-blue/tasks/TASK-007.md').read_text(encoding='utf-8-sig').replace('Статус: IN_PROGRESS','Статус: DONE').replace('- [ ]','- [x]')
card=card[:card.index('## Запись исполнителя')]+'''## Запись исполнителя

- Выполнено 2026-10-23. Пакет: `TestApp/packages/local/theme-nordic-blue`. `package.json` содержит type=theme, toolkit=classic, extend=theme-classic; default UI наследуются, overrides/images пусты.
- Уточнение 007.1: установленный Cmd 7.7.0.36 создаёт JSON scaffold без `.sencha/package`; оригинал сохранён в artifacts/nordic-blue/TASK-007/generated-scaffold. Не подменять современный scaffold устаревшей конфигурацией.
- Лабораторный descriptor: `TestApp/theme-lab/app.json`, build.xml, build-entry.html; два профиля, один fixture. Production TestApp sources/config не изменены.
- Реальные `app build lab-classic testing` и `app build lab-nordic testing`: exit 0. Команды и журналы в TASK-007; окончательные builds без warnings/errors.
- CSS и все runtime resources builds побайтово одинаковы (отличается только незагружаемый generated Readme.md). Сравнение с TASK-006: 102 сценария × DPR1/2, 11 280 element и 1 926 icon observations; ноль отличий computed metrics и пикселей компонентов. Только имя темы в двух служебных HTML controls исключено из raster comparison; raw сохранён.
- [Отчёт наследования](../../../../artifacts/nordic-blue/TASK-007/inheritance-report.md), [детальные сравнения](../../../../artifacts/nordic-blue/TASK-007/inheritance-comparison.json).
- Ограничение: пустая тема, без палитры/новых icons; release matrix ещё не пройдена.
- Следующая доступная задача: TASK-008.
'''
write('docs/plans/nordic-blue/tasks/TASK-007.md',card)
index=(ROOT/'docs/plans/nordic-blue/README.md').read_text(encoding='utf-8-sig')
index=index.replace('Реализация темы ещё не выполнена.','TASK-007 завершена: пустой child theme-classic собран и совпал с Classic при DPR1/2. Палитра и иконки в тему ещё не интегрированы.')
index=index.replace('| 001, 002, 006 | TODO |','| 001, 002, 006 | DONE |')
write('docs/plans/nordic-blue/README.md',index)
profile=read(ROOT/'TestApp/theme-lab/build-profiles.json')
profile['description']='Active lab build profiles mirrored from theme-lab/app.json (TASK-007). They belong to the lab descriptor in the existing TestApp workspace, not TestApp/app.json. Both testing builds succeeded; outputs validated.'
assert profile['builds']==read(ROOT/'TestApp/theme-lab/app.json')['builds']
write('TestApp/theme-lab/build-profiles.json',json.dumps(profile,indent=2)+'\n')
labread=(ROOT/'TestApp/theme-lab/README.md').read_text(encoding='utf-8-sig')
start=labread.index('## Theme selection');end=labread.index('## State drivers',start)
labread=labread[:start]+'''## Theme selection и реальные builds (TASK-007)

`profiles.json` проверяет toolkit/theme, включённый package и SDK. Classic оставляет принятый `classic-reference.json` с полным установленным prebuilt CSS; Nordic загружает **реальный** `../build/theme-lab/nordic/testing/app.json` и его compiled CSS. Нет fallback Nordic → Classic. Один fixture.js остаётся общим.

Рабочая папка лабораторных сборок: `D:\\Projects\\Extjs7ClassicThemeUpgradeNordicBlue\\TestApp\\theme-lab`.

```powershell
..\\..\\node_modules\\@sencha\\cmd-windows\\dist\\sencha.exe app build lab-classic testing
..\\..\\node_modules\\@sencha\\cmd-windows\\dist\\sencha.exe app build lab-nordic testing
```

Обе команды прошли с Cmd 7.7.0.36 / Java 8. `app.json` здесь — отдельный лабораторный build descriptor в существующем workspace TestApp, без копии SDK и component configs. `build-requires.js` обеспечивает полное fixture CSS. `build-entry.html` — только вход анализа зависимостей Cmd; открывать для ручной проверки нужно `index.html?theme=nordic`, где выполняется реальный общий fixture. `build-profiles.json` отражает активные builds, outputs проверены: `TestApp/build/theme-lab/{classic,nordic}/testing/`.

Production `TestApp/app.json` и пользовательские команды из его папки не изменены. Не переносить lab profiles в него без необходимости. Builds запускать последовательно: промежуточная папка временных файлов общая.

После TASK-007 Nordic намеренно выглядит как Classic: palette и новые icons ещё не интегрированы. Строгое сравнение с принятым Classic baseline при DPR1/2 прошло; отчёт — `artifacts/nordic-blue/TASK-007/inheritance-report.md` от корня проекта. Для последующих сравнений сохранить software raster/sRGB и политику анимации TASK-006. Не перезаписывать baseline.

''' +labread[end:]
write('TestApp/theme-lab/README.md',labread)
agents=(ROOT/'AGENTS.md').read_text(encoding='utf-8-sig')
agents+='''
## Generated Nordic package and laboratory builds (TASK-007)

The Cmd-generated theme is at `TestApp/packages/local/theme-nordic-blue`. Cmd 7.7.0.36 generated the modern `package.json` (`sencha` metadata) and a build.xml importing installed Cmd package build logic; it did **not** generate `.sencha/package`. Preserve this actual scaffold and any `.sencha/package` produced by a future supported migration; do not fabricate old configuration. The original generated files, including the archived identity-only overrides/init.js, are in artifacts/nordic-blue/TASK-007/generated-scaffold. Active overrides/ and resources/images/ are empty after TASK-007.

Lab builds use the separate `TestApp/theme-lab/app.json` descriptor in the same TestApp workspace, with the common fixture and build-requires.js. From `TestApp/theme-lab`, run `..\\..\\node_modules\\@sencha\\cmd-windows\\dist\\sencha.exe app build lab-classic testing` and `..\\..\\node_modules\\@sencha\\cmd-windows\\dist\\sencha.exe app build lab-nordic testing` sequentially. Outputs: `TestApp/build/theme-lab/{classic,nordic}/testing`. The original TestApp commands above and production source/config remain unchanged. Empty child inheritance passed DPR1/2 comparisons; palette/icons and release acceptance remain future tasks.
'''
write('AGENTS.md',agents)
expected={str(p.relative_to(doc)).replace('\\','/'):sha(ROOT/p.relative_to(doc)) if (ROOT/p.relative_to(doc)).exists() else None for p in doc.rglob('*') if p.is_file()}
(OUT/'delivery-expected.json').write_text(json.dumps(expected,indent=2),encoding='utf-8')
print(json.dumps({'status':'PASS','resources':len(resource_comparisons),'loaded':len(loaded),'baselineInputsUnchanged':len(baseline),'deliveryFiles':len(expected)}))
