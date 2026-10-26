# TASK-048 — прежний фон активной вкладки

По уточнению пользователя из candidate palette удалена белая background-color активной вкладки: снова наследуется compiled1.5.0 фон#edf2f8. Для выделения используется синяя border-color#3275d6, native border widths сохранены. Существующие акценты/тонкий фокус1.5.0 и остальные кандидатные tabs/buttons colors не менялись.

Ручной browser просмотр и computed readback active-tab-paint.json подтверждают фон rgb(237,242,248), border rgb(50,117,214). Screenshot comparison-full.png; comparison.png — crop без масштабирования. Пакеты1.5.0/SDK/WGR не менялись, сборки/автоматические тесты/полная новая приёмка не запускались. Доработано только preview TASK-047, интеграция отдельно после выбора.
