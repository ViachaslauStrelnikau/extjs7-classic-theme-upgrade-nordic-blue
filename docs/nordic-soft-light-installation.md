# Nordic Soft 1.1 — светлая многоуровневая шапка

Отдельный пакет: `theme-nordic-blue-soft-contrast`, версия1.1.1. Имя сохранено от первоначального контрастного варианта; по одобренному отзыву пользователя заголовки теперь светлые. Наследование: theme-nordic-blue-soft-contrast → theme-nordic-blue-soft → theme-nordic-blue → theme-classic. SDK7.7.0.31, Cmd7.7.0.36. SDK7.9 не проверена.

## Установка

Скопировать все3пакета из TestApp/packages/local архива в packages/local вашего workspace: theme-nordic-blue, theme-nordic-blue-soft, theme-nordic-blue-soft-contrast. Установленная Classic SDK нужна отдельно; SDK и лицензия Sencha не входят в поставку.

В app.json приложения выбрать:

```json
"theme": "theme-nordic-blue-soft-contrast"
```

Собрать приложение штатным Sencha Cmd. В данном репозитории из TestApp:

```powershell
..\node_modules\@sencha\cmd-windows\dist\sencha.exe app build testing
..\node_modules\@sencha\cmd-windows\dist\sencha.exe app watch
```

Оригинальный TestApp/app.json не переключался автоматически. Отдельные consuming descriptors: TestApp/contrast-lab и TestApp/theme-acceptance/contrast. Из contrast-lab местный Cmd находится по пути `..\..\node_modules\@sencha\cmd-windows\dist\sencha.exe`; доступны testing/development/production. Выходы build/theme-contrast и build/theme-acceptance/contrast.

## Оформление

Группы колонок #e8eef6; названия #f4f6f9, текст #304a68. Синие оттенки для наведения/фокуса/сортировки. Без вертикальной линии в названиях колонок; синий акцент заголовка панели сохраняется. Стили v2 для полей/кнопок/вкладок, одобренные папки и прочие648ресурсов наследуются. Новых значков/Ext overrides нет. Собственные правила не меняют геометрию или шрифты; полная совместимость не выводится из одного успешного build.

Необязательная основная кнопка: `cls: 'nb-primary'` — назначается явно приложением; не добавляет новые размеры UI. Без этого обычные кнопки остаются обычными. Это opt-in, существующие приложения не требуют изменения конфигураций компонентов.

Optional motion API наследуется от Soft; автоматически не включается. Подключение и ограничения — docs/nordic-soft-installation.md. Данная ревизия не заявляет повторную полную приёмку motion.

## Просмотр и откат

http://127.0.0.1:51754/contrast-preview/index.html — существующий read-only server из TestApp/modern-preview/serve.cjs. Загружается compiled CSS новой темы, без reference.css и без JS-патчей фреймворка. Пример содержит отдельную таблицу с многоуровневыми заголовками. Исходный design-preview сохранён как история выбора.

Откат: вернуть app.json theme на theme-nordic-blue-soft либо ext-theme-classic и пересобрать приложение. Старые пакеты сохранены.

Фактические build logs и наблюдения: artifacts/nordic-blue/TASK-030. Проверенные режимы и ограничения указаны в отчёте этой задачи. Старые Classic/Nordic goldens неизменны и не являются визуальной приёмкой этой ревизии. Произвольные custom UI/полная RTL/другие ОС/версии SDK отдельно не подтверждены.

## Исправление пользовательских иконок1.1.1 (TASK-031)

Обновить все3пакета из нового архива, особенно **theme-nordic-blue1.0.1**: причина была в наследуемых tree image rules с !important. Замена только theme-nordic-blue-soft-contrast недостаточна. После замены пересобрать приложение. Soft остаётся1.0.0, отдельная тема —1.1.1.

Стандартные папки/листья сохраняют approved1x/2x и16pxCSSsize. У пользовательского `icon` URL имеет штатный inline приоритет; `iconCls` определяет рисунок своим CSS. Подключать CSS приложения после темы, как в Classic. Приложение задаёт background-size пользовательского artwork, если оно использует2x или sprites; тема больше не навязывает ему свои !important. Нативный glyph renderer не меняется. Исправление не добавляет JS overrides. Примеры URL/iconCls/renderer и custom folder находятся в contrast-preview.
