# Folder revision v3 — APPROVED AND INTEGRATED

Одобрено и подключено2026-10-24. Сообщение пользователя «хорошо. продолжай» относится к показанному nordic-folders-v3-draft1, revision manifest SHA72e4d34c0d548cf1149e72e946313f6e88c340499382bcb6d6a777f9a735ba87.

Три изменённых ресурса: folder-open, folder-rtl, folder-open-rtl. Open folder имеет заметную наклонную заполненную створку; RTL-варианты зеркальные. Обычный folder не менялся. Всего заменены12 PNG/GIF files (3варианта ×1x/2x ×PNG/GIF), остальные636 файлов совпадают с v2. Размеры16×16 CSS px, bitmap16×16/32×32, число кадров1; paths, offsets, hit areas, CSS и component behavior сохранены.

Активная версия nordic-icons-v3-folders. Новый полный approved-icon-manifest.json сохраняет182 entries,3изменённых master hashes и прежние sprite contracts. Старые TASK-004 approval/manifest/masters/candidates и TASK-013 evidence не редактировались. approval.json связывает базовое одобрение, точный показанный revision manifest и новый полный manifest. Исторический revision-manifest.json со статусом WAITING_USER_APPROVAL сохранён как объект, который был показан; актуальное решение — approval.json и integration-status.json.

В config/nordic-blue-icons.json обновлены approval/manifest bindings и только12 bitmap hashes. В config/nordic-blue-policy.json обновлены approval metadata без изменения разрешённых CSS/metrics. Линтер поддерживает второй точный source root artifacts/nordic-blue для смешанного набора v2+revision; прежний default source root сохранён, сторонний root отклоняется. Проверены backward compatibility для v2, canonical equality v3 и отказ unapproved root. Новый icon font, runtime JS или CSS positions не добавлялись.

## Проверки

- SDK7.7.0.31 / Cmd7.7.0.36 / Java1.8.0_501: реальные testing/development/production lab builds exit0, без ERR/WRN. Каждый из648 runtime files во всех3 outputs соответствует active approved hash.
- Полный fixture102states ×DPR1/2:11280element comparisons /1926icon observations, zero unexplained drift. Contract normalizer проверяет точные утверждённые sheet sizes/density и image mappings; прочие box/font/offset/state/data metrics сравниваются без допуска.
-92genuine Grid/Tree/paging executions,46paired comparisons /3572elements PASS, включая mouse/keyboard expand/collapse/selection дерева.
-9native build-mode/DPR/fallback runs: все182sheets/run загружены, density/bitmap/CSS размеры, HTTP bytes и cache reload PASS. Fallback при DPR2 имитирует отсутствие min-resolution support только в QA HTTP response. Никакие application source/config не менялись.
- Lint PASS:177colors/15tokens/31gradients/648approvedimages/300SDK Sass.45policy controls PASS плюс3source-root controls.18protected application/shared-fixture inputs и CSS stylesheet byte identity сохранены.
- Визуально просмотрен native Tree normal DPR2 с новой открытой и прежней закрытой папкой. Raw screenshots не редактировались.

Первый integration helper сравнил byte SHA CRLF-файла с нормализованным LF SHA, используемым линтером; checksum assertion уточнён. Сам stylesheet не менялся, byte identity со snapshot TASK-013 подтверждена отдельно. Это диагностическое уточнение, не обход style gate.

Команды из TestApp/theme-lab: `..\..\node_modules\@sencha\cmd-windows\dist\sencha.exe app build lab-nordic testing`, затемdevelopment иproduction с Java8. Оригинальные TestApp build/watch commands сохранены. Build logs здесь; raw/JSON/tools и manifests — validation/. Перед изменениями сделаны backups в before-integration/.

Готовность всей темы не объявляется. Следующая задача: TASK-014 — общий воспроизводимый geometry/functional gate; активный approved icon manifest нужно читать из config/nordic-blue-icons.json, а не фиксировать TASK-004/v2.
