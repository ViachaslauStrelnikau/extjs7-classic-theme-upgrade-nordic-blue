# Instructions for Codex

## Project goal

Build a Sencha Cmd theme package named **Nordic Blue** for the Ext JS **Classic** toolkit. The intended framework target is Ext JS **7.7.0**, using the added SDK build **7.7.0.31**. The Ext JS 7.9 themes example is a visual reference only: https://examples.sencha.com/extjs/7.9.0/examples/classic/themes/

Read [the requirements](docs/nordic-blue-requirements.md) before making changes. The Classic screenshot captured from the original conversation is in [docs/reference/classic-baseline.png](docs/reference/classic-baseline.png).

## Environment checks before implementation

- The added SDK is at ext-7.7.0.31. Its version.properties reports version.full 7.7.0.31 and version.release 7.7.0. The TestApp/ext/version.properties copy reports the same. Recheck both if the SDK changes.
- The SDK package at ext-7.7.0.31/classic/theme-classic/package.json identifies sencha.name as theme-classic, toolkit as classic, and ext-theme-classic as an alternate name. TestApp/app.json selects toolkit classic and theme ext-theme-classic.
- The project package.json declares @sencha/cmd-windows ^7.7.0; installed package metadata reports version 7.7.0 and version_full 7.7.0.36. A local binary invocation with -v did not return during the check; verify that Cmd runs before building.
- PATH also resolves to C:\Users\Damned\bin\Sencha\Cmd\4.0.5.87\sencha.exe; sencha version did not return before interruption. Prefer the project-local Cmd only after confirming its runtime works.
- Inspect existing project files before modifying them. Never edit the installed SDK. Preserve the existing TestApp, package.json, package-lock.json, and node_modules unless a documented setup step requires a change.
- Never edit the installed SDK. Keep the theme in its own package and use Sencha Cmd's generated package structure.

## Architecture and compatibility

- Create a theme package with Sencha Cmd for toolkit classic, extending the installed theme-classic package. Verify the generated package.json and inheritance chain against the SDK actually in use.
- Keep application code, component configs, data, and event behavior unchanged. The theme must be selectable in the same Classic applications that use theme-classic.
- Preserve Classic component geometry and typography exactly: rendered bounds, positions, dimensions, spacing, line height, font family, size, weight, and letter spacing. Nordic Blue changes colors and visual treatment only unless a separately documented design decision is approved by the user.
- The user requires updated standard icons. Inventory Classic assets and create the Nordic icon set early (TASK-003/004), then integrate it (TASK-013). Preserve image/display dimensions, sprite cell grid/offsets, hit targets, states and behavior. Retain the original Classic baseline and inherit resources not explicitly replaced. Follow docs/nordic-blue-agent-guide.md; the PDF recommendation to retain all original icons is superseded by this user instruction.
- Keep fixes for clipped text and misaligned arrows within the geometry and behavior requirements. Check the relevant font metrics, padding, line height, sprite/glyph, and alignment rules; do not hide a defect by changing component size.

## Work and completion gate

Follow the roadmap and acceptance checks in the requirements document. Compare Classic and Nordic Blue using the same Ext JS 7.7 SDK, application, data, browser, viewport, zoom, and device scale. Record component bounds and compare screenshots; inspect interactions, keyboard navigation, and component states.

Do not report the theme as ready until a real Sencha Cmd build succeeds and the built theme has been exercised in a Classic test application. Report the exact SDK/Cmd versions, build command, browser and scenarios checked, and any remaining visual differences.


## Implementation plan from the complete research PDF

Read [the agent guide](docs/nordic-blue-agent-guide.md) and [the task index](docs/plans/nordic-blue/README.md). These documents incorporate all 32 PDF pages, the Nordic screenshot and subsequent user instructions. Target 7.7.0.31; 7.9 is optional. Require unchanged geometry, not automatic acceptance of the PDF diagnostic 1 px threshold. Complete tasks by dependencies and record evidence; preparation of this plan does not complete implementation tasks.

## Icon density and user approval

Increase icon pixel density where the SDK/Cmd pipeline safely supports it (e.g. 2x bitmap for the same CSS size). Keep rendered/physical interface size, CSS rects, hit targets, spacing and logical sprite offsets unchanged; preserve a working 1x fallback. Validate DPR 1 and 2 separately. After generating the complete icon set, show all states and real-size/HiDPI previews to the user. TASK-004 enters WAITING_USER_APPROVAL; obtain explicit approval of its version/hash before TASK-013 integration or adopting icon golden snapshots. No response is not approval. Follow the detailed guide for density handling and renewed approval of changed artwork.

## Project build and development commands

Working directory for both commands: D:\Projects\Extjs7ClassicThemeUpgradeNordicBlue\TestApp (the folder containing app.json).

Testing build (user-provided and successfully verified with Cmd 7.7.0.36):

```powershell
..\node_modules\@sencha\cmd-windows\dist\sencha.exe app build testing
```

Start the development server and watcher:

```powershell
..\node_modules\@sencha\cmd-windows\dist\sencha.exe app watch
```

Use the project-local executable above rather than the old global sencha on PATH. The verified build environment uses Java 8 from C:\Program Files\Java\jdk1.8.0_501 and Node.js on PATH. The testing build passed; it reported pre-existing missing tab-navigation image warnings from TestApp's navigation UI. Keep those warnings in the baseline audit. The watch command is the user-provided development command; report its actual server URL after launch rather than assuming a port. Watch is a long-running process and does not replace testing/production acceptance builds.
