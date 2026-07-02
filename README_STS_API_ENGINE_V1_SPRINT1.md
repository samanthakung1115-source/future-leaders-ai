
# STS API Engine v1.0 - Sprint 1

## Goal

Replace unstable Google Sheet CSV export with Apps Script JSON API.

## Package includes

### Google Apps Script

```text
apps_script/STS_API_ENGINE_V1_SPRINT1.gs
```

Actions:

```text
?action=health
?action=portfolio
?action=summary
?action=all
```

### Future Leaders AI Python client

```text
src/sts_api/client.py
src/ui/sts_api_page.py
config/sts_api_config.json
```

## Google Apps Script Deployment

1. Open your STS Google Sheet.
2. Extensions → Apps Script.
3. Create / open a script file.
4. Paste `apps_script/STS_API_ENGINE_V1_SPRINT1.gs`.
5. Deploy → New deployment.
6. Type: Web app.
7. Execute as: Me.
8. Who has access: Anyone with the link.
9. Copy Web App URL.
10. Paste it into:

```text
config/sts_api_config.json
```

Example:

```json
{
  "api_base_url": "https://script.google.com/macros/s/XXXXX/exec"
}
```

## Suggested commit

```text
feat: add sts api engine v1 sprint1
```
