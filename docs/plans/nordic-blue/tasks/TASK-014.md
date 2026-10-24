# TASK-014: Автоматизировать геометрию и функциональные сценарии

Статус: DONE

Зависимости: [TASK-006](TASK-006.md), [TASK-013](TASK-013.md)

Основание: PDF, стр. 18–20, 24, 28–29. Общие правила: [руководство агента](../../../nordic-blue-agent-guide.md).

## Подзадачи

- [x] 014.1. Настроить geometry comparison по stable IDs: rects и полная typography/box-model, icon boxes и transforms/offsets.
- [x] 014.2. Проверять existence/count/state correspondence; отсутствие элементов или mismatch — FAIL.
- [x] 014.3. Реализовать keyboard/mouse flows: tabs/forms/grid/menu/window/tree/paging/slider и collapse/resize.
- [x] 014.4. Проверить отрицательный контроль: умышленный сдвиг 1 px и изменение font должны проваливать gate; удалить контрольные изменения.

Повторить icon geometry/hit area checks при DPR=1 и DPR=2, сравнивая Classic/Nordic внутри одного DPR; размер bitmap может отличаться, физический/CSS размер значка — нет.

## Артефакты

regression suite, JSON/HTML reports, functional results. Размещать отчёты и доказательства в artifacts/nordic-blue/TASK-014/; пути к исходникам и outputs указать в итоговой записи.

## Критерий завершения

0 необъяснённых geometry deltas; computed metrics идентичны; suite ловит изменения и проходит все coverage states.

## Запись исполнителя

- Выполнено 2026-10-24. Suite: tools/nordic-blue-regression/, команда run.py --output <новая папка>.
- Полный отчёт: artifacts/nordic-blue/TASK-014/regression-report.md; HTML/JSON и raw evidence: run-1/.
- 204 coverage pairs +236 action/state pairs, 12 adapter checks, 14 negative controls, 0 metric deltas. Все child exit codes 0.
- Настоящие +1 px/font controls отвергнуты; после удаления изменений PASS. SDK/fixture/theme/application не менялись. Сборка повторно не требовалась.
- Ограничения и версии: regression-report.md, provenance.json и execution.json. Блокеров нет.
- Следующая доступная задача: TASK-015; финальная готовность пока не заявляется.
