# TASK-015 — визуальные сравнения и Nordic golden

Статус: **PASS / DONE**,2026-10-24.

## Результаты

- 102 сценария (включая общий обзор) при каждом DPR1/2: **204 пары** Classic/Nordic. После нормализации вне точных контуров artwork **0 отличающихся пикселей**.
- 11280 точных межтематических сравнений элементов; метрики до/после нормализации также совпали. Все counts/states присутствуют, ошибок загрузки нет.
- **408 raw повторных сравнений** с исходным Classic TASK-006 и Nordic TASK-014:0pixels. Независимые повторные **464 изображения**:0pixels. Это подтверждает порог0 для данного окружения.
- Nordic golden: **408 raw/normalized snapshots**, **204 frozen supports**, **648 runtime-файлов / 694 декодированных кадров**. Все проверки PASS без допуска.
- **6 настоящих отрицательных контролей** отвергнуты: значок и соседний текст сдвинуты на1CSSpx; рисунок изменён без metric delta. После точного восстановления0pixels и исходные metrics. На каждом DPR отдельно; размеры значка сохранены.
- Lint PASS; 701 protected source/resource файлов неизменны. Тема, SDK, приложение и fixture не редактировались. Новая сборка не требовалась; реальные три сборки v3 из предшествующей задачи остаются актуальными.

## Проверка и воспроизведение

[Открыть галерею](run-3/review.html), [визуальная политика](visual-policy.md), [точные команды и exit codes](commands.json), [происхождение и hashes](provenance.json).

Единый запуск: `python tools/nordic-blue-visual/run.py --output artifacts/nordic-blue/visual-new-run`. Требует работающего Theme Lab и актуальной testing build; существующий output отклоняется. Инструкция: tools/nordic-blue-visual/README.md. Фактическая первичная калибровка выполнялась отдельными драйверами; все перечисленные команды завершились exit0. Обычный runner не создаёт/не обновляет golden автоматически.

Edge155.0.4283.62, SDK7.7.0.31/Cmd7.7.0.36, Python3.12.14, Pillow12.3.0, NumPy2.3.5;1280×1600,sRGB/software raster,en-US/Europe-Minsk,DPR1/2. Версия Node записана в provenance.

## Диагностика метода

run-1 выявил потерю слабого bitmap edge при измерении только прозрачного alpha. В run-2 диагностированы designMode caret в iframe и особенности границ checkbox pseudo/дробного tab-close. Финальный run-3 использует black/white support и явное скрытие каретки только в normalization. Bounding guards привязаны к настоящим containing elements; маски не расширялись, metric/pixel threshold не ослаблялся. Диагностические данные сохранены отдельно и не являются golden.

## Границы результата

Golden-v1 — технический начальный эталон реализации; пользовательское одобрение относится к artwork v2/v3, не является заявлением об окончательном одобрении всей темы. Нормализация не стирает URL background-image. Новые значки покрыты собственным unmasked Nordic golden; структура не маскируется целыми triggers/tools/ячейками/вкладками. Native snapshots относятся к testing при native1x/2x; fallback файлы и все кадры также проверены, но новая release matrix — TASK-016. Анимационная плавность и произвольные application configs не покрываются.

Артефакты: run-3/captures/,diffs/,golden-diffs/,negative-controls/,visual-results.json,golden-results.json; golden-v1/manifest.json,native/,artwork/; calibration-final/ и calibration-report.json; source-guard.json;config/nordic-blue-visual.json. Artifact manifest связывает SHA доказательств. Исходные TASK-004/006/013/014 и v3 approval неизменны.

Следующая задача: **TASK-016 — матрица сборок и интеграция**. Финальная готовность темы пока не заявляется.
