# TASK-017: Подготовить поставку и отчёт приёмки

Статус: DONE

Зависимости: [TASK-016](TASK-016.md)

Основание: PDF, стр. 27–30. Общие правила: [руководство агента](../../../nordic-blue-agent-guide.md).

## Подзадачи

- [x] 017.1. Проверить все критерии coverage/traceability, завершить журнал отклонений и hashes артефактов.
- [x] 017.2. Документировать установку темы, переключение обратно на Classic, использование локального Cmd и воспроизводимые команды.
- [x] 017.3. Включить icon masters/license/manifest, palette, build/validation reports; исключить временные debug patches.
- [x] 017.4. Отметить DONE только по доказательствам; указать, что 7.9 не проверена, если задача 018 не выполнена.

## Артефакты

release notes, usage guide, acceptance report. Размещать отчёты и доказательства в artifacts/nordic-blue/TASK-017/; пути к исходникам и outputs указать в итоговой записи.

## Критерий завершения

Пакет воспроизводимо собирается и проверяется на 7.7; все обязательные критерии подтверждены, ограничения явно перечислены.

## Запись исполнителя

- Добавлены installation/rollback и release notes, coverage/traceability, журнал решений/ограничений; tools/nordic-blue-release.py собирает source-only handoff с SVG/approvals/notices/palette/reports.
- Предыдущие artifacts TASK-014/015/016 перепроверены по SHA;700protected source files неизменны. Результаты: TASK-017/integrity-check.json.
- Две независимые упаковки и их CRC/entries/SHA PASS; 883payload files, 1180161bytes. Exact archive SHA: 907de6f78c401109afb1c0205ad3b480bd7522452e4b4cdfc55201efe349b802.
- Никаких SDK/Classic reference assets/node_modules/compiled apps/debug patches в архиве. Лицензия нового artwork честно отмечена как ещё не назначенная владельцем. Технический handoff не заменяет финальное одобрение пользователем вида всех экранов.
- [Receipt](../../../../artifacts/nordic-blue/TASK-017/FINAL-RECEIPT.md), [отчёт](../../../../artifacts/nordic-blue/TASK-017/acceptance-report.md), [установка](../../../nordic-blue-installation.md).
- Обязательные TASK-001–017 завершены. TASK-018 (SDK7.9) OPTIONAL / NOT_RUN; совместимость не заявляется.
