# TASK-016: Пройти матрицу сборок и интеграцию

Статус: DONE

Зависимости: [TASK-014](TASK-014.md), [TASK-015](TASK-015.md)

Основание: PDF, стр. 24–29. Общие правила: [руководство агента](../../../nordic-blue-agent-guide.md).

## Подзадачи

- [x] 016.1. Собрать development/testing/production на SDK 7.7.0.31 и проверить соответствующие output pages, а не старый dev/watch.
- [x] 016.2. Проверить resource URLs, sprites, console/network, inclusion flags и отсутствие смешения build outputs.
- [x] 016.3. Пройти geometry/function на Chromium, Edge и Firefox при доступности; при отсутствии браузера оставить конкретную проверку NOT_RUN.
- [x] 016.4. Проверить реальные экраны TestApp и существующие app styles; standalone package build выполнять, если он входит в обещанный формат поставки.

## Артефакты

build logs, browser matrix, real-app evidence. Размещать отчёты и доказательства в artifacts/nordic-blue/TASK-016/; пути к исходникам и outputs указать в итоговой записи.

## Критерий завершения

Обязательные build modes PASS; результаты браузеров явные, нет скрытых NOT_RUN; нет app-specific исправлений ради темы.

## Запись исполнителя

- Изменения: отдельные theme-acceptance descriptors, local.properties для упаковки development pages, tools/nordic-blue-acceptance и отчёты. SDK/theme/app sources не менялись (700 SHA).
- 17 сборок exit0; SDK7.7.0.31/Cmd7.7.0.36, Edge155/Chromium156/Firefox152. Полные версии/команды в acceptance-matrix/build-commands.
- Каждый браузер: 204 fixture +236 action/state pairs, 20 core flows. Реальные output pages:144pairs/40230elements, PASS. Все648resources×6outputs, manifest flags и cache reload — PASS.
- Старые navigation warnings сохранены; standalone precompiled package NOT_REQUIRED; SDK7.9 NOT_RUN. Диагностика Firefox157 и development CLI сохранена отдельно и не считается PASS.
- [Отчёт](../../../../artifacts/nordic-blue/TASK-016/acceptance-report.md), [галерея](../../../../artifacts/nordic-blue/TASK-016/review.html).
- Следующая задача: TASK-017.
