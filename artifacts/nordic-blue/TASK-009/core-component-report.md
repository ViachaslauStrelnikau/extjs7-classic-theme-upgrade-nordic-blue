# TASK-009 — Panel, Window, Toolbar, Button: DONE

Завершено 2026-10-24 (Europe/Minsk). Рабочий SDK 7.7.0.31 / Cmd 7.7.0.36 / Java 8. Это промежуточный этап темы; release acceptance остаётся впереди.

## Изменения

- `sass/var/panel/Panel.scss`: цвет текста body, framed background, inner header border и focus outlines, дополнительно к цветам TASK-008. Normal/framed/collapsed/disabled используют неизменённую конструкцию Classic.
- `sass/var/window/Window.scss`: body/background/inner border в Nordic palette, body text; сохранены Classic radius, header padding, border widths, modal mask, drag/resize behavior и существующая тень. Новые тени не добавлялись.
- `sass/var/toolbar/Toolbar.scss`: text, footer, separators и surfaces; normal/overflow/open/disabled покрыты.
- `sass/var/button/Button.scss`: все семь normal/hover/focus/pressed/focus-over/focus-pressed/disabled состояний default и toolbar family. Цвет текста остаётся Nordic text; disabled использует унаследованное ослабление opacity Classic. Split/menu arrow boxes, hit areas и images не менялись.
- Всего активно **104 color hooks**: 52 из TASK-008 + 52 новых. Все подтверждены installed SDK и фактическим compiled consumption. Проверка сначала выявила 14 неиспользуемых inner-border hooks; они удалены вместо включения внутренних рамок. Удаление дало byte-identical CSS/resources, доказательство `prune-output-identity.json` относится к этому этапу до последующих state-color fixes.

## Градиенты и особенности SDK

Сначала собрана полная state palette с наследуемыми gradients (phase A): **22 сценария × DPR1/2**, **2738 element comparisons**, zero drift. Только после этого разрешены **14** конкретных `dynamic('none')` assignments: Panel header, Toolbar background, 7 default button gradients, 5 toolbar button interaction gradients. Window header уже flat в родительском SDK. Radius/frame padding/widths и shadow geometry унаследованы.

Lint допускает эти 14 hooks только по точным имени/пути/value и SHA-связанному `gradient-review.json`, который ссылается на принятый phase-A geometry report. Остальные gradients и любой произвольный CSS/selector/UI mixin/JS override остаются запрещены. Политика была расширена проверенными toolbar gradient declarations, отсутствовавшими в первоначальном общем списке TASK-002.

Попарная проверка обнаружила особенность `theme-neutral/sass/var/button/Button.scss`: комбинированные backgrounds не выводятся, когда равны соответствующим over/pressed значениям. Из-за specificity keyboard focus мог скрыть hover или pressed. Исправлено только штатными цветами:

| State | Background | Border / indicator |
|---|---|---|
| normal | nb-control-bg (toolbar transparent) | nb-border (toolbar transparent) |
| hover | nb-control-hover | nb-accent-hover |
| focus | nb-control-bg | nb-accent + inherited dotted outline |
| pressed | nb-control-pressed | nb-accent |
| focus-over | nb-accent-soft | nb-accent + inherited dotted outline |
| focus-pressed | #C7DCF6 | nb-accent + inherited dotted outline |
| disabled | nb-control-bg (toolbar transparent) | inherited disabled opacity |

`#C7DCF6` — узкий компонентный state value: rounded RGB mix 90% `#D8E7FA` + 10% `#3275D6` = (199,220,246). 15 публичных tokens не изменились. Этот оттенок достаточно светлый для унаследованных тёмных стрелок. Причины/исправления и отклонённые comparisons сохранены в focus decision/diagnostic JSON; CSS overrides и metric changes не потребовались.

## Реальная сборка и policy

Из `TestApp/theme-lab`:

```powershell
..\..\node_modules\@sencha\cmd-windows\dist\sencha.exe app build lab-nordic testing
```

Фактические вызовы использовали эквивалентный `-cwd=.../TestApp/theme-lab`, Java 8 и bundled Node на PATH. Phase A и окончательный flat build: **exit 0**, без warnings/errors. Полные build logs сохранены. CSS SHA-256: `4b035e7934362bf70237f9ead07014b06fed98d98b681a59e43a2eb6f1dca54d`. SDK, production TestApp app.json/app.js/config и общий fixture.js не изменялись.

Read-only `python tools/lint-nordic-blue.py --check-icon-candidates`: **PASS/exit 0**, 15 tokens, 104 colors, 14 reviewed gradients, 300 SDK Sass hashes, 648 approved icon path contracts. Python 3.12.14. **39 положительных/отрицательных controls PASS**; добавлены exact reviewed gradient, неверный enum/path/color и altered-review checks. SDK declarations и consumers перечислены в policy; `compiler-consumption.json` доказывает **104** фактических CSS consumers через уникальные временные цвета в изолированном Fashion probe. Marker rules не добавлялись, рабочий CSS sentinel colors не получал.

## Итоговые сравнения

Edge 155.0.4283.62, Windows, 1280×1600, DPR1 и DPR2, en-US, Europe/Minsk. Детерминированная дата fixture остаётся 2026-10-23 как в принятом baseline; дата завершения работы и дата fixture различаются намеренно. Software raster/sRGB и first-frame GIF routing соответствуют TASK-006.

- **102 сценария × 2 DPR** окончательной сборки: raw PNG/JSON в `nordic/captures/pass-3/dpr-1` и `dpr-2`. **11 280 element comparisons, 1926 icon observations: zero geometry/typography/box/scroll/visibility/opacity/offset drift**. Нового text overflow нет: client/scroll bounds и typography сравнивались точно. Сохраняется исходное Classic clipping.
- Дополнительные **4 targets × 7 states × 2 DPR**: 56 пар Classic↔Nordic, 112 raw screenshots/JSON в `core-states-v3`. **1710 element comparisons** без отличий метрик; **168 попарных paint comparisons** подтверждают различимость всех семи состояний каждого target. Background gradients на этих кнопках отсутствуют. Hover/pressed вводятся реальной мышью, focus — стандартным API, disabled — API; фактические классы и state flags проверяются. `pressed` property не использовался как единственное доказательство: он отражает enableToggle, а pointer press проверяется по штатному x-btn-pressed.
- **20 mouse/keyboard checks PASS** (Classic/Nordic × DPR1/2): click menu/split arrow, focus on real menu item + Escape, focused normal button + Space, overflow menu + Escape, panel collapse/expand mouse. Focus menu item является явным предусловием Escape; не заявляется, что нажатие Escape с произвольным фокусом проверяет menu navigation.
- Normal/framed/collapsed panels, modal/moved/resized windows, split/menu buttons, narrow/open/disabled toolbar также вошли в общий fixture. Полная drag/resize/keyboard release matrix — TASK-014–016.
- Цвета, разрешённые gradient layers и данные профиля исключаются только из geometry comparison; image URLs/sizes/offsets и все прочие метрики сравниваются. **Pixel equality с Classic не заявляется**: оформление изменено. Raw captures сохранены; это не новые release golden snapshots.
- Все **180** parent icon resources, намеченных к замене, пока byte-identical Classic. Source images/overrides пусты, artwork approved v2 не редактировался и не интегрирован. Generated slicer frame surfaces изменены штатной компиляцией colors/gradients, не правкой SDK/resources.

Подробности: [геометрия](flat-geometry.json), [состояния и действия](core-state-comparison.json), [policy controls](policy-controls.json), [consumers](compiler-consumption.json). [Визуальное сравнение](review.html) показывает исходные raw кадры. Итоговыми являются pass-3 и core-states-v3.

### Хранение кадров при заполненном D:

Во время копирования дубликатов промежуточных кадров диск D: заполнился. Удалены только частично скопированные собственные диагностические каталоги TASK-009; оригиналы остались на C:. **Итоговые raw PNG/JSON, phase-A кадры, compiled stylesheet и source snapshots хранятся в `evidence.zip`** внутри TASK-009. Указанные выше пути — имена entries этого архива. `evidence-index.json` содержит SHA-256 архива и исходных кадров. Gallery server читает ZIP в память и показывает PNG без распаковки на D.

Предыдущие raw диагностические проходы дополнительно сохранены в `C:/Users/Damned/.codex/.chatgpt-projects/g-p-6909aeed3f508191801b816a6bd2b338/output/task009/diagnostics.zip`; их summary JSON находятся в проекте. Это локальное ограничение поставки диагностики, не изменение SDK/приложения или критериев приёмки. Полные распакованные копии всех кадров также остались в C staging. Не распаковывать архивы на D до освобождения места. Запуск просмотра: bundled Node `artifacts/nordic-blue/TASK-009/review-server.cjs` из корня проекта, открыть напечатанный loopback URL.

## Продолжение

TASK-009 DONE. Следующая задача — **TASK-010**, fields/triggers/fieldsets. TASK-011/012 ещё TODO; новые icons — TASK-013, после её зависимостей. Готовность всей темы не заявляется.
