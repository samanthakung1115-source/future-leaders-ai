# Apps Script Deploy Steps

1. Open STS Google Sheet.
2. Extensions → Apps Script.
3. Paste `apps_script/STS_API_ENGINE_V1_SPRINT2.gs`.
4. Deploy → New deployment.
5. Type: Web app.
6. Execute as: Me.
7. Who has access: Anyone with the link.
8. Deploy.
9. Copy Web App URL.
10. Paste into `config/sts_api_config.json`.

Test:
YOUR_WEB_APP_URL?action=health
YOUR_WEB_APP_URL?action=sheets
YOUR_WEB_APP_URL?action=portfolio
YOUR_WEB_APP_URL?action=watch
YOUR_WEB_APP_URL?action=decision
YOUR_WEB_APP_URL?action=summary
YOUR_WEB_APP_URL?action=roles
YOUR_WEB_APP_URL?action=all
