# TASK-002: Аудит Sass, default UI и приложения

Статус: DONE

Зависимости: [TASK-001](TASK-001.md)

Основание: PDF, стр. 3–13, 24–26. Общие правила: [руководство агента](../../../nordic-blue-agent-guide.md).

## Подзадачи

- [x] 002.1. Проверить theme-classic/theme-neutral/theme-base и места объявления/использования переменных из PDF.
- [x] 002.2. Составить allowlist color variables и denylist метрик; выявить производные значения, frames, gradients и inclusion flags.
- [x] 002.3. Проверить TestApp Sass/CSS, overrides и required packages на selectors .x-* и font icons, способные менять тему.
- [x] 002.4. Зафиксировать actual SDK values и источники; не переносить в Nordic копию всех значений Classic.

## Артефакты

sdk-audit.md и variable-map.md. Размещать отчёты и доказательства в artifacts/nordic-blue/TASK-002/; пути к исходникам и outputs указать в итоговой записи.

## Критерий завершения

Для каждой планируемой переменной указан SDK-файл, назначение и риск; конфликтующие app styles перечислены.

## Запись исполнителя

- Изменённые файлы: artifacts/nordic-blue/TASK-002/*, эта карточка, индекс плана; palette.md дополнена ссылкой на проверенную карту. Исходники приложения и SDK не менялись.
- Команды, версии, exit codes: статический rg/Python аудит SDK 7.7.0.31; finish_task002.py exit 0, validation.json PASS. Сборки не повторялись: source-only audit использует testing evidence TASK-001.
- Проверки и ссылки на доказательства: artifacts/nordic-blue/TASK-002/sdk-audit.md, variable-map.md/JSON, variable-policy.json, source-index.json, app-audit.json, sdk-copy-comparison.json, input-hashes.json, validation.json.
- Отклонения / блокеры: аудит завершён без блокеров. Navigation UI приложения не является default Classic baseline; warnings вызваны отсутствием navigation-relative image resources. Slider/Tree color hooks зависят от renderer flags; подробнее в отчёте.
- Следующая доступная задача: TASK-003; также доступна TASK-005 по её зависимостям.
