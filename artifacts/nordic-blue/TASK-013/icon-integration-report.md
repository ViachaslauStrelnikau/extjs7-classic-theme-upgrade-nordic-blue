# TASK-013 — Интеграция approved Nordic icons v2: DONE

Завершено 2026-10-24. SDK 7.7.0.31 / Cmd 7.7.0.36 / Java 1.8.0_501; Edge 155.0.4283.62, viewport1280×1600, zoom100%, DPR1/2, CPU raster/sRGB. Готовность всей темы не объявляется: TASK-014–017 впереди.

## Одобрение и изменения

Интегрирован именно nordic-icons-v2, одобренный пользователем 2026-10-23 («Отлично одобряю»). Approved manifest SHA a7ac4cc21bdac41de0dffc6e5fc1dee3adf72eb01edfe6f0ca4de4bbb8433a20, approval SHA50cba91d56499fc59cc29cf86e5e80b91a04f6e1b3c0ec64be1cc855272cca1c. Сам approval, masters и candidates не редактировались. Поле integrationStatus внутри исторической записи TASK-004 описывает момент одобрения; фактическая интеграция зафиксирована здесь и в новом integration-manifest.json.

- В theme-nordic-blue/resources/images установлены **648** точных approved PNG/GIF: 180 замен +2 adapters, original-format fallback и preferred1x/2x варианты. Ни рисунок, ни число кадров/размеры approved assets не изменены.
- Новый sass/src/Component.scss содержит294 уникальных resource-selector mappings, извлечённых из установленного Classic LTR/RTL CSS, и2 отдельно одобренных adapters. Меняются только background-image и background-size всего sheet; для resize/move дополнительно ровно background-position-y:0. Везде сохранены background-position-x и прочие исходные offsets/box metrics.
- При1x выбирается preferred1x (PNG для статических листов, GIF для анимаций), при min-resolution:192dpi — preferred2x. Логический размер всего листа фиксирован по approved classicDimensions. Например, tool bitmap60×720 остаётся30×360 CSS px; сама ячейка15×15. Original-format1x файлы доступны и по прежним путям.
- Точные image declarations используют !important, чтобы последующие родительские component rules не отменяли выбор ресурса. Это не общее разрешение CSS: весь файл привязан SHA в allowedReviewedScss. Посторонний selector, размер, offset или media-query change проваливает lint. Metadata ссылается на неизменённые approval/manifest и ранее принятую TASK-004 density geometry evidence.
- config/nordic-blue-icons.json integrationEnabled=true. Цветовая политика остаётся177 hooks /15tokens /31gradients. SDK/application/common fixture/package scaffold/JS overrides не менялись; overrides/ пуст.

## Адаптеры и наследование

Classic tool sheet30×360 не содержит строки resize(-360) и move(-375). Применены approved отдельные sheets30×15 с normal x=0, hover x=-15,y=0; общий sheet не расширен. Native graphic15×15 сохранён. Родительский component click box также сохранён: standalone lab растягивает его до140×15, что точно совпадает с Classic, и он не был ошибочно уменьшен до15px. Реальные normal/hover/disabled clicks проверены.

По approved manifest **Slider tracks и toast fader наследуются**, Slider thumbs заменены; переключение slider-imageless/font renderer не выполнялось. Остальные незаменяемые SDK backgrounds/frame slices/fonts наследуются. Пять legacy aliases не встречаются ни в LTR, ни в RTL Classic CSS: button/s-arrow-light-rtl.gif, grid/dd-insert-arrow-left.gif, grid/dd-insert-arrow-right.gif, grid/group-by.gif, grid/hd-pop.gif. Их approved1x bytes всё равно установлены по прежним путям; полный built catalog загружает также их preferred1x/2x sheets. Для несуществующего CSS consumer не придуман новый runtime selector.

## Фактические результаты

| Проверка | Результат |
|---|---|
| Cmd lab builds | testing/development/production exit0, без ERR/WRN |
| Bytes в outputs | все648 approved files ×3 режима: SHA, dimensions, frame count PASS |
| Полный fixture |102states ×DPR1/2;11280elements /1926icons, zero unexplained drift |
| Approved image contracts |3360 observations,104 distinct density paths (=52 logical resources),48 exact adapter observations |
| Build-mode native overview и reload |18 comparisons,15138elements PASS;9 комбинаций mode/DPR/fallback |
| Полный built sheet catalog |182sheets ×9runs =1638 загрузок, правильные bitmap/CSS sizes и density, без404 |
| Genuine native interactions |304 executions,152 Classic/Nordic pairs /8186elements PASS |
| Resize/move |12 normal/hover/disabled observations при DPR1/2;graphic15×15, parent hit box и click dispatch сохранены |
| Policy/geometry negative controls |45 lint controls +7 in-memory image/geometry controls PASS |
| Guards |18 application/common fixture inputs,300SDK Sass sources,1474baseline hashes проверены; approval/master/candidate SHA неизменны |

Повторены готовые TASK-010–012 drivers: формы/readOnly/disabled/invalid, Combo/date/time/spinner/clear, checkbox/radio/fieldsets; Grid sort/checkcolumn/header-menu/resize/scroll, Tree/paging; Tabs close/overflow/disabled/keyboard, nested/check menu, DatePicker navigation/today, оба Slider drag/keyboard, Progress и Mask. Это интеграционная перепроверка; общая release suite и дополнительные window/drag/resize flows остаются TASK-014.

Сравнение НЕ маскирует regions и не исключает icon geometry. Для каждой замены проверяется approved parent→runtime path, density и точный whole-sheet background-size; затем сопоставляется с родительским ресурсом. Только два явно одобренных y offsets приводятся к родительскому representation после проверки исходного/нового y. Rects, fonts, padding, hit boxes, transforms, visibility/opacity, client/scroll/data/focus и остальные sprite offsets сравниваются точно. Pseudo-elements проверены и как nested metadata, и как отдельные icon observations. Контрольные1px size, неверный sheet-size/x/y/URL/density отклоняются.

## Реальная плотность, fallback и анимации

В testing/development/production браузер загрузил native overview с фактическим manifest каждого режима при DPR1 и2 и повторно после reload. HTTP body SHA всех наблюдаемых replacement resources совпал с approved файлами. Fallback проверен при DPR2: только в тестовом HTTP response media query192dpi заменён недостижимым19200dpi, native CSS выбрал1x. Source/application config не менялись. Development Cmd разбивает CSS на import-файлы _1/_2; probe обрабатывает их, а не только wrapper. Production minification также проверена. Все исходные original-format fallback files отдельно проверены по built SHA.

Полный catalog показывает все182 sheets и все их ячейки через реальные built URLs. Native fixture непосредственно наблюдает52 logical replacement paths; остальные sheets покрыты full-catalog contracts и побайтной проверкой, а не утверждением о вызове каждого возможного SDK consumer. LTR/RTL selectors извлечены из установленных prebuilt styles; отдельная полная RTL interaction matrix здесь не заявляется.

Raw102states используют первый composited кадр **реального Nordic GIF**, включая его2x вариант. Classic GIF никогда не подставлялся вместо Nordic artwork. Только6 approved animated paths имеют frame0 QA derivatives; runtime GIF bytes untouched и frame counts проверены. Build-mode native screenshots живые, поэтому не назначены pixel golden. Raw PNG не ретушировались. Визуально просмотрены Tool normal и Form normal DPR1: approved gear, arrows, resize/move и triggers видны; сравнительная gallery сохраняет Classic рядом с Nordic.

## Диагностика и воспроизведение

Уточнения драйверов: обработка nested pseudo image metadata; нормализация только трёх явных build resource roots; fallback interception импортированных development CSS; различение graphic15×15 и исходного растянутого component140×15. Ни один metric/style SDK ради прохождения gate не менялся.

Команды: из корня `python tools/lint-nordic-blue.py --check-icon-candidates`; из TestApp/theme-lab `..\..\node_modules\@sencha\cmd-windows\dist\sencha.exe app build lab-nordic testing`, затемdevelopment иproduction с Java8. Оригинальные TestApp build/watch commands сохранены. Все outputs лежат в TestApp/build/theme-lab/nordic/{testing,development,production}. Точные версии/exit codes и ограничения — commands.json и этот отчёт.

Артефакты: integration-manifest.json (parent/new hashes), resource-adapter-review.json, parent-selectors.json, geometry-comparison.json, icon-contract-observations.json, native-action-comparison.json, build-mode-validation.json, build-mode-geometry.json, adapter-validation.json, source-guards.json, policy-controls.json, contract-controls.json, lint-report.json, build-*.log, raw captures и review.html. source-snapshot/ фиксирует пакет/config/lint; compiled/{mode} — outputs. artifact-manifest.json содержит SHA файлов; before/, before-theme/, before-final-documents/ — backups.

Следующая задача: **TASK-014 — общий воспроизводимый geometry/functional gate**, затем TASK-015 визуальные golden и TASK-016/017 приёмка/поставка. Nordic Blue пока не объявляется готовой темой.
