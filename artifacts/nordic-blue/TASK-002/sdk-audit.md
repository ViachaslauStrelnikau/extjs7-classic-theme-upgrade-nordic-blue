# TASK-002: аудит установленного SDK и TestApp

Дата: 2026-10-23. Статус: DONE (аудит, без реализации темы). Основание: карточка TASK-002, палитра проекта и исходники установленного SDK.

## Область и воспроизводимость

Рабочий SDK берётся из TestApp/workspace.json: path=ext, version=7.7.0.31. Parent chain подтверждена package.json: theme-classic → theme-neutral → theme-base, toolkit=classic; theme-base requires classic. ext-theme-classic — alternateName. Обе копии SDK проверены по содержимому Sass/resources/package.json, не только по version.properties.

| Тема | Файлов TestApp/ext | Файлов root SDK | Различий |
|---|---|---|---|
| theme-base | 108 | 108 | 0 |
| theme-neutral | 168 | 168 | 0 |
| theme-classic | 336 | 336 | 0 |

Индекс: 300 SCSS, 2077 глобальных имён. Политика: 50 точных color overrides; 857 обнаруженных имён метрик; списки flags/image hooks/gradients записаны отдельно. Полные hashes и относительные пути — input-hashes.json; поля объявлений и ссылок проверены по строкам исходников.

## Фактические значения parent SDK

Таблица показывает ближайшие исходные выражения. Это не результат вычисления всех mixins и не измерения готового fixture. Значения с dynamic() и ссылками наследуются, а не копируются в дочернюю тему.

| Переменная | Classic parent expression | Источник |
|---|---|---|
| `$font-family` | `dynamic(tahoma, arial, verdana, sans-serif)` | [TestApp/ext/classic/theme-classic/sass/var/Component.scss:8](D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue/TestApp/ext/classic/theme-classic/sass/var/Component.scss:8) |
| `$font-size` | `dynamic(12px)` | [TestApp/ext/classic/theme-classic/sass/var/Component.scss:9](D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue/TestApp/ext/classic/theme-classic/sass/var/Component.scss:9) |
| `$form-field-height` | `dynamic(22px)` | [TestApp/ext/classic/theme-classic/sass/var/form/field/Base.scss:4](D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue/TestApp/ext/classic/theme-classic/sass/var/form/field/Base.scss:4) |
| `$form-trigger-width` | `dynamic(17px)` | [TestApp/ext/classic/theme-classic/sass/var/form/field/Trigger.scss:4](D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue/TestApp/ext/classic/theme-classic/sass/var/form/field/Trigger.scss:4) |
| `$form-trigger-border-width` | `dynamic(0 0 1px)` | [TestApp/ext/classic/theme-classic/sass/var/form/field/Trigger.scss:5](D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue/TestApp/ext/classic/theme-classic/sass/var/form/field/Trigger.scss:5) |
| `$grid-header-trigger-width` | `dynamic(14px)` | [TestApp/ext/classic/theme-neutral/sass/var/grid/header/Container.scss:86](D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue/TestApp/ext/classic/theme-neutral/sass/var/grid/header/Container.scss:86) |
| `$grid-header-trigger-height` | `dynamic(22px)` | [TestApp/ext/classic/theme-neutral/sass/var/grid/header/Container.scss:80](D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue/TestApp/ext/classic/theme-neutral/sass/var/grid/header/Container.scss:80) |
| `$tool-size` | `dynamic(15px)` | [TestApp/ext/classic/theme-classic/sass/var/panel/Tool.scss:4](D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue/TestApp/ext/classic/theme-classic/sass/var/panel/Tool.scss:4) |
| `$panel-frame-border-radius` | `dynamic(4px)` | [TestApp/ext/classic/theme-neutral/sass/var/panel/Panel.scss:334](D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue/TestApp/ext/classic/theme-neutral/sass/var/panel/Panel.scss:334) |
| `$panel-frame-padding` | `dynamic(4px)` | [TestApp/ext/classic/theme-neutral/sass/var/panel/Panel.scss:357](D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue/TestApp/ext/classic/theme-neutral/sass/var/panel/Panel.scss:357) |
| `$panel-ignore-frame-padding` | `dynamic(false)` | [TestApp/ext/classic/theme-neutral/sass/var/panel/Panel.scss:480](D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue/TestApp/ext/classic/theme-neutral/sass/var/panel/Panel.scss:480) |
| `$image-extension` | `dynamic('gif')` | [TestApp/ext/classic/theme-classic/sass/var/Component.scss:10](D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue/TestApp/ext/classic/theme-classic/sass/var/Component.scss:10) |
| `$enable-font-icons` | `dynamic(false)` | [TestApp/ext/classic/theme-neutral/sass/var/Component.scss:70](D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue/TestApp/ext/classic/theme-neutral/sass/var/Component.scss:70) |
| `$slider-imageless` | `dynamic($enable-font-icons)` | [TestApp/ext/classic/theme-neutral/sass/var/slider/Multi.scss:57](D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue/TestApp/ext/classic/theme-neutral/sass/var/slider/Multi.scss:57) |
| `$include-default-uis` | `dynamic(true)` | [TestApp/ext/classic/theme-classic/sass/var/Component.scss:11](D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue/TestApp/ext/classic/theme-classic/sass/var/Component.scss:11) |
| `$include-rtl` | `false !default` | [TestApp/ext/classic/theme-base/sass/var/Component.scss:94](D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue/TestApp/ext/classic/theme-base/sass/var/Component.scss:94) |

Ширина form trigger именно **17px**, а не общий neutral default 22px. Tool — 15px вместо neutral 16px. Global font — tahoma, arial, verdana, sans-serif / 12px вместо neutral Helvetica / 13px. Эти различия подтверждают необходимость наследовать установленный theme-classic.

## Allowlist, denylist и производные значения

1. Разрешить только точные color assignments из variable-policy.json. Значения Nordic и источник каждого имени находятся в variable-map.md/JSON. Не применять wildcard `*-color`. Не изменять глобальный `$base-color` (#C0D4ED в Classic): от него зависят многочисленные component base/state colors.
2. Запретить изменение fonts/line-height/letter-spacing/text-transform, widths/heights/min/max/size, border-width, padding/margin/spacing/indent, radius/frame padding, позиции/sprite offsets и box-sizing. Политика содержит обнаруженные имена метрик; произвольный CSS с этими свойствами запрещён независимо от того, попало ли имя в список.
3. Default deny для всех иных Sass overrides. Существующие image/glyph hooks перечислены отдельно: artwork и HiDPI согласуются по manifest/одобрению в TASK-003/004/013; не менять логические box sizes/offsets.
4. Не изменять include/enable flags, prefix, image-extension, slider-imageless и panel-ignore-frame-padding. `include-default-uis=true` не гарантирует включение всех классов: generated Sass содержит class-specific `$include-ext-*` и фактические imports. Theme-lab должен явно требовать нужные компоненты.
5. Gradients отделены от color allowlist. Например, button-default-background-gradient можно убрать только после component/frame сравнения. Shadow и radius не считать безопасными автоматически. Никакого глобального shadow/radius patch.
6. Политика — спецификация для будущего lint в TASK-008. Наличие JSON не означает, что CI уже блокирует нарушения.

### Frames и default UI

theme-neutral/sass/var/panel/Panel.scss:334,357,480 задаёт radius=4px, padding=4px и ignore-frame-padding=false. Описание там же и frame mixin theme-base/sass/etc/mixins/frame.scss:126–137 подтверждают обработку дополнительного frame padding. Не менять даже radius без пересмотра геометрии.

Основные mixins находятся и в sass/var, а не только в sass/etc: panel/Panel.scss содержит extjs-panel-ui, tab/Tab.scss — extjs-tab-ui, tab/Bar.scss — extjs-tab-bar-ui и extjs-tab-panel-ui. Наличие color variable в var-файле не означает, что её единственный consumer — другой var. Default tab UI вызывается theme-neutral/sass/src/tab/Bar.scss:1–3. Panel default/default-framed включаются своими include flags.

## Аудит TestApp: отдельные конфликтующие стили

Все app-owned JS/SCSS/CSS/JSON/HTML вне ext/build/bootstrap перечислены в app-audit.json. В app.json требуется только font-awesome; overrides путь объявлен, но TestApp/overrides отсутствует. В проверенных app sources `override:` не найден.

| Источник | Что обнаружено | Последствие / действие следующего агента |
|---|---|---|
| TestApp/app/view/main/Main.js:24 | ui: navigation | Стартовый экран не является стандартным default UI. Сохранить для интеграционной регрессии, добавить отдельный default fixture в TASK-005. |
| Main.scss:8–42 | extjs-tab-panel-ui navigation: padding 24px, fonts 15px/19px/bold, icons 24×24, border 0, bar #404040, strip height 0 | Эти размеры и цвета принадлежат приложению и могут перекрывать Nordic default tokens. Не переносить и не исправлять их в теме. |
| Main.scss:47–61 | extjs-panel-ui navigation: header font 20px/24px, icons 24×24, icon-spacing 15px, text margin 36px, header padding 0 | Дополнительный custom UI с собственной геометрией. Отдельно проверять Classic↔Nordic в этом приложении. |
| Main.scss:64–87 | .x-title-icon-navigation, .x-tab-icon-el-navigation, .x-tab-over/.x-tab-active; Font Awesome, font-size/line-height 24px, :after top 30px/right -24px | Application CSS может фиксировать glyph/color/position независимо от темы. Не брать эти selectors как образец для Nordic. |
| Main.js:40,79,86,92,98 | fa-th-list/home/user/users/cog | Это app-level Font Awesome icons, отдельные от штатных Classic image sprites. Не заменять glyph font для всей темы. |
| app/Application.scss:5; app.json requires | enable-font-awesome=true и пакет font-awesome | Не путать с enable-font-icons: false в parent Classic. Подключение шрифта не переводит штатные tools/triggers в font-icons branch. |
| Main.js:64–73 | bodyPadding 20, tab width 120 в tall, responsive header orientation | App configs меняют размеры независимо от темы; geometry сравнивать при одинаковом viewport/state. |

Generated TestApp-all.scss подтверждает порядок: theme-base/neutral/classic → font-awesome → app/Application → app/view/main/Main. Приложение добавляет UI mixins и CSS после theme src. Доказательства строк imports — app-audit.json. Общих app-level .x-btn/.x-form-trigger overrides не найдено; найденные .x-* scoped navigation rules перечислены выше.

## Причина warnings tab-navigation-*

Main.scss вызывает extjs-tab-panel-ui($ui: navigation). В theme-neutral/sass/var/tab/Bar.scss этот mixin вызывает extjs-tab-ui с тем же $ui. При enable-font-icons=false Tab.scss:4114 ищет `tab/tab-#{$ui}-close`; Bar.scss:709–712,846–876 — `tab-bar/#{$ui}-more*` и scroll images. Поэтому для navigation строятся navigation-relative имена, тогда как parent Classic поставляет default variants. Проверка наличия всех 11 предупреждённых имён и default counterparts записана в app-audit.json.

Это воспроизводимые предупреждения исходного app UI: testing build в TASK-001 завершился exit 0, а стартовая browser smoke-проверка не показала failed requests. Это НЕ доказательство корректности всех close/overflow состояний navigation. Не скрывать warning переключением enable-font-icons, SDK-редактированием или переносом готовых sprites между SDK.

Для TASK-005 использовать default UI fixture, сохранив navigation как отдельный integration case. Если продукту понадобится полнота navigation UI, отдельно определить требуемые ресурсы по его геометрии/состояниям в рамках приложения; не менять Nordic default размеры ради устранения предупреждения. Здесь UI не переименовывался и файлы изображения не копировались.

## Важные зависимости цвета и условные ветки

- panel-header-background-color, toolbar-background-color, panel-border-color производны от base-color/component base variables. Для Nordic назначать конкретные color hooks, сохраняя parent sizing.
- tab-base-color имеет state/gradient/border производные. Местный tab-base-color разрешён только по карте; глобальный base-color запрещён. Явные tab state colors приложения navigation продолжат действовать.
- grid-row-cell-border-color в Classic задаётся списком цветов (#ededed и adjust-color(...)); переопределение одним Nordic цветом делает стороны одинаковыми, не изменяя widths. Это намеренное визуальное изменение, проверить grid lines и states.
- form-field-focus-border-color транзитивно влияет на trigger focus/hover border через Classic Trigger.scss. Width 17px и border-width остаются parent.
- Tree glyph color hooks не окрасят image-backed arrows/folders при enable-font-icons=false. Slider palette hooks под slider-imageless=false не окрасят bitmap thumb/track. Это задача artwork, а не причина переключать renderer.
- LoadMask message colors внесены в allowlist; opacity/size/padding и loading-image наследуются. Progress front/back text colors и прочие state hooks пока наследуются, перечислены в карте.

## Результат и границы аудита

Проверены источники всех запланированных color variables, их declarations/use/dependencies, метрики, frames, gradients/inclusion flags, app cascade/Font Awesome и происхождение navigation warnings. Изменения темы, SDK, TestApp исходников и icon assets не выполнялись. Новую сборку для чистого анализа источников не запускали: использованы реальные testing outputs и log TASK-001. Ни lint, ни default theme-lab, ни геометрические тесты Nordic этим аудитом не объявляются выполненными.

Следующая задача: TASK-003 (asset inventory/state mapping); после TASK-002 также доступна TASK-005 (theme-lab). Дополнительных обязательных уточнений пользователя для выполнения этих задач нет.
