# TASK-001: Проверить окружение, Cmd и существующий TestApp

Статус: DONE

Зависимости: нет

Основание: PDF, стр. 8–14, 24–26. Общие правила: [руководство агента](../../../nordic-blue-agent-guide.md).

## Подзадачи

- [x] 001.1. Зафиксировать текущие файлы/изменения, workspace descriptors и фактический путь SDK TestApp; сравнить версии ext-7.7.0.31 и TestApp/ext.
- [x] 001.2. Проверить локальный Cmd 7.7.0.36, Java и wrapper; диагностировать зависание команды версии и существующий sencha-error log. Не использовать старый Cmd 4 из PATH.
- [x] 001.3. Определить корректные Windows-команды запуска и сборки для этого workspace; проверить исходный Classic development build и локальную страницу.
- [x] 001.4. Записать версии, команды, URL, exit codes, logs и ограничения.

## Артефакты

environment.md, исходный Classic build log. Размещать отчёты и доказательства в artifacts/nordic-blue/TASK-001/; пути к исходникам и outputs указать в итоговой записи.

## Критерий завершения

SDK 7.7.0.31 и theme-classic подтверждены; Cmd запускается; Classic TestApp доступен либо точно описан блокер.

## Запись исполнителя

- Изменённые файлы: AGENTS.md (команды), build/bootstrap outputs TestApp, artifacts/nordic-blue/TASK-001/*, эта карточка и индекс плана. SDK и исходники приложения не редактировались.
- Команды, версии, exit codes: Cmd 7.7.0.36, SDK 7.7.0.31, Java 8; development/testing exit 0; app watch работает на localhost:64193.
- Проверки и ссылки на доказательства: artifacts/nordic-blue/TASK-001/environment.md, page-check.json, classic-testapp.png, input-hashes.json, testing-build.log. Браузерная smoke-проверка PASS.
- Отклонения / блокеры: нет блокера запуска; исходные warnings отсутствующих navigation UI images переданы в аудит TASK-002. Production и полная geometry suite ещё не выполнялись.
- Следующая доступная задача: TASK-002 и TASK-003.
