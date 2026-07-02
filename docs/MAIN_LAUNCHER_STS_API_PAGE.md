
# Add STS API Engine to Main Launcher

In `src/main_launcher/launcher.py`, add page:

```python
"STS API Engine",
```

Then add route:

```python
elif page == "STS API Engine":
    safe_page("STS API Engine", "ui.sts_api_page", "render")
```

For future Auto-Install versions, this will be included automatically.
