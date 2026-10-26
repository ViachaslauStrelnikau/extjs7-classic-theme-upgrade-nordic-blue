# TASK-046 — оформление вкладок интегрировано1.5.0

Пользователь после preview TASK-043/044/045 попросил «собери тему». Child theme-nordic-blue-soft-contrast1.5.0 включает утверждённую3px#3275d6 полосу слева активной верхней вкладки и прежнее нижнее подчёркивание. Фокус использует native1px border color без дополнительной inset рамки. Native dotted label pseudo outline выключен, внешний синий фокус остаётся. Native border widths/шрифты/spacing/JS behavior не менялись. Scope native top tabs, без app-owned preview атрибута. Parent NordicBlue1.0.2/Soft1.0.0 побайтово сохранены; WGR не менялся и не пересобирался.

## Фактические проверки

- SDK7.7.0.31/Cmd7.7.0.36,6lab/real x testing/development/production сборок exit0. Стабильные входные SHA, final-build-commands.json и final-build-*.log. Существующие warnings навигационных изображений TestApp остаются в логах.
-3source lint PASS;648утверждённых image SHA в каждом выходе; версии child1.5.0/parent1.0.2/Soft1.0.0. Parent integrity PASS. Новых ресурсов/шрифтов/JS нет.
- Ручной browser click по native вкладкам на фактически собранной1.5.0. Readback3px left/bottom shadow, отсутствие extra1px inset focus frame и label outline none, native borders сохранены. compiled-tab-paint.json. Дополнительный tab-accent.css не загружается: правила идут из compiled CSS.
- Live comparison tab-accent.html показывает локальный compiled1.4.1 reference и current1.5.0, один sample.js. compiled-comparison.png — crop без масштабирования; полный screenshot сохранён отдельно. Старый compiled reference ignored/local, в поставку не входит.

## Поставка и границы

Source-only архив включает3пакета, инструкции и утверждённые исходники/проверки; SDK/node_modules/compiled apps не входят. Два запуска упаковки сверены по SHA/bytes в source-reproducibility.json. Заменить все3пакета и пересобрать приложение. Для возврата Classic выбрать theme-classic и пересобрать, пакетные стили будут исключены.

Полная новая автоматическая geometry/function/pixel/DPR/RTL/browser/motion приёмка не запускалась. Исторические goldens не менялись; ранние regression gates не выдаются за приёмку1.5.0. Ручной просмотр не доказывает совместимость всех приложений и custom UI.
