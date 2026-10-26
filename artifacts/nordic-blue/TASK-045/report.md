# TASK-045 — более тонкий фокус вкладки в превью

По просьбе пользователя убрана дополнительная inset1px рамка фокуса. В candidate top tabs фокус теперь обозначается только цветом существующей native1px border. Активные3px полосы слева/снизу сохранены, пунктир текста остаётся выключенным. Нативные размеры/ширина border/spacing/fonts/JS не менялись.

Ручной click по native tab и computed readback: border1px, нет дополнительного inset1px focus shadow, label pseudo outline none; активные3px shadows сохранены. См. focus-paint.json и preview.png (точный crop preview-full.png). Пакеты темы1.4.1/SDK/WGR неизменны. Сборки/автоматические тесты/полная функциональная/геометрическая/pixel/DPR/RTL/browser приёмка не запускались. Это только уточнение preview TASK-043/044; результат ещё не оценён пользователем.
