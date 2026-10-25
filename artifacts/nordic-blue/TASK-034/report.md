# TASK-034: заметный вариант сравнения v2

2026-10-25. DONE как исправление слишком слабого визуального предложения. Дизайн ожидает выбора пользователя; пакет темы не менялся.

Причина предыдущего результата: candidate.css действительно загружался и html scope сохранялся. Наблюдение реального DOM показало transparent right border, но selected background rgb(217,233,255) совпадал с текущей темой; тонкие inset1px плохо читались. Не ошибка загрузки и не повод заявлять, что разница уже была достаточной. До изменения сохранены before-candidate.css, before-index.html, before-shell.js; TASK-033 immutable.

v2 только в TestApp/state-preview: group headers#d7e4f3, leaf headers#e6eef8, выбранная строка#bfd7f5, inset2px#3275d6 сверху/снизу и4px с первого края, более явное hover#e3eefc, vertical separators transparent. Business backgrounds fixture остаются app!important и не заменяются. Нет изменений размеров/шрифтов/иконок/Ext overrides. Геометрия не измерялась и не объявляется доказанной. Добавлены Рядом/До/После v2, два одиночных режима показывают один fixture на одинаковом месте и полной ширине. Нативные iframe resize события обслуживает Ext; темы и WGR не изменены. Версии демо asset URLs обновлены для загрузки v2.

Фактический IAB просмотр: обе реальные compiled таблицы отрисованы; native select выбрал ID78568 в обеих. Computed paint подтверждает group rgb215,228,243 / leaf230,238,248 / selected191,215,245, inset4px+2px, transparent right border (computed-paint.json). Screenshot comparison-v2.png показывает различие шапки и выбора. Переключены После/До/Рядом; AX отражает соответствующий видимый заголовок и aria-pressed. Это узкое ручное наблюдение, не полная functional/metrics/pixel/browser/DPR acceptance. Новые сборки и автоматические тесты не запускались. Бизнес-строка в финальном v2 отдельно не проверялась; её CSS fixture неизменён. Новое artwork/motion не добавлялись.

URL остаётся http://127.0.0.1:51754/state-preview/index.html . Перед production integration нужен пользовательский выбор и отдельные проверки совместимости, старые goldens не обновлять.
