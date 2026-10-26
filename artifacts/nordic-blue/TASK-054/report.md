# TASK-054 — сдержанные анимации Nordic Soft Contrast

Статус: DONE для theme-package integration и testing build (2026-10-26). Пакет `theme-nordic-blue-soft-contrast` обновлён до 1.6.3.

Одобренные переходы ограничены paint/opacity: активный tab content 90 ms, окно 70 ms, меню 110 ms, tooltip 100 ms, цветовое состояние кнопок/вкладок/редактируемых полей 120 ms ease-out. Pressed/focus feedback остаётся немедленным. Нативное раскрытие и сворачивание дерева ускорено с SDK default 250 ms до 125 ms. `prefers-reduced-motion: reduce` отключает transitions/fades и animation дерева.

Реализация остаётся в отдельном дочернем пакете. В `sass/etc/all.scss` подключён hash-bound `sass/src/Motion.scss`; единственный runtime override — hash-bound `overrides/Ext/tree/View.js` для `Ext.tree.View`. `tools/lint-nordic-soft-contrast.py` по-прежнему запрещает все другие JS/overrides и unreviewed Sass. `TestApp/app.json`, contrast-lab descriptor/fixture, WGR, parent packages и SDK не менялись.

Проверки: `tools/lint-nordic-soft-contrast.py` PASS; `tools/lint-nordic-blue.py --check-icon-candidates` PASS; SDK 7.7.0.31 / Cmd 7.7.0.36; testing build из `TestApp/contrast-lab` PASS. Compiled `NordicThemeLab-all_1.css` содержит все timings и reduced-motion media rule; compiled `app.js` содержит tree override и оба значения 125.

Ограничение: theme package собран и compiled output проверен, но полная геометрическая/функциональная/DPR/RTL/browser regression для этой ревизии не запускалась. Поэтому этот результат сам по себе не является полной релизной приёмкой. Сборка выдала warning о slicing `button-1024` из-за унаследованного border-radius 3px и завершилась с exit code 0.

Runtime review note: a read-only launch attempt through `TestApp/contrast-lab/index.html?theme=nordic&case=tree&state=normal` could not start because `profiles.json` points to missing `TestApp/theme-lab/sdk/build/ext-all-debug.js`. The SDK contains `ext-7.7.0.31/build/ext-all-debug.js`, but I did not change the test harness or copy files into the project to work around it. Compiled output checks passed; actual browser interaction of the new production CSS/override remains pending.
