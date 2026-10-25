# TASK-037: интегрировать одобренные таблицы и состояния

Статус: DONE для интеграции/сборки, проверок Edge DPR1/2 и source-only поставки. Полная новая cross-browser/pixel/RTL/7.9 приёмка не подразумевается.

- [x] Зафиксировать явное одобрение финального demo после TASK-035/036.
- [x] Перенести paint в child1.2.0, сохранить parent1.0.1/Soft1.0.0 и648иконок.
- [x] Записать узкий exact-source review декоративной полосы/outline, не разрешать произвольную геометрию.
- [x] Собрать lab и TestApp во всех3режимах; проверить версии/resources/source lint.
- [x] Завершить чистый Classic/child geometry+actions DPR1/2 с проверяемыми paint exceptions и отрицательными контролями.
- [x] Документировать результаты/границы, создать воспроизводимую source-only поставку.
- [x] Отдельный commit/push.

Доказательства: artifacts/nordic-blue/TASK-037/. Первый regression — диагностический FAIL измерителя плоских полей; final regression-2 учитывает native input независимо от декоративной текстуры. Старые baseline/golden не менялись.
