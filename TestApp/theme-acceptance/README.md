# Real TestApp acceptance descriptors

classic/ and nordic/ build the same original TestApp application classes, view Sass, controller/store, app.js and workspace. Only the theme selection, output root and paths rebased to the original workspace differ from TestApp/app.json. index.html/build.xml are byte copies of their original counterparts. Original TestApp source and descriptor remain unchanged.

From either directory, use `..\..\..\node_modules\@sencha\cmd-windows\dist\sencha.exe app build testing` (or development/production). Use the project Java 8 / Cmd-bundled Node environment. Outputs: TestApp/build/theme-acceptance/{classic,nordic}/{mode}.

local.properties enables skip.page=0 and skip.js=0, because installed Cmd development defaults skip both. This packages real development output pages without altering debug/logger, app behavior or theme rendering. The laboratory uses the same packaging properties. Do not add these validation-only hooks to the original TestApp unless explicitly needed.

TASK-016 captures the actual output pages, responsive navigation, all tabs, selection confirmation and cancellation. Existing app-specific navigation Sass and font-awesome remain intact, including pre-existing missing navigation image build warnings. No theme-specific app fixes were introduced.
