# TASK-017 — DONE

Техническая поставка исходного пакета для7.7.0.31 завершена. Две упаковки совпали byte-for-byte; каждый entry/CRC/SHA проверен. Source archive: `nordic-blue-extjs-classic-7.7-source.zip`, 1180161bytes, 883payload files.

SHA256: `907de6f78c401109afb1c0205ad3b480bd7522452e4b4cdfc55201efe349b802`.

[Архив](source-release/nordic-blue-extjs-classic-7.7-source.zip), [manifest](source-release/release-manifest.json), [проверка повторяемости](reproducibility-check.json), [целостность прежних доказательств](integrity-check.json), [итоговый отчёт](acceptance-report.md), [ограничения](deviations.md).

Архив локальный и исключён из Git; recipe и все его исходники/manifest доступны в репозитории. Воспроизведение: `python tools/nordic-blue-release.py --output artifacts/nordic-blue/release-new-run`. Папка должна быть новой. SDK/node_modules/compiled outputs не включены. Для установки следовать docs/nordic-blue-installation.md; отчёт не назначает лицензии и не заявляет7.9/полнуюпользовательскуювизуальнуюприёмку.
