# Unified application chrome study

http://127.0.0.1:51754/chrome-preview/index.html

Same native Ext Viewport border layout, transparent north container, center tab panel and docked-top grid toolbar in both iframes. Simplified fixture follows WGR topology with synthetic data, not a copy of the whole application. Current compiled1.3.0 vs demo-only paint. Candidate uses native theme classes in root viewport context, no .header-main or WGR-specific selector. Shared .header-main typography exists only to reproduce app north styling identically. Common surface#edf2f8, separator colors blend, active tab underline and grid headers unchanged. CSS does not change layout/font/box metrics. Actual Ext7 tab panel root is .x-panel, not .x-tabpanel; selectors follow observed native bodyWrap/tabbar and body/tabpanel-child/grid-toolbar ownership with direct-child combinators. Nested tabs/windows excluded by hierarchy. Production review still required. Classic link loads real Classic CSS and never candidate CSS. No WGR/theme package changes/builds/automated tests. Await visual review before source integration and compatibility checks.

Fixture uses HBox toolbar with native overflow menu to keep actions on one row in narrow preview; WGR uses Column layout plus app CSS. This is a structural visual study, not an exact copy of the whole WGR app.
