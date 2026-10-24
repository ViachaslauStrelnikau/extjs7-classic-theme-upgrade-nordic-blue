# Журнал решений и ограничений

| Решение | Состояние / доказательство |
|---|---|
| SDK7.7 вместо7.9 из PDF | Прямое указание пользователя; 7.7.0.31 принят,7.9 NOT_RUN/optional018 |
| Новый artwork вместо Classic images | Прямое указание; v2 approval и folder-v3 approval, immutable SHA |
| Строго0px вместо PDF≤1px | TASK-014/015/016, отрицательные контроли не допускают маскировки |
| Classic radius/font/layout/behavior наследуются | No arbitrary CSS/JS; narrow policy and700protected files in016 |
| Gradient flattening / icon resize-move mappings | Только SHA-bound reviewed exceptions, сохранены offsets/hit boxes |
| Старые navigation image build warnings | Совпадают с исходным TestApp/Classic; приложение не исправлялось ради темы |
| Development skip.page/skip.js | Installed Cmd defaults1; validation local.properties0 даёт actual pages. Unsupported CLI attempt retained as failed diagnostic |
| Firefox157 protocol failure | Не PASS; совместимый152.0.4 прошёл полный набор |
| Concurrent browser timeouts | Сохранены; повтор завершён без изменения readiness/metric policy; global driver timeout60s for native page operations |
| Browser favicon404 on original lab server | Точный /favicon.ico; acceptance read-only server51753 отвечает204; component requests не перехватываются |
| Initial visual golden | Технический Edge baseline, не полная пользовательская приёмка дизайна |
| Source-only theme distribution | Consuming app Cmd builds приняты; precompiled standalone package NOT_REQUIRED |
| Новые SVG: лицензия не назначена | Честный notice включён; владелец определяет лицензию отдельно. Sencha права не меняются |
| Непроверенные области | 7.9,другиеOS/browser versions,произвольныеcustomUI,полнаяRTL app layout,GIFsmoothness — не заявлены |

Нет неустранённых сбоев обязательной технической матрицы7.7; перечисленные границы не превращаются в PASS вне её объёма.
