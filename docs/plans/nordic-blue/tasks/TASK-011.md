# TASK-011: Оформить Grid, Tree и paging

Статус: DONE

Зависимости: [TASK-008](TASK-008.md)

Основание: PDF, стр. 6, 12, 18, 28. Общие правила: [руководство агента](../../../nordic-blue-agent-guide.md).

## Подзадачи

- [x] 011.1. Применить header/row/alternate/selection/hover/border colors, не меняя row/cell/header heights.
- [x] 011.2. Проверить sort, header menu trigger, column resizing, scrollbars, tree indent/expand/selection.
- [x] 011.3. Проверить paging first/previous/next/last/refresh и disabled boundary states.
- [x] 011.4. Сопоставить внутренние rects, focus/navigation и текстовые переносы.

## Артефакты

grid/tree SCSS, comparisons. Размещать отчёты и доказательства в artifacts/nordic-blue/TASK-011/; пути к исходникам и outputs указать в итоговой записи.

## Критерий завершения

Header/rows/triggers/indent/paging geometry и действия сохранены; state colors соответствуют palette.

## Запись исполнителя

Завершено 2026-10-24. Изменены view/Table.scss и grid/header/Container.scss, добавлен grid/column/Column.scss в пакете Nordic; расширен config/nordic-blue-policy.json. Итого 130 color hooks, 15 tokens, 17 reviewed gradients. Grid/Tree используют общие row hooks; Paging — существующие toolbar/form hooks. Row/cell/header heights, tree indent, fonts и behavior сохранены.

- SDK 7.7.0.31 / Cmd 7.7.0.36 / Java 8; две реальные testing сборки лаборатории: exit 0, без ERR/WRN.
- Phase-A 20 states × DPR1/2: 3044 metrics / 326 icon observations PASS; затем 3 header gradients flattened с SHA-linked review.
- Финальный полный fixture: 102 states × DPR1/2, 11280 elements / 1926 icon observations, zero drift. Overflow/clipping и внутренние rects совпадают.
- 23 сценария мыши/клавиатуры × Classic/Nordic × DPR1/2 = 92 PASS, 46 paired comparisons / 3572 elements. Sort, checkcolumn, selection, header menu, resize drag, scrolling, tree navigation, paging controls и disabled boundaries проверены.
- 130 actual compiled color consumers, lint и 39 controls PASS. SDK/application/common fixture и 180 inherited icon resources unchanged. Approved v2 интегрируется в TASK-013.

Отчёт и ограничения: [отчёт](../../../../artifacts/nordic-blue/TASK-011/grid-component-report.md), [геометрия](../../../../artifacts/nordic-blue/TASK-011/geometry-comparison.json), [действия](../../../../artifacts/nordic-blue/TASK-011/grid-action-comparison.json), [галерея](../../../../artifacts/nordic-blue/TASK-011/review.html).

Следующая задача: TASK-012. Готовность всей темы не объявляется.
