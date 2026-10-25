# TASK-030: отдельная тема1.1 со светлой шапкой

2026-10-25. DONE для создания/сборки отдельной темы и одобренной светлой ревизии. Это не полная повторная приёмка Classic.

## Решение и архитектура

Тёмный вариант v2 первоначально выбран для отдельного пакета TASK-029. После production-скриншота пользователь одобрил светлые группы/названия колонок. Имя theme-nordic-blue-soft-contrast сохранено для существующего подключения, version1.1.0. Наследование Soft → Nordic Blue → Classic. Cmd-generated child, namespaceExt/classic, overrides пустые, собственного JS/artwork/fonts нет.23parent-reviewed color hooks, ограниченные component paint rules. Original TestApp/config/classes/Sass, родители и SDK не менялись. Старый dark source и6build logs сохранены в TASK-029, не выданы за финальную тёмную поставку.

Группы .x-column-header.x-group-header #e8eef6, названия #f4f6f9, текст #304a68; нейтральные borders/нижняя линия. Active hover/focus/sort #e3edfc. Вертикальная синяя линия у panel title сохраняется, у названий колонок убрана. group-header подтверждён Column.groupHeaderCls в installed classic/classic/src/grid/column/Column.js. cls nb-primary — явный opt-in без изменения размеров. Optional Soft motion наследуется и не auto-included.

## Реальная сборка и просмотр

6Cmd builds exit0: lab и отдельный original-TestApp descriptor × testing/development/production. Cmd7.7.0.36, SDK7.7.0.31, Java8 jdk1.8.0_501 и bundledNode6. Точные папки/команды/logs — build-commands.json/build-*.log. Все3source lint PASS.648approved image SHA совпали в каждом из6выходов; manifests содержат новую тему/version/SDK. Загрузчик Cmd встроен в index.html, отдельного microloader.js после упаковки нет. Первоначальная проверка, требовавшая отдельный файл, была ошибочной; фактический embedded loader подтверждён по id=microloader и Ext.manifest. Old TestApp navigation-image warnings сохранены.

В браузере приложения открыт actual compiled TestApp testing/index.html: Personnel и4вкладки отрисованы. contrast-preview загружает compiled CSS новой темы без reference.css. Просмотрены обычная и grouped таблицы, выполнены сортировка Дата (ASC, computed RGB227,237,252) и выбор строки. Groups computed RGB232,238,246, leaves244,246,249, text48,74,104. observations.json и viewport shots built-preview.png/grouped-headers.png. Full-page screenshot был недоступен, использованы viewport screenshots; высота внешнего iframe увеличена, размеры компонентов не менялись.

## Честные пределы проверки

Новая полная geometry/function/pixel-golden/DPR/browser matrix не запускалась; автоматические тесты не добавлялись. Не заявляется окончательная1:1приёмка всех Classic/custom UI этой ревизии. Перед таким заявлением нужен полный регрессионный gate; source paint-only и успешный Cmd build этого не заменяют. Старые base/Soft acceptance не приписываются новой версии. Goldens неизменны. SDK7.9/полныйRTL/другиеОС/всеproductionoverrides/motion API заново не подтверждены.

## Поставка

Инструкция docs/nordic-soft-light-installation.md. tools/nordic-soft-light-release.py создаёт source-only ZIP со всеми3пакетами/approved masters/configs/notices, безSDK/compiledapp/node_modules; новая лицензия не выдумывается. Первые source-release/source-release-repeat — диагностическая упаковка до итогового отчёта; итоговая поставка source-delivery/source-delivery-repeat включает текущий отчёт. ZIP local/gitignored, manifests versioned. URL http://127.0.0.1:51754/contrast-preview/index.html . TASK-029 — SUPERSEDED по тёмному дизайну, TASK-030 — DONE в пределах описанной сборки/поставки, не полного release gate.
