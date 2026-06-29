
def split_text(value) -> list[str]:
    if not value:
        return []
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    return [item.strip() for item in str(value).replace("|", ";").split(";") if item.strip()]


def to_float(value) -> float:
    if value is None or value == "":
        return 0.0
    try:
        return float(str(value).replace("%", "").replace(",", "").strip())
    except ValueError:
        return 0.0


def to_int_or_none(value):
    if value is None or value == "":
        return None
    try:
        return int(float(str(value).replace(",", "").strip()))
    except ValueError:
        return None
