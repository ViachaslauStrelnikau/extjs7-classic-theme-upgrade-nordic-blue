# TASK-013: Интегрировать новые значки

Статус: DONE

Зависимости: [TASK-004](TASK-004.md), [TASK-007](TASK-007.md), [TASK-009](TASK-009.md), [TASK-010](TASK-010.md), [TASK-011](TASK-011.md), [TASK-012](TASK-012.md)

Основание: PDF, стр. 12, 24–26; уточнение пользователя. Общие правила: [руководство агента](../../../nordic-blue-agent-guide.md).

## Условие начала

TASK-004 завершена после явного одобрения пользователя. Проверить записанные дату, решение и hash/версию одобренного manifest; интегрировать именно этот набор. Отсутствие ответа или готовый контактный лист не разрешают интеграцию.

## Подзадачи

- [x] 013.1. Размещать только изменяемые runtime resources по проверенным parent-relative путям; проверить фактические output URLs Cmd.
- [x] 013.2. Применить подтверждённые adapters для font/CSS icons без изменения box/DOM/behavior; остальные assets наследовать.
- [x] 013.3. Проверить все state sprite cells, offsets, transparency, cache reload и отсутствие 404 во всех build modes.
- [x] 013.4. Снять Classic→Nordic icon gallery и обновить manifest с hash исходного/нового asset.

Проверить выбор 1x/2x ресурсов, 1x fallback и все state mappings в реальной сборке при DPR=1/2. Отображаемый физический/CSS размер, rects и hit areas остаются исходными.

## Артефакты

runtime icon set, asset manifest, built icon gallery. Размещать отчёты и доказательства в artifacts/nordic-blue/TASK-013/; пути к исходникам и outputs указать в итоговой записи.

## Критерий завершения

Все planned replace реально видны в сборке; размеры/offsets/хит-области неизменны; нет случайного наследования старого значка или подмены соседней sprite cell.

## Запись исполнителя

Завершено2026-10-24. Интегрирован именно approved nordic-icons-v2 с неизменённым manifest SHA a7ac4cc21bdac41de0dffc6e5fc1dee3adf72eb01edfe6f0ca4de4bbb8433a20. Установлены648 runtime files, новый exact SHA-bound sass/src/Component.scss (294 parent-selector mappings плюс2 approved adapters), integrationEnabled=true. Artwork не менялся; повторное одобрение не требовалось.

- Testing/development/production Cmd7.7.0.36 на SDK7.7.0.31: exit0, без ERR/WRN. Все648 approved bytes в трёх outputs совпадают.
-102states ×DPR1/2:11280elements/1926icons, zero unexplained geometry drift. Approved size/path/density и48 adapter observations проверены, offsets остальных ячеек неизменны.
-9 build-mode/DPR/fallback runs:182sheets/run, реальные native URLs/HTTP hashes/cache reload;18overview comparisons/15138elements PASS.
-304 executions прежних form/grid/secondary drivers,152pairs/8186elements PASS. Resize/move graphic15×15 и Classic component hit areas сохранены; normal/hover/disabled clicks проверены.
-45 policy controls и7 geometry/resource negative controls PASS. SDK/application/common fixture и approved masters/manifest/approval неизменны; JS overrides пусты.
- Slider tracks/toast fader наследуются по approved manifest; thumbs заменены.52 logical replacement resources наблюдались native, все182 sheets загружены в full built catalog. Нет заявления о вызове каждого SDK consumer либо финальной готовности темы.

[Отчёт](../../../../artifacts/nordic-blue/TASK-013/icon-integration-report.md), [manifest](../../../../artifacts/nordic-blue/TASK-013/integration-manifest.json), [геометрия](../../../../artifacts/nordic-blue/TASK-013/geometry-comparison.json), [build modes](../../../../artifacts/nordic-blue/TASK-013/build-mode-validation.json), [галерея](../../../../artifacts/nordic-blue/TASK-013/review.html).

Следующая задача: TASK-014; затем visual golden/release gates TASK-015–017.

## Одобренная последующая ревизия папок

2026-10-24 пользователь одобрил v3: «хорошо. продолжай». Подключены3 изменённых folder variants (12PNG/GIF1x/2x), ordinary folder и636остальных файлов сохранены. Реальные3build modes,102states×DPR1/2 и92Grid/Tree/paging actions PASS. [Отчёт ревизии](../../../../artifacts/nordic-blue/REV-001-folders-v3/integration-report.md). Актуальные manifest/approval paths находятся в config/nordic-blue-icons.json; исходные v2 evidence неизменны. Следующая задача — TASK-014.
