# TASK-003: Инвентаризация стандартных значков

Статус: DONE

Зависимости: [TASK-001](TASK-001.md)

Основание: PDF, стр. 3–4, 12, 24–26. Общие правила: [руководство агента](../../../nordic-blue-agent-guide.md).

## Подзадачи

- [x] 003.1. Каталогизировать tools, triggers, spinner, grid arrows, paging, button/menu/split, tabs, tree, picker, editor и прочие видимые symbols.
- [x] 003.2. Для каждого получить parent path/render mechanism, image/display dimensions, sprite cell offsets, state map, transparency и component usage.
- [x] 003.3. Сравнить источники в двух SDK-копиях; отделить application icons и font-awesome от штатных assets темы.
- [x] 003.4. Пометить replace/inherit и причину для каждого symbol, включая checkbox/radio, loading и slider.

Дополнительно записать исходный DPR/density, bitmap dimensions, CSS dimensions и logical offsets для каждого asset; отделить число пикселей файла от физического размера значка в интерфейсе.

## Артефакты

icon-manifest.json и контактный лист Classic со всеми состояниями. Размещать отчёты и доказательства в artifacts/nordic-blue/TASK-003/; пути к исходникам и outputs указать в итоговой записи.

## Критерий завершения

Все symbols fixture имеют semantic ID и происхождение; размеры/offsets измерены, нет догадок по одному скриншоту.

## Запись исполнителя

- Изменённые файлы: artifacts/nordic-blue/TASK-003/*, эта карточка и индекс плана. SDK и исходники TestApp не менялись.
- Команды, версии, exit codes: Edge 155.0.4283.62 / SDK 7.7.0.31, isolated capture.cjs exit 0, Python inventory generator exit 0; validation.json PASS. DPR=1, LTR; состояния частично проецируются CSS classes.
- Проверки и ссылки на доказательства: artifacts/nordic-blue/TASK-003/icon-audit.md, icon-manifest.json, sprite-contracts.json, runtime.json, contact-sheets/, parent-atlas/, index.html, validation.json.
- Отклонения / блокеры: блокеров инвентаризации нет. Исходные resize/move tools используют offsets за концом sprite sheet и повторяют другие glyphs; стратегия нового artwork должна быть явно описана в TASK-004. RTL/DPR=2 runtime и функциональное acceptance здесь не выполнялись.
- Следующая доступная задача: TASK-004; по зависимостям также доступна TASK-005.
