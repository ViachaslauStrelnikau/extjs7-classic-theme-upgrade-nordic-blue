# TASK-031: пользовательские значки дерева

2026-10-25. DONE как исправление priority/custom icons и поставка1.1.1; полная Classic acceptance не подразумевается.

## Причина

Наследуемые Nordic Blue правила .x-tree-icon-leaf/parent/parent-expanded задавали background-image/background-size с !important (LTR/RTL,1x/2x). Штатный Ext7.7 Tree.Column добавляет эти стандартные классы даже при пользовательских icon/iconCls. Поэтому !important перекрывал и inline URL, и CSS-класс приложения. Renderer metadata icon/iconCls также сохраняет стандартные классы и не всегда добавляет custom marker. Причина в исходном parent Sass, не в данных пользователя.

## Исправление

Из12только стандартных tree image rules убран !important; селекторы и изображения не переименованы. В конце восстановлен штатный SDK reset .x-tree-icon-custom и его RTL-вариант: background-image:none, background-size:auto. Приложение может переопределять их обычным CSS после темы, как в Classic. URL inline имеет нативный приоритет. Стандартные 1x/2x картинки/16px CSS scaling и остальные control/loading rules сохранены. Background-size пользовательских изображений не фиксируется !important. Glyph renderer/Ext classes/метрики не переопределены. Все648image bytes неизменны.

Точные before/after12строк, нормализованные hashes и SDK evidence — selector-review.json; исходный Sass сохранён Component-before.scss. Родительская policy обновлена только на точные новые source/metadata SHA, связь с review записана; не добавлялось широкого разрешения CSS/геометрии. Theme parent patch1.0.1, отдельная тема1.1.1, Soft1.0.0. Parent package.json изменён только literal version, остальные bytes сохранены (package-version-review.json). Обновлять нужно все3пакета.

## Фактический просмотр и сборка

В compiled preview отображены icon URL, iconCls CSS, renderer URL, renderer CSS и пользовательская папка. Рядом стандартные папка/лист со штатными approved assets. Записаны actual computed backgrounds/sizes/16×20 CSS boxes (высота коробки штатная для fixture); screenshot custom-icons.png. Папка реально свёрнута/раскрыта, custom CSS icon сохраняется (folder-collapse.json). Demo SVG — только условные рисунки приложения, не новые системные иконки темы и не production artwork.

6окончательных release-build-* Cmd invocations exit0 (lab+real×testing/development/production), Cmd7.7.0.36/SDK7.7.0.31/Java8/bundledNode6. Source hashes неизменны на всём финальном run (release-build-inputs.json). Во всех6manifest parent1.0.1/child1.1.1 и648approvedimageSHA. Три source lint PASS. Предварительные build-/final-build- записи — диагностика уточнения фикса; final-build input guard отверг run, во время которого правился исходник. Это не финальная приёмка; использовать только release-build-* с успешной проверкой неизменности.

Это узкий фактический просмотр LTR в браузере приложения. Полная новая DPR/browser/RTL/custom-renderer matrix и Classic geometry/function/pixel regression не запускались, автоматические тесты не добавлялись. RTL specificity reset отражает installed Classic SDK; все renderer CSS ordering/specificity должны соблюдать нативный cascade. Старые goldens и иконки не обновлялись.

## Поставка

docs/nordic-soft-light-installation.md содержит обязательное обновление parent. Новый source-only архив включает theme-nordic-blue1.0.1, theme-nordic-blue-soft1.0.0 и theme-nordic-blue-soft-contrast1.1.1. После замены пересобрать приложение. SDK/compiled output/node_modules не включены. Custom demo http://127.0.0.1:51754/contrast-preview/custom-icons.html?variant=soft&motion=off . Основной preview тоже содержит эти примеры. ZIPs local/gitignored, receipts/source versioned. Отдельный commit/push по поручению пользователя.
