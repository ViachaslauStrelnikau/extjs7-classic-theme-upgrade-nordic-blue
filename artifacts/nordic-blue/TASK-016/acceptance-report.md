# TASK-016 — матрица сборок и интеграция

Статус: **PASS / DONE**, 2026-10-24. SDK **7.7.0.31**, Sencha Cmd **7.7.0.36**, Windows, Java 8. Тема и исходное приложение не менялись.

## Сборки и настоящие output pages

- 12 сборок: laboratory и исходный TestApp через отдельные Classic/Nordic descriptors × development/testing/production; плюс исходная пользовательская `app build testing`: все exit 0.
- Четыре дополнительные development-сборки с поддерживаемыми local.properties: все exit 0. Cmd по умолчанию устанавливает skip.page=1/skip.js=1. Для acceptance включены только упаковка index.html/JS (значения 0); не изменены debug/logger и приложение. Неудачная попытка CLI -D сохранена как диагностика, не считается успешной сборкой.
- Проверены реальные `TestApp/build/{theme-lab,theme-acceptance}/{classic,nordic}/{mode}/index.html`, их microloader/manifest/JS/CSS, cache reload. Ни старый watch, ни замена SDK debug JS не выдаются за output pages. Lab fixture подключается после готовности реального compiled entry; real TestApp работает без инъекции fixture.
- 72 отдельных контекста (24 на браузер), каждый с начальной загрузкой и reload: 144 загрузки, 288 snapshots; **144 пары / 40 230 элементов**, точные размеры, шрифты, offsets, состояния и данные совпали.
- 36 пар manifest: одинаковые родительские packages/inclusion/runtime flags; добавлен только theme-nordic-blue extending theme-classic. Ext.theme.name остаётся Classic: никаких runtime JS overrides не добавлено.
- 648 одобренных resources в каждой из шести Nordic outputs совпали по SHA. Девять каталогов по 182 sheets, DPR1/2 и вынужденный 1x fallback, 18 overview/reload сравнений — PASS. Development CSS imports включены в проверку.
- Console/page errors, HTTP404 и смешение build outputs: 0 в принятой матрице. Исходная пользовательская testing-страница: SDK 7.7.0.31, 4 вкладки / 4 записи, PASS.

## Браузеры и поведение

- edge **155.0.4283.62**: PASS, 204 fixture pairs + 236 action/state pairs + 20 additional core flows, DPR1/2.
- chromium **156.0.8078.4**: PASS, 204 fixture pairs + 236 action/state pairs + 20 additional core flows, DPR1/2.
- firefox **152.0.4**: PASS, 204 fixture pairs + 236 action/state pairs + 20 additional core flows, DPR1/2.

Fresh Classic/Nordic baseline сравнивается строго внутри каждого браузера/DPR. Между браузерами равенство координат/шрифтов не заявляется. TASK-006 неизменён. Полный визуальный pixel golden относится к Edge из TASK-015, не переносится автоматически на Firefox/Chromium.

Firefox 157 запускался, но протокол управления прервался при закрытии context; частичные результаты сохранены в browsers/firefox-157-diagnostic и не включены как PASS. С установленным совместимым Firefox152.0.4 повторён весь набор с нуля. Первые output-page пробы остановились на отсутствии development index; они сохранены в native-pages-initial. Оба диагностических препятствия устранены и перепроверены. Дополнительно сохранены timeout-диагностики при конкурентных запусках; повтор проводится без изменения readiness/сравнений. Исходный сервер возвращал 404 на браузерный /favicon.ico; отдельный read-only acceptance server на51753 отвечает на этот служебный запрос204. Компонентные requests не перехватываются. Принятая матрица явно слушает console.error/pageerror/requestfailed; исходный сервер51752 и приложение не изменены.

## Реальное приложение и ограничения

700 защищённых файлов (пакет, исходный TestApp и общая fixture) неизменны по SHA. Проверены home, confirm selection/No, три другие вкладки и responsive wide navigation. Существующие Main.scss/Application.scss, navigation UI и font-awesome сохранены. Старые build warnings о navigation images встречаются и в исходном Classic; новых warnings нет. Не добавлялись app-specific theme fixes.

Поставка — исходный theme package, собираемый потребляющим приложением; отдельный precompiled standalone package не обещан, standalone build — NOT_REQUIRED. Ext JS7.9 — NOT_RUN, отдельная необязательная TASK-018. Это завершение технической матрицы 7.7, не новое одобрение полного дизайна пользователем и не гарантия для всех сторонних приложений/браузеров.

Доказательства: acceptance-matrix.json, build-commands.json, development-output-commands.json, browser-availability.json, browsers/*/browser-results.json, native-page-comparison.json, native-pages-*.json, source-resource-mode-audit.json, build-mode-validation.json, original-app-testing.json. Все команды и exit codes сохранены; скриншоты доступны в review.html. Следующая задача: TASK-017 (поставка и итоговый отчёт).
