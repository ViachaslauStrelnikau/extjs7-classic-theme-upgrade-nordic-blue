# TASK-010: Оформить поля, triggers и fieldsets

Статус: DONE

Зависимости: [TASK-008](TASK-008.md)

Основание: PDF, стр. 3–4, 11, 15–16, 18. Общие правила: [руководство агента](../../../nordic-blue-agent-guide.md).

## Подзадачи

- [x] 010.1. Применить цветовые параметры Text/Combo/Date/Time/Number/TextArea, Checkbox/Radio и Fieldset.
- [x] 010.2. Проверить trigger/spinner boxes, focus/invalid/disabled/readonly и checked/collapsed состояния.
- [x] 010.3. Диагностировать overflow и arrows через baseline; удалить причину drift без top/left/transform или изменения шрифта.
- [x] 010.4. Не добавлять глобальный ellipsis/nowrap; существующее Classic clipping воспроизвести.

## Артефакты

form SCSS, form state comparisons. Размещать отчёты и доказательства в artifacts/nordic-blue/TASK-010/; пути к исходникам и outputs указать в итоговой записи.

## Критерий завершения

Rect/typography/trigger dimensions и behavior совпадают с Classic, новых overflow нет.

## Запись исполнителя

Завершено 2026-10-24. Изменены form/field/Base.scss, form/field/Trigger.scss, добавлен form/FieldSet.scss в пакете Nordic; config/nordic-blue-policy.json расширен 13 конкретными color hooks. Итого 117 verified color hooks, 15 tokens, 14 прежних gradients. SDK, общая fixture, application configs/code и геометрия не изменены.

- SDK 7.7.0.31 / Cmd 7.7.0.36 / Java 8. Реальная testing сборка `app build lab-nordic testing` из TestApp/theme-lab: exit 0, без ERR/WRN.
- 102 states × DPR1/2: 11280 element comparisons, 1926 icon observations, exact geometry/typography/state/image-offset PASS. Новых overflow нет.
- 24 genuine input/action scenarios × Classic/Nordic × DPR1/2 = 96 успешных выполнений; 48 paired comparisons/2490 elements PASS.
- Compiler consumption всех 117 hooks; lint и 39 policy controls PASS. 18 protected application/fixture inputs, 300 SDK Sass files и 180 inherited icons unchanged. Исходные images/overrides пусты.
- Значки и исходные text-bg/sprites пока Classic; одобренный v2 подключается в TASK-013. Error colors/readonly/disabled behavior сохранены. Готовность всей темы не объявляется.

Подробности, команды и ограничения: [отчёт](../../../../artifacts/nordic-blue/TASK-010/form-component-report.md), [геометрия](../../../../artifacts/nordic-blue/TASK-010/geometry-comparison.json), [действия](../../../../artifacts/nordic-blue/TASK-010/form-action-comparison.json), [галерея](../../../../artifacts/nordic-blue/TASK-010/review.html).

Следующая задача: TASK-011 — Grid, Tree и paging.
