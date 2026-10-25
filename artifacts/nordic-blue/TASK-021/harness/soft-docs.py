from pathlib import Path
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');P=R/'TestApp/packages/local/theme-nordic-blue-soft'
doc='''# Nordic Soft: подключение и откат

Nordic Soft — отдельный дочерний пакет для Ext JS Classic7.7.0.31, созданный Cmd7.7.0.36. Цепочка: theme-nordic-blue-soft → theme-nordic-blue → theme-classic. Принятая исходная Nordic Blue сохраняется.

## Подключение

Скопировать оба исходных пакета из TestApp/packages/local/ в packages/local/ своего Cmd workspace. В app.json выбрать `"theme": "theme-nordic-blue-soft"`; xtype/ui, store/controller, шрифты и app Sass не переписывать. Собрать установленным локальным Cmd. Для отката вернуть `theme-nordic-blue` и пересобрать outputs. Для исходного Classic выбрать прежний `ext-theme-classic`. Не использовать старый compiled output после переключения theme.

В проекте:

```powershell
# Из TestApp/soft-lab (полный набор компонентов)
..\\..\\node_modules\\@sencha\\cmd-windows\\dist\\sencha.exe app build testing
# Из TestApp/theme-acceptance/soft (исходный TestApp, свои app styles)
..\\..\\..\\node_modules\\@sencha\\cmd-windows\\dist\\sencha.exe app build testing
```

Также development/production. Нужны Java8 и совместимый Node из Cmd (окружение в AGENTS.md). Outputs: TestApp/build/theme-soft/{mode} и TestApp/build/theme-acceptance/soft/{mode}. В validation descriptors local.properties включает упаковку development pages; SDK и оригинальный app.json не меняются. Просмотр: запустить `node TestApp/modern-preview/serve.cjs`, затем http://127.0.0.1:51754/soft-preview/index.html .

## Что меняется

- Скругления:3px на кнопках/полях/меню/списках и4px у окон. Это выбранное пользователем изменение оформления, не допуск на геометрию. Все остальные шрифтовые и box metrics проверяются строго.
- Одобренные папкиv2 и документы:24PNG/GIF resources,1x/2x, прежние16×16CSSpx. Остальные624runtime files наследуются без изменения. Полный merged manifest/config — config/nordic-soft-icons.json; решение пользователя иSHA — TASK-021/artwork-approval.json. Предыдущие approvals/кандидаты не заменены.
- Мягкие тени и добавленные эффекты подключаются через отдельный API ниже. Выбор одной CSS темы не добавляет глобальные JS overrides и не меняет timing событий приложения.

## Анимации — явное подключение

Включить `resources/soft-motion.js` из output приложения после SDK и вызвать API в Ext.onReady/app launch. Можно добавить исходный файл пакета в app.json js bundle перед своим initializer. Файл не включается автоматически в runtime JS темы.

```javascript
Ext.onReady(function () {
    NordicSoftMotion.enable();
    var dialog = Ext.create('Ext.window.Window', {
        title: 'Настройки', width: 320, height: 220,
        shadow: false, closeAction: 'hide'
    });
    var detach = NordicSoftMotion.attach(dialog, { elevation: true });
    // dialog.show() —150ms opacity; повторное show работает.
    // dialog.hide() / Escape — штатное мгновенное закрытие.
    // detach() снимает добавленные слушатели и оформление elevation.
});
```

Для меню/Combo picker — attach к созданному компоненту до первого show; пример подключения в TestApp/soft-preview/sample.js. Приложение само выбирает компоненты. `shadow:false` задаётся через публичный config при создании; elevation применяется только при этом явном выборе. У существующих компонентов с native shadow он сохраняется; закрытые SDK методы управления тенями не вызываются. `animateTarget` сохраняет приоритет штатной анимации окна, дополнительный fade пропускается.

`enable()` добавляет120ms transitions только для background-color/border-color/color. Контур keyboard focus не анимируется. `disable()` отменяет добавленные эффекты и убирает переходы; `enable(false)` эквивалентен. Системный prefers-reduced-motion отключает добавленное движение, в том числе отменяет уже начавшееся появление. SDK-native эффекты этим API глобально не переписываются. На hide/destroy анимация отменяется; destroy снимает listeners, повторный attach идемпотентен. При отсутствии Web Animations API дополнительный fade пропускается. Координаты, размеры, шрифты и hit areas не анимируются; нет Promise/delay перед native show/hide/focus.

## Проверки и границы

`python tools/lint-nordic-blue.py --check-icon-candidates` проверяет родителя; `python tools/lint-nordic-soft.py` — отдельно дочерние исходники/24resources и точные hashes. Разрешения базовой политики не расширены. Изменение Soft CSS/JS/artwork требует новой проверки, не обновления SHA для сокрытия дефекта.

Точные результаты интеграции и проверенные браузеры — artifacts/nordic-blue/TASK-021/integration-report.md. Старые TASK-014–017/golden относятся к исходной теме и остаются неизменными. Для Soft нельзя автоматически присвоить им прежний pixel PASS: скругления намеренно меняют контуры. Новая полная pixel-golden/калибровка — отдельный этап; исходные screenshots и ресурсные SHA здесь фиксируют техническое состояние.

7.9, другиеOS, произвольные custom ui и плавность inherited GIF анимаций не заявляются проверенными. SDK, зависимости и compiled outputs не входят в source handoff. Artwork создан для проекта, новая лицензия владельцем пока не назначена; исходные условия Sencha не изменены.
'''
(R/'docs/nordic-soft-installation.md').write_text(doc,encoding='utf-8')
(P/'README.md').write_text('''# Nordic Soft

Source child of theme-nordic-blue for Classic7.7.0.31. User-selected Soft corners and approved squarer warm folders/blue documents;1x/2x, unchanged CSS boxes. No Ext overrides. Optional resources/soft-motion.js uses public per-component listeners; no automatic runtime inclusion. Public shadow:false config is required to opt into the CSS elevation.

Installation, opt-in motion, rollback and limitations: docs/nordic-soft-installation.md in the repository/source handoff. Evidence: artifacts/nordic-blue/TASK-021/integration-report.md. Existing Nordic Blue and its goldens remain unchanged. Do not claim the parent's pixel baseline as Soft acceptance.
''',encoding='utf-8')
(R/'TestApp/soft-lab/README.md').write_text('''# Soft validation app

Separate consuming descriptor for the generated Soft package. Common fixture/clock/build-requires are byte copies of the accepted Theme Lab; original lab remains unchanged. The copied fixture disables native Ext effects for deterministic geometry checks; opt-in addon motion is tested separately on actual build pages. Profiles keep query theme=nordic for existing drivers but resolve to theme-nordic-blue-soft and distinct build/theme-soft outputs. Default source/reference is Classic. Native compiled pages and full-scenario captures are complementary evidence.
''',encoding='utf-8')
(R/'TestApp/soft-preview/README.md').write_text('''# Built Nordic Soft preview

Open /soft-preview/index.html on the preview server51754. Loads real Soft compiled testing CSS and copied SDK debug runtime, plus the actual built optional soft-motion.js resource. Demonstrates attach/show/hide and public shadow:false configuration. Candidate artwork CSS is not used: tree images come from compiled Soft output. Actual compiled microloader/JS pages are tested independently in TASK-021. No original app/view code is modified.
''',encoding='utf-8')
print('Prepared installation, rollback, opt-in motion and scope documentation')
