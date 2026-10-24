# TASK-006: Зафиксировать исходный Classic baseline

Статус: DONE

Зависимости: [TASK-003](TASK-003.md), [TASK-005](TASK-005.md)

Основание: PDF, стр. 17–24, 28–29. Общие правила: [руководство агента](../../../nordic-blue-agent-guide.md).

## Подзадачи

- [x] 006.1. Снять raw screenshots и DOM rects внутренних/внешних частей по semantic IDs.
- [x] 006.2. Сохранить computed typography, box model, icon boxes/resources/offsets и число ожидаемых элементов.
- [x] 006.3. Запустить повторный захват в том же окружении и убедиться в стабильности.
- [x] 006.4. Записать browser/OS/fonts/version, viewport/DPR, data/state и hash исходников.

## Артефакты

Classic screenshots, metrics JSON, environment manifest. Размещать отчёты и доказательства в artifacts/nordic-blue/TASK-006/; пути к исходникам и outputs указать в итоговой записи.

## Критерий завершения

Baseline получен с SDK 7.7.0.31 и стабильным fixture; пустые группы не принимаются как успех; повторный захват стабилен.

## Запись исполнителя

- 2026-10-23: [Classic baseline](../../../../artifacts/nordic-blue/TASK-006/README.md), ID `classic-7.7.0.31-theme-lab-v1-20261023`, manifest SHA-256 `e3f285aa3a130fe9c74eb7ebff0c290f9ec225d63d2acabc80eaf4ec480faf25`.
- 20 групп, 101 состояние + обзор; два независимых прохода при DPR1/2, 408 raw screenshots + metrics.
- Повторяемость PASS: 11280 element comparisons, 1926 icon observations, отличия метрик/пикселей 0; пустых групп и duplicate/unowned graphics 0.
- Edge 155.0.4283.62; Windows build 26300.9711, 1280×1600, en-US, Europe/Minsk, fonts/source hashes записаны. Capture/compare exit 0.
- Начальный GPU raster отклонён из-за шума градиентов на 1 уровень RGB в 5 DPR2 случаях. Принят software/sRGB launch с точным повторным совпадением; диагностика сохранена. Допуски не увеличивались.
- GIF frame0 route — только snapshot stabilization с исходным размером; живые оригинальные loading снимки сохранены отдельно. Псевдоэлементы имеют CSS box/offsets + hostRect, native DOMRect отсутствует.
- Fixture, SDK, app configs и одобренные Nordic icons не изменены. Полный functional release suite/Nordic golden не заявлены.
- Следующая задача: TASK-007.
