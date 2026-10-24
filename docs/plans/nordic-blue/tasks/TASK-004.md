# TASK-004: Создать дизайн и исходники Nordic icon set

Статус: DONE

Зависимости: [TASK-003](TASK-003.md)

Основание: PDF, стр. 5, 14–17; уточнение пользователя. Общие правила: [руководство агента](../../../nordic-blue-agent-guide.md).

## Подзадачи

- [x] 004.1. Изучить docs/reference/nordic-blue; описать толщину штриха, pixel grid, цвета, hover/disabled и оптический центр значков.
- [x] 004.2. Создать редактируемые masters и runtime assets с прежними размерами отображения и 1x fallback; включить все состояния из manifest.
- [x] 004.3. Собрать sprites с исходными логическими размерами sheet/cell и offsets; для 2x согласовать bitmap dimensions и CSS mapping по руководству; не менять типографику/DOM ради нового символа.
- [x] 004.4. Подготовить контактный лист Classic→Nordic, source/license сведения и перечень символов, которым нужен специальный adapter.

- [x] 004.5. Оценить поддержку 2x в SDK/Cmd; экспортировать повышенную детализацию из masters, сохранив физический/CSS размер. Не ограничиваться увеличением bitmap или DPI-метаданных.
- [x] 004.6. Проверить preview при DPR=1/2: прежние rects/hit areas/логические offsets, все sprite states, отсутствие blur/clipping. Зафиксировать density mapping и fallback в manifest; если 2x невозможен, объяснить причину.
- [x] 004.7. Показать пользователю полный контактный лист, все состояния, Classic→Nordic, натуральный размер и увеличенные 1x/2x фрагменты; перевести задачу в WAITING_USER_APPROVAL.
- [x] 004.8. Получить явное одобрение конкретной версии набора и записать дату, решение и manifest hash. При замечаниях доработать и показать заново. До одобрения TASK-013 не начинать.

## Артефакты

icon masters, runtime candidates, icon-style.md, contact sheet, обновлённый manifest. Размещать отчёты и доказательства в artifacts/nordic-blue/TASK-004/; пути к исходникам и outputs указать в итоговой записи.

## Критерий завершения

Новый набор реально создан; каждый replace покрыт всеми состояниями, сохраняет размеры/offsets и читается на Nordic backgrounds. Невозможные замены явно BLOCKED. Физический размер в интерфейсе сохранён; density/fallback проверены. Пользователь явно одобрил представленный набор; версия/hash и решение записаны. Без одобрения задача остаётся WAITING_USER_APPROVAL, а не DONE.

## Запись исполнителя

- 2026-10-23: создан набор nordic-icons-v2. Каталог: [TASK-004](../../../../artifacts/nordic-blue/TASK-004/README.md), [полная галерея](../../../../artifacts/nordic-blue/TASK-004/review/index.html).
- 180 заменяемых ресурсов + 2 adapters, SVG masters, 1x GIF/PNG fallback, 2x из вектора; анимационные кадры/тайминги сохранены. Три несимвольных фона из TASK-003 явно оставлены inherit.
- Fashion Cmd 7.7.0.36 со встроенным Node: compile exit 0, 182 sheets при DPR1/2 выбирают правильный ресурс, прежний CSS размер. Исправлен найденный дефект compact media syntax; использовать `min-resolution: 192dpi`.
- Edge 155.0.4283.62: 415 состояний fixture, 25 308 сравнений элементов при DPR1/2 (preferred + fallback), геометрические/типографические расхождения — 0. Два tool adapters явно меняют только ошибочные source y offsets, 56 наблюдений; 15×15 CSS box сохранён.
- Ограничения: реальные consumers fixture покрывают 55 заменённых путей; весь каталог проверен отдельным compiled-CSS probe. Hover/focus/pressed — class projection. App/package builds с кандидатами, полноценные interaction tests и Nordic golden не заявлены.
- SDK/TestApp исходники сохранены; TASK-013 не начата.
- Одобрение пользователя: **получено 2026-10-23 (Europe/Minsk)**. Явное решение: «Отлично одобряю». Утверждена версия `nordic-icons-v2`, manifest SHA-256 `a7ac4cc21bdac41de0dffc6e5fc1dee3adf72eb01edfe6f0ca4de4bbb8433a20`, включая 1x/2x и два adapters resize/move. Запись: [approval.json](../../../../artifacts/nordic-blue/TASK-004/approval.json). Существенные изменения требуют нового показа.
- TASK-004 завершена. Следующая доступная задача: TASK-005. Интеграция значков в TASK-013 требует также выполнения остальных зависимостей.
