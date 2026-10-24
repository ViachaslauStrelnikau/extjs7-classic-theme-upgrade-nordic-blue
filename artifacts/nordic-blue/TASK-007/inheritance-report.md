# TASK-007 — пустой child theme: PASS

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

CSS обоих builds **побайтово одинаков**: SHA-256 `f45a7a5442df11dc08bf263ccc9f427c7de9126669ee6b5a5f2c52256afae3aa`. Все 556 runtime файлов resources обоих builds также побайтово совпадают, включая созданные Cmd slicer assets. Единственное отличие каталога resources — generated `Readme.md` с названием пакета; этот Markdown не загружается приложением. 53 различных built resources реально загружены стендом без 404/ошибок. Новые иконки и цвета в теме отсутствуют.

## Сравнение с зафиксированным Classic TASK-006

- Edge 155.0.4283.62 / Windows, 1280×1600, DPR 1 и 2, en-US, Europe/Minsk, фиксированная дата, software raster + sRGB как в принятом baseline.
- 102 сценария при каждом DPR: всего 204 raw PNG и 204 JSON измерений.
- **11 280 сравнений элементов и 1 926 icon observations: ноль отличий** геометрии, шрифтов, box model, paint, offsets, scroll, data и focus state. Пустые выборки, duplicates, unowned graphics и runtime errors отсутствуют.
- Адреса ресурсов приведены к одному логическому корню только для сравнения строк URL; имена, offsets, размеры и bytes не менялись. Сведения о выбранном профиле проверены отдельно от остального окружения.
- Пиксели Ext fixture совпадают без допуска. В raw PNG отличается имя темы в нативном HTML select и служебной подписи стенда. Исключены только прямоугольник этого select и измеренный DOM Range суффикса подписи для каждого сценария; весь остальной кадр сравнивается. Никакие triggers/tools/текст компонентов не маскируются. Raw PNG и raw diff с различиями подписи сохранены. Точные области: `lab-chrome.json`.
- Семь анимированных Classic GIF стабилизированы тем же first-frame browser routing, что в baseline; перед снимками реальные bytes в обоих builds проверены по исходным Classic SHA-256. SDK и build файлы не переписывались. Это политика только данного сравнения пустого child; после замены значков нужно выводить кадр из фактического нового asset.
- Принятый TASK-006 baseline не перезаписан. Все 1474 его source inputs и 18 дополнительно защищённых файлов совпали с исходными SHA до обновления документации. `TestApp/app.json`, app.js, build.xml, workspace.json, index.html, application sources и fixture.js не изменены.

Подробности: [inheritance-comparison.json](inheritance-comparison.json), [inheritance-proof.json](inheritance-proof.json), raw captures `nordic/captures/pass-1/dpr-1` и `dpr-2`. Это не полная функциональная/release matrix: расширенные проверки TASK-014–016 ещё впереди.

## Продолжение

TASK-007 DONE. Следующая задача — TASK-008: разрешённая палитра и проверенный Sass allowlist. Не подключать значки до TASK-013 и не заявлять готовность темы по этому отчёту.
