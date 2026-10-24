# Theme Lab — Ext JS Classic 7.7.0.31

Один fixture внутри существующего TestApp для Classic и Nordic Blue. Используется установленный SDK и его полный prebuilt Classic CSS. Production view/Application/app.js, app.json, SDK и утверждённый набор значков не меняются.

## Открыть

Из TestApp запустить отдельный read-only static server стенда (не меняет существующий app watch):

```powershell
..\node_modules\@sencha\cmd-windows\dist\bin\windows\node\node.exe theme-lab\serve.cjs
```

Открыть напечатанный адрес `/theme-lab/index.html?theme=classic&case=all&state=normal`. Сервер слушает только 127.0.0.1 и выбирает свободный порт. `sdk/` — read-only alias к существующему ext-7.7.0.31, физической копии SDK нет. Обычный app watch не содержит этого alias: не открывать данный standalone fixture через него.

Пользовательские команды основной TestApp сохранены без изменений:

```powershell
..\node_modules\@sencha\cmd-windows\dist\sencha.exe app build testing
..\node_modules\@sencha\cmd-windows\dist\sencha.exe app watch
```

## Сценарии и состояния

Верхняя панель выбирает theme/case/state и перезагружает страницу: каждый сценарий начинает с чистых компонентов и тех же данных. `case=all` показывает обзор всех 20 строк, состояние normal. Для воспроизводимого capture выбирать конкретную case/state из `themeLab.cases`.

- normal/disabled/collapsed/selected/open/sorted/readonly/invalid — реальные configs и API Ext, общие для обеих тем.
- hover/pressed — **настоящий указатель**, без подстановки CSS-классов. `themeLab.pendingActions` возвращает стабильный CSS selector. Для hover навести курсор; для pressed навести и удерживать кнопку мыши. После события состояние готовности завершается. При ручном просмотре до действия нет искусственного тайм-аута.
- focus — реальный `component.focus()`. Проверки Tab/Space/Arrow/Home/End выполнять через браузер, а не генерировать поддельные keyboard events.
- Кнопки, меню, split buttons, collapse tools, column menus, paging, tree, date picker, sliders и editor остаются интерактивными. Captures перечисленных состояний не являются полной функциональной приёмкой.

## Стабильные имена и readiness

`window.themeLab` содержит `components` (Map), `component(id)`, `selector(id, part)`, `snapshot()`, `environment()`, `navigate(case,state)`, `whenReady()` и `actions`.

Идентификаторы: `panel.main`, `form.text`, `grid.main/row/person-03`, `grid.main/cell/person-03/name`, `tree.main/row/leaf-1`, `paging.toolbar/next`, `editor.main/content`. В DOM — `data-lab-id`. Сгенерированные Ext IDs не используются для сопоставления. Числовые суффиксы вкладок/действий являются явными именами fixture, а не индексами текущего DOM. Ext itemId кодирует точки как `--`, semantic ID сохраняет точки.

`await themeLab.whenReady()` ждёт:

1. Ext-ready, построения компонентов и синхронных фиксированных stores.
2. Инициализации HtmlEditor и загрузки fonts основного/iframe document.
3. Отсутствия активного/suspended layout и незавершённого mouse action.
4. Трёх последовательных кадров с одинаковыми semantic rects/computed metrics.

Пустая выборка и ошибка компонента не считаются READY. Deadline 20 секунд — предел ошибки, не фиксированная пауза для снимка. После действий/изменений вызывать `whenReady()` заново. `snapshot()` сохраняет координаты iframe body в отдельном `coordinateSpace=editor-iframe`.

## Данные и окружение

- 32 локальные записи с явными person-01…person-32, 4 страницы по 8; MemoryProxy enablePaging, без сети/случайных данных.
- Tree node IDs фиксированы: folder-alpha/folder-beta/leaf-1…leaf-3.
- Дата `new Date()` фиксирована на 2026-10-23 09:00 Europe/Minsk. Date.now() — монотонный отсчёт от того же epoch, необходимый TaskRunner/HtmlEditor. Это изменение только isolated lab page до загрузки SDK, без Ext overrides. Performance/timers продолжают работать.
- Целевой UI locale en-US (английский SDK, явные date/time formats), browser capture context locale en-US и timezone Europe/Minsk.
- Viewport 1280×1600, zoom 100%, основной DPR1; отдельно DPR2. `environment()` записывает фактические viewport/DPR/timezone/browserLocale/fonts. Ручное окно другого размера не является эталоном.
- Шрифты компонентов наследуются из compiled Classic CSS; scaffold CSS ограничен lab wrappers. Нет геометрических/font overrides `.x-*`. Fx отключены только в fixture; CSS animation/transition/caret нейтрализованы для capture. Анимированные loading GIF требуют выбора/нормализации кадра в TASK-006/015: их bitmap animation не объявляется замороженной.

## Theme selection и будущие builds

`profiles.json` проверяет toolkit, theme alias, включённый пакет и SDK. Classic использует явно обозначенный installed-sdk-prebuilt-reference manifest: loader сверяет настоящие version.properties и classic/theme-classic/package.json, затем runtime version. Будущий Nordic использует реальный generated app.json и его compiled CSS entries. Одна fixture.js используется для обоих профилей. Нет смешивания CSS двух тем и нет fallback Nordic → Classic.

Classic сейчас читает `classic-reference.json` и полный SDK theme-classic-all-debug.css. Изначальная сборка TestApp pruning исключает неиспользуемые в Main классы (например Slider): она не подходит как полный stylesheet стенда. Она не подменяется утверждением о проверке новых theme builds. Nordic ожидает `../build/theme-lab/nordic/testing/app.json`, пакет theme-nordic-blue. До TASK-007 его отсутствие — явная ошибка `Profile/build unavailable`; это не READY и не доказательство поддержки Nordic.

`build-profiles.json` — подготовленные Sencha app.json fragments lab-classic/lab-nordic с отдельными output directories. Они **не активированы** в production TestApp/app.json, чтобы обычная пользовательская build testing не пыталась собрать пока отсутствующий Nordic package. В TASK-007 включить theme-lab/build-requires.js в JS inputs lab profiles, чтобы Cmd сохранил CSS всех fixture classes. Затем после генерации темы активировать профили, проверить фактические Cmd output paths и связать profiles.json с полученными manifests. Один fixture не менять при переключении темы.

## State drivers / ручные действия

| Case | Semantic target / driver | Действие |
|---|---|---|
| Panel | panel.main; actions.panelToggle() | Collapse/expand, gear tool |
| Window | window.main; windowMove/Resize/Close | Title drag, border resize, Escape/close |
| Button | button.normal; button.menu; button.split | Hover, hold mouse, Tab/Space, menu |
| Toolbar | toolbar.main | Overflow menu, separators, action buttons |
| Form | form.text/inputEl; form.combo; form.date; form.time; form.number; form.notes | Input, validation, readonly |
| Triggers | triggers.combo/picker; triggers.date; triggers.spinner | Dropdown/calendar/spin, hover/press/focus |
| Checkbox/Radio | checks.unchecked/inputEl; checks.radio-a/inputEl | Tab/Space/arrow keys, checked/unchecked/disabled |
| Fieldset | fieldset.collapsible; fieldset.checkbox | Collapse and checkbox-toggle |
| HTML editor | editor.main; editor.main/content; refreshEditor() | Toolbar/iframe text; preserve content on layout refresh |
| Grid | grid.main/view; actions.gridSelect/Sort() | Selection, header menu/sort, column edge drag, arrow keys |
| Paging | paging.toolbar/first, prev, next, last, refresh; actions.page(1…4) | Boundary buttons and refresh |
| BorderLayout | border.north/south/west/east/center | Region collapse/expand and splitter drag |
| Tabs | tabs.tab-0…tabs.tab-7 | Active/disabled/close/overflow, keyboard |
| Tree | tree.main/view; actions.treeToggle() | Node expand/collapse/select, keyboard |
| DatePicker | datepicker.main; actions.dateMonth(-1/1) | Today/selected/prev/next, keyboard |
| Progress | progress.main | 42% / 100% |
| Slider | slider.horizontal; slider.vertical; actions.sliderValue(0…100) | Horizontal/vertical thumbs, keyboard/mouse |
| Menu | menu.parent, checked, unchecked; actions.menuToggle() | Submenu/check/radio/separator, keyboard/focus |
| Tool | tool.close…tool.collapse-bottom | Full audited tool family; normal/hover/focus/pressed/disabled |
| Mask | mask.main | LoadMask visible/hidden and original loading GIF |

Release geometry/keyboard/visual suites and Nordic snapshots are later TASK-006/014/015. TASK-005 supplies the fixture and accessible state drivers.
