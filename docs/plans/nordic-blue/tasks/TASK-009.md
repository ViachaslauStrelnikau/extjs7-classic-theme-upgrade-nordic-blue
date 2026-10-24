# TASK-009: Оформить Panel, Window, Toolbar и Button

Статус: DONE

Зависимости: [TASK-008](TASK-008.md)

Основание: PDF, стр. 6–7, 10–11, 17. Общие правила: [руководство агента](../../../nordic-blue-agent-guide.md).

## Подзадачи

- [x] 009.1. Применить цвета headers/body/borders/toolbars и normal/hover/pressed/focus/disabled buttons.
- [x] 009.2. Проверить normal/framed/collapsed panels, modal/resizable windows, split/menu buttons и overflow toolbar.
- [x] 009.3. Убирать gradients только после сравнения; radius/frame padding не менять; тени отложить.
- [x] 009.4. Снять промежуточные geometry и визуальные доказательства.

## Артефакты

SCSS core components, core comparison report. Размещать отчёты и доказательства в artifacts/nordic-blue/TASK-009/; пути к исходникам и outputs указать в итоговой записи.

## Критерий завершения

Метрики Classic совпадают; текст не получил новых overflow; все состояния визуально различимы.

## Запись исполнителя

- Завершено 2026-10-24. SCSS Panel/Window/Toolbar/Button: core surfaces, all 7 default/toolbar button states, focus outlines и disabled colors с унаследованной opacity. Активно 104 verified color hooks (52 новых); 14 неиспользуемых inner-border hooks удалены по compiler proof.
- Gradients убраны только после phase-A comparison: 22 сценария × DPR1/2, 2738 comparisons, zero drift. Разрешены 14 конкретных dynamic('none') hooks, SHA-связанных с review evidence. Frame radius/padding/widths и тени не менялись.
- SDK combined-state omission/specificity исправлена через color variables: focus control-bg, focus-over accent-soft, focus-pressed #C7DCF6 (90% control-pressed + 10% accent, RGB rounded). Публичные 15 tokens сохранены, нет CSS/JS overrides.
- Cmd 7.7.0.36 / SDK 7.7.0.31, `app build lab-nordic testing` из theme-lab: exit 0, без warnings/errors. Lint PASS, 39 controls PASS; реальный Fashion probe подтверждает 104 compiled color consumers.
- Финальная geometry: 102 сценария × DPR1/2, 11 280 elements и 1926 icon observations без отклонений; client/scroll bounds и шрифты совпадают, нового overflow нет. Extra core states: 56 Classic/Nordic pairs / 1710 elements, 168 paint pairs distinct, 20 mouse/keyboard checks PASS.
- Все 180 parent icons пока unchanged; approved v2 не подключён. SDK/application/fixture неизменны. Full drag/resize/keyboard release gate ещё впереди.
- Диск D заполнился при копировании diagnostics. Итоговые raw кадры/JSON и snapshots сохранены losslessly в artifacts/nordic-blue/TASK-009/evidence.zip; gallery читает архив без распаковки. Предыдущие диагностические кадры дополнительно сохранены на C (storage-decision.json); SDK и исходники не удалялись.
- [Отчёт](../../../../artifacts/nordic-blue/TASK-009/core-component-report.md), [визуальный просмотр](../../../../artifacts/nordic-blue/TASK-009/review.html), [geometry](../../../../artifacts/nordic-blue/TASK-009/flat-geometry.json), [states](../../../../artifacts/nordic-blue/TASK-009/core-state-comparison.json).
- Следующая задача: TASK-010. Готовность всей темы не заявляется.
