# TASK-021 — Nordic Soft: интеграция

Статус: техническая интеграция PASS, 2026-10-25. Отдельный пакет `theme-nordic-blue-soft`, сгенерированный установленным Cmd7.7.0.36, наследует Nordic Blue→Classic7.7.0.31. Папкиv2 одобрены пользователем ответом «хорошо. продолжай» на прямой вопрос об интеграции показанных пропорций. Решение связано с точным SHA кандидата в artwork-approval.json. Старые кандидаты/approvals/golden не заменены.

## Реализация

- 3px скругления controls/menu/list и4px окон;24 собственныхPNG/GIF1x/2x дерева,624унаследованных runtime files неизменны. CSS размеры16×16, logical offsets/hit areas не менялись. GIF fallback механически экспортирован из утверждённого PNG с бинарной прозрачностью, как в прежнем pipeline;12GIF sheets декодированы с ожидаемым размером/числом кадров.
- Opt-in `resources/soft-motion.js`:120ms переходы фона/рамки/цвета и150ms opacity при show, мгновенный hide, повторное открытие, учёт authored opacity и системного/ручного reduction. Public component events; нет Ext overrides или изменений прототипов. SDK private shadow API не используется. CSS elevation подключается только при явном публичном shadow:false. Native animateTarget остаётся приоритетным.
- Без автоматического подключения JS к чужому приложению. В выбранной теме статическое оформление работает само; новые эффекты включаются через API. Пример собранного варианта: /soft-preview/index.html . Оригинальный TestApp не переключался молча; есть отдельный consuming descriptor theme-acceptance/soft.

## Доказательства

Начальные6 и финальные6 consuming app builds (lab/real×3modes) завершились exit0. Последняя сборка содержит уточнённый optional opacity module; весь compiled CSS остался byte-for-byte идентичен входам geometry captures. Не заявляется изменение runtime opacity как геометрическая ошибка; оно проверено отдельно и не меняет rect. Все648resource SHA и модуль совпали с источниками в6outputs.

- edge 156.0.4314.42:204fixture pairs+236action/state pairs+20additional core flows, DPR1/2, PASS.
- chromium 156.0.8078.4:204fixture pairs+236action/state pairs+20additional core flows, DPR1/2, PASS.
- firefox 152.0.4:204fixture pairs+236action/state pairs+20additional core flows, DPR1/2, PASS.

Fresh Classic/Soft сравниваются внутри одного браузера/DPR. Разрешены только точные3/4px corner paint по фактической selector ownership; все остальные box/font/offset/state/data/focus проверки остались строгими. 5negative controls (rect/font/radius, реальные source image/Sass изменения) отвергнуты; source bytes и исходные данные восстановлены. Captured-JSON controls не выдаются за реальные DOM mutations.

Финальные actual index.html/microloader/manifest/compiled JS/CSS:144pairs/40230elements, lab и реальные экраны TestApp,3modes×3browsers×DPR1/2, cache reload,0console/page/network errors и смешения outputs. Реальное приложение: home, selection confirm/No,3другие вкладки, wide responsive; app styles и700защищённых файлов неизменны. Existing navigation image build warnings исходного TestApp сохранены, не исправлялись через app-specific patches.

18runtime mode/DPR contexts проверили opacity-only appearance, стабильный rect, authored opacity.6, повторное show/Escape/hide, системное reduction с отменой текущей анимации, ручной off, detach/destroy. Полный182sheet catalog:9mode/native1x/native2x/forced1x runs, HTTP bytes/cache reload и размеры листов PASS. Fallback не меняет source CSS: unsupported density media query симулируется только в response.

## Диагностика и ограничения

Исходный Edge comparator имел отсутствующий browser-config metadata: после добавления фактической версии повторно сравнены те же кадры. Firefox window DPR2 вызвал themeLab до завершения asynchronous boot Classic; copied driver дополнен явным ожиданием создания fixture, затем применяет прежний строгий whenReady. Последний шаг повторён; диагностика и failed execution entries сохранены. Начальный Soft lint ошибочно считал наследуемые tree resources собственными; scope уточнён до24реальных overrides, полная648SHA проверка не ослаблена.

Принятый родительский pixel golden остаётся неизменным. Новой полной Soft pixel-golden калибровки здесь нет: выбранные скругления намеренно меняют контуры. Не выдаём прежний visual PASS за проверку нового варианта. Технический объём и версии перечислены в acceptance-matrix.json; SDK7.9, другиеOS/версии, все customUI и полнаяRTLlayout matrix не заявляются. RTL рисунки и density catalog проверены; inherited GIF smoothness не измерялась. Source package собирается consuming приложением; precompiled standalone theme не обещан.

Установка/опциональные эффекты/откат: docs/nordic-soft-installation.md. Source handoff включает оба пакета и editable masters/approval/manifests/policies/notices/reports, без SDK/compiled apps/Classic reference bitmaps. Новая лицензия artwork владельцем пока не назначена. Release manifest и две одинаковые упаковки фиксируются отдельно; технические результаты не заменяют пользовательский просмотр любых сторонних экранов.
