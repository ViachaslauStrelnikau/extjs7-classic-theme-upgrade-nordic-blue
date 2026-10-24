# TASK-015: Настроить визуальные сравнения с учётом нового icon set

Статус: DONE

Зависимости: [TASK-006](TASK-006.md), [TASK-013](TASK-013.md), [TASK-014](TASK-014.md)

Основание: PDF, стр. 17, 21–24. Общие правила: [руководство агента](../../../nordic-blue-agent-guide.md).

## Подзадачи

- [x] 015.1. Захватить raw и normalized screenshots без удаления background-image; исправить нормализацию, если gradients дают ложные различия.
- [x] 015.2. Сравнивать структуру вне точно описанных icon regions; их geometry проверять отдельно и artwork — по Nordic golden.
- [x] 015.3. Сформировать Nordic golden и diff artifacts; зафиксировать и обосновать thresholds вместо слепого копирования 0.001 из PDF.
- [x] 015.4. Проверить отрицательным контролем drift значка/соседнего текста и документировать review обновлений golden.

## Артефакты

raw/normalized/diff PNG, Nordic golden, visual policy/report. Размещать отчёты и доказательства в artifacts/nordic-blue/TASK-015/; пути к исходникам и outputs указать в итоговой записи.

## Критерий завершения

Структурный drift обнаруживается; новые иконки не создают blanket masks; artwork и состояния набора проверяются golden snapshots.

## Запись исполнителя

- Выполнено2026-10-24. Код: tools/nordic-blue-visual/; binding: config/nordic-blue-visual.json.
- Отчёт/политика/галерея: artifacts/nordic-blue/TASK-015/visual-report.md,visual-policy.md,review.html. Принятый прогон run-3; диагностические run-1/2 не golden.
- 204 пары,0 структурных пикселей;408 raw repeats +464 независимых calibration images совпали точно. Порог RGB0/pixels0/dilation0.
- 408 native snapshots,204 frozen supports,648 runtime resources/694 frames. Шесть реальных контролей отвергнуты, restorePASS. Все команды/exit0 в commands.json.
- Theme/SDK/fixture/application неизменны; новый build не требовался. Ограничения и golden-review procedure документированы. Блокеров нет.
- Следующая доступная задача: TASK-016. Технический golden не означает финальную пользовательскую/выпускную приёмку всей темы.
