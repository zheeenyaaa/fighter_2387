from typing import Annotated
from fastapi import Header
from translations import TRANSLATIONS


# Возможные значения "ru", "en", "es", "en-US", "es-ES", "en;q=0.5, es;q=0.9"
def get_language(
    accept_language: Annotated[str | None, Header(alias="Accept-Language")] = None,
) -> str:
    preferences = []
    for item in (accept_language or "").split(","):
        parts = item.strip().split(";")
        language = parts[0].strip().lower().split("-")[0]
        quality = 1.0
        try:
            for parameter in parts[1:]:
                key, value = parameter.strip().split("=", 1)
                if key.lower() == "q":
                    quality = float(value)
        except ValueError:
            continue
        if 0 < quality <= 1 and language in TRANSLATIONS:
            preferences.append((quality, language))
    return max(preferences, key=lambda item: item[0])[1] if preferences else "ru"
