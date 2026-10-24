# TASK-004 — Nordic icon set v1

**WAITING_USER_APPROVAL**. Выполнены дизайн, masters, 1x/2x export и технические сравнения. Для DONE требуется явное одобрение пользователя по AGENTS.md и его прямому условию.

Версия: `nordic-icons-v1`  
SHA-256 `icon-manifest.json`: `fe8f2ff09d9d1704b6354f46a3927f83e801c845d67d286b8e45c317701c04d6`

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

Требуется одобрить эту версию/hash, рисунок и 2x-варианты, включая два resource adapters resize/move. Решение пока не получено. TASK-013 не начата. Набор не является Nordic golden. После замечаний версия и hash меняются, изменённая часть показывается снова.

## Воспроизведение

Рядом включены make_task004.py, export_task004.py, render.cjs, validate.cjs, make-density-probe.cjs и check-density-probe.cjs; fixture.html совпадает с TASK-003. Python требует Pillow; browser scripts требуют локального Playwright и Edge. Генерация пишет в эту папку и заменяет generated candidates; не запускать поверх уже утверждённого набора без копии версии.

Порядок: make_task004.py → render.cjs → export_task004.py → validate.cjs → make-density-probe.cjs → Fashion compile density-probe.scss density-probe.css → check-density-probe.cjs. Fashion запускать встроенным Node из Cmd: `node_modules/@sencha/cmd-windows/dist/bin/windows/node/node.exe`, CLI: `dist/js/node_modules/fashion/fashion.js compile`. Все итоговые проверки завершились exit 0. Прямой Fashion CLI с внешним Node24 не используется из-за fswin ABI.

В рабочие TestApp, SDK и theme package кандидаты не подключены. Реальная app/package build с ними остаётся TASK-013/016 после одобрения.
