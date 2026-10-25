# TASK-038: выделение без рамки — два варианта

2026-10-25. DONE как сравнение двух вариантов по запросу пользователя; выбор для интеграции ожидается.

URL http://127.0.0.1:51754/selection-preview/index.html . Оба iframe используют compiled theme1.2.0, один sample.js и одинаковые данные/конфиги. Вариант1 — текущая голубая заливка без рамки; вариант2 — та же заливка плюс inset3px#3275d6 с первого левого края, как panel header accent. Preview-only CSS через owned html[data-selection-preview], без body cache identity и Ext overrides.

Убраны не только child box shadows1.2.0, но и штатные Classic dotted selected-row/following-row borders. Существующие border widths не менялись; цвета/стиль нейтральные. Mouse-focused cells не добавляют контур выбора; keyboard-only focus сохраняет отдельный индикатор. Последний отдельно вручную не проверялся. Новых artwork/assets/SDK/пакетных/WGR изменений нет. Ни одна из альтернатив ещё не принята в production package.

Для воспроизведения высокой строки, как на пользовательском screenshot, native cellWrap:true задан только demo document column, а selected record содержит длинный текст. Конфиг одинаковый в обоих iframe; это fixture-вариант, не изменение theme geometry. Нативная selection остаётся настоящей, dropdown синхронизирует ID78568 или business ID78565. Parent readiness handshake устраняет load race. App business!important fills сохранены, поэтому color-only выбор на цветных строках может быть незаметен; stripe оставляет видимый акцент.

Фактически в IAB просмотрены оба варианта, tall selected row и business selection. AX подтверждает одинаковые selected ID в обеих таблицах; comparison.png и business-colors.png показывают отсутствие рамок и левую полосу. Native dropdown изменён обратно на tall row перед передачей пользователю. Автоматические тесты, сборки и полная Classic metrics/function/RTL/browser/DPR матрица не запускались. Production1.2.0 и его предыдущие доказательства/goldens остаются неизменными. Следующий шаг — выбор пользователя, затем отдельная интеграция/проверка/поставка.
