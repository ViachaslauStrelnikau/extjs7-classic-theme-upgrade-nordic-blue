# TASK-005: Создать детерминированный theme-lab

Статус: DONE

Зависимости: [TASK-001](TASK-001.md), [TASK-002](TASK-002.md)

Основание: PDF, стр. 18–24. Общие правила: [руководство агента](../../../nordic-blue-agent-guide.md).

## Подзадачи

- [x] 005.1. Переиспользовать TestApp; добавить один fixture с идентичной структурой для Classic/Nordic и стабильными semantic IDs.
- [x] 005.2. Покрыть все компоненты из coverage.md и управляемые normal/hover/focus/disabled/open/collapsed/selected состояния.
- [x] 005.3. Зафиксировать данные, даты, layout, fonts, locale/timezone; реализовать Ext/layout/data readiness.
- [x] 005.4. Подготовить theme selection/build profiles без изменений production component configs.

## Артефакты

theme-lab fixture, state drivers, coverage checklist. Размещать отчёты и доказательства в artifacts/nordic-blue/TASK-005/; пути к исходникам и outputs указать в итоговой записи.

## Критерий завершения

Все строки coverage доступны и воспроизводимы; одинаковый fixture для обеих тем; нет случайных данных и динамического сопоставления по Ext IDs.

## Запись исполнителя

- 2026-10-23: создан [TestApp/theme-lab](../../../../TestApp/theme-lab/README.md); один fixture для Classic и будущего Nordic, 20 строк coverage, 101 состояний + overview.
- Данные и semantic IDs фиксированы; readiness ждёт editor/fonts/stores/layouts; hover/pressed — реальные browser events, остальные состояния — configs/API Ext.
- [Отчёт и доказательства](../../../../artifacts/nordic-blue/TASK-005/README.md): все Classic сценарии READY без page errors/404; 2 overview reloads дали одинаковые 302 semantic measurements. Доказаны paging, tree, grid, editor и реальные Space/ArrowRight/collapse click.
- Edge 155.0.4283.62; SDK 7.7.0.31; 1280×1600 DPR1, en-US, Europe/Minsk. Evidence collectors exit 0.
- Classic использует полный SDK prebuilt CSS через read-only alias: обычная TestApp build prunes неиспользуемые классы. Исправлены служебные часы HtmlEditor и наблюдение pointerdown у trigger.
- Theme/build profiles подготовлены, Nordic build пока явно unavailable и не подменяется Classic. Активация profiles и сверка реальных Cmd output paths — TASK-007. Это не новая theme build и не release acceptance.
- Существующие production TestApp configs/entry points, SDK, node_modules и одобренный icon set не менялись.
- Следующая доступная задача: TASK-006.
