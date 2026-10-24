# TASK-008: Ввести палитру и проверенный Sass allowlist

Статус: DONE

Зависимости: [TASK-002](TASK-002.md), [TASK-007](TASK-007.md)

Основание: PDF, стр. 5–12. Общие правила: [руководство агента](../../../nordic-blue-agent-guide.md).

## Подзадачи

- [x] 008.1. Задать 15 Nordic tokens из palette.md через dynamic() и согласовать различия имён токенов в таблице/примерах PDF.
- [x] 008.2. Разнести компонентные color overrides по реальному Ext namespace и карте SDK.
- [x] 008.3. Добавить lint-policy для metric/image/position переменных, global base-color, произвольных UI mixins и JS overrides.
- [x] 008.4. Проверить, что lint учитывает разрешённые новые image resources через icon manifest и запрещает изменение их геометрии.

## Артефакты

palette tokens, variable allowlist, lint command/report. Размещать отчёты и доказательства в artifacts/nordic-blue/TASK-008/; пути к исходникам и outputs указать в итоговой записи.

## Критерий завершения

Нет неиспользуемых или несуществующих SDK-переменных; метрики не переопределены; policy обнаруживает контрольное запрещённое изменение.

## Запись исполнителя

- Выполнено 2026-10-23. В package sass/var/all.scss — 15 dynamic tokens. В 13 namespace files — 52 проверенных color hooks; все реально потребляются CSS, все токены используются. Единственные добавления к TASK-002: hover border кнопки и placeholder color поля.
- package.json: explicit sass/var/all.scss перед var directory; реальная сборка Cmd показала необходимость для app/slicer. Generated структура сохранена, SDK/application не изменены.
- Policy: config/nordic-blue-policy.json, config/nordic-blue-icons.json; команда `python tools/lint-nordic-blue.py --check-icon-candidates` (проверена bundled Python 3.12.14). PASS/exit 0; 300 SDK files, 648 image contracts, 182 approved masters; source resources/images и overrides пусты.
- 33 policy controls PASS, включая реальные padding/font size, sprite position, 2x CSS size, JS override и manifest geometry mutation. Integration disabled до TASK-013.
- `app build lab-nordic testing` с Cmd 7.7.0.36 / SDK 7.7.0.31: exit 0, без warnings/errors. Первый отказ с отсутствующим token import сохранён отдельно; причина исправлена.
- Geometry: 102 сценария × DPR1/2, 11 280 element и 1 926 icon comparisons; ноль расхождений метрик/типографики/offsets. Цветовые отличия ожидаемы; pixel equality не заявляется. 180 parent icon assets пока unchanged.
- [Отчёт](../../../../artifacts/nordic-blue/TASK-008/palette-policy-report.md), [compiler proof](../../../../artifacts/nordic-blue/TASK-008/compiler-consumption.json), [policy controls](../../../../artifacts/nordic-blue/TASK-008/policy-controls.json), [geometry](../../../../artifacts/nordic-blue/TASK-008/geometry-comparison.json).
- Ограничения: state palette/gradients/компонентная визуальная приёмка — TASK-009–012, icons — TASK-013, release checks — TASK-014–016.
- Следующая задача: TASK-009.
