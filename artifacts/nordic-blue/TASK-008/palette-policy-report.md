# TASK-008 — палитра и проверенный allowlist: DONE

Дата: 2026-10-23. SDK 7.7.0.31 / Cmd 7.7.0.36 / Java 8. Эта задача создаёт цветовую основу, не завершает тему.

## Реализация

- В `TestApp/packages/local/theme-nordic-blue/sass/var/all.scss` заданы все **15 canonical Nordic tokens** из palette.md через `dynamic()`. Короткие aliases таблицы PDF (`nb-header` и подобные) не вводились. Значения из PDF не объявляются результатом точного замера screenshot.
- **52 color-only SDK variables** распределены по 13 реальным Ext namespace files: 50 проверенных в TASK-002 плюс `$button-default-border-color-over = $nb-accent-hover` и `$form-field-empty-color = $nb-muted`. Эти два существующих SDK hook используют последние два токена; не добавлены пустые/imageless/glyph hooks.
- Явные компонентные исключения PDF сохранены: Grid header `#EAF0F8`, Window border `#AFC2D9`, Grid header trigger `transparent`. Они не размножают базовые 15 tokens.
- `package.json` сохранён в штатной Cmd структуре. Единственное необходимое изменение конфигурации: добавить `${package.dir}/sass/var/all.scss` первым в `sencha.sass.var`, перед каталогом. В реальном Cmd 7.7 автоподключение package all.scss не сработало; первый build завершился `Reference to undeclared variable: $nb_surface`. Исправлен explicit import для app и slicer; отклонённый build сохранён в `build-missing-token-import.log`.
- Общий `$base-color`, fonts, sizes, padding, radius, positions, image/glyph flags, UI mixins, JS overrides и новые icons не вводились. Classic gradients пока наследуются. `overrides/` и source `resources/images/` пусты.

## Политика и команда

- `config/nordic-blue-policy.json`: точный allowlist имён/значений/файлов, 300 хешей SDK Sass, ссылки на declarations/consumers, защищённый generated package config. Все остальные overrides отклоняются.
- `config/nordic-blue-icons.json`: привязка к одобренному v2 manifest/approval по SHA-256, **648** уникальных runtime path contracts для 1x/2x PNG/GIF, exact bytes/dimensions, CSS sheet size и sprite contracts. 2x не удваивает размер в CSS. Все 182 vector masters также сверяются с одобренными hashes.
- `tools/lint-nordic-blue.py`: read-only, только Python standard library, не запускает сборку и не меняет файлы. SCSS допускает лишь конкретные `dynamic(color/token)` assignments. Произвольный CSS/import/function/mixin, metric/image/position variable, неизвестные имена и runtime JS/font файлы запрещены.
- Image resources распознаются по manifest, но `integrationEnabled=false`: рабочее подключение резервируется до TASK-013 и остальных её зависимостей. Смена bitmap/CSS размеров, density или sprite contract выявляется. Geometry adapters сейчас не разрешены; их точное CSS и данные потребуется проверить на TASK-013, широкого исключения для background-size/position нет.

Из корня проекта:

```powershell
& 'C:\Users\Damned\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' tools/lint-nordic-blue.py --check-icon-candidates
```

Можно использовать `python tools/lint-nordic-blue.py --check-icon-candidates`, если Python доступен на PATH. Флаг `--report <path>` сохраняет JSON отчёт. Проверенный результат: **PASS, exit 0**, 15 tokens, 52 overrides, 300 SDK files, 648 candidate contracts. Никакие новые test suites приложения не добавлялись; контрольные изменения ниже — обязательная проверка policy этой карточки.

## Доказательство использования переменных

Из реального Cmd-generated stylesheet создан отдельный `compiler-probe/consumption-probe.scss`: перед RULE section каждому из 52 hooks назначен уникальный временный цвет. **Все 52** цвета найдены в настоящих compiled CSS declarations с примерами selectors/properties (`compiler-consumption.json`). Marker CSS не добавлялся; theme sources и рабочий compiled CSS sentinel values не получали. Отдельный Fashion probe использует тот же встроенный Node/Fashion, exit 0; imports относительные на диске D (Windows absolute import из внешней копии Fashion интерпретировал неправильно, этот служебный probe исправлен до принятия доказательства).

**33 policy controls: PASS.** Положительные проверки принимают разрешённый color hook и одобренные 1x/2x contracts. Отрицательные выявляют padding/font/radius, global base-color, image/gradient/position change, неизвестную переменную, token alias, неверный namespace/value, новый UI/JS/font, непросмотренный image, изменение bitmap/CSS size, sprite contract, early icon integration, duplicate/missing assignments и изменение package config. Все изменения сделаны в памяти или disposable копии малого child package, не в SDK/приложении. Полный список: `policy-controls.json`.

## Реальная сборка и геометрия

Рабочая папка `TestApp/theme-lab`:

```powershell
..\..\node_modules\@sencha\cmd-windows\dist\sencha.exe app build lab-nordic testing
```

Окончательный build: **exit 0**, без `[WRN]`/`[ERR]`; output `TestApp/build/theme-lab/nordic/testing/app.json`, CSS `resources/NordicThemeLab-all.css` (SHA-256 `1cf5fe1dbd1a134947e7921bbc9677d1972631b6f3d2698614c115d15fb543bd`). Полный build log сохранён. Java 8 + bundled Node в PATH как TASK-007. Вызов при выполнении использовал эквивалентный `-cwd=.../TestApp/theme-lab` из staging workspace.

Один неизменённый fixture, Edge 155.0.4283.62, Windows, 1280×1600, en-US, Europe/Minsk, фиксированная дата, software raster/sRGB и GIF frame0 policy принятого TASK-006. При DPR1 и DPR2 снято **102 сценария × 2 = 204 raw PNG/JSON pairs**. Сравнены **11 280 elements и 1 926 icon observations**: геометрия/типографика/box model/offsets/focus/data/scroll/opacity совпадают точно, без 1px tolerance; нет пустых выборок, duplicates, runtime errors или 404. В color comparison исключены только перечисленные paint properties и цветовые части gradient/shadow; их структура и все остальные параметры сравниваются. **Pixel equality с Classic не заявляется**: палитра изменилась. Визуальная приёмка состояний/gradients и полный release gate остаются следующим задачам.

Все **180** родительских icon resources, намеченных к будущей замене, пока побайтово совпадают с Classic (`inherited-icons.json`); два adapter resources ещё не подключены. Одобренные masters/candidates не редактировались. Контроль 1474 baseline source inputs показал лишь ранее документированные изменения инструкций TASK-007; оригинальные TestApp app.json/code и обе SDK не менялись (`source-guards.json`).

## Продолжение

TASK-008 DONE. Следующая задача по порядку — **TASK-009**, Panel/Window/Toolbar/Button: полная палитра состояний, отдельное решение по gradients, визуальные/геометрические доказательства. 010–012 также получили выполненную зависимость 008. Новые значки остаются до TASK-013. Готовность всей темы не заявляется.
