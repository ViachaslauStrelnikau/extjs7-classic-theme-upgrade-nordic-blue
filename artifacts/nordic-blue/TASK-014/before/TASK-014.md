# TASK-014: Автоматизировать геометрию и функциональные сценарии

Статус: TODO

Зависимости: [TASK-006](TASK-006.md), [TASK-013](TASK-013.md)

Основание: PDF, стр. 18–20, 24, 28–29. Общие правила: [руководство агента](../../../nordic-blue-agent-guide.md).

## Подзадачи

- [ ] 014.1. Настроить geometry comparison по stable IDs: rects и полная typography/box-model, icon boxes и transforms/offsets.
- [ ] 014.2. Проверять existence/count/state correspondence; отсутствие элементов или mismatch — FAIL.
- [ ] 014.3. Реализовать keyboard/mouse flows: tabs/forms/grid/menu/window/tree/paging/slider и collapse/resize.
- [ ] 014.4. Проверить отрицательный контроль: умышленный сдвиг 1 px и изменение font должны проваливать gate; удалить контрольные изменения.

Повторить icon geometry/hit area checks при DPR=1 и DPR=2, сравнивая Classic/Nordic внутри одного DPR; размер bitmap может отличаться, физический/CSS размер значка — нет.

## Артефакты

regression suite, JSON/HTML reports, functional results. Размещать отчёты и доказательства в artifacts/nordic-blue/TASK-014/; пути к исходникам и outputs указать в итоговой записи.

## Критерий завершения

0 необъяснённых geometry deltas; computed metrics идентичны; suite ловит изменения и проходит все coverage states.

## Запись исполнителя

- Изменённые файлы: не заполнено.
- Команды, версии, exit codes: не заполнено.
- Проверки и ссылки на доказательства: не заполнено.
- Отклонения / блокеры: не заполнено.
- Следующая доступная задача: определить по выполненным зависимостям.
