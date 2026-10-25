# TASK-042 — тонкая рамка кнопки,1.4.1

Пользователь попросил уменьшить рамку после нажатия, так как она заходит на иконку. В child theme-nordic-blue-soft-contrast1.4.1 удалена дополнительная inset1px focus-тень; существующий1px focus outline перенесён с offset -3px на -1px, поверх native border. Border width/размеры/шрифты/отступы/иконки/JS не менялись. Нажатое состояние и native keyboard focus сохраняются. Родительские пакеты NordicBlue1.0.2/Soft1.0.0 не изменены. WGR не менялся и не пересобирался.

## Фактические проверки

- SDK7.7.0.31/Cmd7.7.0.36;6lab/real x testing/development/production builds exit0, стабильные входные SHA. Логи final-build-* и final-build-commands.json. Существующие navigation-image warnings остаются в логах.
- 3source lint PASS,648approved image SHA в каждом из6выходов; parent-integrity PASS.
- Ручной browser click по native toggle toolbar button «Груз» с существующей folder.png. Compiled1.4.1: selected/focused border1px, outline1px offset-1px, shadow none, button height22px, icon16x16 с left3px. Ненажатая/нажатая соседние кнопки отображены. Записано compiled-button-paint.json. Размеры прочитаны, полная сравнительная geometry приёмка не проводилась.
- Screenshot compiled-button-full.png; compiled-button-detail.png — точный crop его верхней левой области без масштабирования. Preview chrome-preview/button.html загружает compiled CSS, не prototype CSS. Существующий образ папки используется только как demo icon, новых изображений темы нет.

Полная новая автоматическая functional/geometry/pixel/DPR/RTL/browser/motion регрессия не запускалась. Исторические goldens и результаты не переиспользуются как новая приёмка. Поставка source-only содержит3пакета; архивы двух запусков сверены по SHA/bytes в source-reproducibility.json. После обновления пакетов требуется rebuild приложения.

Первый проход сохранён в diagnostic-initial: при diff-review обнаружен слишком широкий replace, затронувший focus поля. До выпуска восстановлен исходный файл и применены ровно2изменения правил кнопки с сохранением исходных переводов строк. Только финальные final-build-* в корне TASK-042, audits и source-delivery являются поставкой. Диагностические архивы не использовать.
