# TASK-005 — детерминированный Theme Lab

Статус: **DONE**, 2026-10-23. Исходники: [TestApp/theme-lab](../../../TestApp/theme-lab/README.md).

## Сделано

- Один fixture.js в существующем TestApp: все 20 строк coverage, 101 именованных состояний + обзор.
- Стабильные data-lab-id, явные record/node IDs, фиксированные 32 записи / 4 страницы, дата 2026-10-23. Никакого сопоставления по сгенерированным Ext IDs.
- Readiness Ext + stores + initialized HtmlEditor + document/iframe fonts + idle layouts + 3 стабильных кадра. Пустое покрытие не принимается.
- Настоящие браузерные hover/pressed/focus. Наблюдение pointerdown до Ext delegation; mousedown у ComboBox может подавляться. Служебный Date.now монотонный: полностью остановленный таймер блокировал HtmlEditor; new Date() для данных и календаря остаётся фиксированным.
- Profile selection с проверкой SDK/theme; build profile fragments и class input build-requires.js подготовлены к TASK-007. Ошибка отсутствующего Nordic build явная, Classic не подставляется.
- Отдельный локальный read-only сервер обслуживает TestApp и alias существующего SDK, без копии framework tree.

## Доказательства

- [coverage-checklist.md](coverage-checklist.md), [coverage.json](coverage.json).
- [inspection.json](inspection.json): overview + 101 states READY; Classic resource 404/page errors — 0. Edge 155.0.4283.62, Windows, en-US, Europe/Minsk, 1280×1600, DPR1.
- [reproducibility.json](reproducibility.json): два независимых запуска, 302 semantic elements совпали точно по IDs/rects/computed metrics; дубликатов 0. Paging последняя страница person-25, disabled next/last; tree collapse/expand; grid person-03 + DESC; editor content refresh; настоящие Space (checkbox), ArrowRight (slider 42→43), click (panel collapse).
- [Снимки](screenshots/overview.png): обзор и 20 отдельных normal cases. Это preview, не adopted golden.
- [input-hashes.json](input-hashes.json), [fixture-hashes.json](fixture-hashes.json): исходные inputs и поставленная fixture.

## Решение о CSS

Исходная TestApp testing build вырезает CSS неиспользуемых Main view классов. Slider thumb без полного stylesheet получался невидимым; расширять SDK или менять production Main ради этого нельзя. Classic reference поэтому использует **полный неизменённый prebuilt CSS установленного ext-7.7.0.31**, проверяя version.properties/package metadata/runtime version. SDK alias только read-only, resources не копируются.

Будущий Nordic profile должен быть реальной Cmd build с theme-nordic-blue и всеми lab classes. build-requires.js содержит нужные classes; профили не активируются в production app.json до TASK-007. Фрагменты output paths ещё требуют проверки в первой реальной сборке этих profiles. Текущая TASK-005 не заявляет новую app/package build.

## Запуск

Из TestApp: `..\node_modules\@sencha\cmd-windows\dist\bin\windows\node\node.exe theme-lab\serve.cjs`. Открыть напечатанный адрес. Старый app watch сохранён и продолжает обслуживать исходный TestApp; у него нет sdk/ alias этого стенда.

inspect.cjs и replay.cjs — локальные сборщики доказательств TASK-005 с Playwright/Edge, exit 0. Они читают установленный проект; src fallback нужен только при подготовке до установки. Полные geometry/keyboard/visual suites выполняются позднее.

## Что не заявляется

Nordic CSS/build ещё отсутствует; сравнение Classic/Nordic NOT_RUN. Release interaction matrix, frozen loading GIF frame, geometry/icon golden и build matrix относятся к TASK-006/014/015/016. Утверждённые значки v2 сохранены, в lab/тему не интегрированы. SDK, Main/Application/app.js, app.json, build.xml, node_modules не изменены.

Следующая задача — TASK-006: зафиксировать Classic baseline на этом стенде.

## Проверка установленного сервера

Сервер запущен встроенным Node Sencha Cmd; helper совместим с его старым URL/http API. Реальный live-preview.json: 20 cases, 302 semantic elements, READY, resource/page errors 0. Текущий локальный URL: http://127.0.0.1:51752/theme-lab/index.html?theme=classic&case=all&state=normal . После перезапуска порт может измениться.
