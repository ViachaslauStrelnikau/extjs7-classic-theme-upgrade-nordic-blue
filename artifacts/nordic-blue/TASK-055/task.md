# TASK-055 — анимация переключения вкладок

Статус: DONE для integration/testing build. Версия отдельного пакета: 1.6.4.

Изменить Tab switching: убрать active-panel entrance fade, оставить содержимое панели без анимации и плавно менять paint выбранной вкладки, включая существующий синий inset индикатор, за 180 ms ease-out. Геометрия/фокус/pressed неизменны; reduced motion отключает переход.

Policy разрешает точные SHA-bound Motion.scss и runtime tree override (наследуемый TASK-054); другие override/Sass остаются запрещены. Acceptance — два source lint, реальный Sencha Cmd testing build из contrast-lab, compiled CSS/JS inspection. Не заявлять full release acceptance.

Runtime caveat: contrast-lab не стартует, пока настроенный путь `TestApp/theme-lab/sdk/build/ext-all-debug.js` отсутствует. Не меняй harness/app/SDK для обхода.
