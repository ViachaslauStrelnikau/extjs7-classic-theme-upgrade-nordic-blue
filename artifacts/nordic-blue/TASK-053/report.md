# TASK-053 — возврат исходных полей и более заметное недоступное поле

Пользователь подтвердил кандидат v6 сообщением «Отлично. Собери тему». В `theme-nordic-blue-soft-contrast` версии 1.6.2 поля редактирования оставлены с унаследованными фоном и цветом Nordic Soft; для disabled form item прозрачность повышена с 0.3 до 0.6, чтобы значение и подпись были различимее. Согласованное оформление нижней панели действий (спокойный фон, тонкий верхний разделитель) сохранено.

Изменена только отдельная contrast-тема и её lint/approval metadata. Исходный `TestApp/app.json`, родительские пакеты, SDK и WGR не изменялись. Метрики, размеры, шрифты, поведение компонентов и ресурсы темы не менялись; opacity disabled item является явным утверждённым исключением к исходному требованию сохранения Classic disabled opacity.

## Проверка

- SDK Ext JS 7.7.0.31, Sencha Cmd 7.7.0.36.
- `tools/lint-nordic-soft-contrast.py` — PASS.
- `tools/lint-nordic-blue.py --check-icon-candidates` — PASS (177 color overrides, 31 reviewed gradients, 648 approved image files).
- Из `TestApp/contrast-lab`: `..\..\node_modules\@sencha\cmd-windows\dist\sencha.exe app build testing` — PASS, exit code 0.
- CSS содержит правила TASK-053 в `TestApp/build/theme-contrast/testing/resources/NordicThemeLab-all_2.css`.
- Проверка после build ограничена линтерами, успешной компиляцией и наличием правил в compiled CSS. Полный visual/geometry/function/DPR/RTL/browser acceptance для 1.6.2 не выполнялся; успешная сборка не является полной приёмкой темы.
