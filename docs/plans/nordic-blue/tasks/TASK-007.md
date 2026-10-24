# TASK-007: Сгенерировать и подключить пакет темы

Статус: DONE

Зависимости: [TASK-001](TASK-001.md), [TASK-002](TASK-002.md), [TASK-006](TASK-006.md)

Основание: PDF, стр. 8–14. Общие правила: [руководство агента](../../../nordic-blue-agent-guide.md).

## Подзадачи

- [x] 007.1. Определить существующий workspace и сгенерировать Cmd theme package theme-nordic-blue; сохранить .sencha/package.
- [x] 007.2. Подтвердить type=theme, toolkit=classic, extend=theme-classic и использование default UI.
- [x] 007.3. Добавить Nordic профиль к тому же fixture, не дублируя component configs; resources/images и overrides сначала пусты.
- [x] 007.4. Собрать неизменённый child и сравнить его с Classic до палитры и новых иконок.

## Артефакты

package scaffold, build profiles, контрольный отчёт inheritance. Размещать отчёты и доказательства в artifacts/nordic-blue/TASK-007/; пути к исходникам и outputs указать в итоговой записи.

## Критерий завершения

Child без overrides совпадает с Classic по геометрии и виду; parent resources загружаются; нет новых JS overrides/UI.

## Запись исполнителя

- Выполнено 2026-10-23. Пакет: `TestApp/packages/local/theme-nordic-blue`. `package.json` содержит type=theme, toolkit=classic, extend=theme-classic; default UI наследуются, overrides/images пусты.
- Уточнение 007.1: установленный Cmd 7.7.0.36 создаёт JSON scaffold без `.sencha/package`; оригинал сохранён в artifacts/nordic-blue/TASK-007/generated-scaffold. Не подменять современный scaffold устаревшей конфигурацией.
- Лабораторный descriptor: `TestApp/theme-lab/app.json`, build.xml, build-entry.html; два профиля, один fixture. Production TestApp sources/config не изменены.
- Реальные `app build lab-classic testing` и `app build lab-nordic testing`: exit 0. Команды и журналы в TASK-007; окончательные builds без warnings/errors.
- CSS и все runtime resources builds побайтово одинаковы (отличается только незагружаемый generated Readme.md). Сравнение с TASK-006: 102 сценария × DPR1/2, 11 280 element и 1 926 icon observations; ноль отличий computed metrics и пикселей компонентов. Только имя темы в двух служебных HTML controls исключено из raster comparison; raw сохранён.
- [Отчёт наследования](../../../../artifacts/nordic-blue/TASK-007/inheritance-report.md), [детальные сравнения](../../../../artifacts/nordic-blue/TASK-007/inheritance-comparison.json).
- Ограничение: пустая тема, без палитры/новых icons; release matrix ещё не пройдена.
- Следующая доступная задача: TASK-008.
