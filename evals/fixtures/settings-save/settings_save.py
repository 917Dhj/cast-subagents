"""Small writable smoke fixture for mixed delegation."""


def save_settings(current: dict[str, object], updates: dict[str, object]) -> dict[str, object]:
    """Apply every explicit update, including False, zero, and empty strings."""
    return {**current, **{key: value for key, value in updates.items() if value}}
