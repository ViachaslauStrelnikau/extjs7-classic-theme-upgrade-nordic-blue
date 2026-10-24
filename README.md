# Nordic Blue for Ext JS Classic

Тема Nordic Blue для **Ext JS Classic 7.7.0.31**, расширяющая установленную `theme-classic`. Изменяет палитру и согласованные bitmap-значки, сохраняя размеры, положение, шрифтовые метрики и поведение Classic. Пример [Ext JS 7.9 themes](https://examples.sencha.com/extjs/7.9.0/examples/classic/themes/) служит только визуальным референсом.

## Состояние

Выполнены **TASK-001–015**: аудит SDK/Cmd, theme package, палитра, согласованные значки v3, сравнения геометрии/поведения и начальный визуальный эталон. Реальные testing/development/production сборки лаборатории проходили; окончательная матрица сборок/интеграции и поставка остаются **TASK-016/017**. Это не заявление об окончательной готовности темы.

- [Инструкции Codex](AGENTS.md), [требования](docs/nordic-blue-requirements.md), [руководство агента](docs/nordic-blue-agent-guide.md).
- [Задачи и статусы](docs/plans/nordic-blue/README.md).
- [Пакет темы](TestApp/packages/local/theme-nordic-blue/), [общая Theme Lab](TestApp/theme-lab/README.md).
- [Геометрия и поведение](artifacts/nordic-blue/TASK-014/regression-report.md):204 coverage pairs,236 action/state pairs,0 metric deltas.
- [Визуальные проверки](artifacts/nordic-blue/TASK-015/visual-report.md):204 сценария DPR1/2,408 golden snapshots,648 runtime resources/694 frames;0 structural pixels вне точных контуров согласованных значков.
- [Визуальная политика и обновление golden](artifacts/nordic-blue/TASK-015/visual-policy.md). Начальный golden технический; не означает окончательную пользовательскую приёмку всей темы.

## Локальные зависимости

Рабочий путь этого проекта и исторических проверок: `D:\Projects\Extjs7ClassicThemeUpgradeNordicBlue\`. Скрипты и provenance сохраняют этот Windows-путь; для другой машины/папки потребуется явная настройка путей.

SDK, node_modules, compiled application outputs и кэши в Git не включены. Используйте свой доступный SDK **7.7.0.31**: полный SDK в `ext-7.7.0.31/`, framework workspace той же версии в `TestApp/ext/`. SDK не скачивается и не подменяется этим репозиторием. Восстановите npm-зависимости из корня:

```powershell
npm ci
```

Сборки используют локальный **Sencha Cmd7.7.0.36** из `node_modules/@sencha/cmd-windows`, Java8 и совместимый Node из Cmd; точное проверенное окружение описано в AGENTS.md. Для инструментов проверок нужен Node24 с Playwright/Edge и Python3.12 с Pillow/NumPy; имеющиеся Windows-пути bundled runtimes перечислены в инструкциях.

## Сборка и запуск

Из `TestApp/` (оригинальное приложение):

```powershell
..\node_modules\@sencha\cmd-windows\dist\sencha.exe app build testing
..\node_modules\@sencha\cmd-windows\dist\sencha.exe app watch
```

Из `TestApp/theme-lab/` (отдельная Nordic laboratory build):

```powershell
..\..\node_modules\@sencha\cmd-windows\dist\sencha.exe app build lab-nordic testing
```

Затем из `TestApp/` современным Node запустить `node theme-lab/serve.cjs`. Сервер напечатает выбранный localhost URL; SDK доступен через его read-only alias. Build/watch не заменяют acceptance gates.

## Проверки

Из корня, после реальной актуальной testing build и запуска Theme Lab:

```powershell
python tools/lint-nordic-blue.py --check-icon-candidates
python tools/nordic-blue-regression/run.py --output artifacts/nordic-blue/regression-new-run --url http://127.0.0.1:PORT/theme-lab/
python tools/nordic-blue-visual/run.py --output artifacts/nordic-blue/visual-new-run --url http://127.0.0.1:PORT/theme-lab/
```

Каждому запуску нужна новая папка. Golden/approval нельзя автоматически обновлять ради PASS. Новое artwork требует показа и явного одобрения пользователя; CSS размер значков и hit area должны сохраняться. Изменение browser/font/rendering требует калибровки и review, не повышения допуска.

## Доказательства в Git

Сохранены исходники, планы, approved masters/candidates, baseline captures, отчёты/контроли и golden-v1. `.gitattributes` сохраняет точные байты: approval/политики/снимки привязаны к SHA, автоматическая замена LF/CRLF нарушила бы проверки.

Исключены только локальные SDK/зависимости/outputs/caches, архивы evidence.zip и каталоги archived compiled CSS/resources. Архив TASK-009 содержит compiled SDK CSS и остаётся локальным. Исторические artifact manifests описывают полный локальный audit и поэтому могут перечислять исключённые файлы; они не являются inventory Git checkout. Для повторного запуска восстановите SDK/dependencies и сборку. Предыдущая история ChatGPT не переносилась буквально — архитектурный контекст сохранён в документах проекта.
