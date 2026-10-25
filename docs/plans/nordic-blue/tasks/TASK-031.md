# TASK-031: Сохранить пользовательские иконки дерева

Статус: DONE для исправления наследуемого приоритета иконок и поставки 1.1.1. Полная новая Classic acceptance НЕ ВЫПОЛНЕНА.

- Найдена причина в parent Nordic Blue: !important перекрывал icon/iconCls, включая renderer metadata.
- Из 12 стандартных tree mappings убран !important; восстановлен штатный custom reset. Artwork, метрики и SDK не менялись.
- Parent theme-nordic-blue обновлён до 1.0.1, child theme-nordic-blue-soft-contrast до 1.1.1. Soft остаётся 1.0.0. Установить все три пакета и пересобрать приложение.
- Шесть окончательных release builds успешны; 648 approved image SHA совпали во всех выходах; три source lint PASS.
- Реальный compiled demo просмотрен: icon URL, CSS iconCls, renderer URL/CSS, custom folder со сворачиванием/раскрытием и стандартные папка/лист.
- Две source-only поставки идентичны. Доказательства и ограничения: artifacts/nordic-blue/TASK-031/report.md. Новые автоматические тесты и полная browser/DPR/RTL/geometry/function/pixel matrix не запускались; старые goldens сохранены.
