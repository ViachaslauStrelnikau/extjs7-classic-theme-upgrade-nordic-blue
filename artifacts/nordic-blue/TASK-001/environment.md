# TASK-001: проверенное окружение

Дата: 2026-10-23, Europe/Minsk. Цель: SDK Ext JS 7.7.0.31, Classic.

## Результаты

- SDK root и TestApp/ext/version.properties подтверждают version.full=7.7.0.31 и release=7.7.0.
- TestApp/workspace.json выбирает ext по относительному пути ext: рабочая копия SDK приложения находится в TestApp/ext.
- TestApp/app.json содержит toolkit=classic, theme=ext-theme-classic. Это alternateName пакета theme-classic.
- Локальный Cmd реально вывел Sencha Cmd v7.7.0.36 через java -jar sencha.jar which, затем через sencha.exe при сборке.
- Проверенное окружение: JAVA_HOME=C:/Program Files/Java/jdk1.8.0_501; его bin и bundled Node.js добавлены в PATH только дочерней команды. Глобальные установки не изменялись.
- Development build через Java 8 / локальный sencha.jar: exit 0, Fashion completed.
- Testing build через указанную пользователем команду: exit 0; Capturing theme image / Capture complete / Slicing complete - generated 280 images; CSS и index.html созданы.
- app watch через указанный пользователем sencha.exe: Waiting for changes. Порт 1841 занят; сервер выбрал 64193. URL относится к текущему запуску, не гарантирован для следующих запусков.
- Браузерная проверка http://localhost:64193/: Ext 7.7.0.31, один rendered app-main, title TestApp. pageerror=[], requestfailed=[], HTTP >=400=[]; screenshot и полный JSON рядом.

## Команды

Рабочая папка D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue/TestApp:

```powershell
..\node_modules\@sencha\cmd-windows\dist\sencha.exe app build testing
..\node_modules\@sencha\cmd-windows\dist\sencha.exe app watch
```

Команды добавлены в AGENTS.md. Проверка через Java служила диагностикой launcher и подтвердила версию; основной интерфейс проекта — предоставленные пользователем команды.

## Диагностика и ограничения

Старый sencha-error-20261023.log относится к generate app и содержит Fashion build exited with code 1. Текущие development/testing сборки уже проходят. Точная прежняя причина по crash log не установлена; не приписывать её автоматически Java или отсутствию файлов.

В TestApp нет .sencha/app; это сначала было подозрением, но сборки успешно завершились. Ничего не восстанавливалось и исходники TestApp не заменялись. Пробная генерация --refresh=false выполнялась в отдельной рабочей временной папке, не в TestApp.

У исходного TestApp используется custom ui navigation (Main.js). Fashion предупреждает о недостающих tab/tab-navigation-close.gif и tab-bar/navigation-* scroll/more assets. Это исходные build warnings, их нужно отразить в TASK-002 и не лечить изменением SDK. Они не превратились в 404 в проверенной начальной странице; дополнительные состояния требуют отдельного fixture.

Это smoke-проверка существующего приложения, не геометрический baseline всей темы и не acceptance Nordic. Отдельный theme-lab и Classic geometry baseline создаются в TASK-005/006. Production build пока NOT_RUN. Полный текст новой testing-сборки сохраняется отдельно в testing-build.log, если присутствует; перечисленные выше development/testing итоги взяты из реально выполненных команд, а не старого build-каталога.

## Переход к аудиту

В SDK theme-classic/sass/var/form/field/Trigger.scss подтверждён $form-trigger-width: dynamic(17px); panel/Tool.scss содержит $tool-size: dynamic(15px). Это показывает, почему generic значения из документации (например, 22px) нельзя брать вместо фактического parent Classic.

Следующие задачи: TASK-002 аудит Sass и приложения; TASK-003 каталог ресурсов и state mappings. Набор значков ещё не создан, одобрение ещё не запрашивается.
