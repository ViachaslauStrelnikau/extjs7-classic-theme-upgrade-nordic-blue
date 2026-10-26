# TASK-054 — согласованные анимации темы

Статус: DONE для integration и testing build (2026-10-26). Полная Classic регрессия не заявляется. Одобрен набор анимаций из motion preview и реализуется только в `theme-nordic-blue-soft-contrast` версии 1.6.3.

Решения: переключение активного tab content — fade opacity 90 ms; окно 70 ms, меню 110 ms, tooltip 100 ms; цветовые переходы кнопок/вкладок/редактируемых полей 120 ms ease-out; focus/pressed feedback без задержки; native tree expand/collapse по 125 ms вместо Ext JS 7.7 default 250 ms. `prefers-reduced-motion: reduce` отключает CSS и tree-анимацию. Геометрия, hit targets и шрифты не меняются.

Линтер разрешает только hash-bound `sass/src/Motion.scss` и единственный hash-bound `overrides/Ext/tree/View.js`; все прочие JS/overrides и новые Sass-правила по-прежнему запрещены.

Приёмка: лinter, реальная Sencha Cmd testing сборка из contrast-lab, проверка compiled CSS/JS и фактического theme output. Не заявлять релизную готовность: полная геометрическая/функциональная браузерная регрессия после изменения motion не входит в эту задачу.


Runtime caveat: the contrast-lab browser harness could not start because its configured `TestApp/theme-lab/sdk/build/ext-all-debug.js` bundle is absent. The installed SDK debug bundle exists elsewhere, but no harness, app or SDK path was changed. Do not treat this as a runtime browser check.
