# TASK-051 — мягче кнопки, неактивные вкладки в цвет кнопок

После просмотра1.6.0 пользователь просит мягче границы кнопок и менее отвлекающий фон inactive tabs, совпадающий с кнопками. Отдельное preview softer-contours.html сравнивает compiled1.6.0 и scoped candidate CSS на одинаковом palette-sample.js. Неактивные tabs и обычные кнопки: fill#eaf2ff/border#a6bad4; hover#dce9fa/#7f9fc8; buttons pressed#c4daf4/#668cbb. Неактивный tab text#48627f. Фокус#3275d6, active tab fill#edf2f8 и прежние акценты сохранены. Остальные panel/field colors1.6.0 не менялись.

CSS меняет только background/border/text colors, без border widths/fonts/spacing/runtimeJS/artwork или semantic primary inference. Disabled исключены. Предлагаемая иерархия: спокойные ordinary surfaces, более явный blue только для active/focus и взаимодействия.

Ручной browser просмотр и readback computed-paint.json: inactive tabs/buttons совпадают по fill rgb(234,242,255) и border rgb(166,186,212); active rgb(237,242,248). comparison.png — crop полного screenshot без масштабирования. Полная автоматическая geometry/function/pixel/DPR/RTL/browser приёмка и новые сборки не выполнялись. Production package1.6.0/SDK/WGR не менялись. Preview для оценки, интеграция отдельно после направления пользователя.
