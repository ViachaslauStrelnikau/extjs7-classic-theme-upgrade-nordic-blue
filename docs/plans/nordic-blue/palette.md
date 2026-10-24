# Палитра и карта переменных

Источник: PDF, стр. 5–12. TASK-008: базовые значения применены к теме через dynamic tokens и 52 SDK color hooks; компонентная приёмка состояний/gradients остаётся TASK-009–012. Имена framework variables должны быть подтверждены в SDK 7.7.0.31 (TASK-002), включая фактическое влияние на default UI.

| Token | Значение | Назначение |
|---|---|---|
| nb-accent | #3275D6 | focus, selection, progress |
| nb-accent-hover | #2868C4 | accent hover |
| nb-accent-soft | #E3EDFC | selected/pressed |
| nb-header-bg | #E8EFF8 | headers/tab chrome |
| nb-toolbar-bg | #F4F7FC | toolbars |
| nb-control-bg | #EDF3F9 | controls/triggers |
| nb-control-hover | #E3EDF9 | control hover |
| nb-control-pressed | #D8E7FA | control pressed |
| nb-border | #B7C8DC | borders |
| nb-grid-line | #DCE5EF | grid separators |
| nb-surface | #FFFFFF | body |
| nb-surface-alt | #F7F9FC | alternate row |
| nb-text | #25374D | text |
| nb-heading | #304A68 | heading |
| nb-muted | #687B92 | secondary text |

Использовать единые имена nb-header-bg/nb-toolbar-bg/nb-control-bg из примеров PDF, не дублировать их короткими aliases из таблицы. Пользовательский дизайн служит проверкой визуального результата; расхождения с палитрой PDF фиксировать, не выдавать приблизительный подбор за точный HEX из картинки.

| Группа | Кандидаты переменных PDF | Значения |
|---|---|---|
| Panel | $panel-header-background-color, $panel-header-color, $panel-header-border-color, $panel-border-color, $panel-body-border-color, $panel-body-background-color | header-bg, heading, border, surface |
| Toolbar | $toolbar-background-color, $toolbar-border-color | toolbar-bg, border |
| Button | $button-default-background-color, *-over, *-pressed, $button-default-border-color, $button-default-color | control-bg/hover/pressed, border, text |
| Form | $form-field-background-color, $form-field-border-color, $form-field-focus-border-color, $form-trigger-background-color, $form-trigger-border-color | surface, border, accent, control-bg |
| Grid header | $grid-header-background-color, $grid-header-over-background-color, $grid-header-sorted-background-color, $grid-header-border-color, $grid-header-trigger-background-color, *-open | #EAF0F8, accent-soft, border, transparent/accent-soft |
| Grid rows | $grid-row-cell-background-color, $grid-row-cell-alt-background-color, $grid-row-cell-border-color | surface, surface-alt, grid-line |
| Tabs | $tab-base-color, $tab-base-color-active, $tab-border-color, $tab-color | header-bg, surface, border, heading |
| Picker | $datepicker-background-color, $datepicker-header-background-color, $datepicker-item-selected-background-color | surface, accent, accent-soft |
| Progress | $progress-background-color, $progress-bar-background-color | accent-soft, accent |
| Window | $window-header-background-color, $window-header-color, $window-border-color | header-bg, heading, #AFC2D9 |

Звёздочки здесь — сокращение перечня, не Sass-код. Неподтверждённые переменные не добавлять. Menu/Tree/Slider/Mask и полную state palette вывести из SDK-аудита. Flat gradients разрешать по отдельным компонентам. Цвета иконок выбирать из этой палитры с проверкой читаемости; disabled не должен сливаться с поверхностью. Типографику, border widths, frames и hit areas не менять.

## Проверено в TASK-002

Аудит SDK 7.7.0.31 завершён: [карта переменных](../../../artifacts/nordic-blue/TASK-002/variable-map.md), [отчёт](../../../artifacts/nordic-blue/TASK-002/sdk-audit.md) и [точная политика](../../../artifacts/nordic-blue/TASK-002/variable-policy.json). Все явно перечисленные здесь color variables найдены; wildcard-сокращения раскрыты в карте. В ней также добавлены Menu/LoadMask. Tree/Slider glyph/imageless colors существуют, но не включены в renderer Classic по умолчанию; artwork и его метрики проверяются отдельно. Назначения Nordic применены и проверены в TASK-008; полная карта находится в config/nordic-blue-policy.json и artifacts/nordic-blue/TASK-008/variable-allowlist.md.

## TASK-008: активная цветовая основа

Все 15 canonical tokens находятся в package sass/var/all.scss; explicit entry в package.json sencha.sass.var обеспечивает включение в Cmd 7.7 app и slicer. 50 исходных назначений сохранены; дополнительно `$button-default-border-color-over: dynamic($nb-accent-hover)` и `$form-field-empty-color: dynamic($nb-muted)` используют остальные токены. Декларации/consumers подтверждены локальным SDK; изолированный Fashion probe доказал compiled usage всех 52 hooks. Короткие aliases PDF не вводятся. Grid header #EAF0F8, Window border #AFC2D9 и transparent trigger остаются конкретными исключениями из таблицы.

Команда read-only policy: `python tools/lint-nordic-blue.py --check-icon-candidates` из корня. Геометрия и fonts совпали с Classic в 102 сценариях при DPR1/2; цвета изменились намеренно. Подробности — artifacts/nordic-blue/TASK-008/palette-policy-report.md. Gradients, дополнительные state colors и component visual acceptance — следующие задачи; эта запись не означает готовность темы.

## TASK-009: основные компоненты

Завершено 2026-10-24: активны 104 verified color hooks и 14 отдельно проверенных flat-gradient hooks. Политика обновлена без metric overrides. Для default/toolbar buttons: normal control-bg (toolbar transparent), hover control-hover, focus control-bg + accent border/inherited outline, pressed control-pressed, focus-over accent-soft, focus-pressed #C7DCF6, disabled сохраняет Classic opacity. #C7DCF6 — компонентный state color, RGB 90% control-pressed + 10% accent, rounded; это не новый публичный token. Отличающиеся combined-state значения необходимы для реального вывода правил button mixin в SDK 7.7.

Frames/radius/padding и все шрифты наследуются. 14 unused inner-border color assignments удалены по compiler proof. Следующий этап — TASK-010; новые icon assets по-прежнему не интегрированы. Подробности: artifacts/nordic-blue/TASK-009/core-component-report.md.

## Итог реализации 7.7

В TASK-008–012 проверены177compiled color hooks и31узкое reviewed flat-gradient exception;15канонических токенов выше неизменны. Точные имена/значения/доказательства — config/nordic-blue-policy.json и sass/var в пакете. Исторические52hooks TASK-008 не описывают итоговое число. Нельзя расширять allowlist на geometry/fonts/flags или новые artwork без предусмотренной проверки.
