# Nordic Blue icons v1 — стиль и контракты

Статус: WAITING_USER_APPROVAL. Набор создан для проекта; в рабочую тему не интегрирован.

## Рисунок

- Открытые геометрические контуры, лёгкие шевроны, монохромные папки и документы; без объёмных Classic бликов. Векторные мастера созданы заново по смыслу действий.
- Базовый штрих 1.25 единицы на сетке 16×16, round cap/join; для маленьких ячеек минимальная логическая толщина 0.85 CSS px, чтобы резервный GIF не терял стрелку. Большие status icons масштабируют рисунок внутри прежнего canvas.
- Основной контур #43658B, active/hover #3275D6, контур рамки #B7C8DC, мягкая заливка #E3EDFC, disabled baked variant #A7B5C6. Ошибка #BE5363, предупреждение #AD7C27. Для состояний, где Classic применяет opacity/focus ring, сохраняется механизм Classic.
- Центр рисунка совпадает с центром исходной ячейки; размеры DOM, клеток, trigger hit areas и типографика не меняются. Tree elbow/indent и спрайтовые отступы сохранены. Pixel grid привязан к исходным 13/15/16/17 CSS px, а не заменён общей сеткой.
- Источник направления дизайна: локальный Nordic screenshot в docs/reference/nordic-blue. Его неизвестный масштаб не используется для измерений.

## Объём

180 замен ресурсов, 2 отдельных tool adapters, редактируемые SVG со всеми ячейками, отдельные SVG кадров анимаций. Три ошибочно отнесённых к значкам фона из TASK-003 (slider tracks и toast fader) явно переведены в inherit в manifest. Остальные 372 inherit из TASK-003 сохраняются, включая рамки, старые неиспользуемые ресурсы и FontAwesome приложения. Не подключается новый icon font.

## Плотность и fallback

Исходный GIF/PNG 1x остаётся по прежнему относительному пути. Для каждого листа есть независимый 2x экспорт из SVG, включая анимацию; он не получен увеличением растрового 1x. Дополнительный PNG 1x/2x сохраняет полупрозрачное сглаживание, GIF остаётся бинарным по alpha. Для анимаций preferred остаётся GIF с исходными числом кадров, длительностями и loop.

CSS выбирает 2x через `@media (min-resolution: 192dpi)`. `background-size` всегда равен исходной ширине и высоте ВСЕГО sheet в CSS px. CSS background-position и dimensions не умножаются. Например, bitmap 60×720 остаётся sheet 30×360 CSS px, ячейка tool 15×15 CSS px. При DPR1 доступен original-format fallback.

Проверено установленным Fashion из Cmd 7.7.0.36 с его встроенным Node: compile exit 0, реальная media-query selection в Edge при DPR1/2 для всех 182 листов. Компактная запись `min-resolution:2dppx` без пробела ошибочно превратилась в `min-resolutiondppx:2`; этот вариант запрещён. Прямой CLI Fashion на Node24 сначала не запустился из-за fswin ABI; проверенная альтернатива — Node, поставляемый вместе с Cmd. Не менять node_modules ради этой проверки.

## Специальные adapters

Classic tool-sprites.gif имеет 24 строки (30×360). CSS resize (-360) и move (-375) выходят за canvas и повторяют другие значки. Для них подготовлены отдельные 30×15 sheets: x=0 normal, x=-15 hover, y=0. CSS box/hit area остаётся 15×15; меняются только background-image/background-position-y. Нужен явный allowlist этих двух artwork offsets при интеграции. Общий tool sheet не увеличивается. Adapter — CSS ресурса, без JS и без изменения DOM.

Остальные offsets и состояния перечислены в spriteContracts и componentStates manifest. Slider сохраняет диагональные 6 ячеек; radio шириной 51px не разбивается на равные части; form trigger — 17px; tab close — 11px. Нативный select HtmlEditor и FontAwesome приложения наследуются.

## Ограничения доказательств

Реальный Ext fixture: 415 состояний, шесть запусков Classic/Nordic/fallback при DPR1/2. 25 308 сравнений элементов без расхождений rect/типографики/box model; 56 явных наблюдений изменения y у двух tool adapters. Hover/pressed/focus проецируются классами, полный interaction test остаётся отдельной задачей. В приложении Nordic CSS ещё не подключён: календарные синие стрелки на тёмном Classic header — не утверждённое цветовое сочетание темы; контактные листы показывают целевые светлые Nordic surfaces.

Все 182 листа загружаются через CSS, скомпилированный Fashion, при DPR1/2 без ошибок загрузки и с прежними CSS canvas dimensions. В real component fixture наблюдаются 55 заменённых путей, остальные покрыты full-catalog probe и сырыми контактными листами. Это не утверждение о полном функциональном покрытии всех consumers SDK.

Sencha app/package build с новыми ресурсами, resource copying в дочерний package и production minification будут проверены в TASK-013/016 после одобрения. Успешная исходная testing build TASK-001 не является сборкой этих кандидатов.
