from pathlib import Path
import json,hashlib,shutil,re,subprocess,sys
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');A=R/'artifacts/nordic-blue/TASK-017';C=Path(__file__).parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
write=lambda p,s:p.write_text(s,encoding='utf-8')
assert 'Статус: DONE' in (R/'docs/plans/nordic-blue/tasks/TASK-016.md').read_text(encoding='utf-8-sig')
assert not A.exists();A.mkdir();(A/'before').mkdir()
for name in ['AGENTS.md','README.md','docs/plans/nordic-blue/README.md','docs/plans/nordic-blue/tasks/TASK-017.md','docs/plans/nordic-blue/coverage.md','docs/plans/nordic-blue/palette.md']:
 p=R/name;shutil.copy2(p,A/'before'/('plan-index.md' if name=='docs/plans/nordic-blue/README.md' else p.name))
p=R/'docs/plans/nordic-blue/tasks/TASK-017.md';write(p,p.read_text(encoding='utf-8-sig').replace('Статус: TODO','Статус: IN_PROGRESS'))
p=R/'docs/plans/nordic-blue/README.md';write(p,p.read_text(encoding='utf-8-sig').replace('| 016 | TODO |','| 016 | IN_PROGRESS |'))
shutil.copy2(C/'nordic-blue-release.py',R/'tools/nordic-blue-release.py')
p=R/'docs/plans/nordic-blue/coverage.md';write(p,p.read_text(encoding='utf-8-sig')+'''\n## Фактические результаты 2026-10-24\n\nВсе20fixture groups и их явно перечисленные состояния проверены в TASK-014/015/016. 102scenarios/DPR, строгая геометрия/типографика и действия — PASS; visual golden относится только к Edge. Настоящие development/testing/production output pages и реальный TestApp проверены на3browser versions/DPR1/2. Точные counts, источники и границы — artifacts/nordic-blue/TASK-017/coverage-traceability.json и TASK-016/acceptance-report.md. Это не покрытие всех Ext JS configs/custom ui; SDK7.9 NOT_RUN.\n''')
p=R/'docs/plans/nordic-blue/palette.md';write(p,p.read_text(encoding='utf-8-sig')+'''\n## Итог реализации 7.7\n\nВ TASK-008–012 проверены177compiled color hooks и31узкое reviewed flat-gradient exception;15канонических токенов выше неизменны. Точные имена/значения/доказательства — config/nordic-blue-policy.json и sass/var в пакете. Исторические52hooks TASK-008 не описывают итоговое число. Нельзя расширять allowlist на geometry/fonts/flags или новые artwork без предусмотренной проверки.\n''')
write(R/'docs/nordic-blue-installation.md','''# Установка Nordic Blue и возврат к Classic

## Проверенная конфигурация

Ext JS **Classic 7.7.0.31**, Sencha Cmd **7.7.0.36**, Windows, Java8. SDK7.9 не проверен; пример https://examples.sencha.com/extjs/7.9.0/examples/classic/themes/ — только референс. SDK и коммерческие права на Ext JS предоставляет владелец приложения; SDK, node_modules и compiled outputs не входят в архив темы.

## Подключение в существующий Cmd workspace

1. Сохранить текущие app.json, workspace config и рабочую Classic build. Работать на своей ветке/копии. Убедиться по version.properties, что SDK соответствует7.7.0.31 и приложение использует toolkit classic.
2. Скопировать **только** `TestApp/packages/local/theme-nordic-blue/` из source-архива в `<workspace>/packages/local/theme-nordic-blue/`, сохраняя package.json, build.xml, sass/ и resources/. Пакет уже сгенерирован Cmd, namespace Ext, type theme, extends theme-classic. Не создавать .sencha/package вручную. Не копировать SDK или весь validation TestApp в своё приложение.
3. В нужном app.json выбрать `"theme": "theme-nordic-blue"`. Остальные xtype/ui, app code, requires, store/controller и app-specific Sass оставить прежними. Пакет наследует установленный theme-classic → theme-neutral → theme-base. Не включать runtime JS overrides, другой font renderer или размеры.
4. Из каталога приложения с app.json собрать testing локальным Cmd. В этом репозитории точная команда ниже; для другого workspace путь до того же Cmd требуется пересчитать.

```powershell
# Из D:\\Projects\\Extjs7ClassicThemeUpgradeNordicBlue\\TestApp
$env:JAVA_HOME = 'C:\\Program Files\\Java\\jdk1.8.0_501'
$nordicCmd = (Resolve-Path '..\\node_modules\\@sencha\\cmd-windows\\dist\\sencha.exe').Path
$env:PATH = "$env:JAVA_HOME\\bin;$(Split-Path $nordicCmd)\\bin\\windows\\node;$env:PATH"
..\\node_modules\\@sencha\\cmd-windows\\dist\\sencha.exe app build testing
```

Для production заменить testing на production. Для watch использовать пользовательскую команду `..\\node_modules\\@sencha\\cmd-windows\\dist\\sencha.exe app watch`; брать фактический URL из вывода. Watch не заменяет testing/production acceptance. Fashion использует совместимый Node из Cmd, не Node24 из browser tooling.

5. Открыть **новый output**, проверить manifest/resources/network и экраны приложения. Сравнивать Classic/Nordic в одном браузере/viewport/DPR, включая custom ui. Существующие app styles могут иметь собственные цвета: тема не переписывает их глобальными overrides. Удалённые/непроверенные SDK, браузеры, кастомные ui не получают автоматического PASS.

## Команды проверенной лаборатории и TestApp

Из `TestApp/theme-lab/`: `..\\..\\node_modules\\@sencha\\cmd-windows\\dist\\sencha.exe app build lab-classic testing`, затем `... app build lab-nordic testing`; также development/production. Выход: TestApp/build/theme-lab/{classic,nordic}/{mode}.

Из `TestApp/theme-acceptance/{classic,nordic}/`: `..\\..\\..\\node_modules\\@sencha\\cmd-windows\\dist\\sencha.exe app build testing` (также development/production). Выход: TestApp/build/theme-acceptance/{theme}/{mode}. Это два descriptors одних и тех же исходных app classes/Sass. В validation directories local.properties включает skip.page=0/skip.js=0: Cmd development по умолчанию не создаёт index.html/JS. Это только упаковка страниц; оригинальный TestApp не менялся.

Сервер лаборатории: `node TestApp/theme-lab/serve.cjs`, он сообщает фактический порт. Отдельный сервер TASK-016: `node tools/nordic-blue-acceptance/serve.cjs` на127.0.0.1:51753, с read-only alias SDK и служебным /favicon.ico→204. Серверы служат проверке и не входят в production приложение.

## Gates после изменения темы

Из корня: `python tools/lint-nordic-blue.py --check-icon-candidates`, реальная Nordic testing build, затем:

```powershell
python tools/nordic-blue-regression/run.py --output artifacts/nordic-blue/regression-new-run
python tools/nordic-blue-visual/run.py --output artifacts/nordic-blue/visual-new-run
```

Требуются работающий lab server, Python3.12/Pillow/NumPy, Node24/Playwright и проверенная версия Edge. Папки output должны быть новыми; --url/--node описаны в соответствующих README. При изменении исходников активный golden устаревает и gate обязан упасть: не обновлять его для сокрытия дефекта. Повторить build/browser matrix по tools/nordic-blue-acceptance/README.md в новой области доказательств. Исторические скрипты содержат пути этой Windows-машины; перенос требует явной настройки, не обещается zero-config.

## Откат

Вернуть сохранённый app.json либо выбрать исходный `"theme": "ext-theme-classic"` (alternateName установленной theme-classic), собрать testing/production тем же локальным Cmd в отдельный или очищенный поддерживаемой сборкой output. Проверить theme-classic в новом manifest и отсутствие theme-nordic-blue, обновить страницу/кэш приложения и повторить smoke. Не менять class configs, font metrics, app Sass или SDK ради отката. Удалять исходный пакет необязательно; критична выбранная theme и актуальный output.

## Значки и права

Активен согласованный nordic-icons-v3-folders; 648 файлов1x/2x, исходные CSS boxes/offsets/hit areas. Автоматический2x при min-resolution:192dpi, рабочий1x fallback. Новая графика требует нового показа и явного одобрения пользователя; отсутствие ответа не является одобрением. SVG masters и SHA/approval входят в source-архив. Лицензия нового artwork владельцем пока не назначена; см. sources-and-license.md. SDK/Classic reference assets сохраняют условия Sencha и в source-архив не включены. Эта документация не назначает новую лицензию чужим материалам.
''')
write(R/'docs/nordic-blue-release-notes.md','''# Nordic Blue — техническая поставка исходного пакета 1.0.0

Дата2026-10-24. Цель: Ext JS Classic7.7.0.31 / Cmd7.7.0.36. Тема расширяет установленную theme-classic. Палитра:15tokens,177compiled color hooks,31 точно разрешённый flat gradient. Изображения:648одобренных runtime files,1x/2x при прежнем CSS размере; активен v3 folders. Runtime JS/font/behavior overrides отсутствуют.

TASK-001–016 подтверждают аудит, общий Classic baseline, реализацию и сравнения. TASK-014:204fixture pairs+236action/state pairs,21614elements,14negative controls; TASK-015:204visual pairs,0unmasked structural pixels,408golden snapshots,648files/694decoded frames,6real defect controls; TASK-016:17successful build invocations,3browser versions×3modes×DPR1/2,144actual-output pairs/40230elements. Подробные отчёты и условия включены; raw screenshots/goldens остаются в основном репозитории/локальных artifacts.

Поставка — исходный theme package, editable SVG masters, approval/manifests, notices, palette/config и report summaries. SDK, node_modules, compiled приложения, Classic reference screenshots/assets и временные debug patches не включены. Архив детерминированно создаётся `python tools/nordic-blue-release.py --output artifacts/nordic-blue/release-new-run`; существующий output запрещён. Проверяются все ZIP entries/CRC и точное равенство source bytes. Архивы исключены из Git; опубликованы исходники/recipe/manifest для воспроизведения.

Ограничения: Windows и записанные версии браузеров; exact pixel golden только Edge155.0.4283.62; Chromium156.0.8078.4 и Firefox152.0.4 имеют собственные свежие Classic/Nordic geometry/function comparisons. Анимация GIF проверена по исходным bytes/decoded frames, не по плавности. Есть RTL artwork/catalog, но полная RTL application layout matrix не заявляется. Произвольные сторонние custom ui и Ext JS7.9 не проверены. Старые TestApp navigation image warnings сохранены одинаково в Classic/Nordic. Полная визуальная приёмка всего приложения пользователем не подменяется техническим golden. Лицензия нового SVG artwork пока не назначена владельцем; оригинальные Sencha права сохраняются.

Следующий необязательный этап: TASK-018 с отдельно установленным SDK7.9 и новой матрицей. Совместимость с7.9 сейчас не заявляется. Установка и откат: docs/nordic-blue-installation.md.
''')
coverage=read(R/'artifacts/nordic-blue/TASK-005/coverage.json')
rows=[{'fixture':name,'states':states,'status':'PASS_IN_RECORDED_MATRIX','geometryEvidence':'TASK-014/run-1 and TASK-016/browsers/*','visualEvidence':'TASK-015/run-3 (Edge only)','browserModeEvidence':'TASK-016/native-pages-*'} for name,states in coverage['cases'].items()]
trace={'status':'PASS','scope':'20 recorded fixture groups; exact listed scenarios, not all Ext JS configurations.','fixtures':rows,'invariants':[{'criterion':c,'evidence':e,'status':'PASS'} for c,e in [('theme/classic/extend and no JS overrides','package.json + TASK-016/source-resource-mode-audit.json'),('exact geometry/typography/state/data','TASK-014 + TASK-016 native-page-comparison.json'),('icon approval/1x/2x/offsets/hit targets','REV-001-folders-v3 approval/manifest + TASK-013/014/016'),('normalized structure and unmasked Nordic golden','TASK-015 visual report/golden-v1'),('actual development/testing/production and browser matrix','TASK-016 acceptance report/matrix'),('real app and existing Sass unchanged','TASK-016 protected-before/source-resource-mode-audit'),('source handoff/install/rollback/provenance','TASK-017 release-manifest + docs/nordic-blue-installation.md')]],'notClaimed':['SDK7.9 optional018','cross-browser pixel identity','complete RTL application-layout matrix','all custom ui/third-party applications','GIF animation smoothness','new artwork license grant','final full-theme user visual approval'],'pdfTraceability':'docs/plans/nordic-blue/traceability.md (all32pages mapped; user overrides win)'}
write(A/'coverage-traceability.json',json.dumps(trace,indent=2))
write(A/'deviations.md','''# Журнал решений и ограничений

| Решение | Состояние / доказательство |
|---|---|
| SDK7.7 вместо7.9 из PDF | Прямое указание пользователя; 7.7.0.31 принят,7.9 NOT_RUN/optional018 |
| Новый artwork вместо Classic images | Прямое указание; v2 approval и folder-v3 approval, immutable SHA |
| Строго0px вместо PDF≤1px | TASK-014/015/016, отрицательные контроли не допускают маскировки |
| Classic radius/font/layout/behavior наследуются | No arbitrary CSS/JS; narrow policy and700protected files in016 |
| Gradient flattening / icon resize-move mappings | Только SHA-bound reviewed exceptions, сохранены offsets/hit boxes |
| Старые navigation image build warnings | Совпадают с исходным TestApp/Classic; приложение не исправлялось ради темы |
| Development skip.page/skip.js | Installed Cmd defaults1; validation local.properties0 даёт actual pages. Unsupported CLI attempt retained as failed diagnostic |
| Firefox157 protocol failure | Не PASS; совместимый152.0.4 прошёл полный набор |
| Concurrent browser timeouts | Сохранены; повтор завершён без изменения readiness/metric policy; global driver timeout60s for native page operations |
| Browser favicon404 on original lab server | Точный /favicon.ico; acceptance read-only server51753 отвечает204; component requests не перехватываются |
| Initial visual golden | Технический Edge baseline, не полная пользовательская приёмка дизайна |
| Source-only theme distribution | Consuming app Cmd builds приняты; precompiled standalone package NOT_REQUIRED |
| Новые SVG: лицензия не назначена | Честный notice включён; владелец определяет лицензию отдельно. Sencha права не меняются |
| Непроверенные области | 7.9,другиеOS/browser versions,произвольныеcustomUI,полнаяRTL app layout,GIFsmoothness — не заявлены |

Нет неустранённых сбоев обязательной технической матрицы7.7; перечисленные границы не превращаются в PASS вне её объёма.
''')
write(A/'acceptance-report.md','''# TASK-017 — итоговая техническая приёмка и поставка

Объём: source theme package для Ext JS Classic7.7.0.31, Cmd7.7.0.36. Полные условия/версии и реальные сборки — TASK-016. Установка и откат — docs/nordic-blue-installation.md; состав/ограничения — docs/nordic-blue-release-notes.md.

Обязательные TASK-001–016 завершены по доказательствам. Матрица20fixture groups связывает их listed states с geometry/function TASK-014, pixel/artwork TASK-015 и builds/browsers/real app TASK-016. coverage-traceability.json не объявляет покрытыми все возможные Ext JS configurations. Журнал PDF/user решений, исходных предупреждений и устранённых диагностик — deviations.md.

Геометрия/шрифты/состояния: строгие Classic/Nordic comparisons, без допуска1px. Artwork: согласованный v3,648resources и SVG masters с точными SHA/1x/2x contracts; прежние физические/CSS размеры. Исходный TestApp, SDK, тема и fixture не менялись при подготовке поставки.

Source-архив собирается из реального принятого пакета, masters/approval/manifests, palette/policy и отчётов. В нём нет SDK/Classic reference bitmaps/screenshots, node_modules, compiled output или debug patches. Включён sources-and-license.md; новая лицензия не выдумана. Полные raw evidence находятся в основном проекте. release-manifest.json связывает каждый payload file, ZIP SHA/bytes и точное byte-for-byte сравнение с источниками; reproducibility-check.json сравнивает две независимые упаковки. Это проверка упаковки принятого пакета, не вымышленная сборка нового blank workspace.

Отдельные integrity результаты содержат фактический повтор проверки SHA всех локальных артефактов TASK-014/015/016 и текущих source/runtime files. Отсутствующие Git-excluded локальные compiled CSS отмечаются явно; не считать отсутствие нового checkout ошибкой оригинальной приёмки.

Техническая поставка7.7 принята в записанной матрице. Она не означает финальное одобрение пользователем вида всех экранов, поддержкуSDK7.9,полнуюRTLlayoutmatrix или любых custom ui/сторонних приложений. Подробные ограничения и права перечислены в release notes/deviations. Необязательный следующий этап — TASK-018; SDK7.9 сейчас NOT_RUN.
''')
print('Prepared TASK-017 documents, traceability and deterministic source packer')
