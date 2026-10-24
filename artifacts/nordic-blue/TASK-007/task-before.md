# TASK-007: Сгенерировать и подключить пакет темы

Статус: TODO

Зависимости: [TASK-001](TASK-001.md), [TASK-002](TASK-002.md), [TASK-006](TASK-006.md)

Основание: PDF, стр. 8–14. Общие правила: [руководство агента](../../../nordic-blue-agent-guide.md).

## Подзадачи

- [ ] 007.1. Определить существующий workspace и сгенерировать Cmd theme package theme-nordic-blue; сохранить .sencha/package.
- [ ] 007.2. Подтвердить type=theme, toolkit=classic, extend=theme-classic и использование default UI.
- [ ] 007.3. Добавить Nordic профиль к тому же fixture, не дублируя component configs; resources/images и overrides сначала пусты.
- [ ] 007.4. Собрать неизменённый child и сравнить его с Classic до палитры и новых иконок.

## Артефакты

package scaffold, build profiles, контрольный отчёт inheritance. Размещать отчёты и доказательства в artifacts/nordic-blue/TASK-007/; пути к исходникам и outputs указать в итоговой записи.

## Критерий завершения

Child без overrides совпадает с Classic по геометрии и виду; parent resources загружаются; нет новых JS overrides/UI.

## Запись исполнителя

- Изменённые файлы: не заполнено.
- Команды, версии, exit codes: не заполнено.
- Проверки и ссылки на доказательства: не заполнено.
- Отклонения / блокеры: не заполнено.
- Следующая доступная задача: определить по выполненным зависимостям.
