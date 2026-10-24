# Визуальная политика Nordic Blue v1

Нулевой допуск: RGB channel delta 0, изменённых пикселей 0, расширение масок 0. Не используется maxDiffPixelRatio=0.001. Основание: 408 повторных raw-сравнений с принятыми TASK-006/TASK-014 и 464 независимых повторных изображения (29 сценариев ×2 DPR ×2 темы ×4 вида) совпали точно.

## Слои

1. Точная геометрия Classic/Nordic и до/после нормализации: bounds, typography, box model, offsets/transforms, counts, состояния, focus/data/scroll; из TASK-014. Изображения отображаются только через точные активные contracts.
2. Структура: canonical paint Classic→обе темы, нейтрализация цветов и только gradient layers; URL background-image сохраняются, размер/offset/repeat не меняются. По stable semantic metrics и полному совпадению body/iframe tree. Для нормализации явно скрыта designMode-каретка HtmlEditor; raw остаётся исходным.
3. Nordic raw/normalized golden без масок, плюс каждый декодированный кадр всех648 runtime bitmap-файлов (1x/2x, PNG/GIF и fallback). Поэтому ошибка внутри исключённого контура не может автоматически пройти.

## Точные исключения значков

Список region для каждого сценария находится в run-3/captures/dpr-N/{classic,nordic}/CASE.json: node, parent/runtime resource, density, recorded owner rect. Учитываются только пары с реально подключёнными approved ресурсами. Никаких произвольных URL и blanket masks для triggers/tools/text.

Контур измеряется двумя вспомогательными чёрным/белым render planes: остальные paint-признаки прозрачны, сохраняются только paired bitmap owners. Любой ненулевой вклад RGB попадает в support. Эти вспомогательные planes не являются нормализованными снимками; URL в normalized сохранены. Простой alpha-plane не годится: слабые границы могут округлиться до alpha0.

Никакого dilation/padding. Для проверки утечек применяется настоящий owner rect. Две конкретные особенности установленного Classic: inline checkcolumn ::after может рисоваться ниже host span, поэтому ограничение проверяется по recorded cell-inner; старый tab-close при DPR2 даёт наблюдаемый device-pixel fringe за дробной границей close element, поэтому используется recorded containing tab. Это только guard; ни ячейка, ни вкладка не превращаются в маску. Добавленных пикселей нет. Псевдоэлементу не выдумывается DOMRect.

Frozen support сохраняется в golden-v1/native/dpr-N/. Каждый последующий прогон обязан совпасть с ним точно; новый контур не может автоматически скрыть drift. Raw Nordic сравнивается целиком, независимо от исключений структуры.

## Захват и область

Edge с software raster/sRGB,1280×1600, zoom100%, DPR1/2 отдельно, en-US/Europe/Minsk; одинаковые SDK7.7.0.31, fixture/data, readiness. GIF frame0 — из фактического approved/built Nordic GIF; source/PNG SHA проверены. Анимационные кадры отдельно покрыты artwork golden; плавность анимации не оценивается.

Clip убирает только лабораторную шапку выше #lab-stage, а не компоненты. Плавающие элементы ниже неё остаются; overview снимается по полной высоте stage. Исходные Classic/TASK-014 snapshots не перезаписаны; crop выполняется только для сравнения с ними.

## Контроли и обновления

Шесть реальных контролей: icon/text +1 CSS px и artwork filter без metric delta при обоих DPR. Golden обязан отвергнуть все, соседний текст — также структура вне frozen support. Точный restore обязан вернуть0 pixels и исходные metrics. Изменения только в disposable browser pages; production files не меняются.

Golden-v1 — начальный технический эталон проверенной реализации, не окончательная пользовательская приёмка всей темы. Согласованный рисунок v2/v3 связан активными approval hashes. Изменение artwork требует нового показа и явного одобрения пользователя. Другие намеренные визуальные изменения требуют объяснения old/new/diff, реальной сборки, PASS геометрии/поведения, повторяемости и controls. Сохранять старую версию, создавать новую папку и осознанно обновлять config binding после review. Не запускать автоматическое принятие текущего результата. Полный порядок: tools/nordic-blue-visual/README.md.

Browser/font/OS/render changes требуют отдельной перекалибровки. Проверена детерминированная матрица Theme Lab, а не все возможные Ext JS configs. Native snapshots: testing, DPR1 native1x/DPR2 native2x; все fallback-файлы проверены покадрово, native fallback/mode checks — прежние TASK-013/REV-001 и следующая TASK-016. Финальная приёмка остаётся TASK-016/017.
