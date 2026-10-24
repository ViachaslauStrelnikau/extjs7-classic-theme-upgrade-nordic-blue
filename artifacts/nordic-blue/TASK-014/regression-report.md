# TASK-014 — геометрия и функциональные сценарии

Статус: **PASS / DONE**, 2026-10-24.

## Результат

- 204 точных сравнения состояний (102 при каждом DPR 1/2) с неизменённым Classic baseline TASK-006.
- 236 пар проверок действий/состояний Classic и Nordic; 360 функциональных checkpoints, 112 проверок состояний основных кнопок и 20 дополнительных реальных flows. Окна: drag, resize, close, Escape, modal Tab/Shift+Tab/Escape; также forms, tabs, grid, tree, menu, paging, slider, panel collapse/expand.
- 21614 сравнений элементов, 3246 сравнений значков, 5400 наблюдений разрешённых image contracts. Необъяснённых различий метрик: **0**.
- 12 проверок resize/move adapter geometry/hit area и реальной click dispatch, включая disabled.
- Все 14 отрицательных контролей отвергнуты. Из них четыре — реальные временные изменения браузера (+1 px transform и +1 px font-size при DPR 1/2); после точного восстановления все четыре снова PASS. Остальные: missing element, wrong count/state, duplicate ID и empty capture при каждом DPR.
- Lint PASS; 672 исходников/ресурсов проверены на неизменность. SDK, приложение, общая fixture и artwork не редактировались.

## Воспроизведение

Из корня проекта: `python tools/nordic-blue-regression/run.py --output artifacts/nordic-blue/regression-new-run`.
Параметры и окружение: [README](../../../tools/nordic-blue-regression/README.md). Нужны работающий lab server и актуальная testing build; output обязан быть новой папкой. Точная фактически выполненная команда: Python runtime из AGENTS, `tools/nordic-blue-regression/run.py --output artifacts/nordic-blue/TASK-014/run-1`. Все шаги завершились с exit code 0; команды/коды — run-1/execution.json.

SDK 7.7.0.31, Cmd 7.7.0.36, Edge 155.0.4283.62, Python 3.12.14, Node (см. provenance.json). Viewport 1280×1600, zoom100%, DPR1/2, en-US, Europe/Minsk, software raster, sRGB. Каждый DPR сравнивался отдельно. Новая сборка темы не требовалась: пакет/compiled outputs не менялись после трёх успешных сборок v3.

## Границы gate

Сравниваются rects, полная записанная typography/box model, transforms/offsets, visibility/opacity, counts/existence/states, focus/scroll/data/stores и approved icon sheet/density contracts. Нет допуска в 1 px. У pseudo нет нативного DOMRect: сохраняются hostRect и точные computed значения, координаты не выдумываются. Только явно перечисленные цвета/обоснованные gradient paint исключаются; shadow geometry остаётся. Это не попиксельная визуальная приёмка.

Драйверы объединены из проверенных TASK-009–013, повторно запущены на активных v3 folders. Активные approval/manifest берутся из config. GIF frame0 policy использует настоящие Nordic GIF; проверяются source/derived SHA. Оригинальная анимация остаётся в runtime; её плавность этим gate не оценивается. Проверены перечисленные детерминированные сценарии, не все возможные конфигурации Ext JS.

Новые window-сценарии не меняют fixture: drag идёт на 60 px вправо/30 px вверх внутри штатного constrainTo; southeast resize добавляет 50×30 px. Первоначальная диагностическая попытка двигать вниз была ограничена Classic host и исправлена в драйвере до принятого запуска. Изменений темы для прохождения теста нет.

## Артефакты

[HTML report](run-1/review.html), run-1/regression-results.json, execution.json, run-status.json, source-guard.json, icon-contract-observations.json, adapter-validation.json, negative-controls/, raw JSON/PNG и поэтапные logs. Код suite: tools/nordic-blue-regression/; исполнявшиеся копии — run-1/. provenance.json связывает версии и активные approval hashes; artifact-manifest.json содержит SHA доказательств.

Следующая задача: **TASK-015**, визуальные сравнения и Nordic golden. Итоговая готовность темы остаётся за TASK-015–017.
