
# Update Instructions

Upload:

- src/ui/dashboard_integrated.py
- patches/MAIN_LAUNCHER_DASHBOARD_INTEGRATION_SNIPPET.md
- README_V1_2_RC_INTEGRATION1.md

Then edit:

- src/main_launcher/launcher.py

Add `("ui.dashboard_integrated", "render_dashboard")` as first Dashboard candidate.

Do not overwrite app.py.

Commit:

feat: add v1.2 rc integration1 dashboard
