# TASK-003: каталог стандартных значков Classic

Статус: DONE. SDK 7.7.0.31 / Classic, дата 2026-10-23.

## Результат

Составлен icon-manifest.json: 555 image assets, 275 parent resources, 183 решений replace и 372 inherit. Каталог охватывает всю цепочку parent resources и prebuilt image output; build-generated frame chrome отделён от иконок. Изолированный fixture содержит 67 semantic component IDs и 415 образцов состояний; получено 1020 background observations, из них 57 разных raster paths. Все эти пути существуют; ошибок создания компонентов, JavaScript и HTTP >=400 нет.

Это инвентаризация Classic, а не созданный Nordic icon set и не выпускной geometry/functional baseline. TASK-004 остаётся TODO. Полный theme-lab создаётся в TASK-005.

## Артефакты

- icon-manifest.json: источник/владелец, hash, реальные bitmap размеры/формат/прозрачность, анимация, source references, CSS rules, component/state mapping, computed display element boxes и offsets, решения replace/inherit и причины.
- sprite-contracts.json: основные размеры и формулы состояний; runtime.json содержит полные вычисленные CSS значения каждого образца.
- contact-sheets/: реальные компоненты tools, fields, checkbox/radio, buttons/paging, grid/tree, tabs/toolbars, datepicker/slider/menu, HtmlEditor, mask/status/layout во всех показанных состояниях.
- parent-atlas/: все parent image assets; каждый composited frame анимированных GIF включён отдельно. Размеры подписаны, крупные sheets показаны как thumbnails; это не предложение менять их pixel grid.
- fixture.html и capture.cjs: отдельная диагностическая страница и средство захвата. Browser 155.0.4283.62, viewport 1320×1600, DPR=1, en-US / Europe/Minsk. Сетевые запросы перехвачены и обслужены из файлов проекта: пользовательская вкладка и TestApp не изменялись.
- familySourceEvidence в manifest: строки Sass с image hooks, glyph branches, размерами, offset/state/opacity правилами. sourceEvidence различает literal paths и default UI interpolation; compiledCssRules позволяют сверить generated selectors.
- input-hashes.json и validation.json: проверяемые входные файлы и итоги.

## Основные геометрические контракты

| Группа | Подтверждённый контракт |
|---|---|
| Tools | 15×15 CSS px; sheet 30×360, normal x=0 / hover x=-15; direction aliases разделяют строки |
| Form triggers | 17×22 CSS px; x=0/-17/-34/-51/-68 для normal/hover/pressed/focus/hover-focus; pressed приоритетнее focus |
| Spinner | 17×11 для каждой половины, y=0/-11; те же горизонтальные state offsets |
| Checkbox/Radio | 13×13; checked y=-13, keyboard-focus x=-13; disabled — прозрачность контейнера, не отдельный обязательный bitmap |
| Slider horizontal | 14×15; шесть диагональных cells: (0,0), (-14,-15), ..., (-70,-75) |
| Slider vertical | 15×14; измеренные диагональные state offsets в manifest |
| HtmlEditor | 14 glyph cells 16×16 в tb-sprite.gif шириной 224; измерены все 14, включая link/source |
| Grid header menu | bitmap hd-pop 10×9 внутри decorated element 14×22, с позиционированием по центру Y |
| Tree | elbow width 16, arrow x=0/-16/-32/-48; folder/open/leaf отдельные ресурсы; сохранять indent и высоту строки |
| DatePicker month | Реальный parent hook указывает button/s-arrow-light, а не neutral datepicker/month-arrow |
| Tab close | 11×11; normal opacity .6, disabled .3; не создавать разные glyphs, если состояние реализовано opacity |

В manifest cssElementBox — прямоугольник элемента, на котором нарисован background, а не автоматически чистый glyph box: например, button arrow украшает элемент с текстом, loader — элемент с текстом и padding. Координаты rect относятся к диагностической странице и не задают положение в приложении. Sprite offsets/background positioning измерены непосредственно браузером.

## Решения для нового набора

replace означает «создать кандидат в TASK-004 и показать пользователю», а не уже заменить файл. Current standard image symbols, checkbox/radio, loading/status и slider thumb/track artwork включены в replace при наличии current source/CSS использования. Наследовать frame/sizing surfaces, shadows, resizer/layout chrome и неподтверждённые legacy resources; каждый такой asset имеет причину. Если позднее fixture задействует legacy asset, пересмотреть его перед заменой, не копировать весь parent images каталог.

Инвентаризовано 7 анимированных assets; frame durations/loop записаны. Новый loader должен сохранить animated behavior и display box, а не стать неподвижным значком по ошибке.

Присутствуют RTL counterparts; файлы обеих SDK-копий сравнены по bytes. Runtime матрица здесь LTR, DPR=1; поддержка RTL/HiDPI не заявляется проверенной. Для 2x сохранить CSS/display размер и logical offsets, повысив только число bitmap pixels; новые 2x sources и отдельный DPR=2 прогон появятся в TASK-004/013.

## Найденные особенности исходного Classic

1. tool-resize и tool-move имеют y=-360/-375 при sheet height=360. Background repeat повторяет первые строки: в контактном листе они выглядят как close/minimize. Это исходный контракт и обнаруженный artwork gap, не ошибка нового Nordic. В TASK-004 предложить явные новые glyphs без изменения 15×15 box; отдельно описать совместимую resource mapping стратегию, не увеличивать component size и не менять существующие offsets молча.
2. Radio bitmap width=51 при CSS cell=13. Не делить sheet на предположительно равные столбцы по ширине файла: сохранять исходные координаты и незадействованные пиксели.
3. Slider states расположены диагонально, не горизонтально. Перепаковка их в ряд сломает focus/drag.
4. navigation-relative resources из TestApp не являются default Classic assets; проблема задокументирована в TASK-002. Текущий fixture использует default UI и prebuilt CSS поставленного SDK; повторной сборки приложения здесь не было.
5. Font Awesome icons приложения th-list/home/user/users/cog выделены отдельно: 5 semantic IDs, ссылки на uses, unicode declarations и application font metrics 24px. Их нельзя выдавать за Classic sprites. Native select indicator в font selector HtmlEditor тоже не является файлом images и оставлен inherit-native.

## Как получены состояния

Компоненты созданы настоящими Ext classes; checked/expanded/sorted/selected/disabled заданы через configs/API. Hover/focus/pressed и их сочетания представлены CSS state classes по исходникам SDK. Это позволяет измерить artwork/state mappings, но не доказывает корректность событий мыши/клавиатуры или product hit targets. Такой функциональный acceptance остаётся задачей 014. В частности, отдельно от panel layout созданный Tool может иметь широкий root element; сохраняемый 15×15 контракт относится к tool-tool-el, не ко всей карточке.

## Проверки завершения

Все 415 state rows имеют semantic ID и хотя бы одно наблюдение, дубликатов (semantic ID,state) нет. Все raster URLs разрешены в существующие файлы; core trigger/slider offsets сверены с вычисленным CSS; все 14 editor glyphs присутствуют. Error arrays пусты. Копии parent images совпадают, входные hashes сохранены. Ни SDK, ни исходники TestApp, ни theme resources не редактировались. Следующая задача: TASK-004 — новый icon set, затем обязательное одобрение пользователя перед интеграцией.
