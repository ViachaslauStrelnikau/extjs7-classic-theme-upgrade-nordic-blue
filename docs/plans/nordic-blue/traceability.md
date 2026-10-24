# Связь плана с техническим проектом

Весь PDF (32 страницы) прочитан. Этот индекс позволяет проверить полноту плана. Номера относятся к печатным страницам PDF.

| Раздел / страницы | Задачи | Решение |
|---|---|---|
| Summary, инварианты 1–4 | 002, 006, 014 | child theme; typography/box/behavior и геометрия сохранены |
| Палитра и variable map 5–8 | 002, 008–012 | явные color variables; без base-color и sizing |
| Package/scaffold/builds 8–14 | 001, 007, 016 | использовать существующий workspace, SDK 7.7 |
| Preview/overflow/arrows 14–16 | 004, 009–015 | дизайн из локального reference; CSS patch не применять вслепую |
| Radius/frames 1, 17, 24–25 | 002, 009–012, 014 | наследовать radius/frame metrics |
| Regression/fixtures 17–24 | 005, 006, 014, 015 | stable IDs, readiness, coverage, три уровня сравнения |
| SDK/app risks 24–26 | 001–003, 013, 016, 018 | source audit, отдельные SDK outputs, app cascade audit |
| Estimate/roadmap 26–27 | README и все карточки | оценку пересчитать с учётом нового набора значков |
| Acceptance 28–29 | 014–017, coverage.md | сборки, геометрия, шрифты, behavior, icon geometry |
| Architecture/sources 29–32 | agent guide, 002 | установленный SDK — источник истины |

## Разрешённые расхождения с PDF

1. PDF предполагает основной target 7.9; пользователь установил цель 7.7. Поэтому используется 7.7.0.31, а 7.9 — дополнительная задача 018.
2. PDF рекомендует оригинальные Classic icons и пустые resources v1; пользователь потребовал обновить стандартные значки. Задачи 003–004 и 013 создают/подключают новый набор. Наследуется геометрия и остающиеся assets; графика заменяется контролируемо.
3. PDF допускает geometry delta ≤1 px. Пользователь требует 1:1: выпускной критерий строгий, 1 px остаётся диагностикой, не допуском.
4. Pixel-diff из PDF не учитывает новый artwork. В плане добавлены точные icon regions, отдельная проверка их геометрии и Nordic icon golden; полный background-image сохраняется при нормализации.
5. Пример теста PDF сопоставляет DOM по индексу и не защищает все пустые группы; план требует semantic IDs, completeness checks, полной typography и readiness Ext/layout/fonts.
6. PDF показывает общий CSS safety patch; план требует локального воспроизведения регрессии и не разрешает blanket ellipsis или transform reset.

## Источники и визуальные материалы

- Технический проект: ../../Nordic Blue для Ext JS Classic_ технический проект полностью взаимозаменяемой темы.pdf.
- Локальный Nordic screenshot: ../../reference/nordic-blue/Снимок экрана 2026-10-23 092528.png; справа обрезан. Не использовать как DOM geometry baseline.
- Classic reference: ../../reference/classic-baseline.png; свежий измерительный baseline строить в TASK-006.
- https://examples.sencha.com/extjs/7.9.0/examples/classic/themes/
- https://docs.sencha.com/extjs/7.7.0/guides/core_concepts/theming.html
- https://docs.sencha.com/cmd/7.7.0/guides/cmd_packages/cmd_creating_packages.html
- Playwright/pixelmatch из PDF — варианты инструментария; версию и API проверить при реализации, не считать приведённый код готовым.

## Последующее уточнение пользователя

Увеличить плотность пикселей значков при технической возможности, не меняя их физический размер в интерфейсе. Допускаются плотные 2x bitmap/sprites с исходными логическими CSS dimensions/offsets и 1x fallback. TASK-004 дополнена проверками DPR и обязательным показом полного набора пользователю: явное одобрение конкретной версии необходимо перед DONE, интеграцией TASK-013 и утверждением icon golden.
