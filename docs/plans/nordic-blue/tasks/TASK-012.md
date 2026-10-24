# TASK-012: Оформить Tabs, Menu, DatePicker, Progress, Slider и Mask

Статус: DONE

Зависимости: [TASK-008](TASK-008.md)

Основание: PDF, стр. 7, 17–18, 28. Общие правила: [руководство агента](../../../nordic-blue-agent-guide.md).

## Подзадачи

- [x] 012.1. Применить color variables оставшихся компонентов, сохранив их radius и размеры.
- [x] 012.2. Проверить closable/disabled/overflow tabs, nested/check menus, selected/today/calendar navigation.
- [x] 012.3. Проверить horizontal/vertical slider, thumb positions, progress partial/full и load mask.
- [x] 012.4. Завершить coverage и список различий дизайна без изменения application configs.

## Артефакты

secondary SCSS и coverage evidence. Размещать отчёты и доказательства в artifacts/nordic-blue/TASK-012/; пути к исходникам и outputs указать в итоговой записи.

## Критерий завершения

Каждый компонент coverage имеет результат; default UI, геометрия и интеракции сохранены.

## Запись исполнителя

Завершено 2026-10-24. Обновлены tab/Tab.scss, menu/Menu.scss, picker/Date.scss, ProgressBar.scss, LoadMask.scss; добавлен tab/Bar.scss. Итого 177 verified color hooks, 15 tokens, 31 reviewed gradients. Slider bitmap renderer и approved artwork сохранены до TASK-013.

- SDK 7.7.0.31 / Cmd 7.7.0.36 / Java8. Финальная реальная testing сборка exit0, без ERR/WRN; предыдущие диагностические сборки сохранены.
- Phase-A 28 states × DPR1/2: zero drift, 2210 elements / 288 icons; затем14 exact gradients flattened с SHA review.
- Финальный fixture102 states × DPR1/2: 11280 elements / 1926 icons, exact geometry/fonts/state PASS, новых overflow нет.
- 29 сценариев ×2 темы ×2 DPR =116 PASS; 58 paired comparisons /2124 elements. Tabs close/disabled/overflow, nested/check menu keyboard, calendar selected/today/navigation, progress0/42/100%, оба Slider keyboard/drag и Mask show/hide проверены.
- 177 actual CSS consumers включая RGBA; lint и39 controls PASS. Из первоначально исключённых четырёх hooks два mask hooks восстановлены после уточнения RGBA проверки; две действительно неиспользуемые переменные удалены. Byte-identity между разными палитрами не заявляется.
- SDK/application/shared fixture, fonts/metrics и180 inherited icons unchanged. Coverage и intentional differences зафиксированы; вся тема ещё не прошла выпускную приёмку.

Ссылки: [отчёт](../../../../artifacts/nordic-blue/TASK-012/secondary-component-report.md), [coverage](../../../../artifacts/nordic-blue/TASK-012/coverage-status.json), [геометрия](../../../../artifacts/nordic-blue/TASK-012/geometry-comparison.json), [действия](../../../../artifacts/nordic-blue/TASK-012/secondary-action-comparison.json), [галерея](../../../../artifacts/nordic-blue/TASK-012/review.html).

Следующая задача: TASK-013 — интегрировать approved v2 icons; одобрение уже зафиксировано в TASK-004.
