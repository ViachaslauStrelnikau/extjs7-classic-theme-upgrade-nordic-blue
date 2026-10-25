# Nordic Blue modernization preview

Preview only: three paint variants of the same Ext JS Classic7.7 components, using the existing Nordic testing CSS and installed SDK. The approved theme package, original Theme Lab, app sources, policy and goldens are unchanged.

Start from project root: `node TestApp/modern-preview/serve.cjs` (Node runtime with HTTP/fs support), then open http://127.0.0.1:51754/modern-preview/index.html . If51754 is occupied, use the existing instance or deliberately change the port; do not kill unrelated processes. Prerequisites: root ext-7.7.0.31 SDK and existing Nordic lab testing output (build with the documented local Cmd command if absent).

- Refined: paint-only frame colors and soft shadows on preview-owned floating components.
- Motion: Refined plus120ms color/border transitions and150ms opacity appearance. Focused controls use immediate state paint. Show listener restarts appearance on every open; hide stays immediate. No close interception, focus delay or transforms/width/height animation.
- Soft: Motion plus3px control/menu and4px window corners. This is a proposal, not a passed production compatibility gate.
- System prefers-reduced-motion and the manual animation switch suppress the added motion. No Ext class/global override; listeners belong only to demo components. Native Ext behavior remains available; tree animation is off identically in each sample.
- Check “Показать текущую тему” for an additional original Nordic column. That column always uses approved v3 artwork. Other columns can switch between approved v3 and candidate warm folders/blue documents. All share identical component config/data; columns resize together.

Candidate artwork is newly drawn SVG plus browser-rendered PNG1x/2x, all16×16CSSpx. REV-002-tree-warm is WAITING_USER_APPROVAL; artwork is scoped to demo-tree-candidate, not installed in the theme. Production GIF fallback/export/selector integration remains future work. Do not change config/nordic-blue-icons.json or refresh goldens just to accept the preview.

Visual rendering only: Edge156.0.4314.42, screenshots in TASK-019. No new Cmd theme build, geometry/function/reduced-motion suite or production release acceptance is claimed for this prototype. Existing TASK-014–017 remain historical evidence, not automatic acceptance of a new optional variant.
