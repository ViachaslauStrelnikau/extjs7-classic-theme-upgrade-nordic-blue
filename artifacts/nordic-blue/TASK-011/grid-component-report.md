# TASK-011 — Grid, Tree и paging: DONE

Завершено 2026-10-24. SDK 7.7.0.31 / Cmd 7.7.0.36 / Java 1.8.0_501. Edge 155.0.4283.62, viewport 1280×1600, zoom 100%, DPR1/2, CPU raster/sRGB, locale en-US, timezone Europe/Minsk. Это промежуточный этап темы; итоговая приёмка остаётся TASK-014–017 после интеграции значков.

## Изменения

- `sass/var/view/Table.scss`: row text nb-text; hover control-hover/grid-line border; selection control-pressed/accent border; focus accent border; selected cell control-pressed; empty text muted и resize marker accent. Classic dotted selection/focus styles и их widths сохранены. Alternate/background/grid-line были заданы TASK-008.
- Новый `sass/var/grid/column/Column.scss`: header text/focus text nb-heading и focus border nb-accent. Размер/вес шрифта, line-height, padding и focus pseudo-element geometry унаследованы.
- `sass/var/grid/header/Container.scss`: normal header background приведён к canonical nb-header-bg вместо прежнего literal #EAF0F8; open header использует accent-soft. Normal/over/sorted headers теперь flat через три конкретных SDK gradient hooks.
- Tree использует общий grid/view row styling; indent, elbows, folders, leaves, expand/selection/navigation не переопределены. Paging наследует проверенные toolbar/buttons/form input colors TASK-009/010; отдельные glyph-only color hooks не добавлялись при enable-font-icons=false.
- Политика: **130 verified color hooks** (13 новых), **15 tokens**, **17 reviewed gradient hooks** (3 новых). Никакого нового общего разрешения CSS/gradient/JS/metric rules. Lint-код не изменён; новый review привязан SHA к результату геометрии.

## Градиенты и доказательства

Сначала реальная phase-A testing сборка с обновлёнными цветами и исходными header gradients: 20 состояний Grid/Tree/paging × DPR1/2, 3044 element comparisons / 326 icon observations, zero drift. После этого разрешены только grid-header-background-gradient, grid-header-over-background-gradient, grid-header-sorted-background-gradient = dynamic('none') в их SDK namespace. `gradient-review.json` содержит SHA `phase-a-geometry.json`. После изменения выполнена новая реальная сборка и все финальные сравнения.

Все **130** color variables получили уникальные временные sentinel colors в отдельной копии реального Cmd-generated SCSS перед RULE. Все встретились в actual compiled declarations. Рабочая тема и её CSS sentinel colors не получали. Probes не добавляют marker rules.

## Результаты

| Проверка | Результат |
|---|---|
| Две реальные Cmd testing сборки | phase-A и final flat exit 0, без ERR/WRN |
| Весь fixture против принятого TASK-006 Classic | 102 states × DPR1/2; 11280 element comparisons и 1926 icon observations, zero drift |
| Действия | 23 сценария × 2 темы × 2 DPR = 92 PASS; 46 paired comparisons / 3572 elements |
| Overflow/trigger audit | 20 Grid/Tree/paging states × DPR1/2: client/scroll excess, clipping и boxes совпадают |
| Lint / policy controls | PASS; 39 controls, 648 approved icon candidates, 300 SDK Sass files |
| Защищённые источники | 18 application/common-fixture inputs unchanged; 1474 baseline input hashes, только прежние различия AGENTS/lab profile/readme |
| Значки | 180 inherited replacement-target resources byte-identical Classic; source images/overrides пусты |

Действия выполнялись настоящей мышью/клавиатурой: header ASC/DESC clicks; row selection/ArrowDown; checkcolumn toggle; header menu trigger и Escape после focus первого menu item; column boundary drag; tree expander collapse/expand, leaf selection/ArrowDown, ArrowLeft/Right; paging first/previous/next/last/refresh и Page input Enter. На первой/последней странице проверены disabled boundaries и реальные record IDs.

Для проверки scrollbar существующий grid одинаково в обеих темах временно уменьшен штатным component.setSize(480,160); getScrollable().scrollTo(90,44) подтвердил фактическую прокрутку обеих осей. Это дополнительное runtime состояние, исходная fixture/application config не менялась. Перетаскивание с 2 px внутри правого края на 50 px даёт ширину 308 px в Classic (260−2+50), та же ширина и все дочерние metrics получены в Nordic. Это проверка поведения изменения размера пользователем, не изменение базовых размеров темы.

Парные сравнения сохраняют rect/typography, borders/spacing/radii, client/scroll/overflow/text wrapping, focus/state/data и icon boxes/sprite offsets. Исключены рассмотренные paint colors и gradient-only layers; структура теней сохраняется. Это не pixel equality новой палитры. 7 анимированных GIF фиксированы на первом исходном кадре по протоколу baseline с проверкой реальных built bytes. Raw PNG не редактировались.

Визуально просмотрены raw DPR1 grid--selected и tree--selected: читаемые строки и заголовки, заметное выделение, прежняя плотность и расположение элементов. Галерея показывает все 20 static states и 23 action checkpoints при обоих DPR. Standard icons и их формы пока Classic, approved v2 подключается в TASK-013; широкая визуальная приёмка остаётся TASK-015.

## Диагностика драйвера

В начальных незавершённых запусках уточнены только проверки: внутренние cell/graphic semantic IDs extract.js являются ключами отчёта, поэтому реальные locators строятся от fixture row ID и установленного DOM класса; исходный active person-01=false читается до toggle; Classic resizer вычисляет ширину от pointer position (308, а не предполагавшиеся 310). Исправления драйвера не меняли production/fixture/theme для подгонки результата. Приняты только полные финальные action indexes. Для pseudo graphics без rect отчёт сохраняет hostRect/cssBox, а не выдуманный прямоугольник.

## Воспроизведение

Из корня проекта: `python tools/lint-nordic-blue.py --check-icon-candidates`.
Из `TestApp/theme-lab`: `..\..\node_modules\@sencha\cmd-windows\dist\sencha.exe app build lab-nordic testing` с Java 8. Исходные пользовательские команды TestApp build/watch в AGENTS.md сохранены.

Артефакты: build-phase-a.log, build-flat.log, commands.json, compiler-consumption.json, gradient-review.json, phase-a-geometry.json, geometry-comparison.json, grid-action-comparison.json, overflow-trigger-audit.json, source-guards.json, inherited-icons.json, lint-report.json, policy-controls.json, tools и review.html. Raw: nordic/probe/dpr-{1,2}/pass-1, nordic/captures/pass-1/dpr-{1,2}, grid-actions/dpr-{1,2}/{classic,nordic}. Classic static states берутся из неизменённого TASK-006. compiled/ и source-snapshot/ фиксируют принятые output/source, artifact-manifest.json — SHA. Резервные копии: before/, before-theme/, before-flat/, before-final-documents/.

Следующая задача: **TASK-012 — Tabs, Menu, DatePicker, Progress, Slider и Mask**. Готовность всей темы не объявляется.
