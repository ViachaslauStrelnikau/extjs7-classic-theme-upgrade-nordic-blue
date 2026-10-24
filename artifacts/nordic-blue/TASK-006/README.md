# TASK-006 — исходный Classic baseline

Статус: **DONE**, 2026-10-23. Baseline `classic-7.7.0.31-theme-lab-v1-20261023`. Manifest SHA-256: `e3f285aa3a130fe9c74eb7ebff0c290f9ec225d63d2acabc80eaf4ec480faf25`.

## Результат

- 20 coverage groups, 101 именованное состояние + обзор. DPR1 и DPR2, два независимых прохода: **408 raw PNG** и 408 metrics JSON.
- Точное повторное сравнение: **11280 элементов**, **1926 icon observations**, отличающихся метрик/пикселей — **0**. В обзоре 841 внутренних/внешних частей поверх 302 исходных semantic элементов fixture. Ожидаемые числа заданы отдельно для каждого состояния и плотности.
- Typography, box model, rects, clipping-related overflow/scroll sizes, image boxes/resources/offsets, pseudo CSS, stores/data/state, browser/OS/font hashes сохранены. Пустых групп, duplicate IDs и неназначенных graphics — 0. Resource/page errors — 0.
- Семь animated GIF стабилизированы первым оригинальным кадром в browser route. Четыре отдельные live screenshots сохраняют оригинальную анимацию SDK. Файлы SDK/TestApp и одобренные Nordic icons не изменялись.

## Просмотр и доказательства

- [Галерея](review.html): выбор case/state/DPR/прохода, оригинальные PNG и JSON.
- [Baseline manifest](baseline-manifest.json), [repeatability](repeatability.json), [expected counts](expected-counts.json).
- [Environment](environment.json), [font hashes](font-files.json), [source hashes](input-hashes.json).
- [Observed resources](resource-manifest.json), [frozen GIF map](frozen-resources.json), [live animated screenshots](live-animated/index.json).
- [Capture protocol](capture-protocol.md), [отклонённая GPU-диагностика](diagnostics/gpu-raster/repeatability.json), [renderer probe](diagnostics/renderer-probe.json).

Сервер галереи: встроенным Node Cmd запустить этот каталог/review-server.cjs; открыть напечатанный локальный адрес. Для воспроизведения collectors нужны bundled runtime Node/Playwright/Edge и Pillow; snapshot source scripts рядом. Существующий TestApp/theme-lab server остаётся отдельным.

## Почему фиксирован renderer

Default GPU launch дал пять DPR2 снимков с шумом градиентов на 1 уровень RGB при полностью одинаковых метриках. Эти результаты не приняты и сохранены с оригиналами/diffs. Проверенный software launch `--disable-gpu --force-color-profile=srgb` дал точное совпадение полного набора в обеих плотностях. Не применялись pixel tolerance, color normalization или masks. Для сравнения Nordic повторять этот режим.

## Границы

Это Classic baseline на полном unchanged SDK prebuilt CSS 7.7.0.31, не новая Cmd theme build и не Nordic golden. Существующие старые warnings TestApp navigation UI не включаются в этот fixture. Native GIF timing не заявляется frozen behavior: контролируется только snapshot frame. Псевдоэлемент не имеет DOMRect API: сохранены его CSS box/offsets и hostRect с rect=null; не выданы выдуманные координаты. Полная interaction/release matrix и Classic↔Nordic comparison ещё NOT_RUN.

Не обновлять baseline ради принятия расхождений новой темы. Следующая задача: **TASK-007**, генерация отдельного theme package и проверка неизменённого child относительно этого эталона.
