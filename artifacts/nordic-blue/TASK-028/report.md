# TASK-028: общее демо четырёх вариантов

2026-10-25. DONE для демонстрации по запросу пользователя.

Обновлён TestApp/design-preview/index.html: current, provisional reference v2, reference+header1 underline, reference+header3 contrast. Все используют один неизменённый sample.js и одну существующую testing-сборку Soft. reference.css сохранён как предварительный дизайн TASK-026. Новый header-variants.css меняет только grid/column header paint; панели, поля, вкладки и прочие элементы двух дополнительных вариантов остаются v2. В отличие от отдельного header-options screenshot, контрастный вариант здесь сохраняет панельные акценты v2.

boot.js принимает только header1/3 для reference и использует независимые html data attributes. Смена motion сохраняет header query, все4iframe перезагружаются с собственными параметрами. При ширине1500px+ четыре колонки, ниже — две; переключатель «Все четыре в ряд» включает горизонтальную раскладку. Компонентные конфигурации/размеры/шрифты не изменялись; изменена только внешняя оболочка карточек.

Фактически наблюдены все4загруженных набора компонентов, distinct header fills/accents и одинаковое оформление панелей всех3reference. observations.json содержит paint до и после motion on/off; header1/3 сохранены после перезагрузки. Переключатель ряда реально дал4CSSколонки. Снимок four-variants.png снят после возврата default layout/motion off и просмотрен. Проверка самой motion API, полная Classic regression/DPR/browser matrix не выполнялись; новая Cmd-сборка не запускалась. Рабочий пакет/SDK/иконки/policies/goldens не менялись. Отдельные header-options TASK-027 и старые evidence сохранены. Ни один вариант не выбран автоматически.

Демо оставлено открытым: http://127.0.0.1:51754/design-preview/index.html . Отдельный commit/push по постоянному поручению пользователя.
