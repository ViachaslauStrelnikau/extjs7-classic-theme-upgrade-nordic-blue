# TASK-005 — coverage checklist

Availability means construction + Ext/data/fonts/layout readiness, not complete release acceptance.

| Case | Available Classic states | Result |
|---|---|---|
| panel | normal, framed, collapsed, disabled, hover, focus | READY |
| window | normal, focus, modal, moved, resized | READY |
| button | normal, hover, focus, pressed, disabled, open | READY |
| toolbar | normal, overflow, open, disabled | READY |
| form | normal, invalid, readonly, disabled, focus | READY |
| triggers | normal, hover, focus, pressed, disabled, open | READY |
| checks | normal, checked, unchecked, disabled, focus | READY |
| fieldset | normal, collapsed, checked, disabled | READY |
| editor | normal, focus, readonly, disabled | READY |
| grid | normal, hover, selected, focus, sort-asc, sort-desc, menu, resized, disabled | READY |
| paging | normal, first, middle, last, disabled | READY |
| border | normal, collapsed, expanded | READY |
| tabs | normal, hover, selected, focus, overflow | READY |
| tree | normal, collapsed, expanded, selected, focus, disabled | READY |
| datepicker | normal, selected, prev, next, focus, disabled | READY |
| progress | normal, partial, full | READY |
| slider | normal, hover, focus, selected, disabled | READY |
| menu | normal, open, checked, unchecked, focus, disabled | READY |
| tool | normal, hover, focus, pressed, disabled | READY |
| mask | normal, loading, hidden | READY |

20 coverage rows, 101 named states plus overview, 302 stable semantic measurements. Real hover/pressed input, no CSS class projection.

Nordic uses the same fixture but no package/build exists yet: explicit ERROR, no fallback to Classic. Prepared profiles and build-requires.js activate in TASK-007. Full interaction/release matrix is NOT_RUN.
