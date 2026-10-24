# TASK-012 — Tabs, Menu, DatePicker, Progress, Slider и Mask: DONE

Завершено 2026-10-24. SDK 7.7.0.31 / Cmd 7.7.0.36 / Java 1.8.0_501. Edge 155.0.4283.62, viewport 1280×1600, zoom 100%, DPR1/2, CPU raster/sRGB, locale en-US, timezone Europe/Minsk. Готовность всей темы не объявляется.

## Изменения

- `sass/var/tab/Tab.scss`: state backgrounds/text/borders для focus/over/active/disabled и их комбинаций; сохранены Classic radius, font, padding, widths и disabled opacity. Неиспользуемый tab-outline-color-focus удалён, body outline остаётся рассмотренным цветовым hook.
- Новый `sass/var/tab/Bar.scss`: bar/strip background и borders. Normal/focus/hover/active gradients Tabs и tabbar gradient заменены только рассмотренными dynamic('none'). Close/scroll bitmap artwork пока Classic.
- `sass/var/menu/Menu.scss`: active item text/border и separator surfaces/borders. Nested/check/radio/disabled menu behavior не менялся; неиспользуемый menu-scroller-border-color удалён. Active gradient flat, arrows/marks остаются исходными.
- `sass/var/picker/Date.scss`: text, hover/selected/today borders, disabled/prev-next text, column header/footer surfaces и monthpicker text/separator. Calendar header остаётся accent с исходным белым month-button text. Today outline и selected fill различимы; геометрия 1:1. Header/column/footer gradients flat.
- `sass/var/ProgressBar.scss`: focus border и front/back text colors; существующие accent bar / accent-soft track сохранены. Bar gradient flat; высота/текст/позиции без изменений.
- `sass/var/LoadMask.scss`: overlay/page color, focus border и inner message border. Alpha/opacity унаследованы; message gradient flat. Spinner animation/asset пока Classic.
- Slider использует bitmap track/thumb (`slider-imageless` следует false из enable-font-icons). Не добавлены неактивные imageless color/glyph hooks и не менялся renderer. Его рисунки обновляются в TASK-013; все положения и действия проверены сейчас.

Активны **177 color hooks** (47 новых), **15 tokens**, **31 reviewed gradient hooks** (14 новых). Изменены только шесть namespace SCSS и policy; SDK/application/common fixture/lint-код не изменялись. Произвольные selectors/UI mixins/JS overrides, geometry/font/position rules по-прежнему запрещены.

## Компиляция и уточнение диагностики

Phase-A с исходными secondary gradients: 28 states × DPR1/2, 2210 element comparisons / 288 icon observations, zero drift. Затем 14 точных gradients разрешены через `gradient-review.json`, SHA-связанный с `phase-a-geometry.json`: 7 Tabs, tabbar, menu, 3 DatePicker, Progress и Mask message. Последующие final geometry/action checks также PASS.

Первоначальная hex-only проверка sentinel colors ошибочно сочла два mask hooks неиспользуемыми: SDK background-opacity выводит их как RGBA. Проверка byte identity после удаления обнаружила различие и не дала принять этот вывод. Оба mask hooks восстановлены; поиск расширен на эквивалентные rgb/rgba. Финальные **177** уникальных sentinel colors найдены в actual CSS declarations из копии реального Cmd-generated SCSS. В рабочие source/build CSS они не попадали. `compiler-probe-correction.json` сохраняет причину и точные RGBA примеры. Полная byte identity между диагностическими сборками НЕ заявляется: далее намеренно менялись gradients. Реально неиспользуемыми остались только tab-outline-color-focus и menu-scroller-border-color; widths/renderer ради их активации не включались.

Четыре последовательные реальные сборки (phase-A, diagnostic prune, flat, corrected final) завершились exit0, без ERR/WRN; принята последняя `build-final.log` с восстановленными mask colors. В `policy-controls.py` отрицательный gradient control перенесён с уже рассмотренного tab gradient на неразрешённый grid-cell-special gradient. Сам lint не ослаблен.

## Проверки

| Проверка | Результат |
|---|---|
| Полный fixture против TASK-006 Classic | 102 states × DPR1/2; 11280 element comparisons / 1926 icon observations, zero drift |
| Действия | 29 сценариев × 2 темы × 2 DPR = 116 PASS; 58 paired comparisons / 2124 elements |
| Secondary overflow/clipping | 28 states × DPR1/2; client/scroll excess, font/wrapping/box/image metrics совпадают |
| Compiler consumers | 177 PASS, hex или эквивалентные rgb/rgba |
| Lint/controls | PASS; 39 controls, 648 approved icon candidates, 300 SDK Sass files |
| Guarded source | 18 application/common-fixture inputs unchanged; 1474 baseline hashes — только прежние AGENTS/lab profile/readme различия |
| Inherited artwork | 180 target resources byte-identical Classic; source images/overrides пусты |

Tabs: mouse/keyboard selection, disabled click ignored, close active tab и overflow scroll. Menu: check off/on, submenu hover, ArrowRight/ArrowLeft with real focus, disabled state. DatePicker: next/previous month, day selection, ArrowRight advances active day 15→16 while selected value stays15, Today selects fixed2026-10-23. Progress: updateProgress 100%/0%/42% через существующий component API. Slider: horizontal ArrowRight/Home/End, vertical ArrowUp, genuine drags обеих ориентаций, disabled blocks changes. Mask: visible/hide/show через существующий setLoading API. Config/renderer/DOM source не менялись для проверок.

Сравнения исключают только рассмотренные paint colors и gradient-only layers, сохраняя структуру shadows, rect/fonts/box metrics, visibility/opacity, focus/value/state/data, image URLs/sizes/offsets и client/scroll. Это не pixel equality палитры. Семь animated GIF обслуживаются первым исходным кадром по baseline protocol с проверкой реальных built hashes; raw PNG не редактировались.

Визуально просмотрены raw DPR1 Tabs normal, DatePicker selected и Progress partial: текст читается, выделение даты/Today различимы, поверхности flat, размещение прежнее. Галерея содержит все28 secondary states и29 action checkpoints при обоих DPR. Начальный action pass сохранён в secondary-actions-initial; принят финальный secondary-actions с отдельной проверкой точного activeDay. Драйвер уточнён по installed SDK getAfterScroller() вместо вымышленного свойства; fixture не менялась.

## Coverage и дальнейшая работа

`coverage-status.json` подтверждает каждую группу/состояние текущего fixture (20 groups, 102 scenarios/DPR), `design-differences.md` перечисляет текущие визуальные отличия и оставшиеся Classic bitmaps. Полная release functional/visual matrix остаётся TASK-014–017. Approved icon v2 не менялся и готов к интеграции TASK-013; новое одобрение неизменённого набора не запрашивается.

Команды: из корня `python tools/lint-nordic-blue.py --check-icon-candidates`; из TestApp/theme-lab `..\..\node_modules\@sencha\cmd-windows\dist\sencha.exe app build lab-nordic testing` с Java8. Исходные TestApp build/watch commands в AGENTS.md сохранены. Точные версии/exit codes в commands.json.

Артефакты: build-*.log, compiler-consumption.json, gradient-review.json, phase-a-geometry.json, geometry-comparison.json, secondary-action-comparison.json, overflow-trigger-audit.json, coverage-status.json, source-guards.json, inherited-icons.json, lint-report.json, policy-controls.json, tools и review.html. Raw: nordic/probe/dpr-{1,2}/pass-1, nordic/captures/pass-1/dpr-{1,2}, secondary-actions/dpr-{1,2}/{classic,nordic}. Source/build snapshots — source-snapshot/ и compiled/; SHA — artifact-manifest.json. Резервные копии before/, before-theme/, before-flat/, before-final-documents/ сохраняются.

Следующая задача: **TASK-013 — интегрировать одобренные значки v2**, сохраняя CSS размеры/hit targets/sprite offsets и проверяя DPR1/2. Набор уже одобрен пользователем; изменение artwork требует нового показа.

## Форматирование

В grid/header/Container.scss дополнительно изменены только пустые строки при переносе существующих reviewed assignments. Проверено точное совпадение всех непустых строк с before-theme; функциональных изменений Grid в TASK-012 нет.
