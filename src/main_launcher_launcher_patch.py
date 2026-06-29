
# Manual patch note:
# In src/main_launcher/launcher.py, replace Dashboard candidate list with this order:
#
# candidates = [
#     ("ui.dashboard_integrated", "render_dashboard"),
#     ("ui.dashboard", "render_dashboard"),
#     ("ui.release_dashboard", "render_release_dashboard"),
#     ("ui.main_dashboard", "render"),
# ]
