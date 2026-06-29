
# Unified Config

Centralizes runtime settings.

Suggested environment variables:

- FL_APP_NAME
- FL_VERSION
- FL_LIVE_PRICE_TTL
- FL_ENABLE_LIVE_PRICE
- FL_ENABLE_AUTO_REFRESH
- FL_GOOGLE_SHEET_URL

Future patches should call `load_config()` instead of hard-coding values.
