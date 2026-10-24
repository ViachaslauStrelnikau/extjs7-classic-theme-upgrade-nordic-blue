# TASK-004 — Nordic icon set v2

**DONE / APPROVED**. Пользователь явно одобрил `nordic-icons-v2` 2026-10-23 (Europe/Minsk): «Отлично одобряю». Выполнены дизайн, masters, 1x/2x export и технические сравнения.

Версия: `nordic-icons-v2`  
SHA-256 `icon-manifest.json`: `a7ac4cc21bdac41de0dffc6e5fc1dee3adf72eb01edfe6f0ca4de4bbb8433a20`

## Просмотр

- [Полная галерея Classic → Nordic, все sheets и состояния](review/index.html)
- [Обзор](review/overview.png) · [детали](review/state-detail.png)
- [Автоматический выбор плотности, весь каталог](density-probe.html)
- [Стиль и adapters](icon-style.md) · [источники и лицензии](sources-and-license.md)
- [Реальная Ext geometry](density-validation.json) · [Fashion + 182 sheets](density-pipeline.json)
- [Manifest](icon-manifest.json), masters/, candidate/1x/, candidate/2x/.

180 стандартных ресурсов заменены, 2 adapters созданы. Три фоновых ресурса явно наследуются. Все исходные размеры листов и fallback-форматы сохранены. Геометрия реального fixture совпала в 25 308 сравнениях элементов. Проверены анимационные durations/loop, все 182 leaf resource dimensions и автоматическое DPR-переключение через CSS после Fashion.

SDK 7.7.0.31; Cmd 7.7.0.36; Edge 155.0.4283.62; locale en-US, Europe/Minsk, fixture 1320×1600 DPR1/2, full-catalog probe 1280×900. Fixture states — CSS class projections для hover/pressed/focus и настоящие configs для checked/open/disabled, не полная функциональная приёмка.

## Одобрение

Одобрена эта версия/hash, рисунок и 2x-варианты, включая два resource adapters resize/move. Решение записано в [approval.json](approval.json). Точный manifest показа сохранён в reviewed-manifest-v2.json; в текущем manifest исправлена оставшаяся метка версии v1 → v2 и записан статус APPROVED. Artwork, masters и runtime assets не менялись. Оба хеша зафиксированы в approval.json. TASK-013 не начата. Набор не является Nordic golden. После замечаний версия и hash меняются, изменённая часть показывается снова.

## Воспроизведение

Рядом включены make_task004.py, export_task004.py, render.cjs, validate.cjs, make-density-probe.cjs и check-density-probe.cjs; fixture.html совпадает с TASK-003. Python требует Pillow; browser scripts требуют локального Playwright и Edge. Генерация пишет в эту папку и заменяет generated candidates; не запускать поверх уже утверждённого набора без копии версии.

Порядок: make_task004.py → render.cjs → export_task004.py → validate.cjs → make-density-probe.cjs → Fashion compile density-probe.scss density-probe.css → check-density-probe.cjs. Fashion запускать встроенным Node из Cmd: `node_modules/@sencha/cmd-windows/dist/bin/windows/node/node.exe`, CLI: `dist/js/node_modules/fashion/fashion.js compile`. Все итоговые проверки завершились exit 0. Прямой Fashion CLI с внешним Node24 не используется из-за fswin ABI.

В рабочие TestApp, SDK и theme package кандидаты не подключены. Реальная app/package build с ними остаётся TASK-013/016 после одобрения.

## Ревизия v2 по замечаниям пользователя, 2026-10-23

Перерисованы отмеченные на скриншоте символы: gear — симметричные 8 зубьев и прозрачное отверстие; group-clear — читаемый крест; sort_asc/desc — заполненные треугольники; checked/unchecked menu и form checkbox — контрастные рамки и белая галочка на синем; loading — непрозрачные RGB-spokes вместо исчезающих при GIF quantization полупрозрачных точек. Состояния и связанные toolbar/tree варианты обновлены согласованно.

13 ресурсов изменены, 169 сохранены побайтно; число кадров/тайминги GIF и все CSS размеры прежние. При показе v2 требовалось новое одобрение; оно явно получено 2026-10-23, см. approval.json.
