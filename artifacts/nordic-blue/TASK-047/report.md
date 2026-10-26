# TASK-047 — превью более выразительной палитры

Пользователь ограничивает изменения уровнем темы и попросил отдельное превью предложенной более яркой палитры. TestApp/chrome-preview/palette.html сравнивает compiled1.5.0 и дополнительные scoped paint rules html[data-palette=bright] на одном palette-sample.js с одинаковыми native настройками/данными.

Новая палитра: navigation#e7eef7; inactive tabs#d8e5f5/border#adc3df/text#365779; active white/text#174f91 с прежними3px акцентами. Обычные buttons#edf4fd/border#9db9dc; hover#d7e8ff/#6397d6; pressed#bdd7f7/#3979c5. Disabled исключены, focus сохраняет#3275d6. Формы/гриды остаются светлыми. CSS меняет только background-color/border-color/color. Нет изменений native widths/fonts/padding или специальных primary classes; назначение кнопок темой не угадывается.

Fixture: native border Viewport/north buttons/west tree/center tabs; компактная form с полями, панелями отправителя/получателя и кнопками «Изменить», grid с toolbar/toggle и textarea. Это синтетический структурный пример, не копия WGR. Неактивные вкладки тоже содержат native форму для ручного переключения.

Ручной browser просмотр обеих форм и click toggle «Закрепить» выполнен; фактические цвета candidate записаны в candidate-paint.json. comparison.png — crop без масштабирования, исходный screenshot comparison-full.png. Интерактивный просмотр сохранён в браузере. Сборки/автоматические тесты/полная geometry/function/pixel/DPR/RTL/browser приёмка не запускались.

Пакеты1.5.0/SDK/WGR не менялись. Дизайн показан для оценки; в production тему не интегрирован. Исторические goldens неизменны.
