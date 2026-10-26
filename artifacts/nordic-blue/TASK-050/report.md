# TASK-050 — палитра3 «Чёткие контуры» включена в1.6.0

Пользователь выбрал «Собери3 · Чёткие контуры» из TASK-049. Child theme-nordic-blue-soft-contrast1.6.0 включает exact selected color-only rules без preview атрибута. Inactive tabs#b7cfea/#648bbb, text#19436f; active text#12477f и прежний фон#edf2f8 с синей рамкой/3px акцентами. Buttons#eaf2ff/#507fb9, hover#c7dfff/#356eae, pressed#a7c9f0/#245e9f; panel headers#e4edf9/#829fc5, обычные nonfocus/noninvalid field borders#829fc5. Disabled исключены. Нет изменения native widths/fonts/spacing/JS/assets или назначения главных действий.

Parents NordicBlue1.0.2/Soft1.0.0 побайтово сохранены. WGR не менялся и не пересобирался.

## Фактические проверки

- SDK7.7.0.31/Cmd7.7.0.36,6lab/real x testing/development/production builds exit0. final-build-commands.json/logs и стабильные SHA final-build-inputs.json. Существующие navigation-image warnings TestApp сохраняются в логах.
-3source lint PASS,648approved imageSHA в каждом выходе; child1.6.0/base1.0.2/Soft1.0.0. Parent integrity PASS, никаких новых artwork/fonts/JS.
- Ручной native browser просмотр compiled1.6.0, цвета tabs/buttons/panels прочитаны в compiled-palette-paint.json. Active background rgb(237,242,248). palette=runtime не загружает palette.css/palette-variants.css, только compiled CSS и общий sample-shell.
- Сравнение palette-release.html использует один native palette-sample.js для locally retained ignored compiled1.5.0 и actual compiled1.6.0. compiled-comparison.png — crop полного screenshot без масштабирования. Старые3preview сохранены на compiled1.5.0 и не накладывают старые предложения поверх нового пакета.

## Поставка и границы

Source-only ZIP включает3пакета, утверждённые исходники/инструкции. SDK/node_modules/compiled apps не включены. Два независимых запуска упаковки совпадают по SHA/bytes, source-reproducibility.json. Заменить3пакета и rebuild. Classic возвращается выбором theme-classic и rebuild, новые правила поставляются только темой.

Новые автоматические functional/geometry/pixel/DPR/RTL/browser/motion tests не запускались. Полная новая приёмка1.6.0 не заявляется; ранние результаты относятся к своим версиям. Исторические goldens неизменны. Проверка сборки и fixture не гарантирует все custom UI приложений.
