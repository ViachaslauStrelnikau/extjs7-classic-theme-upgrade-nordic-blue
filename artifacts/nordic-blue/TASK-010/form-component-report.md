# TASK-010 — Поля, triggers и fieldsets: DONE

Завершено 2026-10-24. SDK 7.7.0.31, Cmd 7.7.0.36, Java 1.8.0_501; Edge 155.0.4283.62, viewport 1280×1600, zoom 100%, DPR 1 и 2, CPU raster и sRGB, locale en-US, timezone Europe/Minsk. Это промежуточный этап; готовность всей темы требует TASK-013–017.

## Изменения

- `sass/var/form/field/Base.scss`: Nordic text для обычных и toolbar labels и Checkbox/Radio box labels; белая поверхность invalid field. Text/Combo/Date/Time/Number/TextArea продолжают использовать проверенные общие form-field hooks TASK-008. Отдельные дублирующие Text overrides не нужны.
- `sass/var/form/field/Trigger.scss`: цвета over/focus/pressed borders; toolbar trigger surface и over/pressed borders. Без размеров/позиционирования и изменения sprite-состояний.
- Новый `sass/var/form/FieldSet.scss`: nb-heading для legend/header, nb-border для рамки. Collapse tool и checkboxToggle используют обычные родительские изображения.
- `config/nordic-blue-policy.json`: 13 точных новых hooks с SDK declarations/consumers; итого **117 color hooks**, 15 tokens и прежние 14 reviewed gradient hooks. Все 117 подтверждены изолированной компиляцией реального Cmd SCSS с уникальными временными цветами; в рабочие CSS/source эти цвета не попадали.
- Кандидат `form-toolbar-trigger-border-color-focus` исключён до установки: в SDK-аудите нет потребителя. Неактивные checkbox/radio/tool glyph hooks также не добавлены: Classic работает с `enable-font-icons: false`. Label hooks охватывают Checkbox и Radio через общий mixin.

## Что сохранено

Цвета ошибок Classic (#c30/#c0272b), invalid indicator, disabled opacity, readonly behavior, фоновые text-bg изображения, trigger/spinner/checkbox/radio/tool sprites. Их рисунки обновляются одобренным v2 в TASK-013. 180 ресурсов, намеченных к замене, пока byte-identical Classic; новые изображения не интегрированы.

Не добавлялись global ellipsis/nowrap, top/left/transform, font или metric overrides, новые UI/mixins, JS overrides. Активные resources/images/ и overrides/ пусты. Generated frame slices могут отражать новые цвета штатной сборки Cmd; это отдельные поверхности, а не подмена стандартных значков.

## Фактические проверки

| Проверка | Результат |
|---|---|
| Реальная Cmd testing сборка лаборатории Nordic | exit 0, без ERR/WRN |
| Полный fixture против принятого Classic TASK-006 | 102 состояния × DPR1/2; 11280 element comparisons и 1926 icon observations, zero drift |
| Действия мышью/клавиатурой | 24 сценария × 2 темы × 2 DPR = 96 успешных выполнений, 48 сравнений пар и 2490 element comparisons |
| Overflow/trigger audit | 20 состояний форм × DPR1/2; client/scroll excess и clipping совпадают, новых overflow нет |
| Color consumption | все 117 hooks найдены в реальных CSS declarations |
| Policy lint и controls | PASS; 39 controls; 648 approved candidates, 300 SDK Sass files |
| Защищённые источники | 18 application/shared-fixture inputs без изменений; baseline 1474 файлов, только прежние документированные различия AGENTS/lab profile/readme |

Действия: text/textarea ввод, ручная дата и выбор времени из picker, Number ArrowUp/Down и max bound, required invalid, readonly блокирует ввод, disabled DOM state; Combo trigger + ArrowDown/Enter, spinner up/down, clear trigger, DatePicker next month + day selection; Checkbox Space on/off, disabled Checkbox, Radio ArrowDown; collapse/expand Fieldset и checkboxToggle. Проверены фактические значения, validity, collapsed/expanded flags, focus/data/scroll и метрики после действия. Полная release functional matrix остаётся TASK-014.

Сравнение геометрии исключает только рассмотренные цвета и gradient-only слои; сохраняет тени по структуре, фоновые URL и icon boxes/offsets, все шрифтовые и box metrics, visibility/opacity, focus/data/scroll. Это не утверждение pixel equality для новой палитры. Для анимированных 7 GIF используется задокументированный первый исходный кадр; реальные собранные GIF проверены по SHA. Raw PNG не редактировались.

Визуально просмотрены raw `form--invalid.png` и `fieldset--checked.png` при DPR1: текст читается, ошибка различима, рамки/легенды на местах. Галерея содержит все 20 form states и 24 action checkpoints при обоих DPR. Более широкая визуальная приёмка после подключения значков — TASK-015.

## Воспроизведение и артефакты

Из корня проекта: `python tools/lint-nordic-blue.py --check-icon-candidates`.
Из `TestApp/theme-lab`: `..\..\node_modules\@sencha\cmd-windows\dist\sencha.exe app build lab-nordic testing` с Java 8. Пользовательские команды сборки/запуска оригинального TestApp в AGENTS.md сохранены.

В этой папке: `build.log`, `commands.json`, `compiler-consumption.json`, `geometry-comparison.json`, `form-action-comparison.json`, `overflow-trigger-audit.json`, `source-guards.json`, `inherited-icons.json`, `lint-report.json`, `policy-controls.json`; исходники capture/analyzers и `review.html`. Raw evidence распаковано в `nordic/captures/pass-1/dpr-{1,2}` и `form-actions/dpr-{1,2}/{classic,nordic}`. Classic states читаются из неизменённого TASK-006. `compiled/` и `source-snapshot/` фиксируют принятый output/source, `artifact-manifest.json` — SHA файлов. `before/` и `before-theme/` — резервные копии до изменений.

Начальные исправления драйвера: отсутствующие в текущем case semantic IDs пропускаются через Map; time picker выбирается по индексу реальной записи, поскольку его DOM item не имеет id. Это исправления диагностики, без изменений SDK или fixture. Первый вызов Fashion без подкоманды завершился exit1; корректный `fashion.js compile` завершился exit0 и дал consumption PASS. Приняты только завершённые capture/action indexes.

Пользователь освободил D; перед работой подтверждено более 4 GiB свободного места. Историческое ограничение TASK-009 снято; архив его evidence остаётся действительным. Следующая задача: **TASK-011 — Grid, Tree и paging**.

## Изменения комментариев

В следующих 11 namespace files обновлён только первый поясняющий комментарий; assignments и их порядок byte-equivalent по строкам, без функциональных изменений:

- `TestApp/packages/local/theme-nordic-blue/sass/var/LoadMask.scss`
- `TestApp/packages/local/theme-nordic-blue/sass/var/ProgressBar.scss`
- `TestApp/packages/local/theme-nordic-blue/sass/var/button/Button.scss`
- `TestApp/packages/local/theme-nordic-blue/sass/var/menu/Menu.scss`
- `TestApp/packages/local/theme-nordic-blue/sass/var/panel/Panel.scss`
- `TestApp/packages/local/theme-nordic-blue/sass/var/picker/Date.scss`
- `TestApp/packages/local/theme-nordic-blue/sass/var/tab/Tab.scss`
- `TestApp/packages/local/theme-nordic-blue/sass/var/toolbar/Toolbar.scss`
- `TestApp/packages/local/theme-nordic-blue/sass/var/view/Table.scss`
- `TestApp/packages/local/theme-nordic-blue/sass/var/window/Window.scss`
- `TestApp/packages/local/theme-nordic-blue/sass/var/grid/header/Container.scss`
