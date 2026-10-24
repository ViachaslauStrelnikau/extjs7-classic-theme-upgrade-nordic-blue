# Матрица покрытия и приёмки

Источник: PDF, стр. 18 и 28–29; расширено новым icon set пользователя.

Для каждой строки сохранить: stable IDs, доступные состояния, Classic/Nordic rects, computed styles, screenshot paths, результаты действий и icon IDs. Изначально все проверки NOT_RUN. Символы/стили дополнительно сверять с icon-manifest и variable-map.

| Fixture | Состояния и действия |
|---|---|
| Panel | normal, framed, collapsed, collapsible; toggle tools |
| Window | normal, focused, modal, resizable; move/resize/close |
| Button | normal, hover, focus, pressed, disabled, menu, split |
| Toolbar | normal, overflow, separators, paging |
| Form | Text, Combo, Date, Time, Number, TextArea; valid/invalid/readonly |
| Triggers | normal, hover, focus, disabled; dropdown/calendar/spinner |
| Checkbox/Radio | checked/unchecked/disabled, keyboard toggle |
| Fieldset | normal, collapsed, checkbox fieldset |
| HTML editor | toolbar icons, iframe content, theme refresh |
| Grid | header/menu/sort, resize columns, striped/hover/selected rows, keyboard |
| Paging | first/prev/next/last/refresh, disabled boundaries |
| BorderLayout | north/south/east/west/center, collapsed regions, splitters |
| Tabs | active/hover/disabled/closable/overflow, keyboard |
| Tree | folder/node/expand/collapse/selection, keyboard |
| DatePicker | today/selected/prev/next month, keyboard |
| Progress | partial/full |
| Slider | horizontal/vertical, thumb positions, keyboard/mouse |
| Menu | normal/submenu/checkitem/separator, keyboard/focus |
| Tool | collapse/expand/close/settings and all available fixture tools |
| Mask | LoadMask/loading text and loading asset |

## Общие выпускные критерии

- Theme manifest: theme/classic/extend theme-classic; существующие xtype/ui и production JavaScript не меняются, новых JS overrides нет.
- Координаты/размеры внутренних и внешних элементов совпадают. Порог ≤1 px в PDF не является автоматическим разрешением отклонения.
- Все computed font-family/size/weight/line-height/letter-spacing/text-transform, padding/margin/border-width/box-sizing/min/max совпадают с Classic.
- Новых overflow/clipping/ellipsis regressions нет; старое поведение Classic зафиксировано, не исправлено изменением размеров.
- Новые стандартные icons созданы, интегрированы и проверены во всех состояниях; box sizes, sprite offsets, hit targets и behavior сохранены. Наследуемые assets перечислены явно.
- Geometry/functional suite и Nordic golden PASS; normalized structure diff объяснён с учётом допустимого нового artwork. Нет широких масок, скрывающих регрессии.
- Development/testing/production 7.7 builds PASS, resource URLs корректны, нет console errors и 404. Standalone build — по формату поставки.
- Browser/OS/version/fonts/viewport/DPR зафиксированы. Для каждого браузера и build mode фактический PASS/FAIL/NOT_RUN; NOT_RUN не приравнивается к PASS.
- 7.9 проверяется отдельно только после расширения матрицы; её отсутствие не подменять заявлением о совместимости.

## Дополнительные критерии значков

- HiDPI поддержка по возможности: качественные masters, 1x fallback, подтверждённый 2x pipeline. При невозможности — конкретное обоснование.
- При каждом DPR=1/2 одинаковые Classic/Nordic CSS rects, физический размер в интерфейсе, hit areas и logical offsets; число пикселей bitmap может быть больше. Все state cells корректны, нет blur/clipping.
- Есть явное одобрение пользователя полного набора: превью всех состояний/натурального размера/1x–2x и записанная одобренная версия/hash. До него нет интеграции TASK-013 и утверждённых Nordic icon golden.
