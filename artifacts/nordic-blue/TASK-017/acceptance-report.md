# TASK-017 — итоговая техническая приёмка и поставка

Объём: source theme package для Ext JS Classic7.7.0.31, Cmd7.7.0.36. Полные условия/версии и реальные сборки — TASK-016. Установка и откат — docs/nordic-blue-installation.md; состав/ограничения — docs/nordic-blue-release-notes.md.

Обязательные TASK-001–016 завершены по доказательствам. Матрица20fixture groups связывает их listed states с geometry/function TASK-014, pixel/artwork TASK-015 и builds/browsers/real app TASK-016. coverage-traceability.json не объявляет покрытыми все возможные Ext JS configurations. Журнал PDF/user решений, исходных предупреждений и устранённых диагностик — deviations.md.

Геометрия/шрифты/состояния: строгие Classic/Nordic comparisons, без допуска1px. Artwork: согласованный v3,648resources и SVG masters с точными SHA/1x/2x contracts; прежние физические/CSS размеры. Исходный TestApp, SDK, тема и fixture не менялись при подготовке поставки.

Source-архив собирается из реального принятого пакета, masters/approval/manifests, palette/policy и отчётов. В нём нет SDK/Classic reference bitmaps/screenshots, node_modules, compiled output или debug patches. Включён sources-and-license.md; новая лицензия не выдумана. Полные raw evidence находятся в основном проекте. release-manifest.json связывает каждый payload file, ZIP SHA/bytes и точное byte-for-byte сравнение с источниками; reproducibility-check.json сравнивает две независимые упаковки. Это проверка упаковки принятого пакета, не вымышленная сборка нового blank workspace.

Отдельные integrity результаты содержат фактический повтор проверки SHA всех локальных артефактов TASK-014/015/016 и текущих source/runtime files. Отсутствующие Git-excluded локальные compiled CSS отмечаются явно; не считать отсутствие нового checkout ошибкой оригинальной приёмки.

Техническая поставка7.7 принята в записанной матрице. Она не означает финальное одобрение пользователем вида всех экранов, поддержкуSDK7.9,полнуюRTLlayoutmatrix или любых custom ui/сторонних приложений. Подробные ограничения и права перечислены в release notes/deviations. Необязательный следующий этап — TASK-018; SDK7.9 сейчас NOT_RUN.
