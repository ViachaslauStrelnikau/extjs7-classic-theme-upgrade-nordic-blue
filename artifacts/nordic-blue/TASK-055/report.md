# TASK-055 — анимация переключения вкладок

Статус: DONE для интеграции в дочернюю тему и testing build (2026-10-26). Пакет `theme-nordic-blue-soft-contrast` обновлён до 1.6.4.

Убрана анимация появления `.x-tabpanel-child`; содержимое после переключения отображается сразу. Вместо неё сама выбранная вкладка плавно меняет фон, border, цвет подписи и уже имеющиеся синие inset-акценты за 180 ms ease-out. Никаких перемещений, изменения размеров/отступов или перекомпоновки нет. Focus/pressed feedback остаётся немедленным.

Остальные настройки TASK-054 сохранены: окно 70 ms, меню 110 ms, tooltip 100 ms, кнопки/редактируемые поля 120 ms, дерево 125 ms. `prefers-reduced-motion` отключает анимации.

Проверки: оба linter PASS; SDK 7.7.0.31 / Sencha Cmd 7.7.0.36; testing build из `TestApp/contrast-lab` завершился exit code 0. Compiled CSS содержит transition selected-tab box-shadow 180 ms, не содержит panel-content fade; app manifest выбирает тему 1.6.4, tree override сохранён.

Runtime harness не запустился: `TestApp/contrast-lab/profiles.json` ссылается на отсутствующий `TestApp/theme-lab/sdk/build/ext-all-debug.js`. Файлы harness и SDK не изменялись. Полная браузерная/геометрическая/функциональная/DPR/RTL regression после этой ревизии не выполнена; полной релизной приёмки нет. Cmd сообщил предупреждение `Expected slices for widget button-1024 due to border radius(3 3 3 3)`; build завершился успешно.
