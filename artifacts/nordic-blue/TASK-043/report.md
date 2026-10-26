# TASK-043 — превью синего акцента вкладки

Пользователь попросил показать вертикальную синюю полосу у заголовка вкладки той же ширины, что у panel/window headers. Отдельный preview TestApp/chrome-preview/tab-accent.html сравнивает compiled1.4.1 с дополнительным paint-only CSS на том же native sample.js.

У активной верхней вкладки добавлен inset3px #3275d6 слева; нижнее3px подчёркивание сохранено. Focus-вариант сохраняет прежнюю1px рамку. Новых border widths/padding/размеров/шрифтов/JS overrides нет. Scope html data-tab-accent=left. Неактивные вкладки без левой полосы.

Ручной browser просмотр и переключение «Инвойсы»/«Журнал СМГС» выполнены. Readback active shadow3px совпадает с panel shadow3px по цвету rgb(50,117,214); compiled-paint в computed-paint.json. comparison.png — crop screenshot без масштабирования, оригинал comparison-full.png. Пакеты/SDK/WGR неизменны, production1.4.1. Новые сборки/автоматические тесты/полная geometry/function/pixel/DPR/browser/RTL приёмка не выполнялись.

Статус: превью подготовлено. В пакет темы не интегрировано; пользователь ещё не оценил этот результат.
