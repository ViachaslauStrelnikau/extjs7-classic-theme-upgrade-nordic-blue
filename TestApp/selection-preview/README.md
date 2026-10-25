# Selection without a row frame

http://127.0.0.1:51754/selection-preview/index.html

Two isolated native Ext JS grids/trees share the same fixture and built Contrast1.2.0. Color-only vs color+3px left stripe matching panel accents. Preview CSS removes both child inset selection frames and Classic row/following-row dotted selection borders while retaining native widths. Keyboard-only focus remains distinguishable. Same wrapped document column creates a tall selected row in both fixtures. App business colors remain intact. No package/SDK/WGR changes, no build or automated tests. Await user choice before integrating either variant. Prior state-preview remains unchanged.

TASK-039: user selected stripe; production1.3.0 now includes it. User approved corrected ancestor-line preview before SVG exports were integrated into parent1.0.2. tree.html now shows actual compiled runtime without line overrides; before/after screenshot retained under REV-003-tree-lines. variant=runtime loads sample without selection.css.
