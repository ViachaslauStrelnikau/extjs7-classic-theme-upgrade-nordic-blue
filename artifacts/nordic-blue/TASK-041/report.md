# TASK-041 — единая верхняя область включена в1.4.0

Пользователь одобрил TASK-040 («Отлично. Мне нравится») и поручил «включай». В theme-nordic-blue-soft-contrast1.4.0 включён общий фон #edf2f8 корневой области, её верхней tab bar и верхнего grid toolbar. Существующие акценты вкладок/заголовков/выбора сохранены.

Правила используют native body.x-border-layout-ct и прямых потомков .x-panel/bodyWrap/tabbar/tabpanel-child/grid-toolbar. Без зависимости от WGR-классов, без runtime overrides, новых JS/изображений/размеров/шрифтов/отступов. Parent NordicBlue1.0.2 и Soft1.0.0 побайтово сохранены (parent-integrity.json). WGR не менялся и не пересобирался.

## Фактически выполнено

- SDK7.7.0.31/Cmd7.7.0.36, шесть lab/real × testing/development/production сборок exit0. final-build-commands.json/logs и стабильные входные SHA final-build-inputs.json. Известные предупреждения об изображениях навигации TestApp остаются в логах.
- Три source lint PASS (source-lint.json);648утверждённых image SHA в каждом из6выходов (resource-audit.json), child version1.4.0/parents1.0.2/1.0.0.
- Ручной браузерный просмотр actual compiled1.4.0: body/tabbar/toolbar rgb(237,242,248), tabbar26px/toolbar27px. Загружены два compiled CSS + общая типографика fixture, unified.css не загружается. compiled-paint.json/compiled-comparison.png.
- Реальный Classic fixture: body rgb(223,232,246), SDK Classic CSS + общая типографика fixture; Nordic CSS отсутствует (classic-styles.json). Возврат theme-classic + rebuild исключает пакетные правила; WGR runtime отдельно не проверен.
- Демо показывает старую1.3.0 из локального ignored build/theme-contrast-1.3.0/testing и новую1.4.0 из текущего build. Упрощённая native структура с HBox/synthetic data, не точная копия WGR.

## Поставка и границы

Обновить все3пакета из source-only ZIP и пересобрать приложение. Новые CSS идут только в дочерней теме. Source-delivery и source-delivery-repeat создаются одинаковой рецептной упаковкой; hashes/bytes сверяются в source-reproducibility.json. SDK/node_modules/compiled apps не входят в ZIP.

Полная повторная автоматическая геометрическая/функциональная/pixel/DPR/RTL/browser/motion регрессия не запускалась. Исторические gates1.2.0 не являются приёмкой1.4.0. Исторические goldens не изменялись. Успешная сборка и просмотр не означают полную проверку всех Classic приложений.
