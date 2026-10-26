# TASK-052 — одобренные мягкие контуры включены в1.6.1

Пользователь одобрил TASK-051: «Отлично. Собери тему». Child theme-nordic-blue-soft-contrast1.6.1 включает exact candidate color rules без необходимости preview атрибута. Ordinary buttons/inactive tabs#eaf2ff/#a6bad4, inactive text#48627f; hover#dce9fa/#7f9fc8, button pressed#c4daf4/#668cbb. Active tab background#edf2f8/3px blue accents/тонкий focus сохранены; disabled исключены. Размеры/border widths/fonts/spacing/JS/assets не менялись. Parent NordicBlue1.0.2/Soft1.0.0 побайтово сохранены, WGR не менялся и не пересобирался.

## Фактические проверки

- SDK7.7.0.31/Cmd7.7.0.36,6lab/real x testing/development/production builds exit0. Стабильные входные SHA и final-build-commands.json/logs. Известные navigation-image warnings TestApp остаются в логах.
-3source lint PASS,648approved imageSHA в каждом выходе, child1.6.1/base1.0.2/Soft1.0.0, parent-integrity PASS.
- Ручной browser просмотр реальных компонентов compiled1.6.1, readback tabs/buttons в compiled-paint.json подтверждает совпадающие fill/border и прежний active background. Подключены только compiled CSS и общий sample-shell, softer-contours.css не загружается.
- softer-contours.html показывает local ignored compiled1.6.0 vs current1.6.1 на одинаковом palette-sample.js. compiled-comparison.png — crop без масштабирования, полный screenshot сохранён отдельно.

## Поставка и границы

Source-only ZIP включает3пакета и утверждённые исходники/документацию, без SDK/node_modules/compiled apps. Два запуска упаковки совпадают по SHA/bytes в source-reproducibility.json. Заменить все3пакета и пересобрать приложение. Для Classic вернуть theme-classic и rebuild, пакетные правила исключаются.

Полная новая автоматическая geometry/function/pixel/DPR/RTL/browser/motion приёмка не выполнялась. Исторические goldens неизменны, ранние regression results не являются приёмкой1.6.1. Сборки/fixture просмотр не гарантируют все app/customUI состояния.
