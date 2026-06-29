
# Future Leaders AI v11 Beta 14

## Goal

Add Settings and Data Validation v1.

This improves app stability before adding more live data features.

## Added

- `config/samantha_config.json`
- `src/config/settings.py`
- `src/validation/csv_validator.py`
- `src/ui/settings_page.py`
- `tests/test_beta14_settings_validation.py`

## Test

```bash
python tests/test_beta14_settings_validation.py
```

Expected output:

```text
Beta 14 Settings + Validation test passed.
```

## Suggested commit

```text
feat: add beta14 settings and data validation
```
