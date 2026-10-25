# TASK-039: Nordic Soft Contrast1.3.0 — полоса выбора и линии дерева

2026-10-25. DONE для интеграции одобренного выделения и исправления линий, сборки и source-only поставки. Полная повторная Classic acceptance1.3.0 не заявляется.

## Одобрение и исправление

Пользователь выбрал «Цвет + синяя полоса слева —3px, как у заголовков». Child theme-nordic-blue-soft-contrast1.3.0 теперь убирает inset selection frame и штатные Classic dotted borders selected row/following row; оставляет голубой фон и3px#3275d6 слева. Нативные border widths/шрифты/раскладка не менялись. Keyboard-only focus сохраняется отдельно от selection, в этой задаче отдельно не проверялся. Exact decorative review/policy обновлены, новые Ext overrides/JS/fonts не добавлялись.

У ошибочных SVG tree/elbow-line LTR/RTL был горизонтальный сегмент, хотя роль используется для проходящей вертикали предков. Удалены только M9.5 10.5h7 / M6.5 10.5h-6; цвет#B7C8DC, вертикальx9.5/x6.5, box16x20 сохранены. Actual before/after shown in selection-preview/tree.html; user explicitly replied «Одобряю исправление справа» before integration, satisfying AGENTS artwork approval gate. SVG masters and exact manifest approvals preserved under REV-003-tree-lines. Export via sharp to PNG/GIF1x(16x20) and2x(32x40), same physical16x20CSS.8runtime files changed,640unchanged; connection elbows/expander images and mapping CSS untouched. Parent theme-nordic-blue bumped1.0.1->1.0.2 only package version metadata plus8images; its Sass/custom icon compatibility fix retained. Soft1.0.0 unchanged, effective manifests/policy SHA updated for inherited correction.

## Actual builds and observation

Preliminary release-build-*6outputs built stripe before tree artwork integration; they are diagnostic, not final output evidence. Authoritative final-build-*6Cmd invocations lab+TestApp contrast descriptors x testing/development/production exit0; exact checked inputs unchanged during final run. SDK7.7.0.31/Cmd7.7.0.36/Java8/bundledNode6. All6manifests child1.3.0/parent1.0.2;648active approved resource SHA per output PASS. Three source lints PASS. Existing original TestApp navigation-image warnings remain in logs. Original TestApp/SDK/WGR not edited.

Actual IAB view of compiled tree has no extra tree-lines.css; bitmap elbow-line.png used at native16x20, ancestor ticks gone, real branch connections remain. Selected row computed shadow is only inset3px#3275d6, outline none. Tall native wrapped grid row height60px viewed/read from compiled theme without selection.css: selected cell first has3px left shadow, other cell none, row border neutral solid rather than blue dotted. Screenshots and computed DOM observations compiled-tree.png / compiled-tree-styles.json / compiled-grid-styles.json. Footer/preview status changed from approval candidate to actual integrated runtime. Earlier before/after screenshot preserved separately.

No new automated tests/full geometry/function/pixel/browser/DPR/RTL matrix were run in this task. TASK-037 Edge1x/2x results apply to1.2.0 only. Export dimension/source/resource audits and narrow actual LTR view are not a replacement for full release acceptance. RTL1x/2x assets corrected/exported; full live RTL layout not claimed. Old goldens/accepted artifacts unchanged.

## Delivery

Source-only deterministic recipe tools/nordic-soft-light-release.py, source-delivery/ and source-delivery-repeat/ receipts; ZIPs local/gitignored. Update all3packages: theme-nordic-blue1.0.2, theme-nordic-blue-soft1.0.0, theme-nordic-blue-soft-contrast1.3.0. Rebuild the consuming app. WGR was not modified or built. No SDK/node_modules/compiled app output included, no new artwork license grant. docs/nordic-soft-light-installation.md documents update paths. Separate commit/push per standing user instruction.
