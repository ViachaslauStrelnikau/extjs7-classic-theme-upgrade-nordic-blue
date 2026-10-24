# Установка Nordic Blue и возврат к Classic

## Проверенная конфигурация

Ext JS **Classic 7.7.0.31**, Sencha Cmd **7.7.0.36**, Windows, Java8. SDK7.9 не проверен; пример https://examples.sencha.com/extjs/7.9.0/examples/classic/themes/ — только референс. SDK и коммерческие права на Ext JS предоставляет владелец приложения; SDK, node_modules и compiled outputs не входят в архив темы.

## Подключение в существующий Cmd workspace

1. Сохранить текущие app.json, workspace config и рабочую Classic build. Работать на своей ветке/копии. Убедиться по version.properties, что SDK соответствует7.7.0.31 и приложение использует toolkit classic.
2. Скопировать **только** `TestApp/packages/local/theme-nordic-blue/` из source-архива в `<workspace>/packages/local/theme-nordic-blue/`, сохраняя package.json, build.xml, sass/ и resources/. Пакет уже сгенерирован Cmd, namespace Ext, type theme, extends theme-classic. Не создавать .sencha/package вручную. Не копировать SDK или весь validation TestApp в своё приложение.
3. В нужном app.json выбрать `"theme": "theme-nordic-blue"`. Остальные xtype/ui, app code, requires, store/controller и app-specific Sass оставить прежними. Пакет наследует установленный theme-classic → theme-neutral → theme-base. Не включать runtime JS overrides, другой font renderer или размеры.
4. Из каталога приложения с app.json собрать testing локальным Cmd. В этом репозитории точная команда ниже; для другого workspace путь до того же Cmd требуется пересчитать.

```powershell
# Из D:\Projects\Extjs7ClassicThemeUpgradeNordicBlue\TestApp
$env:JAVA_HOME = 'C:\Program Files\Java\jdk1.8.0_501'
$nordicCmd = (Resolve-Path '..\node_modules\@sencha\cmd-windows\dist\sencha.exe').Path
$env:PATH = "$env:JAVA_HOME\bin;$(Split-Path $nordicCmd)\bin\windows\node;$env:PATH"
..\node_modules\@sencha\cmd-windows\dist\sencha.exe app build testing
```

Для production заменить testing на production. Для watch использовать пользовательскую команду `..\node_modules\@sencha\cmd-windows\dist\sencha.exe app watch`; брать фактический URL из вывода. Watch не заменяет testing/production acceptance. Fashion использует совместимый Node из Cmd, не Node24 из browser tooling.

5. Открыть **новый output**, проверить manifest/resources/network и экраны приложения. Сравнивать Classic/Nordic в одном браузере/viewport/DPR, включая custom ui. Существующие app styles могут иметь собственные цвета: тема не переписывает их глобальными overrides. Удалённые/непроверенные SDK, браузеры, кастомные ui не получают автоматического PASS.

## Команды проверенной лаборатории и TestApp

Из `TestApp/theme-lab/`: `..\..\node_modules\@sencha\cmd-windows\dist\sencha.exe app build lab-classic testing`, затем `... app build lab-nordic testing`; также development/production. Выход: TestApp/build/theme-lab/{classic,nordic}/{mode}.

Из `TestApp/theme-acceptance/{classic,nordic}/`: `..\..\..\node_modules\@sencha\cmd-windows\dist\sencha.exe app build testing` (также development/production). Выход: TestApp/build/theme-acceptance/{theme}/{mode}. Это два descriptors одних и тех же исходных app classes/Sass. В validation directories local.properties включает skip.page=0/skip.js=0: Cmd development по умолчанию не создаёт index.html/JS. Это только упаковка страниц; оригинальный TestApp не менялся.

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
