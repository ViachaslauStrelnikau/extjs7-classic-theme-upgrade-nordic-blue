# TASK-040: единая верхняя область — сравнение

2026-10-25. DONE для отдельного демо по явному запросу пользователя. Интеграция оформления в пакет ещё не выполнялась, выбор ожидается.

URL http://127.0.0.1:51754/chrome-preview/index.html . Верхний iframe — compiled Nordic Soft Contrast1.3.0; нижний — те же CSS/SDK/sample.js и demo-only unified.css. Структура соответствует диагностированной топологии WGR: прозрачный north container, center tab panel, grid docked-top toolbar, west tree. Данные синтетические. WGR и пакеты темы/SDK не менялись. Новый build не нужен.

Предложение: единая поверхность#edf2f8 у root border-layout body, корневой tab bar и toolbar активной страницы; границы и strip смешаны с поверхностью. Синий active underline и шапка данных сохранены. CSS только background/border paint, без новых размеров/отступов/шрифтов/Ext overrides. Начальный selector .x-tabpanel не совпал с реальным DOM: Ext7 root TabPanel имеет .x-panel; стили уточнены по actual bodyWrap/tabbar и body/tabpanel-child/grid-toolbar цепочке с direct-child combinators. Окна/вложенные tab bars/footers не являются целью. Shared .header-main typography воспроизводит app-like north в обоих fixture одинаково, candidate на этот app class не опирается.

Fixture упрощён: north HBox вместо WGR Column layout, toolbar HBox/native overflow вместо app Column layout с внешним CSS. Это демонстрация композиции поверхностей, не точная копия WGR/его бизнес-компонентов. Широкий экран показывает больше действий; при узком они уходят в стандартное меню. Нельзя считать этот стенд полной production проверкой.

Фактически IAB оба native экрана просмотрены, screenshot comparison.png. Actual unified background body/tabbar/toolbar одинаковый rgb237,242,248; наблюдаемые heights tabbar26px/toolbar27px — readback, не полное доказательство геометрии (unified-paint.json). Отдельно открыт тот же native fixture на реальном theme-classic-all-debug.css: отрисованы tabbar и toolbar, unified.css отсутствует, Classic root background rgb223,232,246 (classic-styles.json). Это подтверждает изоляцию предложения в демо; WGR rollback/сборка не запускались. Автоматические тесты/полная geometry/function/pixel/browser/DPR matrix не выполнялись, production compatibility не заявляется.

Следующий шаг после выбора: интеграция только в тему, без WGR CSS/JS/config, точный source/policy review и отдельно разрешённые build/compatibility проверки. Возврат theme-classic и пересборка исключают пакетные стили. Исторические goldens/поставки неизменны. Отдельный commit/push по standing instruction пользователя.
