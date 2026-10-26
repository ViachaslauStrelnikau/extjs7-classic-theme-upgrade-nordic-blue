# TASK-044 — убрать пунктир текста вкладки

По просьбе пользователя в кандидатном preview удалён native dotted outline псевдоэлемента .x-tab-button::before только у top tabs в html[data-tab-accent=left]. Внешний синий1px focus inset сохранён, вместе с активными полосами3px слева/снизу. Native keyboard listeners/behavior, border widths/шрифты/spacing не менялись. Пунктир внутри лейбла не используется и при keyboard focus; видимый внешний синий фокус остаётся.

Ручной browser click по native вкладке выполнен; computed pseudo outline-style none, внешний focus shadow1px и активные полосы3px сохранены (clicked-tab-paint.json). Скриншот clicked-preview-full.png и точный crop clicked-preview.png. Автоматические тесты/сборки/полная функциональная/геометрическая/визуальная/DPR/RTL/browser приёмка не запускались.

Это дополнение TASK-043 к отдельному превью. Production package1.4.1/SDK/WGR не менялись. Оценка обновлённого результата пользователем ожидается.
