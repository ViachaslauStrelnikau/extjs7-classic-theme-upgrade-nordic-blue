# Nordic Soft — интеграция завершена

TASK-021: DONE. SDK7.7.0.31/Cmd7.7.0.36, Windows. Полные geometry/function проверки: Edge/Chromium/Firefox,DPR1/2. Actual pages:3build modes/3browsers/DPR1/2,144pairs/40230elements. 18motion contexts,9catalog runs по182sheets,648resources×6outputs,5negative controls и700unchanged source files. Точные версии/ограничения — acceptance-matrix.json/integration-report.md.

Source archive: [nordic-soft-extjs-classic-7.7-source.zip](source-release/nordic-soft-extjs-classic-7.7-source.zip), 1328495bytes, 920payload files; SHA256 `f84da9fe88ac9bc5ccda9859c175758aa853f52f632ab156a151babfc7c8234b`. Две упаковки совпали байт в байт.

Включены оба source theme packages и opt-in module, masters/approvals/manifests/policies/notices/reports. SDK/Classic reference bitmaps/compiled apps/dependencies не входят. Воспроизведение: `python tools/nordic-soft-release.py --output artifacts/nordic-blue/soft-release-new-run` (новая папка). Архивы локальные; исходники/recipe/manifest опубликованы в Git.

Просмотр: http://127.0.0.1:51754/soft-preview/index.html . Реальный TestApp: http://127.0.0.1:51754/build/theme-acceptance/soft/testing/index.html . Установка/откат/API — docs/nordic-soft-installation.md. Дополнительные анимации подключаются явно, исходное приложение не переписано. Старые approvals/goldens сохранены; новая полная Soft pixel-golden калибровка отдельно не выполнена, прежний pixel PASS ей не присваивается. Совместимость7.9 не заявляется.
