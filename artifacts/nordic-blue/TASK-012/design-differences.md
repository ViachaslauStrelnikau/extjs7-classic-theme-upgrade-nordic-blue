# Различия дизайна после TASK-012

- Nordic Blue: 15 canonical palette tokens; плоские рассмотренные поверхности Panel/Toolbar/Button/Grid/Tabs/Menu/DatePicker/Progress/Mask. Всего 177 color hooks, 31 exact reviewed gradient hooks.
- Classic без изменений: размеры, шрифтовые метрики, border widths/styles, radius, spacing, tree indent, hit areas, state behavior, opacity и анимации. Существующий clipping/ellipsis воспроизведён; глобальные правила не добавлялись.
- До TASK-013 остаются исходными 180 standard image resources, включая tools, tabs close/scroll, menu marks/arrows, calendar arrows, slider tracks/thumbs, loading/text-bg assets. Рисунок Slider на этом этапе полностью наследуется: slider-imageless=false; переключение renderer ради цветов запрещено. Подключение approved v2 и 1x/2x contracts — следующая задача.
- SVG/font/Unicode/CSS triangles вместо родительских символов не добавлялись. Source resources/images/ и overrides/ пока пусты.
- Пиксельное совпадение Classic/Nordic не заявляется из-за палитры; Nordic golden и окончательные визуальные сравнения после новых значков — TASK-015. SDK 7.9 остаётся отдельной optional задачей.
